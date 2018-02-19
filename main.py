from __future__ import division

import random
from functools import reduce

from operator import add, attrgetter
from types import SimpleNamespace

import sys

import settings


class Advertisement(object):
    def __init__(self, ad_dict):
        self.id = ad_dict['id']
        self.view_count = 0
        self.click_count = 0

        self.conversion_rate = 0

    def collect_click(self):
        self.click_count += 1
        self.conversion_rate = self.click_count / self.view_count * 100

    def collect_view(self):
        self.view_count += 1
        self.conversion_rate = self.click_count / self.view_count * 100


class Emitter(object):

    def __init__(self, **settings_overrides):
        self.settings = SimpleNamespace()

        # Read settings, take into account overrides
        for name, val in settings.__dict__.items():
            if name.isupper():
                setattr(self.settings, name, settings_overrides.get(name, val))

        self.advertisements = [Advertisement(ad_dict) for ad_dict in self.settings.ADS]

    def get_total(self, attribute_name):
        """ Return sum of given statistic across all advertisements """

        return reduce(add, [getattr(ad, attribute_name) for ad in self.advertisements])

    def _get_best_performing_ads(self):
        ads_sorted = list(reversed(sorted(self.advertisements, key=attrgetter('conversion_rate'))))
        return [ad for ad in ads_sorted
                if ads_sorted[0].conversion_rate - ad.conversion_rate < self.settings.NOISE_TRESHHOLD]

    def _get_weights(self, ads):
        if self.get_total('conversion_rate') == 0:
            return [1 for ad in ads]
        else:
            return [ad.conversion_rate for ad in ads]

    def emit_advertisement(self):
        """ Return advertisement to be displayed for the user """

        learning_period_active = self.get_total('view_count') <= self.settings.LEARNING_PERIOD_LENGTH

        if learning_period_active:
            ads = self.advertisements
            weights = [1 for ad in ads]
        else:
            ads = self._get_best_performing_ads()
            weights = self._get_weights(ads)

        return random.choices(ads, weights)[0]

    def get_current_conversion_rate(self):
        return self.get_total('click_count') / self.get_total('view_count') * 100

    def print_report(self):
        print('{h1:<10}{h2:>10}{h3:>10}'.format(h1='ID', h2='CONVERSION', h3='VIEWS'))
        for ad in self.advertisements:
            print('{id:<10}{conversion_rate:>10.2f}{view_count:>10}'.format(id=ad.id, view_count=ad.view_count,
                                                                            conversion_rate=ad.conversion_rate))

        print('\nTOTAL CONVERSION {conversion_rate}'.format(conversion_rate=self.get_current_conversion_rate()))


def simulate_page_views(page_view_count, real_conversion_rates, **settings_overrides):
    emitter = Emitter(**settings_overrides)

    for page_view in range(page_view_count):
        ad = emitter.emit_advertisement()
        # The assumption is that user always sees the ad
        ad.collect_view()

        # simulate interaction
        real_conversion_rate = real_conversion_rates[ad.id]

        click = random.choices([True, False], [real_conversion_rate, 100 - real_conversion_rate])[0]
        if click:
            ad.collect_click()

    emitter.print_report()


if __name__ == '__main__':
    try:
        view_count = sys.argv[1]
    except IndexError:
        view_count = 100000

    simulate_page_views(view_count, settings.REAL_CONVERSION_RATES)

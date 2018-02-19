ADS = [
    {'id': 'A'},
    {'id': 'B'},
    {'id': 'C'},
    {'id': 'D'},
    {'id': 'E'},
]

# Over the learning period weights go from fixed to conversion-based over the learning period
# Expressed as number of ad views
LEARNING_PERIOD_LENGTH = 500

# Difference in performance less than this value will be ignored
NOISE_TRESHHOLD = 0.01


# For simulation purposes only
REAL_CONVERSION_RATES = {
    'A': 10,
    'B': 5,
    'C': 2,
    'D': 1,
    'E': 0.1
}

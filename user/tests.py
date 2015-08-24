from django.test import TestCase

# Create your tests here.

import random

if __name__ == '__main__':
    passcode = "%d" % random.randrange(100000, 999999)
    print(type(passcode))
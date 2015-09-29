from django.test import TestCase

# Create your tests here.


l1 = [1, 2, 3, 4, 5]
l2 = [4, 5, 6, 7]

l3 = list(set(l1) - set(l2))

print(l3)
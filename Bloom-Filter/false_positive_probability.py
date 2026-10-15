import math

m = 50
k = 3
n = 3

p = (1 - math.exp(-k * n / m)) ** k

print("Theoretical False Positive Probability:", p)
print("Percentage:", p * 100)
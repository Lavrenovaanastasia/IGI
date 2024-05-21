# Program: Power Series Expansion of cos(x)
# Lab: Lab 1
# Version: 1.0
import math

def factorial(n):
    """Calculate the factorial of a number."""
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def taylor_cos(x, eps=1e-6, max_iterations=500):
    """Calculate the value of cos(x) using power series expansion."""
    result = math.pi/2 - x
    n = 1
    term = x
    while abs(term) > eps and n < max_iterations:
        term *= -1 * x**2 / ((2 * n + 1) * (2 * n))
        result += term 
        n += 1
    math_result = math.cos(x)
    print(f"x = {x}, F(x) = {result}, n = {n}, Math F(x) = {math_result}, eps = {eps}")    
    return result, n

def task1():
     """Runs task1 
        Task: Вычисление значения функции c помощью разложения функции в степенной ряд"""
     x = float(input("Enter the value of x: "))
     eps = float(input("Enter the desired accuracy (eps): "))
     taylor_cos(x, eps)


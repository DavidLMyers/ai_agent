# driver.py
from pkg.calculator import Calculator

def main():
  calculator = Calculator()
  expression = input("Enter an expression: ")
  try:
    result = calculator.evaluate(expression)
    print(f"Result: {result}")  # This line renders the result to the console
  except ValueError as e:
    print(f"Error: {e})
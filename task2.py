from typing import Callable
import re

def generator_numbers(text):
  #Creating pattern to match numbers from text
  pattern = r"\b\d+\.\d+\b"

  for match in re.finditer(pattern, text):
    #creating generator and convert finding text to float for the next calculation, we can convert to float in next function, but I decided do it here.
    yield float(match.group())



def sum_profit(text: str, func: Callable):
  sum = 0

  for number in func(text):
    sum += number

  return sum



text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")
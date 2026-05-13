def caching_fibonacci():
  cache = {}

  def fibonacci(n):
    #Basic cases
    if n <= 0:
      return 0
    
    if n == 1:
      return 1
    
    #Checking if we have clculated n in cache
    if n in cache:
      return cache[n]
    
    #Calculationg with recursion and store in dictionary {n:value}
    cache[n] = fibonacci(n-1) + fibonacci(n-2)

    return cache[n]
  
  return fibonacci

# створюємо функцію з кешем
fib = caching_fibonacci()

print(fib(10))  # 55
print(fib(15))  # 610
print(fib(9))  # 610
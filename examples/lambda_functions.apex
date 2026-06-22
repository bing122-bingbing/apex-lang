# Lambda Functions and Functional Programming

var numbers: list = [1, 2, 3, 4, 5];

# Using lambda for filtering
var squared: list = map(lambda x => x ** 2, numbers);
print("Squared:");
print(squared);

# Using lambda for filtering
var evens: list = filter(lambda x => x % 2 == 0, numbers);
print("Even numbers:");
print(evens);

# Custom lambda usage
var add: lambda = lambda x => lambda y => x + y;
print("Custom lambda result:");
print(add(5)(3));

# Union Types and Type Flexibility

var data: any = 42;
print("Data as int: ");
print(data);

data = "Hello, Apex!";
print("Data as string: ");
print(data);

data = [1, 2, 3, 4, 5];
print("Data as list: ");
print(data);

data = {"name": "Alice", "age": 30};
print("Data as dict: ");
print(data);

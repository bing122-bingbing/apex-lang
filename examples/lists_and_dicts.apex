# Collections: Lists and Dictionaries

# Lists
var numbers: list = [1, 2, 3, 4, 5];
print("Numbers:");
print(numbers);
print("First element:");
print(numbers[0]);
print("Length:");
print(len(numbers));

# Iteration
for num in numbers {
    print(num);
}

# Dictionaries
var student: dict = {"name": "Bob", "grade": "A", "gpa": 3.9};
print("Student info:");
print(student);
print("Name:");
print(student["name"]);

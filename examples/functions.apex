# Function Definitions

def greet(name: string) -> void {
    print("Hello, ");
    print(name);
    print("!");
}

def add(a: int, b: int) -> int {
    return a + b;
}

def factorial(n: int) -> int {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

greet("World");
print("5 + 3 = ");
print(add(5, 3));
print("5! = ");
print(factorial(5));

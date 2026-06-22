# Apex Programming Language

# WARNING: YOU NEED TO INSTALL GIT AND GIT BASH TO USE IT

A complex, strongly-typed programming language with full Object-Oriented Programming (OOP) support and a Python-based interpreter.

## Features

### Type System
- **Strongly Typed**: Static type checking at compile-time
- **Built-in Types**: `int`, `float`, `string`, `bool`, `list`, `dict`, `void`
- **Type Safety**: Type checking on variable declaration and function calls
- **Custom Types**: User-defined classes

### Object-Oriented Programming
- **Classes**: Full class definition support
- **Inheritance**: Classes can extend other classes
- **Methods**: Instance methods with `this` reference
- **Properties**: Class properties with type declarations
- **Encapsulation**: Private and public members (scope-based)

### Variables & Control Flow
- **Variable Declaration**: `var name: type = value;`
- **Control Structures**:
  - `if/elif/else` statements
  - `while` loops
  - `for` loops with iterables
  - `break` and `continue` statements
- **Operators**: Arithmetic, comparison, logical, assignment

### Functions
- **Function Definition**: `def func_name(param: type) -> return_type { ... }`
- **Return Types**: Explicit return type specification
- **Parameters**: Type-checked function parameters
- **Recursion**: Full support for recursive functions

### Built-in Functions
- `print(*args)`: Output to console
- `len(obj)`: Get length of collections
- `int(value)`, `float(value)`, `string(value)`, `bool(value)`: Type conversion
- `list(*args)`, `dict()`: Create collections

## Installation

```bash
git clone <repository>
cd apex-lang
```

No external dependencies required! The interpreter is written in pure Python.

## Usage

### Running a File

```bash
python main.py examples/hello_world.apex
```

### Interactive Mode

```bash
python main.py -i
```

## Language Syntax Examples

### Hello World

```apex
print("Hello, Apex World!");
```

### Variables

```apex
var x: int = 42;
var name: string = "Alice";
var active: bool = true;
var values: list = [1, 2, 3];
```

### Control Flow

```apex
if (x > 10) {
    print("x is greater than 10");
} elif (x > 5) {
    print("x is greater than 5");
} else {
    print("x is 5 or less");
}

while (count < 10) {
    print(count);
    count = count + 1;
}

for i in [1, 2, 3, 4, 5] {
    print(i);
}
```

### Functions

```apex
def add(a: int, b: int) -> int {
    return a + b;
}

print(add(5, 3));
```

### Classes and OOP

```apex
class Person {
    var name: string;
    var age: int;
    
    def __init__(n: string, a: int) -> void {
        this.name = n;
        this.age = a;
    }
    
    def introduce() -> void {
        print("Hello, I am ");
        print(this.name);
    }
}

var person = new Person("Bob", 30);
person.introduce();
```

### Inheritance

```apex
class Animal {
    var name: string;
    
    def speak() -> void {
        print("Sound");
    }
}

class Dog extends Animal {
    def speak() -> void {
        print("Woof!");
    }
}
```

## Architecture

### Components

1. **Lexer** (`lexer.py`): Tokenizes source code into tokens
2. **Parser** (`parser.py`): Builds an Abstract Syntax Tree (AST) from tokens
3. **AST Nodes** (`ast_nodes.py`): Defines all AST node types
4. **Runtime** (`runtime.py`): Runtime environment, type system, and execution context
5. **Interpreter** (`interpreter.py`): Executes the AST
6. **Main** (`main.py`): Entry point and CLI interface

### Execution Flow

```
Source Code → Lexer → Tokens → Parser → AST → Interpreter → Output
```

## Type System Details

### Type Checking

- Variables must be declared with explicit types
- Function parameters have typed signatures
- Function return types are specified
- Type mismatches raise `TypeError`

### Numeric Type Coercion

- `int` can be used where `float` is expected
- Automatic conversion not performed for other types

## Error Handling

- **Syntax Errors**: Parser detects invalid syntax
- **Type Errors**: Type checker validates type compatibility
- **Runtime Errors**: Interpreter catches execution errors
- **Name Errors**: Undefined variable/function access

## Example Programs

See the `examples/` directory for complete working programs:

- `hello_world.apex`: Basic print statements
- `variables.apex`: Variable declarations and types
- `arithmetic.apex`: Mathematical operations
- `control_flow.apex`: if/elif/else and loops
- `functions.apex`: Function definitions and recursion
- `oop.apex`: Object-oriented programming
- `lists_and_dicts.apex`: Collections
- `inheritance.apex`: Class inheritance

## Running Examples

```bash
python main.py examples/hello_world.apex
python main.py examples/oop.apex
python main.py examples/functions.apex
```

## Future Enhancements

- [ ] Exception handling (try/catch/finally)
- [ ] Interfaces and abstract classes
- [ ] Generics/Templates
- [ ] Pattern matching
- [ ] Module system and imports
- [ ] Package manager
- [ ] Standard library expansion
- [ ] Compiler optimization
- [ ] JIT compilation

## Contributing

Contributions are welcome! Feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## License

MIT License - Feel free to use this project for educational and commercial purposes.

## Author

Created with ❤️ by Copilot and Community Contributors

---

**Happy coding in Apex!** 🚀

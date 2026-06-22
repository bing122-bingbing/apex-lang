# Comprehensive README for Apex Language

# Apex Programming Language 🚀

A **complex, strongly-typed programming language** with full Object-Oriented Programming (OOP) support, advanced error handling, auto-completion, and a Python-based interpreter.

## ✨ Features Overview

### 🎯 Advanced Type System
- **Primitive Types**: `int`, `float`, `string`, `bool`
- **Collection Types**: `list`, `dict`, `set`, `tuple`
- **Special Types**: `any`, `void`, `optional[T]`
- **Type Safety**: Static type checking with compile-time validation
- **Generic Types**: Support for generic/template-like structures

### 🏗️ Object-Oriented Programming
- **Classes**: Full OOP with inheritance and polymorphism
- **Interfaces**: Contract-based programming
- **Traits**: Mixin-style code reuse
- **Enums**: Type-safe enumeration types
- **Structs**: Value-type data aggregation
- **Access Modifiers**: `private`, `public`, `protected`
- **Class Modifiers**: `static`, `abstract`, `final`

### 🔄 Advanced Control Flow
- **Conditionals**: `if/elif/else` with powerful expressions
- **Loops**: `while`, `do-while`, `for-in` iteration
- **Pattern Matching**: `match-case` expressions
- **Exception Handling**: `try-catch-finally` with typed exceptions
- **Flow Control**: `break`, `continue`, `return`

### 📦 Functional Programming
- **Lambda Expressions**: Anonymous functions with `lambda` keyword
- **Higher-Order Functions**: `map`, `filter`, `reduce`, `zip`, `enumerate`
- **Async/Await**: Asynchronous programming support
- **Closures**: Full closure support

### 🛡️ Advanced Error Handling
- **7 Exception Types**:
  - `SyntaxException` - Parse-time errors
  - `TypeError` - Type mismatch errors
  - `NameError` - Undefined variables/functions
  - `RuntimeException` - Runtime errors
  - `AttributeException` - Missing properties
  - `IndexException` - Out of bounds
  - `CallException` - Function invocation errors

- **Rich Error Messages**:
  - Line and column numbers
  - Context code display
  - Smart suggestions
  - Call stack traces

### 🧠 Intelligent Auto-Complete
- **Keyword Suggestions** with code snippets
- **Type Auto-Completion**
- **Built-in Function Hints**
- **User-Defined Symbol Tracking**
- **Similarity Matching** using Levenshtein distance
- **Tab Completion** in interactive mode

### ⚙️ Advanced Operators
- **Arithmetic**: `+`, `-`, `*`, `/`, `%`, `**`
- **Comparison**: `==`, `!=`, `<`, `>`, `<=`, `>=`, `<=>`
- **Logical**: `and`, `or`, `not`, `xor`
- **Bitwise**: `&`, `|`, `^`, `~`, `<<`, `>>`
- **Pattern Matching**: `=~`, `!~`
- **Assignment**: `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `**=`, `&=`, `|=`, `^=`
- **Special**: `->`, `=>`, `::`, `?`

### 🎭 Modifiers and Keywords
- **Access**: `private`, `public`, `protected`
- **Storage**: `var`, `immutable`, `static`
- **Class**: `abstract`, `final`, `static`
- **Inheritance**: `extends`, `implements`, `super`
- **Type Qualifiers**: `optional`, `any`
- **Async**: `async`, `await`
- **Exception**: `try`, `catch`, `finally`, `throw`

## 📋 Installation

```bash
git clone https://github.com/bing122-bingbing/apex-lang
cd apex-lang
```

**No external dependencies required!** The interpreter is written in pure Python 3.6+.

## 🚀 Usage

### Running a File

```bash
python main.py examples/hello_world.apex
```

### Interactive Mode

```bash
python main.py -i
```

In interactive mode, use:
- `exit` - Quit interpreter
- `help` - Show help information
- `clear` - Clear screen
- `symbols` - Show defined variables/functions/classes
- `history` - Show command history
- `? keyword` - Get auto-complete suggestions
- `TAB` - Auto-complete current word

## 📚 Language Syntax

### Variables and Types

```apex
# Immutable variables
immutable var MAX_SIZE: int = 100;

# Regular variables
var name: string = "Apex";
var count: int = 42;
var value: float = 3.14;
var active: bool = true;
var items: list = [1, 2, 3];
var data: dict = {"key": "value"};

# Optional types (nullable)
var nullable: optional[string] = null;

# Any type (flexible)
var flexible: any = 42;
flexible = "now a string";
```

### Functions

```apex
# Simple function
def greet(name: string) -> void {
    print("Hello, ");
    print(name);
}

# Function with return value
def add(a: int, b: int) -> int {
    return a + b;
}

# Recursive function
def factorial(n: int) -> int {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

# Lambda function
var square: lambda = lambda x => x ** 2;
```

### Classes and OOP

```apex
# Basic class
class Person {
    var name: string;
    var age: int;
    
    def __init__(n: string, a: int) -> void {
        this.name = n;
        this.age = a;
    }
    
    def introduce() -> void {
        print("Hi, I am ");
        print(this.name);
    }
}

# Class inheritance
class Student extends Person {
    var studentId: string;
    
    def __init__(n: string, a: int, id: string) -> void {
        this.name = n;
        this.age = a;
        this.studentId = id;
    }
}

# Interface implementation
interface Animal {
    def speak() -> void;
}

class Dog implements Animal {
    def speak() -> void {
        print("Woof!");
    }
}
```

### Control Flow

```apex
# If-Elif-Else
if (x > 10) {
    print("x is greater than 10");
} elif (x > 5) {
    print("x is greater than 5");
} else {
    print("x is 5 or less");
}

# While loop
while (count < 10) {
    print(count);
    count = count + 1;
}

# For-in loop
for item in [1, 2, 3, 4, 5] {
    print(item);
}

# Pattern matching
match (status) {
    case 200 => print("OK");
    case 404 => print("Not Found");
    case 500 => print("Server Error");
}
```

### Exception Handling

```apex
try {
    var result: int = 10 / 0;
} catch (error: RuntimeException) {
    print("Error: Division by zero");
} finally {
    print("Cleanup");
}
```

### Advanced Features

```apex
# Bitwise operations
var flags: int = 12 & 10;  # AND
var combined: int = 8 | 4;  # OR
var shifted: int = 5 << 2;  # Left shift

# Spaceship operator (3-way comparison)
var cmp: int = 5 <=> 10;  # Returns -1

# Pattern matching operators
if (text =~ "[a-z]+") {
    print("Matches pattern");
}

# Static members
class Config {
    static var VERSION: string = "2.0";
    
    static def getVersion() -> string {
        return Config.VERSION;
    }
}
```

## 📁 Project Structure

```
apex-lang/
├── lexer.py              # Tokenization (40+ token types)
├── parser.py             # Syntax analysis (AST generation)
├── ast_nodes.py          # AST node definitions
├── runtime.py            # Type system & environment
├── interpreter.py        # Execution engine
├── error_handler.py      # Advanced error handling
├── autocomplete.py       # Intelligent auto-complete
├── main.py              # CLI & REPL
├── examples/            # 12+ example programs
│   ├── hello_world.apex
│   ├── exception_handling.apex
│   ├── pattern_matching.apex
│   ├── async_await.apex
│   ├── interface_implementation.apex
│   ├── bitwise_operations.apex
│   ├── lambda_functions.apex
│   ├── access_modifiers.apex
│   ├── enumerations.apex
│   ├── static_members.apex
│   ├── immutable_variables.apex
│   ├── optional_types.apex
│   ├── union_types.apex
│   ├── advanced_operators.apex
│   └── struct_example.apex
└── README.md            # This file
```

## 🎯 Execution Flow

```
Source Code → Lexer → Tokens → Parser → AST → Interpreter → Output
```

### With Error Handling:
```
Source Code
    ↓
  Lexer (with error tracking)
    ↓
Tokens (with line/column info)
    ↓
  Parser (with syntax validation)
    ↓
    AST
    ↓
Interpreter (with runtime checks)
    ↓
Output + Error Reports
```

## 🔍 Type System

### Type Checking

- Static type checking at parse time
- Runtime type validation
- Automatic type coercion where appropriate
- Custom type definitions via classes

### Type Compatibility

```apex
# Type promotion
var f: float = 42;  # int auto-promotes to float

# Type checking
if (typeof(x) == "int") {
    print("x is an integer");
}

# Instance checking
if (instanceof(obj, ClassName)) {
    print("obj is an instance of ClassName");
}
```

## 🛠️ Built-in Functions

### I/O Functions
- `print(...args)` - Output to console
- `input(prompt: string)` - Read user input

### Type Functions
- `typeof(value)` - Get type name
- `instanceof(obj, type)` - Check instance type
- `int(value)` - Convert to integer
- `float(value)` - Convert to float
- `string(value)` - Convert to string
- `bool(value)` - Convert to boolean

### Collection Functions
- `len(obj)` - Get length
- `list(...items)` - Create list
- `dict()` - Create dictionary
- `map(func, iterable)` - Map function over items
- `filter(func, iterable)` - Filter items by condition
- `zip(...iterables)` - Combine iterables
- `enumerate(iterable)` - Get indexed items
- `range(start, end, step)` - Generate range

## 💡 Examples

Check the `examples/` directory for comprehensive examples:

### Basic Examples
- `hello_world.apex` - Simple output
- `variables.apex` - Type system
- `functions.apex` - Function definitions
- `oop.apex` - Object-oriented programming

### Advanced Examples
- `exception_handling.apex` - Error handling
- `pattern_matching.apex` - Match expressions
- `async_await.apex` - Async operations
- `interface_implementation.apex` - Interfaces
- `bitwise_operations.apex` - Bitwise operators
- `lambda_functions.apex` - Functional programming
- `access_modifiers.apex` - Encapsulation
- `enumerations.apex` - Enum types
- `static_members.apex` - Static variables/methods
- `immutable_variables.apex` - Constants
- `optional_types.apex` - Nullable types
- `union_types.apex` - Type flexibility
- `advanced_operators.apex` - Spaceship, pattern operators
- `struct_example.apex` - Struct types

## 🚀 Running Examples

```bash
# Run individual examples
python main.py examples/hello_world.apex
python main.py examples/exception_handling.apex
python main.py examples/interface_implementation.apex

# Try interactive mode
python main.py -i

# In interactive mode, type:
# ? class    (to see class keyword suggestions)
# ? def      (to see function definition help)
# help       (to show full help)
```

## 🎓 Learning Path

1. **Basics**: `hello_world.apex` → `variables.apex` → `arithmetic.apex`
2. **Functions**: `functions.apex` → `lambda_functions.apex`
3. **OOP**: `oop.apex` → `access_modifiers.apex` → `interface_implementation.apex`
4. **Advanced**: `exception_handling.apex` → `pattern_matching.apex` → `async_await.apex`
5. **Features**: `bitwise_operations.apex` → `enumerations.apex` → `struct_example.apex`

## 🔧 Troubleshooting

### Auto-Complete Not Working
- Make sure you're in interactive mode (`-i` flag)
- Press `TAB` directly to trigger auto-complete
- Use `? keyword` to see suggestions

### Type Errors
- Always declare variable types: `var x: int = 5;`
- Function parameters need types: `def func(x: int) -> int`
- Return type must be specified

### Syntax Errors
- Statements must end with `;`
- Code blocks use `{ }` (curly braces)
- Conditions require parentheses: `if (x > 5) { ... }`

## 📈 Performance Considerations

- Type checking reduces runtime errors
- Static typing allows for optimization
- Pattern matching more efficient than nested if-else
- Use immutable variables when possible

## 🔐 Security Features

- **Access Control**: Private/public/protected members
- **Type Safety**: Prevents type-related vulnerabilities
- **Bounds Checking**: Array index validation
- **Exception Handling**: Graceful error recovery

## 🎨 Code Style Guide

```apex
# Use camelCase for variables and functions
var myVariable: int = 42;
def myFunction() -> void { }

# Use PascalCase for classes
class MyClass { }

# Use UPPER_SNAKE_CASE for constants
immutable var MAX_SIZE: int = 100;

# Use proper indentation (4 spaces)
if (condition) {
    print("indented");
}

# Add semicolons at end of statements
var x: int = 5;
```

## 🚀 Future Enhancements

- [ ] Module system and imports
- [ ] Generic types/templates
- [ ] Operator overloading
- [ ] Properties with getters/setters
- [ ] Destructuring assignments
- [ ] String interpolation
- [ ] Multi-dimensional arrays
- [ ] Named parameters
- [ ] Default parameter values
- [ ] Compile-time constants
- [ ] Performance optimizations
- [ ] JIT compilation

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation
- Create example programs

## 📄 License

MIT License - Free for educational and commercial use.

## 👨‍💻 Authors

Created with ❤️ by **Copilot and Community Contributors**

## 📞 Support

For issues, questions, or suggestions:
- Check existing documentation
- Review example programs
- Use interactive mode help: `help`
- Report issues on GitHub

---

**Happy coding in Apex!** 🚀✨

*Last Updated: June 2026*

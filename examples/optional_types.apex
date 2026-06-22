# Advanced Type System with Optional Types

var nullable: optional[string] = null;
var value: optional[int] = 42;

if (value != null) {
    print("Value exists: ");
    print(value);
} else {
    print("Value is null");
}

# Type checking
if (typeof(nullable) == "optional") {
    print("nullable is an optional type");
}

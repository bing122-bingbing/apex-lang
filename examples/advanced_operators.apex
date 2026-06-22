# Advanced Operator Examples

# Spaceship operator (3-way comparison)
var a: int = 5;
var b: int = 10;
var c: int = 5;

print("a <=> b:");
print(a <=> b);

print("c <=> a:");
print(c <=> a);

# Pattern matching operators
var text: string = "hello123";

if (text =~ "[a-z]+") {
    print("Text matches pattern");
}

if (text !~ "[0-9]{4}") {
    print("Text does not match 4-digit pattern");
}

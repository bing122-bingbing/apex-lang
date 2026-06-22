# Control Flow Examples

var age: int = 25;

if (age < 18) {
    print("You are a minor");
} elif (age < 65) {
    print("You are an adult");
} else {
    print("You are a senior");
}

# While loop
var count: int = 0;
while (count < 5) {
    print(count);
    count = count + 1;
}

# For loop
for i in [1, 2, 3, 4, 5] {
    print(i);
}

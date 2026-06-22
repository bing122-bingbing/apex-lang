# Object-Oriented Programming

class Person {
    var name: string;
    var age: int;
    
    def __init__(n: string, a: int) -> void {
        this.name = n;
        this.age = a;
    }
    
    def introduce() -> void {
        print("Hello, my name is ");
        print(this.name);
        print(" and I am ");
        print(this.age);
        print(" years old.");
    }
    
    def have_birthday() -> void {
        this.age = this.age + 1;
    }
}

var person1 = new Person("Alice", 30);
person1.introduce();
person1.have_birthday();
print("After birthday:");
person1.introduce();

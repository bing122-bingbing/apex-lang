# Interface Implementation

interface Animal {
    def speak() -> void;
    def move() -> void;
}

class Dog implements Animal {
    var name: string;
    
    def __init__(n: string) -> void {
        this.name = n;
    }
    
    def speak() -> void {
        print(this.name);
        print(" barks!");
    }
    
    def move() -> void {
        print(this.name);
        print(" runs");
    }
}

var myDog: Dog = new Dog("Buddy");
myDog.speak();
myDog.move();

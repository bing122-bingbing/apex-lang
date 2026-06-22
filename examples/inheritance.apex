# Object-Oriented Programming with Inheritance

class Animal {
    var name: string;
    var age: int;
    
    def __init__(n: string, a: int) -> void {
        this.name = n;
        this.age = a;
    }
    
    def speak() -> void {
        print(this.name);
        print(" makes a sound.");
    }
}

class Dog extends Animal {
    var breed: string;
    
    def __init__(n: string, a: int, b: string) -> void {
        this.name = n;
        this.age = a;
        this.breed = b;
    }
    
    def speak() -> void {
        print(this.name);
        print(" barks!");
    }
}

var dog = new Dog("Buddy", 5, "Golden Retriever");
dog.speak();

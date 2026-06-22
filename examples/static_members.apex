# Static Variables and Methods

class Counter {
    static var count: int = 0;
    private var id: int;
    
    def __init__() -> void {
        Counter.count = Counter.count + 1;
        this.id = Counter.count;
    }
    
    static def getCount() -> int {
        return Counter.count;
    }
    
    public def getId() -> int {
        return this.id;
    }
}

var c1: Counter = new Counter();
var c2: Counter = new Counter();
var c3: Counter = new Counter();

print("Total counter instances:");
print(Counter.getCount());

print("Counter 1 ID: ");
print(c1.getId());
print("Counter 2 ID: ");
print(c2.getId());
print("Counter 3 ID: ");
print(c3.getId());

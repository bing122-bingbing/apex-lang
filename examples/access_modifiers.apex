# Access Modifiers and Encapsulation

class BankAccount {
    private var balance: float;
    public var accountNumber: string;
    
    def __init__(number: string, initialBalance: float) -> void {
        this.accountNumber = number;
        this.balance = initialBalance;
    }
    
    public def deposit(amount: float) -> void {
        this.balance = this.balance + amount;
        print("Deposited: ");
        print(amount);
    }
    
    public def withdraw(amount: float) -> bool {
        if (this.balance >= amount) {
            this.balance = this.balance - amount;
            print("Withdrawn: ");
            print(amount);
            return true;
        }
        print("Insufficient funds");
        return false;
    }
    
    public def getBalance() -> float {
        return this.balance;
    }
}

var account: BankAccount = new BankAccount("ACC123", 1000.0);
account.deposit(500.0);
print("Balance: ");
print(account.getBalance());
account.withdraw(200.0);
print("Final Balance: ");
print(account.getBalance());

# Enumerations in Apex

enum Color {
    RED,
    GREEN,
    BLUE,
    YELLOW
}

enum Status {
    PENDING,
    ACTIVE,
    INACTIVE,
    DELETED
}

var current: Color = Color.RED;
print("Current color:");
print(current);

var taskStatus: Status = Status.ACTIVE;
if (taskStatus == Status.ACTIVE) {
    print("Task is active");
}

# Advanced Exception Handling in Apex

try {
    var result: int = 10 / 0;
} catch (error: RuntimeException) {
    print("Caught error: Division by zero");
} finally {
    print("Cleanup completed");
}

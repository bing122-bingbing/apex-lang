# Pattern Matching in Apex

var status: int = 200;

match (status) {
    case 200 => {
        print("Success: OK");
    }
    case 404 => {
        print("Not Found");
    }
    case 500 => {
        print("Server Error");
    }
}

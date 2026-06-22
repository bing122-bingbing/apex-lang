# Struct for Data Aggregation

struct Point {
    x: float;
    y: float;
    z: float;
}

struct Color {
    red: int;
    green: int;
    blue: int;
}

var p1: Point = Point{x: 10.5, y: 20.3, z: 15.0};
print("Point: (");
print(p1.x);
print(", ");
print(p1.y);
print(", ");
print(p1.z);
print(")");

var color: Color = Color{red: 255, green: 128, blue: 0};
print("Color RGB: (");
print(color.red);
print(", ");
print(color.green);
print(", ");
print(color.blue);
print(")");

# Async/Await Operations

async def fetchData() -> string {
    await print("Fetching data...");
    return "Data fetched successfully";
}

var data: string = await fetchData();
print(data);

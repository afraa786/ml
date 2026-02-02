# asynchrnous and synchronous coding
import time
import asyncio
import time

def fetch_user_data():
    print("Fetching user data...")
    time.sleep(2)  # Simulate a delay
    print("User data fetched.")
    return ["Joulene Doe", "John Doe"]

start = time.time()
user = fetch_user_data()      # Wait 2 seconds
   # Wait 2 seconds
end = time.time()

# to avoid this waiting time we use asynchronous coding
# ======================================================

async def fetch_user_data():
    print("Fetching user data...")
    await asyncio.sleep(2)  # Simulate a delay
    print("User data fetched.")
    return {"name": "John Doe", "age": 30}

async def process_user_data(data):
    print("Processing user data...")
    await asyncio.sleep(1)  # Simulate a delay
    processed_data = {**data, "processed": True}
    print("User data processed.")
    return processed_data

async def main():
    start =time.time()

    user, posts = await asyncio.gather (
        fetch_user_data(),
        process_user_data({"name": "Jane Doe", "age": 25})
    )

    end = time.time()
    print(f"Total time: {end - start} seconds")

asyncio.run(main())

# await keyword why is ti used? like it tells the code that i am waiting but, it lets other code runs in the mean time

# Total time: 2.002345323562622 seconds



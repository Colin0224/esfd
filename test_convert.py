import sys
# Add app directory to sys.path to allow importing app
sys.path.append('/app')

from app import convert
import asyncio

async def main():
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Rick Astley - Never Gonna Give You Up
    print(f"Testing convert function with URL: {test_url}")
    output = await asyncio.to_thread(convert, test_url)
    print(f"Convert function output: {output}")

if __name__ == "__main__":
    asyncio.run(main())

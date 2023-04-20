import asyncio
from bleak import BleakClient

address = "a0:6c:65:cf:9e:0e" #MAC
MODEL_NBR_UUID = "0000FFE1-0000-1000-8000-00805F9B34FB"#UUID

async def main(): #
    async with BleakClient(address) as client: #takes address as input and connects to address
        while True: #stays on indefinitely
            print('Hello World!') #To demonstrate that was successfully able to get into function

asyncio.run(main()) #runs async  i/o loop
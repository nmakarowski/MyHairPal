import asyncio
from bleak import BleakClient, BleakScanner
import bleak
import re
import time

from Constants.BlePMDClient import * 


async def run():
    global address
    address = None
    print('Searching for Polar Verity...')
    devices = await BleakScanner.discover()
    for d in devices:
        if 'Polar Sense' in d.name:
            address = d.address
            print(address)
            return d

async def requestSettingsByteString(address, PMD_CP, measurementType):
    data = bytearray([PMD_CP_COMMAND.GET_MEASUREMENT_SETTINGS.value, measurementType])
    async with BleakClient(address) as client:

        def callback(sender: int, data: bytearray):
            print(f"{sender}: {data.hex()}")

        await client.start_notify(PMD_CP, callback)

        await client.write_gatt_char(PMD_CP, data, True)

        await client.stop_notify(PMD_CP)
        return

async def requestPPGMeasurement(address, samplingRate = 135, resolution = 22, channels = 4):
    data = bytearray([PMD_CP_COMMAND.REQUEST_MEASUREMENT_START.value,   
                        PMD_MEASUREMENT_TYPE.PPG.value,
                        PMD_SETTINGS.SAMPLE_RATE.value, 0x01, 0x87, 0x00,
                        PMD_SETTINGS.RESOLUTION.value, 0x01, 0x16, 0x00,
                        PMD_SETTINGS.CHANNELS.value, 0x01, 0x04])
    
    client =  BleakClient(address)

    try:
        await client.connect(timeout=30.0)
    
        def callback(sender: int, data: bytearray):
            print(f"{sender}: {data.hex()}")
        
        await client.start_notify(PMD_UUID.PMD_CP.value, callback)
        await client.write_gatt_char(PMD_UUID.PMD_CP.value, data, True)
        await client.stop_notify(PMD_UUID.PMD_CP.value)

        '''
        await client.start_notify(PMD_UUID.PMD_DATA.value, callback)
        resp = await client.read_gatt_char(PMD_UUID.PMD_DATA.value)
        print(resp.hex())
        time.sleep(30)
        await client.stop_notify(PMD_UUID.PMD_DATA.value)
        '''

        await client.disconnect()

    except Exception as e:
        print(e)

    finally:
        await client.disconnect()


async def readRawData(address):
    async with BleakClient(address) as client:

        def callback(sender: int, data: bytearray):
            print(f"{sender}: {data.hex()}")
        await client.start_notify(PMD_UUID.PMD_DATA.value, callback)
        resp1 = ""
        while(1):
            resp = await client.read_gatt_char(PMD_UUID.PMD_DATA.value)
            
            print(resp.hex())
            resp1 = resp
        await client.stop_notify(PMD_UUID.PMD_DATA.value)



async def stopPPGRead(address):
    data = bytearray([PMD_CP_COMMAND.STOP_MEASUREMENT.value, PMD_MEASUREMENT_TYPE.PPG.value])
    async with BleakClient(address) as client:

        def callback(sender: int, data: bytearray):
            print(f"{sender}: {data.hex()}")

        await client.start_notify(PMD_UUID.PMD_CP.value, callback)
        await client.write_gatt_char(PMD_UUID.PMD_CP.value, data, True)
        await client.stop_notify(PMD_UUID.PMD_CP.value)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    device = loop.run_until_complete(run())


    if address is None:
        print("Failed to locate Polar Verity")
        exit()

    print('Getting PPG measurement...')
    loop.run_until_complete(requestPPGMeasurement(address))
    loop.run_until_complete(readRawData(address))

    loop.run_until_complete(stopPPGRead(address))




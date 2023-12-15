import smbus2
import bme280
import requests
import time
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
port = 1
address = 0x77
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)
server_url = os.getenv('URL')
server_port= os.getenv('PORT')

async def get_measures():
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)

    await send_measures(
        temperature=data.temperature,
        pressure=data.pressure,
        humidity=data.humidity,
        measurementDate=data.timestamp.timestamp(),
    )


async def send_measures(*, temperature, pressure, humidity, measurementDate):
    url = f"{server_url}:{server_port}"
    print("temperature: ", temperature)
    variables = {
        "temperature": temperature,
        "pressure": pressure,
        "humidity": humidity,
        "measurementDate": measurementDate,
        "measurementTable": "measurements"
    }

    body = """
    mutation SaveMeasurements($temperature: Float, $pressure: Float, $humidity: Float, $measurementDate: Float, $measurementTable: String){
        saveMeasurements(
            temperature: $temperature
            pressure: $pressure
            humidity: $humidity
            measurementDate: $measurementDate
            measurementTable: $measurementTable
        ) {
            code
            message
        }
    }
    """
    print(url)
    response = requests.post(url=f"http://{url}", json={"query": body, "variables": variables})
    print(response.json())
    await asyncio.sleep(25)
    await get_measures()

asyncio.run(get_measures())

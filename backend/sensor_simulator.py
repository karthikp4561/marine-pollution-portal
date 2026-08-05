import random
import time
import requests

API_URL = "http://127.0.0.1:8000/api/sensors/"

while True:
    data = {
        "buoy_id": "BUOY_001",
        "ph": round(random.uniform(6.5, 8.5), 2),
        "turbidity": round(random.uniform(5, 50), 2),
        "salinity": round(random.uniform(30, 40), 2),
        "oil_detected": random.choice([True, False])
    }

    try:
        response = requests.post(API_URL, json=data)
        print("Sent:", data)
        print("Status:", response.status_code)
    except Exception as e:
        print("Error:", e)

    time.sleep(10)
import requests
from datetime import datetime

payload = {
    "device_id": "feeder_01",
    "detected_at": datetime.now().isoformat(),
    "detection_type": "video",
    "species": "Parus major",
    "confidence": 0.87,
    "photo_url": None,
    "audio_url": None,
    "location_lat": 52.5200,
    "location_lon": 13.4050,
}

response = requests.post("http://localhost:8000/birds/", json=payload)
print("Status:", response.status_code)
print("Response:", response.text)
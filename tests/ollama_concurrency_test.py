import requests
import threading
import time

def send_request():
    start_time = time.time()
    payload = {"model": "mistral", "prompt": "Test prompt"}
    response = requests.post("http://localhost:11434/api/generate", json=payload)
    end_time = time.time()
    response_time = end_time - start_time
    print(f"Total response time: {response_time:.2f} seconds")

threads = [threading.Thread(target=send_request) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
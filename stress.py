import threading
import urllib.request

def worker():
    try:
        with urllib.request.urlopen("http://localhost:8080/echo", timeout=5) as r:
            assert r.status == 200
    except Exception as e:
        print("FAIL:", e)

threads = [threading.Thread(target=worker) for _ in range(100)]
for t in threads: t.start()
for t in threads: t.join()
print("ALL DONE: 100 requests")
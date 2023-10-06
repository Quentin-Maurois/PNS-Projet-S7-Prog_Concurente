import time
import threading

increment = 1

def worker():
    print("Nouveau thread")
    result = 0
    for i in range(10000000):
        result += increment
    print("Fin du thread")
    return result

start_time = time.time()

threads = []
for i in range (2):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end_time = time.time()
execution_time = end_time - start_time

print(f"Temps d'exécution = {execution_time} secondes")

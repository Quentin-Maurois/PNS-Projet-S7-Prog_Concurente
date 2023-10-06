import time
import threading

# Variable commune partagée par les threads
total = 0

def increment():
    global total
    for i in range(1000):
        total += 1

start_time = time.time()

threads = []
num_threads = 2  # Vous pouvez ajuster le nombre de threads

for i in range(num_threads):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end_time = time.time()
execution_time = end_time - start_time
# Afficher le résultat final (devrait être incorrect en raison de la course)
print(f"Résultat final : {total/1000.0} \t {total}")

print(f"Temps d'exécution = {execution_time} secondes")

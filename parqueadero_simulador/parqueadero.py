import threading
import time
import random
import queue

# Parámetros globales
CAPACIDAD = 5          # Espacios disponibles en el parqueadero
MIN_ESPERA = 1         # Tiempo mínimo antes de intentar entrar (segundos)
MAX_ESPERA = 4         # Tiempo máximo antes de intentar entrar (segundos)
MIN_ESTANCIA = 2       # Tiempo mínimo estacionado (segundos)
MAX_ESTANCIA = 6       # Tiempo máximo estacionado (segundos)

# Recursos compartidos
semaforo = threading.Semaphore(CAPACIDAD)
lock = threading.Lock()
espacios_ocupados = 0

# Cola para comunicar eventos a la GUI
eventos = queue.Queue()

def vehiculo(nombre):
    """Hilo que representa un vehículo en el parqueadero."""
    global espacios_ocupados

    # 1. El vehículo llega y espera un tiempo antes de intentar entrar
    tiempo_espera = random.randint(MIN_ESPERA, MAX_ESPERA)
    eventos.put(("esperando", nombre))
    time.sleep(tiempo_espera)

    # 2. Intenta adquirir un espacio (se bloquea si está lleno)
    semaforo.acquire()

    # 3. Entra al parqueadero — sección crítica
    with lock:
        espacios_ocupados += 1
        eventos.put(("entro", nombre, espacios_ocupados))

    # 4. Permanece estacionado un tiempo aleatorio
    tiempo_estancia = random.randint(MIN_ESTANCIA, MAX_ESTANCIA)
    time.sleep(tiempo_estancia)

    # 5. Sale y libera el espacio
    with lock:
        espacios_ocupados -= 1
        eventos.put(("salio", nombre, espacios_ocupados))

    semaforo.release()
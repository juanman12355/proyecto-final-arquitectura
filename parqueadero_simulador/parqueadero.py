import threading
import time
import random
import queue
import metricas

# Parámetros globales
CAPACIDAD = 5
MIN_ESPERA = 1
MAX_ESPERA = 4
MIN_ESTANCIA = 2
MAX_ESTANCIA = 6

# Recursos compartidos
semaforo = threading.Semaphore(CAPACIDAD)
lock = threading.Lock()
espacios_ocupados = 0

# Cola para comunicar eventos a la GUI
eventos = queue.Queue()

def vehiculo(nombre):
    global espacios_ocupados

    # 1. Llegada
    metricas.registrar_llegada(nombre)
    tiempo_espera = random.randint(MIN_ESPERA, MAX_ESPERA)
    eventos.put(("esperando", nombre))
    time.sleep(tiempo_espera)

    # 2. Intenta entrar
    semaforo.acquire()

    # 3. Entra — sección crítica
    with lock:
        espacios_ocupados += 1
        metricas.registrar_entrada(nombre)
        eventos.put(("entro", nombre, espacios_ocupados))

    # 4. Permanece estacionado
    tiempo_estancia = random.randint(MIN_ESTANCIA, MAX_ESTANCIA)
    time.sleep(tiempo_estancia)

    # 5. Sale
    with lock:
        espacios_ocupados -= 1
        metricas.registrar_salida(nombre)
        eventos.put(("salio", nombre, espacios_ocupados))

    semaforo.release()
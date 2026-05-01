import csv
import os
import time
from datetime import datetime

ARCHIVO_LOG = "logs/eventos.csv"

# Crea la carpeta logs si no existe
os.makedirs("logs", exist_ok=True)

# Diccionario para guardar tiempos por vehículo
tiempos = {}  # nombre -> {"llegada": t, "entrada": t, "salida": t}

def registrar_llegada(nombre):
    tiempos[nombre] = {"llegada": time.time(), "entrada": None, "salida": None}

def registrar_entrada(nombre):
    if nombre in tiempos:
        tiempos[nombre]["entrada"] = time.time()

def registrar_salida(nombre):
    if nombre in tiempos:
        tiempos[nombre]["salida"] = time.time()
        _guardar_evento(nombre)

def _guardar_evento(nombre):
    """Guarda la fila del vehículo en el CSV."""
    datos = tiempos[nombre]
    if None in datos.values():
        return

    espera = round(datos["entrada"] - datos["llegada"], 2)
    estancia = round(datos["salida"] - datos["entrada"], 2)
    hora = datetime.now().strftime("%H:%M:%S")

    archivo_existe = os.path.isfile(ARCHIVO_LOG)
    with open(ARCHIVO_LOG, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not archivo_existe:
            writer.writerow(["Vehiculo", "Hora", "T_espera(s)", "T_estancia(s)"])
        writer.writerow([nombre, hora, espera, estancia])

def obtener_resumen():
    """Calcula promedios para mostrar al final."""
    completados = [
        v for v in tiempos.values()
        if v["entrada"] and v["salida"]
    ]
    if not completados:
        return None

    prom_espera = round(
        sum(v["entrada"] - v["llegada"] for v in completados) / len(completados), 2
    )
    prom_estancia = round(
        sum(v["salida"] - v["entrada"] for v in completados) / len(completados), 2
    )
    return {
        "total": len(completados),
        "prom_espera": prom_espera,
        "prom_estancia": prom_estancia
    }
# 🚗 Simulador de Parqueadero Inteligente

Proyecto final del curso **Arquitectura de Computadores y Sistemas Operativos**  
Universidad EAN — Facultad de Ingeniería — 2025  
**Estudiante:** Juan Manuel Pedraza Sanchez  
**Docente:** Diana Carolina Beltrán Peña

---

## 📌 Descripción

Simulador de parqueadero inteligente desarrollado en Python que modela el comportamiento de un **Sistema Operativo** en la gestión de recursos limitados y procesos concurrentes.

| Simulador | Sistema Operativo |
|---|---|
| Vehículo | Proceso |
| Espacio de parqueo | CPU / Memoria |
| Semáforo | Planificador de recursos |
| Lock / Mutex | Exclusión mutua |
| Vehículo esperando | Proceso bloqueado |
| Vehículo estacionado | Proceso en ejecución |

---

## 🧠 Conceptos aplicados

- **Hilos (Threads):** cada vehículo es un hilo independiente con `threading.Thread`
- **Semáforo:** controla el número máximo de vehículos simultáneos con `threading.Semaphore`
- **Lock:** protege la sección crítica (contador de espacios) con `threading.Lock`
- **Concurrencia:** múltiples vehículos operan al mismo tiempo
- **Queue:** comunicación segura entre hilos y la GUI con `queue.Queue`
- **Métricas:** registro de tiempos de espera y estancia exportados a CSV

---

## 📁 Estructura del proyecto

```
parqueadero_simulador/
│
├── main.py              # Punto de entrada — lanza la interfaz gráfica
├── parqueadero.py       # Lógica de hilos, semáforo y lock
├── gui.py               # Interfaz gráfica con Tkinter
├── metricas.py          # Cálculo de métricas y exportación a CSV
└── logs/
    └── eventos.csv      # Registro automático de eventos (generado al ejecutar)
```

---

## ▶️ Cómo ejecutar

### 1. Requisitos

- Python 3.8 o superior
- Tkinter (incluido por defecto en Python)

No se requieren dependencias externas.

### 2. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/parqueadero-simulador.git
cd parqueadero-simulador
```

### 3. Ejecutar

```bash
python main.py
```

---

## 🖥️ Interfaz

La ventana principal muestra:

- **Cuadros de espacios:** verde = libre, rojo = ocupado
- **Contadores:** espacios disponibles, ocupados y vehículos en espera
- **Tabla de estados:** cada vehículo con su estado actual (esperando / estacionado / salio)
- **Botones de control:**
  - `Iniciar simulación` — lanza 5 vehículos simultáneos
  - `Agregar vehículo` — agrega un vehículo individual
  - `Ver métricas` — muestra resumen de tiempos
  - `Reiniciar` — limpia la tabla de estados

---

## ⚙️ Parámetros configurables

En `parqueadero.py` puedes ajustar:

```python
CAPACIDAD     = 5   # Número de espacios en el parqueadero
MIN_ESPERA    = 1   # Tiempo mínimo antes de intentar entrar (segundos)
MAX_ESPERA    = 4   # Tiempo máximo antes de intentar entrar (segundos)
MIN_ESTANCIA  = 2   # Tiempo mínimo estacionado (segundos)
MAX_ESTANCIA  = 6   # Tiempo máximo estacionado (segundos)
```

---

## 📊 Métricas

Al hacer clic en **Ver métricas** se muestra:

- Total de vehículos completados
- Tiempo promedio de espera (segundos)
- Tiempo promedio de estancia (segundos)

Todos los eventos quedan guardados en `logs/eventos.csv` con el formato:

```
Vehiculo, Hora, T_espera(s), T_estancia(s)
Vehiculo 1, 10:30:27, 2.0, 3.0
Vehiculo 2, 10:30:28, 4.0, 6.0
...
```

---

## 🔗 Recursos

- 📄 [Informe del proyecto (PDF)](./Informe_Parqueadero_JuanPedraza.pdf)
- 🎬 Video explicativo: *(agregar enlace de YouTube o Drive aquí)*

---

## 📜 Licencia

Proyecto académico — Universidad EAN 2026

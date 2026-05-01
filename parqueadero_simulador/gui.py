import tkinter as tk
from parqueadero import CAPACIDAD, eventos
import threading
from parqueadero import vehiculo

class ParqueaderoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Parqueadero Inteligente")
        self.root.geometry("700x500")

        self.contador_vehiculos = 0  # Para nombrar vehículos únicos

        # Widgets principales (por ahora solo texto)
        self.label_titulo = tk.Label(
            root, text="Simulador de Parqueadero", font=("Arial", 16, "bold")
        )
        self.label_titulo.pack(pady=10)

        self.label_estado = tk.Label(
            root, text=f"Espacios disponibles: {CAPACIDAD}", font=("Arial", 12)
        )
        self.label_estado.pack()

        self.log_box = tk.Text(root, height=15, width=70, state="disabled")
        self.log_box.pack(pady=10)

        # Botones
        frame_botones = tk.Frame(root)
        frame_botones.pack()

        tk.Button(
            frame_botones, text="Iniciar simulación",
            command=self.iniciar_simulacion, bg="green", fg="white", width=18
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            frame_botones, text="Agregar vehículo",
            command=self.agregar_vehiculo, bg="blue", fg="white", width=18
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            frame_botones, text="Reiniciar",
            command=self.reiniciar, bg="orange", fg="white", width=18
        ).grid(row=0, column=2, padx=5)

        # Iniciar ciclo de lectura de eventos
        self.leer_eventos()

    def agregar_vehiculo(self):
        """Lanza un nuevo hilo-vehículo."""
        self.contador_vehiculos += 1
        nombre = f"Vehículo {self.contador_vehiculos}"
        t = threading.Thread(target=vehiculo, args=(nombre,), daemon=True)
        t.start()

    def iniciar_simulacion(self):
        """Agrega 5 vehículos de golpe para simular concurrencia."""
        for _ in range(5):
            self.agregar_vehiculo()

    def reiniciar(self):
        """Reinicia el log visual (no detiene hilos activos)."""
        self.log_box.config(state="normal")
        self.log_box.delete("1.0", tk.END)
        self.log_box.config(state="disabled")

    def log(self, mensaje):
        """Escribe un mensaje en el log de la GUI."""
        self.log_box.config(state="normal")
        self.log_box.insert(tk.END, mensaje + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state="disabled")

    def leer_eventos(self):
        """Lee la cola de eventos y actualiza la GUI (corre en hilo principal)."""
        while not eventos.empty():
            evento = eventos.get()

            if evento[0] == "esperando":
                self.log(f"{evento[1]} llegó y está esperando...")

            elif evento[0] == "entro":
                nombre, ocupados = evento[1], evento[2]
                disponibles = CAPACIDAD - ocupados
                self.label_estado.config(
                    text=f"Espacios disponibles: {disponibles}"
                )
                self.log(f"{nombre} entró. Ocupados: {ocupados}/{CAPACIDAD}")

            elif evento[0] == "salio":
                nombre, ocupados = evento[1], evento[2]
                disponibles = CAPACIDAD - ocupados
                self.label_estado.config(
                    text=f"Espacios disponibles: {disponibles}"
                )
                self.log(f"{nombre} salió. Ocupados: {ocupados}/{CAPACIDAD}")

        # Vuelve a revisar la cola cada 200ms
        self.root.after(200, self.leer_eventos)
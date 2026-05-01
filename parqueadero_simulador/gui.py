import tkinter as tk
from tkinter import ttk
import threading
from parqueadero import CAPACIDAD, eventos, vehiculo

class ParqueaderoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Parqueadero Inteligente")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.contador_vehiculos = 0
        self.vehiculos_estado = {}  # nombre -> estado actual

        # Título
        tk.Label(
            root, text="Simulador de Parqueadero Inteligente",
            font=("Arial", 16, "bold"), bg="#f0f0f0"
        ).pack(pady=8)

        # Panel superior: espacios visuales
        frame_espacios = tk.LabelFrame(
            root, text="Estado del parqueadero",
            font=("Arial", 10, "bold"), bg="#f0f0f0", padx=10, pady=8
        )
        frame_espacios.pack(fill="x", padx=20, pady=5)

        self.espacios_canvas = []
        frame_cuadros = tk.Frame(frame_espacios, bg="#f0f0f0")
        frame_cuadros.pack()

        for i in range(CAPACIDAD):
            canvas = tk.Canvas(
                frame_cuadros, width=80, height=60,
                bg="#2ecc71", highlightthickness=2,
                highlightbackground="#27ae60"
            )
            canvas.grid(row=0, column=i, padx=6, pady=4)
            canvas.create_text(40, 30, text=f"E{i+1}", font=("Arial", 14, "bold"), fill="white")
            self.espacios_canvas.append(canvas)

        # Contadores
        frame_contadores = tk.Frame(frame_espacios, bg="#f0f0f0")
        frame_contadores.pack(pady=4)

        self.label_disponibles = tk.Label(
            frame_contadores, text=f"Disponibles: {CAPACIDAD}",
            font=("Arial", 11), bg="#f0f0f0", fg="#27ae60"
        )
        self.label_disponibles.grid(row=0, column=0, padx=20)

        self.label_ocupados = tk.Label(
            frame_contadores, text="Ocupados: 0",
            font=("Arial", 11), bg="#f0f0f0", fg="#e74c3c"
        )
        self.label_ocupados.grid(row=0, column=1, padx=20)

        self.label_espera = tk.Label(
            frame_contadores, text="En espera: 0",
            font=("Arial", 11), bg="#f0f0f0", fg="#e67e22"
        )
        self.label_espera.grid(row=0, column=2, padx=20)

        # Panel central: tabla de vehículos
        frame_tabla = tk.LabelFrame(
            root, text="Estado de vehículos",
            font=("Arial", 10, "bold"), bg="#f0f0f0", padx=10, pady=5
        )
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=5)

        cols = ("Vehículo", "Estado")
        self.tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=8)
        for col in cols:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=300, anchor="center")

        self.tabla.tag_configure("esperando", foreground="#e67e22")
        self.tabla.tag_configure("estacionado", foreground="#27ae60")
        self.tabla.tag_configure("salio", foreground="#95a5a6")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Botones
        frame_botones = tk.Frame(root, bg="#f0f0f0")
        frame_botones.pack(pady=8)

        tk.Button(
            frame_botones, text="Iniciar simulacion (5 vehiculos)",
            command=self.iniciar_simulacion,
            bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
            width=24, height=2, cursor="hand2"
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            frame_botones, text="Agregar vehiculo",
            command=self.agregar_vehiculo,
            bg="#2980b9", fg="white", font=("Arial", 10, "bold"),
            width=18, height=2, cursor="hand2"
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            frame_botones, text="Reiniciar log",
            command=self.reiniciar,
            bg="#e67e22", fg="white", font=("Arial", 10, "bold"),
            width=14, height=2, cursor="hand2"
        ).grid(row=0, column=2, padx=8)

        # Iniciar ciclo de lectura de eventos
        self.ocupados = 0
        self.en_espera = 0
        self.leer_eventos()

    def actualizar_espacios(self, ocupados):
        """Colorea los cuadros del parqueadero: rojo=ocupado, verde=libre."""
        for i, canvas in enumerate(self.espacios_canvas):
            if i < ocupados:
                canvas.configure(bg="#e74c3c", highlightbackground="#c0392b")
            else:
                canvas.configure(bg="#2ecc71", highlightbackground="#27ae60")

    def actualizar_tabla(self, nombre, estado):
        """Inserta o actualiza la fila del vehículo en la tabla."""
        for item in self.tabla.get_children():
            if self.tabla.item(item)["values"][0] == nombre:
                self.tabla.item(item, values=(nombre, estado), tags=(estado,))
                return
        self.tabla.insert("", "end", values=(nombre, estado), tags=(estado,))

    def agregar_vehiculo(self):
        self.contador_vehiculos += 1
        nombre = f"Vehiculo {self.contador_vehiculos}"
        t = threading.Thread(target=vehiculo, args=(nombre,), daemon=True)
        t.start()

    def iniciar_simulacion(self):
        for _ in range(5):
            self.agregar_vehiculo()

    def reiniciar(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

    def leer_eventos(self):
        while not eventos.empty():
            evento = eventos.get()

            if evento[0] == "esperando":
                nombre = evento[1]
                self.en_espera += 1
                self.label_espera.config(text=f"En espera: {self.en_espera}")
                self.actualizar_tabla(nombre, "esperando")

            elif evento[0] == "entro":
                nombre, ocupados = evento[1], evento[2]
                self.ocupados = ocupados
                self.en_espera = max(0, self.en_espera - 1)
                self.label_disponibles.config(text=f"Disponibles: {CAPACIDAD - ocupados}")
                self.label_ocupados.config(text=f"Ocupados: {ocupados}")
                self.label_espera.config(text=f"En espera: {self.en_espera}")
                self.actualizar_espacios(ocupados)
                self.actualizar_tabla(nombre, "estacionado")

            elif evento[0] == "salio":
                nombre, ocupados = evento[1], evento[2]
                self.ocupados = ocupados
                self.label_disponibles.config(text=f"Disponibles: {CAPACIDAD - ocupados}")
                self.label_ocupados.config(text=f"Ocupados: {ocupados}")
                self.actualizar_espacios(ocupados)
                self.actualizar_tabla(nombre, "salio")

        self.root.after(200, self.leer_eventos)
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.io import wavfile

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Aplicación de Señales y Fourier")
        self.geometry("400x200")

        # Combobox para seleccionar el tipo de señal
        self.seleccion = ttk.Combobox(self, values=["Sinusoidal", "Archivo"])
        self.seleccion.grid(row=0, column=0, padx=10, pady=10)
        self.seleccion.bind("<<ComboboxSelected>>", lambda event: self.cargar_opcion())
        self.seleccion.set("Seleccione una opción")

        # Botón para cargar señal o archivo
        self.boton_cargar = tk.Button(self, text="Cargar", command=self.mostrar_grafico)
        self.boton_cargar.grid(row=0, column=1, padx=10, pady=10)

        # Etiqueta y entrada para ingresar frecuencias
        self.label_frecuencias = tk.Label(self, text="Frecuencias (separadas por comas):")
        self.label_frecuencias.grid(row=1, column=0, padx=10, pady=10)

        self.entry_frecuencias = tk.Entry(self)
        self.entry_frecuencias.grid(row=1, column=1, padx=10, pady=10)

        # Botón para representar la señal
        self.boton_representar = tk.Button(self, text="Representar Señal", command=self.mostrar_grafico)
        self.boton_representar.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Deshabilitar elementos al inicio
        self.boton_cargar["state"] = "disabled"
        self.entry_frecuencias["state"] = "disabled"
        self.boton_representar["state"] = "disabled"

    def cargar_opcion(self):
        # Se ejecuta cuando se selecciona una opción en el combobox
        opcion = self.seleccion.get()

        if opcion == "Sinusoidal":
            # Habilita los elementos necesarios para ingresar frecuencias sinusoidales
            self.boton_representar["state"] = "normal"
            self.boton_cargar["state"] = "disabled"
            self.entry_frecuencias["state"] = "normal"

        elif opcion == "Archivo":
            # Habilita los elementos necesarios para cargar un archivo de audio
            self.entry_frecuencias["state"] = "disabled"
            self.boton_cargar["state"] = "normal"
            self.boton_representar["state"] = "disabled"
            
        else:
            # Deshabilita todos los elementos si la opción no es válida
            self.boton_cargar["state"] = "disabled"
            self.entry_frecuencias["state"] = "disabled"
            self.boton_representar["state"] = "disabled"
        

    def mostrar_grafico(self):
        # Se ejecuta al presionar el botón "Cargar" o "Representar Señal"
        opcion = self.seleccion.get()

        if opcion == "Sinusoidal":
            self.mostrar_grafico_sinusoidal()
        elif opcion == "Archivo":
            self.mostrar_grafico_archivo()

    def mostrar_grafico_sinusoidal(self):
        # Genera y muestra gráficos para señales sinusoidales
        try:
            frecuencias = [float(f) for f in self.entry_frecuencias.get().split(',')]
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese frecuencias válidas.")
            return
    
        tiempo = np.arange(0, 1, 0.001)
        senales = np.sum([np.sin(2 * np.pi * f * tiempo) for f in frecuencias], axis=0)
    
        # Gráfico de la señal sinusoidal
        fig, axs = plt.subplots(2, 1, figsize=(12, 8))
        axs[0].plot(tiempo, senales)
        axs[0].set_title("Señal Sinusoidal")
        axs[0].set_xlabel("Tiempo")
        axs[0].set_ylabel("Amplitud")
        axs[0].grid(True)
    
        # Transformada de Fourier y gráfico
        transformada = fft(senales)
        frecuencias = np.fft.fftfreq(len(transformada), 0.001)
        frecuencias_positivas = frecuencias[:len(frecuencias)//2]
        modulo_transformada = 20 * np.log10(np.abs(transformada[:len(transformada)//2]))
        #modulo_transformada = np.abs(transformada[:len(transformada)//2]) SIN dB

        axs[1].plot(frecuencias_positivas, modulo_transformada)
        axs[1].set_title("Transformada de Fourier (dB)")
        axs[1].set_xlabel("Frecuencia")
        axs[1].set_ylabel("Magnitud (dB)")
        axs[1].grid(True)

    def mostrar_grafico_archivo(self):
        # Abre un cuadro de diálogo para seleccionar un archivo de audio y muestra gráficos
        archivo_path = filedialog.askopenfilename(filetypes=[("Archivos de audio", "*.wav")])

        if archivo_path:
            fs, data = wavfile.read(archivo_path)

            # Gráfico de la señal del archivo de audio
            fig, axs = plt.subplots(2, 1, figsize=(12, 8))
            axs[0].plot(data)
            axs[0].set_title("Señal del Archivo")
            axs[0].set_xlabel("Tiempo (s)")
            axs[0].set_ylabel("Amplitud")
            axs[0].grid(True)

            # Transformada de Fourier y gráfico
            transformada = fft(data)
            frecuencias = np.fft.fftfreq(len(transformada), 1/fs)
            frecuencias_positivas = frecuencias[:len(frecuencias)//2]
            modulo_transformada = 20 * np.log10(np.abs(transformada[:len(transformada)//2]))
            #modulo_transformada = np.abs(transformada[:len(transformada)//2]) SIN dB
            axs[1].plot(frecuencias_positivas, modulo_transformada )
            axs[1].set_xlabel("Frecuencia (Hz)")
            axs[1].set_ylabel("Magnitud (dB)")
            axs[1].grid(True)

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.io import wavfile

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Aplicación de Señales y Fourier")
        self.geometry("400x200")

        self.seleccion = ttk.Combobox(self, values=["Sinusoidal", "Archivo"])
        self.seleccion.set("Seleccione una opción")
        self.seleccion.grid(row=0, column=0, padx=10, pady=10)
        self.seleccion.bind("<<ComboboxSelected>>", lambda event: self.cargar_opcion())


        self.boton_cargar = tk.Button(self, text="Cargar", command=self.mostrar_grafico)
        self.boton_cargar.grid(row=0, column=1, padx=10, pady=10)

        self.label_frecuencias = tk.Label(self, text="Frecuencias (separadas por comas):")
        self.label_frecuencias.grid(row=1, column=0, padx=10, pady=10)

        self.entry_frecuencias = tk.Entry(self)
        self.entry_frecuencias.grid(row=1, column=1, padx=10, pady=10)

        self.boton_representar = tk.Button(self, text="Representar Señal", command=self.mostrar_grafico)
        self.boton_representar.grid(row=2, column=0, columnspan=2, pady=10)


    def cargar_opcion(self):
        opcion = self.seleccion.get()

        if opcion == "Sinusoidal":
            self.boton_representar["state"] = "normal"
            self.boton_cargar["state"] = "disabled"
            self.entry_frecuencias["state"] = "normal"

        elif opcion == "Archivo":
            self.entry_frecuencias["state"] = "disabled"
            self.boton_cargar["state"] = "normal"
            self.boton_representar["state"] = "disabled"
        

    def mostrar_grafico(self):
        opcion = self.seleccion.get()

        if opcion == "Sinusoidal":
            self.mostrar_grafico_sinusoidal()
        elif opcion == "Archivo":
            self.mostrar_grafico_archivo()

    def mostrar_grafico_sinusoidal(self):
        try:
            frecuencias = [float(f) for f in self.entry_frecuencias.get().split(',')]
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese frecuencias válidas.")
            return
    
        tiempo = np.arange(0, 1, 0.001)
        senales = np.sum([np.sin(2 * np.pi * f * tiempo) for f in frecuencias], axis=0)
    
        fig, axs = plt.subplots(2, 1, figsize=(12, 8))
        axs[0].plot(tiempo, senales)
        axs[0].set_title("Señal Sinusoidal")
        axs[0].set_xlabel("Tiempo")
        axs[0].set_ylabel("Amplitud")
        axs[0].grid(True)
    
        transformada = fft(senales)
        frecuencias = np.fft.fftfreq(len(transformada), 0.001)
        axs[1].plot(frecuencias[frecuencias >= 0], 20 * np.log10(np.abs(transformada[frecuencias >= 0]) + 1e-10))
        axs[1].set_title("Transformada de Fourier (dB)")
        axs[1].set_xlabel("Frecuencia")
        axs[1].set_ylabel("Magnitud (dB)")
        axs[1].grid(True)



    def mostrar_grafico_archivo(self):
        archivo_path = filedialog.askopenfilename(filetypes=[("Archivos de audio", "*.wav")])

        if archivo_path:
            fs, data = wavfile.read(archivo_path)

            # Mostrar la señal
            fig, axs = plt.subplots(2, 1, figsize=(12, 8))
            axs[0].plot(data)
            axs[0].set_title("Señal del Archivo")
            axs[0].set_xlabel("Tiempo (s)")
            axs[0].set_ylabel("Amplitud")
            axs[0].grid(True)

            # Mostrar la Transformada de Fourier
            transformada = fft(data)
            frecuencias = np.fft.fftfreq(len(transformada), 1/fs)
            axs[1].plot(frecuencias[frecuencias >= 0], 20 * np.log10(np.abs(transformada[frecuencias >= 0])))
            axs[1].set_title("Transformada de Fourier del Archivo (dB)")
            axs[1].set_xlabel("Frecuencia (Hz)")
            axs[1].set_ylabel("Magnitud (dB)")
            axs[1].grid(True)


   

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()

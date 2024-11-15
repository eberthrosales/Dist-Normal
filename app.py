from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Implementar la función que calcula la PDF de acuerdo a la fórmula de la distribución normal
def calcular_funcion_densidad(x, media, desviacion_estandar):
    """Calcula la densidad de probabilidad para un conjunto de puntos."""
    return (1 / (desviacion_estandar * np.sqrt(2 * np.pi))) * np.exp(-((x - media)**2) / (2 * desviacion_estandar**2))

# Generar datos simulados basados en la distribución normal
def generar_datos_normal(media, desviacion_estandar, num_muestras=1000):
    """Genera un conjunto de datos aleatorios con distribución normal."""
    return np.random.normal(media, desviacion_estandar, num_muestras)

# Calcular la media y desviación estándar de un conjunto de datos
def calcular_media_y_desviacion(muestras):
    """Calcula la media y desviación estándar de las muestras."""
    return np.mean(muestras), np.std(muestras)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Obtener los valores de la media y la desviación estándar desde el formulario
            media = float(request.form["media"])
            desviacion_estandar = float(request.form["desviacion"])

            # Validar que la desviación estándar sea positiva
            if desviacion_estandar <= 0:
                raise ValueError("La desviación estándar debe ser positiva.")

            # Generar los datos y la gráfica
            muestras = generar_datos_normal(media, desviacion_estandar)

            # Calcular la media y la desviación estándar de las muestras generadas
            calculada_media, calculada_desviacion = calcular_media_y_desviacion(muestras)

            # Crear un conjunto de puntos para la distribución normal
            x = np.linspace(min(muestras), max(muestras), 1000)
            pdf = calcular_funcion_densidad(x, media, desviacion_estandar)

            # Crear el gráfico
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(muestras, bins=30, density=True, alpha=0.6, color='g', label='Histograma de Muestras')
            ax.plot(x, pdf, 'k-', lw=2, label='Distribución Normal (PDF)')
            ax.set_title('Distribución Normal')
            ax.set_xlabel('Valor')
            ax.set_ylabel('Densidad de Probabilidad')
            ax.legend()
            ax.grid(True)

            # Guardar la gráfica en un objeto en memoria y convertirla a formato base64
            img = io.BytesIO()
            plt.savefig(img, format="png")
            img.seek(0)
            img_base64 = base64.b64encode(img.getvalue()).decode("utf-8")
            plt.close(fig)

            # Pasar los resultados al renderizar la plantilla
            return render_template(
                "index.html", 
                img_data=img_base64, 
                media=media, 
                desviacion=desviacion_estandar, 
                calculada_media=calculada_media, 
                calculada_desviacion=calculada_desviacion
            )

        except ValueError as e:
            # Si hay un error en los datos, mostrar un mensaje de error
            return render_template("index.html", error=str(e))

    return render_template("index.html", img_data=None)

if __name__ == "__main__":
    app.run(debug=True)

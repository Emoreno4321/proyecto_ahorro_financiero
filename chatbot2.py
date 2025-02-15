from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# Función para cargar datos desde el archivo CSV
def cargar_datos():
    gastos_hormiga = {}
    decisiones_inteligentes = {}

    with open('gastos_hormiga.csv', newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Saltar la cabecera

        for categoria, gasto, recomendacion in lector:
            if categoria not in gastos_hormiga:
                gastos_hormiga[categoria] = []
            gastos_hormiga[categoria].append(gasto)
            decisiones_inteligentes[gasto] = recomendacion

    return gastos_hormiga, decisiones_inteligentes

# Cargar datos una sola vez al inicio
gastos_hormiga, decisiones_inteligentes = cargar_datos()

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    mensaje = "¡Bienvenido a tu chatbot de decisiones inteligentes!"
    categorias = ["Selecciona Opción"] + list(gastos_hormiga.keys())
    seleccion_categoria = None
    lista_gastos = []
    seleccion_gasto = None
    recomendacion = None
    ahorro_semanal = ahorro_mensual = ahorro_anual = None
    
    if request.method == 'POST':
        seleccion_categoria = request.form.get('categoria')
        if seleccion_categoria in gastos_hormiga:
            lista_gastos = ["Selecciona Opción"] + gastos_hormiga[seleccion_categoria]
        
        seleccion_gasto = request.form.get('gasto')
        if seleccion_gasto in decisiones_inteligentes:
            recomendacion = decisiones_inteligentes[seleccion_gasto]
            
            # Obtener el valor ingresado por el usuario
            costo = request.form.get('costo')
            if costo and costo.isdigit():
                costo = int(costo)
                ahorro_semanal = costo * 7
                ahorro_mensual = costo * 30
                ahorro_anual = costo * 365
    
    return render_template('chatbot.html', mensaje=mensaje, categorias=categorias, 
                           seleccion_categoria=seleccion_categoria, lista_gastos=lista_gastos, 
                           seleccion_gasto=seleccion_gasto, recomendacion=recomendacion,
                           ahorro_semanal=ahorro_semanal, ahorro_mensual=ahorro_mensual, ahorro_anual=ahorro_anual)

if __name__ == '__main__':
    app.run(debug=True)
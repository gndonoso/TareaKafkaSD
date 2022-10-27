import json
from flask import Flask, render_template, request
from kafka.structs import TopicPartition
from kafka import KafkaConsumer

app = Flask(__name__)

def consumeVenta():

    topic = 'NuevaVenta'
    bootstrap_servers = 'kafka:9092'

    consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers, group_id='estadisticasVentas', consumer_timeout_ms = 1000)
    consumer.assign([TopicPartition(topic, 0)])

    for msg in consumer:
        agregar_venta(json.loads(msg.value))

    consumer.close()

def consumeCliente():

    topic = 'NuevaVenta'
    bootstrap_servers = 'kafka:9092'

    consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers, group_id='estadisticasCliente', consumer_timeout_ms = 1000)
    consumer.assign([TopicPartition(topic, 1)])

    for msg in consumer:
        agregar_cliente(json.loads(msg.value))
    
    consumer.close()

ventas = []
clientes = []
estadisticas = []
promedios = []

def agregar_venta(msg):

    info = []
    info.append(msg['carrito'])
    info.append(msg['cantidad'])
    ventas.append(info)

def agregar_cliente(msg):
    print("Agregando cliente", msg)
    info = []
    info.append(msg['carrito'])
    info.append(msg['cliente'])
    info.append(msg['cantidad'])
    clientes.append(info)

def calcular_estadisticas():

    ventas.sort(key=lambda x: x[0])
    carrito_actual = int(ventas[0][0])
    ventas_totales = 0
    cantidad_total = 0

    for i in range (len(ventas) + 1):
        if i != len(ventas):
            if int(ventas[i][0]) == carrito_actual:
                cantidad_total += int(ventas[i][1])
                ventas_totales += 1
            else :
                promedio_venta = cantidad_total / ventas_totales
                agregar = [carrito_actual, ventas_totales, cantidad_total, promedio_venta]
                estadisticas.append(agregar)
                carrito_actual = int(ventas[i][0])
                cantidad_total = int(ventas[i][1])
                ventas_totales = 1
        else:
            promedio_venta = cantidad_total / ventas_totales
            agregar = [carrito_actual, ventas_totales, cantidad_total, promedio_venta]
            estadisticas.append(agregar)

def calcular_estadisticas_cliente():
    
    clientes.sort(key=lambda x: (x[0], x[1]))
    print("Clientes ordenados", clientes)
    carrito_actual = int(clientes[0][0])
    cliente_actual = clientes[0][1]
    cantidad_cliente = 0
    compras_cliente = 0
    print("Carrito actual", carrito_actual)
    print("Cliente actual", cliente_actual)

    for i in range (len(clientes) + 1):
        if i != len(clientes):
            if int(clientes[i][0]) == carrito_actual and clientes[i][1] == cliente_actual:
                cantidad_cliente += int(clientes[i][2])
                compras_cliente += 1
                print("Cantidad cliente", cantidad_cliente)
                print("Compras cliente", compras_cliente)
            else :
                promedio_venta = cantidad_cliente / compras_cliente
                agregar = [carrito_actual, cliente_actual, promedio_venta]
                print("Agregando promedio", agregar)
                promedios.append(agregar)
                carrito_actual = int(clientes[i][0])
                cliente_actual= clientes[i][1]
                cantidad_cliente = int(clientes[i][2])
                compras_cliente = 1
        else:
            promedio_venta = int(cantidad_cliente) / compras_cliente
            agregar = [carrito_actual, cliente_actual, promedio_venta]
            print("Agregando promedio", agregar)
            promedios.append(agregar)

def view_estadisticas():
    return estadisticas

def view_promedios():
    print("Promedios", promedios)
    return promedios

def get_ventas():
    return ventas

def delete_data():
    estadisticas.clear()
    promedios.clear()
    clientes.clear()
    ventas.clear()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Ventas', methods = ['POST'])
def Ventas():
    if request.method == 'POST':
        delete_data()
        consumeVenta()
        consumeCliente()
        if get_ventas() != []:
            calcular_estadisticas()
            calcular_estadisticas_cliente()
        estadistica = view_estadisticas()
        promedio = view_promedios()
    return render_template('estadisticas.html', estadisticas = estadistica, promedios = promedio)

if __name__== "__main__":
    app.run(debug=True)
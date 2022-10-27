from kafka import KafkaConsumer
from kafka.structs import TopicPartition
import json
from flask import Flask, render_template, redirect
import time

app = Flask(__name__)

carritosActivos = []
infoCarritos = []
carritosPerdidos = []

def venta():

    topic = 'Ubicacion'
    bootstrap_servers = 'kafka:9092'

    consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers, auto_offset_reset='latest', group_id='ubiActual', consumer_timeout_ms = 700)
    consumer.assign([TopicPartition(topic, 0)])

    for message in consumer:
        valores = json.loads(message.value)
        verificarCarrito(valores)
        
    consumer.close()

def aviso():

    topic = 'Ubicacion'
    bootstrap_servers = 'kafka:9092'
    
    consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers, auto_offset_reset='latest', group_id='aviso', consumer_timeout_ms = 1500)
    consumer.assign([TopicPartition(topic, 1)])

    for message in consumer:
        valores = json.loads(message.value)
        perdido = []
        perdido.append(valores['carrito'])
        perdido.append(valores['latitud'])
        perdido.append(valores['longitud'])
        perdido.append(valores['hora'])
        carritosPerdidos.append(perdido)
        
    consumer.close()

def verificarCarrito(msg):

    nuevoCarrito = []
    carrito = msg['carrito']
    latitud = msg['latitud']
    longitud = msg['longitud']
    segundos = msg['segundos']

    if carrito not in carritosActivos:
        carritosActivos.append(carrito)
        nuevoCarrito.append(carrito)
        nuevoCarrito.append(latitud)
        nuevoCarrito.append(longitud)
        nuevoCarrito.append(segundos)
        infoCarritos.append(nuevoCarrito)

    else:
        for info in infoCarritos:
            if info[0] == carrito:
                info[1] = latitud
                info[2] = longitud
                info[3] = segundos     

def verificarHora():
    
    for info in infoCarritos:
        if float(info[3]) + 60 < time.time():
            infoCarritos.remove(info)
            carritosActivos.remove(info[0])

def viewInfoCarritos():
    return infoCarritos

def viewCarritosPerdidos():
    return carritosPerdidos

@app.route('/')
def index():
    return redirect('ubicacion')

@app.route('/ubicacion')
def ubicacion():
    verificarHora()
    venta()
    aviso()
    infoCarritos = viewInfoCarritos()
    carritosPerdidos = viewCarritosPerdidos()
    return render_template('index.html', carritos=infoCarritos, perdidos=carritosPerdidos)

if __name__== "__main__":
    app.run(debug = True)
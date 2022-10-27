import json
from flask import Flask, render_template, request
from aiokafka import AIOKafkaProducer
import asyncio

app = Flask(__name__)
topic_list = []

async def IngresoMiembro(miembro):
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092')
    await producer.start()
    try:
        await producer.send_and_wait("NuevoMiembro", miembro, partition=0)
    finally:
        await producer.stop()

async def IngresoMiembroPremium(miembro):
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092')
    await producer.start()
    try:
        await producer.send_and_wait("NuevoMiembro", miembro, partition=1)
    finally:
        await producer.stop()

async def IngresoVenta(venta):
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092')
    await producer.start()
    try:
        await producer.send_and_wait("NuevaVenta", venta, partition=0)
    finally:
        await producer.stop()

async def IngresoCliente(venta):
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092')
    await producer.start()
    try:
        await producer.send_and_wait("NuevaVenta", venta, partition=1)
    finally:
        await producer.stop()

async def Stock(stock):
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092')
    await producer.start()
    try:
        await producer.send_and_wait("Stock", stock, partition=0)
    finally:
        await producer.stop()

async def alertaStock(stock):
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092')
    await producer.start()
    try:
        await producer.send_and_wait("Stock", stock, partition=1)
    finally:
        await producer.stop()

async def IngresoUbicacion(coordenadas):
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092')
    await producer.start()
    try:
        await producer.send_and_wait("Ubicacion", coordenadas, partition=0)
    finally:
        await producer.stop()

async def IngresoAviso(coordenadas):
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092')
    await producer.start()
    try:
        await producer.send_and_wait("Ubicacion", coordenadas, partition=1)
    finally:
        await producer.stop()

#---------------------- Nueva Venta ----------------------    
@app.route('/')
def index():
        return render_template('index.html')

@app.route('/NuevaVenta', methods=['POST']) 
def NuevaVenta():
    if request.method == 'POST':

        carrito = request.form['carrito']
        cliente = request.form['cliente']
        cantidad = request.form['cantidad']
        hora = request.form['hora'] 

        venta = {'carrito' : carrito, 'cantidad': cantidad, 'hora': hora}
        venta = json.dumps(venta).encode('utf-8')

        asyncio.run(IngresoVenta(venta))

        nuevoCliente = {'carrito' : carrito, 'cliente': cliente, 'cantidad': cantidad}
        nuevoCliente = json.dumps(nuevoCliente).encode('utf-8')

        asyncio.run(IngresoCliente(nuevoCliente))
        
        latitud = request.form['Latitud']
        longitud = request.form['Longitud']
        segundos = request.form['segundos']

        ubicacion = {'carrito' : carrito, 'latitud' : latitud, 'longitud': longitud, 'segundos': segundos}
        ubicacion = json.dumps(ubicacion).encode('utf-8')

        asyncio.run(IngresoUbicacion(ubicacion))

        stock = request.form['stock']

        stockCarrito = {'carrito' : carrito, 'stock': stock}
        stockCarrito = json.dumps(stockCarrito).encode('utf-8')

        if int(stock) < 20:
            asyncio.run(alertaStock(stockCarrito))
        else:
            asyncio.run(Stock(stockCarrito))
        
    return render_template('index.html')

#---------------------- Nuevo Miembro ----------------------
@app.route('/Miembro')
def Miembro():
    return render_template('NuevoMiembro.html')

@app.route('/NuevoMiembro', methods=['POST'])
def NuevoMiembro():
    if request.method == 'POST':
        nombre = request.form['name']
        apellido = request.form['lastname']
        rut = request.form['rut']
        email = request.form['email']
        patente = request.form['patente']
        premium = request.form['premium']
        cliente={'nombre': nombre, 'apellido': apellido, 'rut': rut, 'email': email, 'patente': patente,'premium': premium}
        cliente = json.dumps(cliente).encode('utf-8')
        if premium == 'true':
            asyncio.run(IngresoMiembroPremium(cliente))
        elif premium == 'false':
            asyncio.run(IngresoMiembro(cliente))
    return render_template('NuevoMiembro.html')

#---------------------- Aviso ----------------------
@app.route('/Perdido')
def Perdido():
    return render_template('index.html')

@app.route('/Aviso', methods=['POST'])
def Aviso():
    if request.method == 'POST':
        carrito = request.form['carrito']
        latitud = request.form['LatitudAviso']
        longitud = request.form['LongitudAviso']
        hora = request.form['horaAviso'] 
        ubicacion = {'carrito' : carrito, 'latitud' : latitud, 'longitud': longitud, 'hora': hora}
        ubicacion = json.dumps(ubicacion).encode('utf-8')
        asyncio.run(IngresoAviso(ubicacion))
    return render_template('index.html')

if __name__== "__main__":
    app.run(debug = True)
    

import Dispositivo

if __name__ == '__main__':
    print("---- SENSOR - Temperatura y Humedad ----")
    sensor = Dispositivo.Sensor("sensor_DHT11", "NNN", "activo", 5, 23)
    sensor.iniciar_conexion()
    sensor.mantener_conexion()
    
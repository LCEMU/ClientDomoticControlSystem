import Dispositivo

if __name__ == '__main__':    
    print("\n---- ACTUADOR - Rele ----")
    actuador = Dispositivo.Actuador("actuador_rele", "YNN", "inactivo", 5, 17)
    actuador.iniciar_conexion()
    actuador.mantener_conexion()
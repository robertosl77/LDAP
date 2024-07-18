class Consola:
    def manejador(self):
        while True:
            opcion = self.bienvenida()
            if opcion == 3:
                print("Saliendo...")
                break
            self.ejecutar_opcion(opcion)

    @staticmethod
    def bienvenida():
        mensaje=f"""

            Bienvenido al LdapManager by Sr.Macros! [Python]
            --------------------------------------

            Ingrese la opcion deseada: 
            \t1. Nueva Ldap
            \t2. Lista las ldap almacenados
            \t3. Salir

            >"""
        # 
        while True:
            respuesta= input(mensaje).strip()
            if respuesta.isnumeric():
                respuesta= int(respuesta)
                if respuesta in range(1,4):
                    return respuesta

    def ejecutar_opcion(self, opcion):
        switcher = {
            1: self.nueva_ldap,
            2: self.lista_ldap,
            3: self.salir
        }
        func = switcher.get(opcion, self.default)
        func()

    def nueva_ldap(self):
        print("Nueva LDAP seleccionada.")
        # Lógica para nueva LDAP

    def lista_ldap(self):
        print("Lista de LDAP almacenados.")
        # Lógica para listar LDAP

    def salir(self):
        print("Saliendo...")
        # Lógica para salir                
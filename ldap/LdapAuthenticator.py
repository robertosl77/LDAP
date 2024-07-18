from ldap3 import Server, Connection, ALL, SUBTREE
import ldap3
import re

class LdapAuthenticator:
    def __init__(self, server_address, user_dn, password, user_search_base, user_search_filter):
        self.server_address = server_address
        self.user_dn = user_dn
        self.password = password
        self.user_search_base = user_search_base
        self.user_search_filter = user_search_filter
        self.server = Server(self.server_address, get_info=ALL)
    
    def autenticar(self, username, user_password):
        try:
            conn = Connection(self.server, user=self.user_dn, password=self.password, auto_bind=True)
            search_filter = self.user_search_filter.format(username)
            conn.search(search_base=self.user_search_base, search_filter=search_filter, search_scope=SUBTREE, attributes=['cn', 'memberOf'])

            if len(conn.entries) == 0:
                print("Authentication failed: user not found or not in required groups.")
                return False, []

            user_dn = conn.entries[0].entry_dn
            user_conn = Connection(self.server, user=user_dn, password=user_password, authentication='SIMPLE')
            if user_conn.bind():
                print(f"Authentication successful for user: {username}")
                user_groups = conn.entries[0].memberOf.values if 'memberOf' in conn.entries[0] else []

                # Extraer los grupos del filtro de búsqueda
                pattern = re.compile(r'memberOf=([^)]*)')
                search_groups = pattern.findall(self.user_search_filter)

                user_roles = [group for group in search_groups if group in user_groups]

                user_conn.unbind()
                return True, user_roles
            else:
                print("Authentication failed: incorrect password.")
                return False, []
        except Exception as e:
            print(f"An error occurred: {e}")
            return False, []

# Configuración de los parámetros LDAP
URL_LDAP = "ldap://192.168.145.50:389"
USUARIO_LDAP = "CN=SVC_consulta_ot,OU=Cuentas de Servicio,DC=pro,DC=edenor"
PASSWORD_LDAP = "Edenor2010"
USER_SEARCH_FILTER = "(&(cn={0})(|(memberOf=CN=APP_PortalENRE_Reclamos_Operador,OU=PortalENRE_Reclamos,OU=Aplicaciones,OU=Grupos,DC=pro,DC=edenor)(memberOf=CN=APP_PortalENRE_Reclamos_Consulta,OU=PortalENRE_Reclamos,OU=Aplicaciones,OU=Grupos,DC=pro,DC=edenor)))"
USER_SEARCH_BASE = "DC=pro,DC=edenor"

# Ejemplo de uso
ldap_auth = LdapAuthenticator(URL_LDAP, USUARIO_LDAP, PASSWORD_LDAP, USER_SEARCH_BASE, USER_SEARCH_FILTER)
username = 'rsleiva'
user_password = 'Vegetta13'

authenticated, roles = ldap_auth.autenticar(username, user_password)

if authenticated:
    print("Usuario autenticado correctamente.")
    if roles:
        print(f"El usuario pertenece a los roles: {', '.join(roles)}")
    else:
        print("El usuario no pertenece a los grupos requeridos.")
else:
    print("Error en la autenticación del usuario.")

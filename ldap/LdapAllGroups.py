from ldap3 import Server, Connection, ALL, SUBTREE
import ldap3

class LdapAllGroups:
    def __init__(self, server_address, user_dn, password, user_search_base, group_search_base, user_search_filter):
        self.server_address = server_address
        self.user_dn = user_dn
        self.password = password
        self.user_search_base = user_search_base
        self.group_search_base = group_search_base
        self.user_search_filter = user_search_filter
        self.server = Server(self.server_address, get_info=ALL)
    
    def authenticate(self, username, user_password):
        try:
            conn = Connection(self.server, user=self.user_dn, password=self.password, auto_bind=True)
            search_filter = self.user_search_filter.format(username)
            conn.search(search_base=self.user_search_base, search_filter=search_filter, search_scope=SUBTREE, attributes=['cn', 'memberOf'])

            if len(conn.entries) == 0:
                print("Authentication failed: user not found or not in required groups.")
                return False, []

            user_dn = conn.entries[0].entry_dn
            user_conn = Connection(self.server, user=user_dn, password=user_password, authentication=ldap3.SIMPLE)
            if user_conn.bind():
                print(f"Authentication successful for user: {username}")
                # Obtener los grupos del usuario
                user_groups = conn.entries[0].memberOf.values if 'memberOf' in conn.entries[0] else []
                user_conn.unbind()
                return True, user_groups
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
GROUP_SEARCH_BASE = "OU=PortalENRE_Reclamos,OU=Aplicaciones,OU=Grupos,DC=pro,DC=edenor"

# Ejemplo de uso
ldap_auth = LdapAllGroups(URL_LDAP, USUARIO_LDAP, PASSWORD_LDAP, USER_SEARCH_BASE, GROUP_SEARCH_BASE, USER_SEARCH_FILTER)
username = 'rsleiva'
user_password = 'Vegetta13'

authenticated, groups = ldap_auth.authenticate(username, user_password)

if authenticated:
    print("Usuario autenticado y perteneciente a los grupos requeridos.")
    print("Grupos del usuario:", groups)
else:
    print("Error en la autenticación o el usuario no pertenece a los grupos requeridos.")

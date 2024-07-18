import ldap.LdapConfigManager as ldap
from consola.Consola import Consola

def obtieneJsonID():
    config_manager = ldap.LdapConfigManager()
    # Obtener las claves primarias
    return config_manager.get_primary_keys()

def existeJsonID(compara):
    primary_keys = obtieneJsonID()
    resultado= compara.upper() in [key.upper() for key in primary_keys]
    return resultado

# print(existeJsonID('PRO GELEC'))

Consola.manejador()



# Agregar una nueva configuración
# config_manager.add_configuration(
#     "NEW CONFIG",
#     "ldap://new.url:389/DC=new,DC=domain",
#     "CN=new_user,OU=Users,DC=new,DC=domain",
#     "new_password",
#     "(&(cn={0})(|(memberOf=CN=new_group,OU=Groups,DC=new,DC=domain)))",
#     "ou=NewBase",
#     "ou=NewGroups"
# )

# Modificar una configuración existente
# config_manager.modify_configuration(
#     "NEW CONFIG",
#     url_ldap="ldap://modified.url:389/DC=modified,DC=domain"
# )

# Eliminar una configuración
# config_manager.delete_configuration("NEW CONFIG")
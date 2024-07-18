import json

class LdapConfigManager:
    def __init__(self):
        self.json_file = 'ldap.json'

    def _read_json(self):
        try:
            with open(self.json_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"configurations": {}}

    def _write_json(self, data):
        with open(self.json_file, 'w') as file:
            json.dump(data, file, indent=4)

    def get_primary_keys(self):
        data = self._read_json()
        return list(data["configurations"].keys())

    def delete_configuration(self, primary_key):
        data = self._read_json()
        if primary_key in data["configurations"]:
            del data["configurations"][primary_key]
            self._write_json(data)
            return True
        else:
            return False

    def add_configuration(self, name, url_ldap, usuario_ldap, password_ldap, user_search_filter, user_search_base, group_search_base):
        data = self._read_json()
        data["configurations"][name] = {
            "url_ldap": url_ldap,
            "usuario_ldap": usuario_ldap,
            "password_ldap": password_ldap,
            "user_search_filter": user_search_filter,
            "user_search_base": user_search_base,
            "group_search_base": group_search_base
        }
        self._write_json(data)

    def modify_configuration(self, name, url_ldap=None, usuario_ldap=None, password_ldap=None, user_search_filter=None, user_search_base=None, group_search_base=None):
        data = self._read_json()
        if name in data["configurations"]:
            if url_ldap:
                data["configurations"][name]["url_ldap"] = url_ldap
            if usuario_ldap:
                data["configurations"][name]["usuario_ldap"] = usuario_ldap
            if password_ldap:
                data["configurations"][name]["password_ldap"] = password_ldap
            if user_search_filter:
                data["configurations"][name]["user_search_filter"] = user_search_filter
            if user_search_base:
                data["configurations"][name]["user_search_base"] = user_search_base
            if group_search_base:
                data["configurations"][name]["group_search_base"] = group_search_base
            self._write_json(data)
            return True
        else:
            return False

# Ejemplo de uso
# config_manager = LdapConfigManager('ldap.json')

# Obtener las claves primarias
# primary_keys = config_manager.get_primary_keys()
# print(primary_keys)

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

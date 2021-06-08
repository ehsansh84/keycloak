# firstly install:=> pip install python-keycloak
from keycloak import KeycloakOpenID

# Configure client
client_id = "ehsan-app"
realm_name = "demo"
usernme = "admin"
password = "admin"
keycloak_openid = KeycloakOpenID(server_url="http://localhost:8080/auth/",
                    client_id=client_id,
                    realm_name=realm_name,
                    client_secret_key="secret")

# Get WellKnow
config_well_know = keycloak_openid.well_know()

# Get Token
token = keycloak_openid.token(username, password)
token = keycloak_openid.token(username, password, totp="012345")

# Get Userinfo
userinfo = keycloak_openid.userinfo(token['access_token'])

# Refresh token
token = keycloak_openid.refresh_token(token['refresh_token'])

# Logout
keycloak_openid.logout(token['refresh_token'])

# Get Certs
certs = keycloak_openid.certs()

# Get RPT (Entitlement)
token = keycloak_openid.token("user", "password")
rpt = keycloak_openid.entitlement(token['access_token'], "resource_id")

# Instropect RPT
token_rpt_info = keycloak_openid.introspect(keycloak_openid.introspect(token['access_token'], rpt=rpt['rpt'],
                                     token_type_hint="requesting_party_token"))

# Introspect Token
token_info = keycloak_openid.introspect(token['access_token'])

# Decode Token
KEYCLOAK_PUBLIC_KEY = keycloak_openid.public_key()
options = {"verify_signature": True, "verify_aud": True, "verify_exp": True}
token_info = keycloak_openid.decode_token(token['access_token'], key=KEYCLOAK_PUBLIC_KEY, options=options)

# Get permissions by token
token = keycloak_openid.token("user", "password")
keycloak_openid.load_authorization_config("example-authz-config.json")
policies = keycloak_openid.get_policies(token['access_token'], method_token_info='decode', key=KEYCLOAK_PUBLIC_KEY)
permissions = keycloak_openid.get_permissions(token['access_token'], method_token_info='introspect')

# KEYCLOAK ADMIN

from keycloak import KeycloakAdmin

keycloak_admin = KeycloakAdmin(server_url="http://localhost:8080/auth/",
                               username='example-admin',
                               password='secret',
                               realm_name="master",
                               user_realm_name="only_if_other_realm_than_master",
                               client_secret_key="client-secret",
                               verify=True)
        
# Add user                       
new_user = keycloak_admin.create_user({"email": "example@example.com",
                    "username": "example@example.com",
                    "enabled": True,
                    "firstName": "Example",
                    "lastName": "Example"})    

# Add user and raise exception if username already exists
# exist_ok currently defaults to True for backwards compatibility reasons
new_user = keycloak_admin.create_user({"email": "example@example.com",
                    "username": "example@example.com",
                    "enabled": True,
                    "firstName": "Example",
                    "lastName": "Example"},
                    exist_ok=False)
                                        
# Add user and set password                    
new_user = keycloak_admin.create_user({"email": "example@example.com",
                    "username": "example@example.com",
                    "enabled": True,
                    "firstName": "Example",
                    "lastName": "Example",
                    "credentials": [{"value": "secret","type": "password",}]})

# Add user and specify a locale                       
new_user = keycloak_admin.create_user({"email": "example@example.fr",
                    "username": "example@example.fr",
                    "enabled": True,
                    "firstName": "Example",
                    "lastName": "Example",
                    "attributes": {
                      "locale": ["fr"]
                    })    

# User counter
count_users = keycloak_admin.users_count()

# Get users Returns a list of users, filtered according to query parameters
users = keycloak_admin.get_users({})

# Get user ID from name
user_id_keycloak = keycloak_admin.get_user_id("example@example.com")

# Get User
user = keycloak_admin.get_user("user-id-keycloak")

# Update User
response = keycloak_admin.update_user(user_id="user-id-keycloak", 
                                      payload={'firstName': 'Example Update'})

# Update User Password
response = keycloak_admin.set_user_password(user_id="user-id-keycloak", password="secret", temporary=True)
                                      
# Delete User
response = keycloak_admin.delete_user(user_id="user-id-keycloak")

# Get consents granted by the user
consents = keycloak_admin.consents_user(user_id="user-id-keycloak")

# Send User Action
response = keycloak_admin.send_update_account(user_id="user-id-keycloak", 
                                              payload=json.dumps(['UPDATE_PASSWORD']))

# Send Verify Email
response = keycloak_admin.send_verify_email(user_id="user-id-keycloak")

# Get sessions associated with the user
sessions = keycloak_admin.get_sessions(user_id="user-id-keycloak")

# Get themes, social providers, auth providers, and event listeners available on this server
server_info = keycloak_admin.get_server_info()

# Get clients belonging to the realm Returns a list of clients belonging to the realm
clients = keycloak_admin.get_clients()

# Get client - id (not client-id) from client by name
client_id = keycloak_admin.get_client_id("my-client")

# Get representation of the client - id of client (not client-id)
client = keycloak_admin.get_client(client_id="client_id")

# Get all roles for the realm or client
realm_roles = keycloak_admin.get_realm_roles()

# Get all roles for the client
client_roles = keycloak_admin.get_client_roles(client_id="client_id")

# Get client role
role = keycloak_admin.get_client_role(client_id="client_id", role_name="role_name")

# Warning: Deprecated
# Get client role id from name
role_id = keycloak_admin.get_client_role_id(client_id="client_id", role_name="test")

# Create client role
keycloak_admin.create_client_role(client_id='client_id', {'name': 'roleName', 'clientRole': True})

# Assign client role to user. Note that BOTH role_name and role_id appear to be required.
keycloak_admin.assign_client_role(client_id="client_id", user_id="user_id", role_id="role_id", role_name="test")

# Retrieve client roles of a user.
keycloak_admin.get_client_roles_of_user(user_id="user_id", client_id="client_id")

# Retrieve available client roles of a user.
keycloak_admin.get_available_client_roles_of_user(user_id="user_id", client_id="client_id")

# Retrieve composite client roles of a user.
keycloak_admin.get_composite_client_roles_of_user(user_id="user_id", client_id="client_id")

# Delete client roles of a user.
keycloak_admin.delete_client_roles_of_user(client_id="client_id", user_id="user_id", roles={"id": "role-id"})
keycloak_admin.delete_client_roles_of_user(client_id="client_id", user_id="user_id", roles=[{"id": "role-id_1"}, {"id": "role-id_2"}])

# Create new group
group = keycloak_admin.create_group(name="Example Group")

# Get all groups
groups = keycloak_admin.get_groups()

# Get group 
group = keycloak_admin.get_group(group_id='group_id')

# Get group by name
group = keycloak_admin.get_group_by_path(path='/group/subgroup', search_in_subgroups=True)

# Function to trigger user sync from provider
sync_users(storage_id="storage_di", action="action")

# Get client role id from name
role_id = keycloak_admin.get_client_role_id(client_id=client_id, role_name="test")

# Get all roles for the realm or client
realm_roles = keycloak_admin.get_roles()

# Assign client role to user. Note that BOTH role_name and role_id appear to be required.
keycloak_admin.assign_client_role(client_id=client_id, user_id=user_id, role_id=role_id, role_name="test")

# Get all ID Providers
idps = keycloak_admin.get_idps()

# Create a new Realm
keycloak_admin.create_realm(payload={"realm": "demo"}, skip_exists=False)


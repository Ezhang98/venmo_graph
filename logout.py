from venmo_api import Client
import sys

access_token = str(sys.argv[1])
client = Client(access_token=access_token)
client.log_out(f'Bearer {access_token}')
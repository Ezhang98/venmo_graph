# Evan Zhang
# 7/24/2022

import datetime
import traceback
from venmo_api import Client
from pyvis.network import Network

# Read login info from text file
login = open("login_info.txt", "r")

# Get your access token. You will need to complete the 2FA process
# Please store it somewhere safe and use it next time
# Never commit your credentials or token to a git repository
access_token = Client.get_access_token(username=login.readline().strip(),
                                        password=login.readline().strip())

# Initialize api client using an access-token
client = Client(access_token=access_token)
login.close()

# Track how many accounts have private info
num_public = 0
num_private = 0

# Create graph
friend_net = Network()
friend_net.add_node("Evan Zhang", label = "Evan Zhang")

# Transactions
# callback is optional. Max number of transactions per request is 50.
# next_users = client.user.get_user_transactions(user_id=user.id)
error_log = open("log.txt", "a")
error_log.write("\n" + str(datetime.datetime.now()) + "\n")

friend_dic = {}
people = []

try:
    friend_txt = open("people.txt", "r")
    current_line = friend_txt.readline()
    while current_line != "":
        parts = current_line.split()
        friend_net.add_node(parts[2].strip(), label=parts[0])
        friend_net.add_edge("Evan Zhang", parts[2].strip())
        friend_dic[parts[2].strip()] = []
        try:
            users = client.user.get_user_friends_list(user_id=parts[2].strip())
            for user in users:
                # print(user.display_name, user.id, user.username)
                try:
                    friend_net.add_edge(parts[2].strip(), user.display_name)
                except:
                    friend_dic[parts[2].strip()].append(user.display_name)
                    
                    if user.username in people:
                        friend_net.add_node(user.username, label=user.display_name)
                        for friend in friend_dic:
                            for x in friend_dic[friend]:
                                if x == user.username:
                                    friend_net.add_edge(friend, user.username)
                    people.append(user.username)
            # friends_of_friends = client.user.get_user_friends_list(user_id=user.id)
            # for fri in friends_of_friends:
            #     friend_net.add_node(fri.display_name,label=fri.display_name)
            #     friend_net.add_edge(user.display_name, fri.display_name)
            num_public += 1
        except Exception as e1:
            num_private += 1
            tb_str = traceback.format_exception(etype=type(e1), value=e1, tb=e1.__traceback__)
            error_log.write("\n" + "".join(tb_str) + "\n")
        current_line = friend_txt.readline()
except Exception as e2:
    tb_str = traceback.format_exception(etype=type(e2), value=e2, tb=e2.__traceback__)
    error_log.write("\n" + "".join(tb_str) + "\n")


print(f'public: {num_public}, private: {num_private}')
friend_net.show_buttons(filter_=['physics'])
friend_net.show('mygraph.html')

error_log.close()
client.log_out(f'Bearer {access_token}')

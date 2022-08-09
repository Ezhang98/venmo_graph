# Evan Zhang
# 7/24/2022
# updated: 7/31/2022


import datetime
import time
from re import U
import traceback
from venmo_api import Client
from pyvis.network import Network


def make_friend_dic(lst):
    dic = []
    for friend in lst:
        dic.append(friend.display_name)
    return dic


def print_friends_list():
    try:
        users = client.user.get_user_friends_list(user_id=id)
        for friend in users:
            print(friend.display_name, friend.id, friend.username)
    except Exception as e1:
        tb_str = traceback.format_exception(etype=type(e1), value=e1, tb=e1.__traceback__)
        error_log.write("\n" + "".join(tb_str) + "\n")
        print("\n" + "".join(tb_str) + "\n")


def create_transaction_graph(friend_id):
    friend_id = friend_id.strip()
    friend_net = Network()
    friend_net.add_node(id, label = id)
    friend_net.add_node(friend_id, label = friend_id)
    friend_net.add_edge(id, friend_id)

    try:
        my_friends = client.user.get_user_friends_list(user_id=id)
        friend_dic = make_friend_dic(my_friends)
        transactions = client.user.get_user_transactions(user_id=friend_id)
        fr_lst = []
        notes = []
        dates = []
        for tr in transactions:
            if tr.target.id == friend_id:
                fr_lst.append(tr.actor)
            else:
                fr_lst.append(tr.target)
            notes.append(tr.note)
            dates.append(time.ctime(tr.date_completed))
            print(tr)
        for i, friend in enumerate(fr_lst):
            friend_net.add_node(friend.display_name, label = friend.display_name + "\n" + notes[i] + "\n" + dates[i])
            friend_net.add_edge(friend_id, friend.display_name)
            if friend.display_name in friend_dic:
                friend_net.add_edge(id, friend.display_name)
    except Exception as e1:
        tb_str = traceback.format_exception(etype=type(e1), value=e1, tb=e1.__traceback__)
        error_log.write("\n" + "".join(tb_str) + "\n")
        print("\n" + "".join(tb_str) + "\n")

    friend_net.show_buttons(filter_=['physics'])
    friend_net.show('graph.html')


def create_mutuals_graph(friend_id):
    friend_id = friend_id.strip()
    friend_net = Network()
    friend_net.add_node(id, label = id)
    friend_net.add_node(friend_id, label = friend_id)
    friend_net.add_edge(id, friend_id)
    
    try:
        my_friends = client.user.get_user_friends_list(user_id=id)
        friend_dic = make_friend_dic(my_friends)
        friend_of_friends = client.user.get_user_friends_list(user_id=friend_id)
        for friend in friend_of_friends:
            if friend.display_name in friend_dic:
                friend_net.add_node(friend.display_name, label = friend.display_name)
                friend_net.add_edge(friend_id, friend.display_name)
                friend_net.add_edge(id, friend.display_name)
    except Exception as e1:
        tb_str = traceback.format_exception(etype=type(e1), value=e1, tb=e1.__traceback__)
        error_log.write("\n" + "".join(tb_str) + "\n")
        print("\n" + "".join(tb_str) + "\n")

    friend_net.show_buttons(filter_=['physics'])
    friend_net.show('graph.html')


def create_mutual_mutual_graph(fr1, fr2):
    friend_net = Network()
    friend_net.add_node(fr1, label = fr1)
    friend_net.add_node(fr2, label = fr2)
    friend_net.add_edge(fr1, fr2)
    
    try:
        my_friends = client.user.get_user_friends_list(user_id=fr1)
        friend_dic = make_friend_dic(my_friends)
        friend_of_friends = client.user.get_user_friends_list(user_id=fr2)
        for friend in friend_of_friends:
            if friend.display_name in friend_dic:
                friend_net.add_node(friend.display_name, label = friend.display_name)
                friend_net.add_edge(fr2, friend.display_name)
                friend_net.add_edge(fr1, friend.display_name)
    except Exception as e1:
        tb_str = traceback.format_exception(etype=type(e1), value=e1, tb=e1.__traceback__)
        error_log.write("\n" + "".join(tb_str) + "\n")
        print("\n" + "".join(tb_str) + "\n")

    friend_net.show_buttons(filter_=['physics'])
    friend_net.show('graph.html')


# MAIN EXECUTION THREAD

# Read login info from text file
login = open("login.txt", "r")

username = ((login.readline()).split(":")[1]).strip()
password = ((login.readline()).split(":")[1]).strip()
id = ((login.readline()).split(":")[1]).strip()

# Get your access token. You will need to complete the 2FA process
# Please store it somewhere safe and use it next time
# Never commit your credentials or token to a git repository
access_token = Client.get_access_token(username=username,
                                        password=password)
# Initialize api client using an access-token
client = Client(access_token=access_token)
login.close()

error_log = open("log.txt", "a")
error_log.write("\n" + str(datetime.datetime.now()) + "\n")

user_input = ""
input_prompt = "\n\nChoose from these options:\n" + \
                "\t1 - Create a graph of mutual friends from recent transactions of a friend\n" + \
                "\t2 - Create a graph of mutual friends between you and another friend\n" + \
                "\t3 - Print your friends list\n" + \
                "\t4 - Create a graph of mutual friends between 2 friends\n" + \
                "\t0 - Exit\n--> "

while user_input != "0":
    user_input = input(input_prompt)
    if user_input == "1":
        friend_id = input("Enter your friend's id: ")
        create_transaction_graph(friend_id)
    if user_input == "2":
        friend_id = input("Enter your friend's username: ") 
        create_mutuals_graph(friend_id)  
    if user_input == "3":
        print_friends_list()
    if user_input == "4":
        fr1 = input("Enter username 1: ")
        fr2 = input("Enter username 2: ")
        create_mutual_mutual_graph(fr1, fr2)

error_log.close()
client.log_out(f'Bearer {access_token}')

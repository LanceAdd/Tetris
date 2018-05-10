# -*- coding:utf-8 -*-

# server.py 服务器端

import time, threading, socket, json

HOST = "0.0.0.0" # 绑定ip
PORT = 80 # 绑定端口
BUFSIZ = 40960 # 接受数据大小
ADDR = (HOST, PORT) # 地址

users = [] # 用户名
rooms = {} # 房间 用户名->socket
resp_info = {} # 返回信息
grade = {} # 用户名 -> grade

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
server.bind(ADDR)
server.listen(3)

def broadcast(conn ,msg):
    # 对其他的人广播
    for one_conn in rooms.values():
        if one_conn != conn:
            one_conn.send(msg)

def broadcast2(msg):
    # 对所有人广播
    for one_conn in rooms.values():
        one_conn.send(msg)

def manage(client, username):
    while True:
        data = client.recv(BUFSIZ)
        data = json.loads(data.decode("utf-8"))
        print(data)
        if data["behavior"] == "quit":
            client.close()
            if users.index(username) == 0:
                msg = {
                    "result": "OK",
                    "behavior": "roomer leave",
                    "leave_username": username,
                    "leave_user_number": users.index(username)
                }
            else:
                msg = {
                    "result": "OK",
                    "behavior": "user leave",
                    "leave_username": username,
                    "leave_user_number": users.index(username)
                }
            del rooms[username]
            del grade[username]
            users.remove(username)
            msg["room_content"] = len(users)
            print("*"*100)
            print(msg["room_content"])
            print("*"*100)
            if msg["behavior"] == "roomer leave":
                if len(users) == 0:
                    pass
                elif len(users) == 1:
                    msg["new_roomer"] = users[0]
                elif len(users) == 2:
                    msg["new_roomer"] = users[0]
                    msg["new_user2"] = users[1]
                elif len(users) == 3:
                    msg["new_roomer"] = users[0]
                    msg["new_user2"] = users[1]
                    msg["new_user3"] = users[2]
            elif msg["behavior"] == "user leave":
                if len(users) == 0:
                    pass
                elif len(users) == 1:
                    msg["new_roomer"] = users[0]
                elif len(users) == 2:
                    msg["new_roomer"] = users[0]
                    msg["new_user2"] = users[1]
                elif len(users) == 3:
                    msg["new_roomer"] = users[0]
                    msg["new_user2"] = users[1]
                    msg["new_user3"] = users[2]
            print("*"*50)
            print(msg)
            print("*"*50)
            msg = (json.dumps(msg)).encode("utf-8")
            broadcast2(msg)
            print("%s logout" % username)
            break
        elif data["behavior"] == "grade":
            pass
        elif data["behavior"] == "start game":
            if data["username"] == users[0]:
                msg = {
                    "result": "OK",
                    "behavior":"game start"
                }
                msg = (json.dumps(msg)).encode("utf-8")
                current_con = rooms[data["username"]]
                broadcast(current_con, msg)

if __name__ == "__main__":
    while True:
        
        print("wait connect...")
        conn, addr = server.accept()
        userip = addr[1]
        rec = conn.recv(BUFSIZ)
        rec = json.loads(rec.decode("utf-8"))
        username = rec["username"]
        if rec["behavior"] == "enter":
            print("username=" + username + "  ip=" + str(userip))
            if len(rooms) >= 3 and len(users) >= 3:
                resp_info["result"] = "refuse"
                resp_info["reason"] = "the room is full"
                conn.send((json.dumps(resp_info)).encode("utf-8"))
                conn.close()
            elif username in rooms.keys():
                resp_info["result"] = "refuse"
                resp_info["reason"] = "the username exists"
                conn.send((json.dumps(resp_info)).encode("utf-8"))
                conn.close()
            else:
                rooms[username] = conn
                users.append(username)
                grade[username] = 0                
                resp_info["result"] = "OK"
                resp_info["reason"] = "welcome " + username
                resp_info["number"] = users.index(username)
                resp_info["room_content"] = len(users)
                if len(users) == 0:
                    pass
                elif len(users) == 1:
                    resp_info["new_roomer"] = users[0]
                elif len(users) == 2:
                    resp_info["new_roomer"] = users[0]
                    resp_info["new_user2"] = users[1]
                elif len(users) == 3:
                    resp_info["new_roomer"] = users[0]
                    resp_info["new_user2"] = users[1]
                    resp_info["new_user3"] = users[2]
                conn.send((json.dumps(resp_info)).encode("utf-8"))
                if users.index(username) != 0:
                    msg = {
                        "result": "OK",
                        "behavior": "add new user",
                        "new_username": username,
                        "new_user_number": users.index(username)
                    }
                    msg["room_content"] = len(users)
                    if len(users) == 0:
                        pass
                    elif len(users) == 1:
                        msg["new_roomer"] = users[0]
                    elif len(users) == 2:
                        msg["new_roomer"] = users[0]
                        msg["new_user2"] = users[1]
                    elif len(users) == 3:
                        msg["new_roomer"] = users[0]
                        msg["new_user2"] = users[1]
                        msg["new_user3"] = users[2]
                    msg = (json.dumps(msg)).encode("utf-8")
                    broadcast(conn, msg)

                if len(users) == len(rooms) == 3:
                    current_roomer = users[0]
                    current_roomer_connect = rooms[current_roomer]
                    play_msg = {
                        "result":"OK",
                        "behavior":"ready to begain"
                    }
                    current_roomer_connect.send((json.dumps(play_msg)).encode("utf-8"))
                    play_msg2 = {
                        "result":"OK",
                        "behavior":"please wait"
                    }

                    current_user2 = users[1]
                    current_user2_connect = rooms[current_user2]
                    current_user2_connect.send((json.dumps(play_msg2)).encode("utf-8"))
                    
                    current_user3 = users[2]
                    current_user3_connect = rooms[current_user3]
                    current_user3_connect.send((json.dumps(play_msg2)).encode("utf-8"))
                else:
                    pass
                chat = threading.Thread(target=manage, args=(conn, username))
                chat.start()
        else:
            resp_info["result"] = "refuse"
            resp_info["reason"] = "illegal behavior"
            conn.send((json.dumps(resp_info)).encode("utf-8"))
            conn.close()
            
    server.close()








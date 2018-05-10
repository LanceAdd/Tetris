# -*- coding:utf-8 -*-

import sys, socket, json, threading, random

from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget, QMessageBox,
                            QPushButton, QTextEdit, QLineEdit, QToolTip, QLabel,
                            QTextEdit, QMessageBox, QProgressDialog, QComboBox,
                            QMainWindow, QFrame, QDesktopWidget)
from PyQt5.QtGui import QIcon, QFont, QPainter, QColor
from PyQt5.QtCore import QCoreApplication, Qt, QBasicTimer, pyqtSignal

HOST = "127.0.0.1" # 服务器ip
PORT = 80 # 服务器端口号
ADDR = (HOST, PORT) # 服务器地址

# 客户端登录界面
class Login(QWidget):
    def __init__(self):
        # 初始界面
        super().__init__()
        self.initUI()

    def initUI(self):
        # 界面大小，标题， 图标
        self.setGeometry(500, 500, 300, 300)
        self.center()
        self.setWindowTitle("三人俄罗斯方块")
        self.setWindowIcon(QIcon("眼镜蛇.png"))

        # 创建label
        self.lab1 = QLabel("用户名", self)
        self.lab1.setGeometry(20, 50, 100, 30)
        self.lab2 = QLabel("服务器地址", self)
        self.lab2.setGeometry(20, 100, 100, 30)

        # 创建用输入框
        self.current_username = QLineEdit("请输入用户名", self)
        self.current_username.setGeometry(100, 50, 150, 30)
        self.current_username.selectAll()
        self.addr_input = QLineEdit("", self)
        self.addr_input.setGeometry(100, 100, 150, 30)
        
        # 设置提示文本字体和大小
        QToolTip.setFont(QFont("SansSerif", 10))
        # 设置文本提示
        self.addr_input.setToolTip("公网连接无需填写，局域网内填写地址")

        # 获得主机名
        self.hostname = socket.gethostname()

        # 用户名
        if len(self.hostname) != 0:
            self.current_username.setText(self.hostname)
            self.current_username.selectAll()

        # 设置聚焦
        self.current_username.setFocus()

        # 退出键
        self.quit_btn = QPushButton("退出", self)
        self.quit_btn.clicked.connect(QCoreApplication.instance().quit)
        self.quit_btn.resize(100, 30)
        self.quit_btn.move(170, 200)

        # 登录键
        self.login_btn = QPushButton("登录", self)
        self.login_btn.resize(100, 30)
        self.login_btn.move(30, 200)
        self.login_btn.clicked.connect(self.login)
        self.show()

    def login(self):
        # 登录提示
        current_name = self.current_username.text()
        if len(self.addr_input.text()) != 0:
            conn_info = self.addr_input.text()
            HOST = self.addr_input.text().split(":")[0]
            PORT = int(self.addr_input.text().split(":")[1])
        else:
            pass
        if len(current_name) == 0:
            current_name = "用户名为空"
            QMessageBox.about(self, "警报", current_name)
            self.username.clear()
            self.username.setFocus()
        else:
            QMessageBox.about(self, "用户名", "用户名:" + current_name)
            self.client = socket.socket()
            self.client.connect(ADDR)
            self.menu = Menu()
            self.menu.getconnect(current_name, self.client)
            self.menu.show()
            self.close()

    def showprogress(self):
        # 进度条
        self.progress = QProgressDialog(self)
        self.progress.setWindowTitle("登录")
        self.progress.setLabelText("正在连接中")
        self.progress.setCancelButtonText("取消")
        self.progress.setMinimumDuration(5)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setRange(0, 100000)
        for i in range(100000):
            self.progress.setValue(i)
            if self.progress.wasCanceled():
                QMessageBox.warning(self, "提示", "操作失败")
                break
        else:
            self.progress.setValue(100000)

    def center(self):
        # 界面居中
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())

    def closeEvent(self, event):
        # 关闭提示
        reply = QMessageBox.question(self, '三人贪吃蛇',"你确定要离开吗？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# 主菜单界面
# 消息列表 
class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # menu页
        self.setGeometry(300, 300, 300, 300)
        self.center()
        self.setWindowTitle("三人俄罗斯方块")
        self.setWindowIcon(QIcon("眼镜蛇.png"))

        self.title = QLabel("    系统消息", self)
        self.title.setGeometry(0, 0, 300, 20)

        self.user_lab1 = QLabel("房主:", self)
        self.user_lab1.setGeometry(20, 180, 50, 20)
        
        self.user_lab2 = QLabel("玩家一:", self)
        self.user_lab2.setGeometry(120, 180, 50, 20)

        self.user_lab3 = QLabel("玩家二:", self)
        self.user_lab3.setGeometry(210, 180, 50, 20)

        self.username_lab1 = QLabel("", self)
        self.username_lab1.setGeometry(50, 180, 50, 20)

        self.username_lab2 = QLabel("", self)
        self.username_lab2.setGeometry(160, 180, 50, 20)

        self.username_lab3 = QLabel("", self)
        self.username_lab3.setGeometry(250, 180, 50, 20)

        # 消息列表
        self.msg_list = QTextEdit("",self)
        self.msg_list.setGeometry(10, 20, 280, 150)

        self.lab1 = QLabel("难度", self)
        self.lab1.setGeometry(10, 220, 30, 20)

        self.lab2 = QLabel("速度", self)
        self.lab2.setGeometry(10, 250, 30, 20)

        self.lab3 = QLabel("", self)
        self.lab3.setGeometry(150 , 250, 30, 30)

        # 难度选择
        self.double_box1 = QComboBox(self)
        self.double_box1.setGeometry(50, 220, 60, 20)
        self.double_box1.addItem("1")
        self.double_box1.addItem("2")
        self.double_box1.addItem("3")
        self.double_box1.addItem("4")

        # 下降速度选择
        self.double_box2 = QComboBox(self)
        self.double_box2.setGeometry(50, 250, 60, 20)
        self.double_box2.addItem("1")
        self.double_box2.addItem("2")
        self.double_box2.addItem("3")
        self.double_box2.addItem("4")

        self.double_box1.currentTextChanged.connect(self.get_difficulty)
        self.double_box2.currentTextChanged.connect(self.get_speed)

        # 等待游戏键
        self.wait_btn = QPushButton("", self)
        self.wait_btn.setGeometry(200, 220, 50, 50)
        self.wait_btn.setIcon(QIcon("暂停.png"))

        # # 显示分数与等级

        # self.player_1__name = QLabel:

        # self.player_1_grade = QLabel("", self)
        # self.player_1_grade.setGeometry()

        # self.player_2_grade = QLabel("", self)
        # self.player_2_grade.setGeometry()

        # self.player_3_grade = QLabel("", self)
        # self.player_3_grade.setGeometry()


        # self.player_1_level = QLabel("", self)
        # self.player_1_level.setGeometry()

        # self.player_2_level = QLabel("", self)
        # self.player_2_level.setGeometry()

        # self.player_3_level = QLabel("", self)
        # self.player_3_level.setGeometry()


        # 设置文本框只可读
        self.msg_list.setReadOnly(True)
        self.actor = None
    
    def get_difficulty(self):
        # 监听并获取难度等级
        self.difficulty = self.double_box1.currentText()
        print("难度等级" + self.difficulty)
    
    def get_speed(self):
        # 监听并获取方块下降速度
        self.speed = self.double_box2.currentText()
        print("下降速度" + self.speed)

    def getconnect(self, username, client):
        # 传递用户名与连接
        self.username = username
        self.client = client
        self.data = {}
        self.data["username"] = username
        self.data["behavior"] = "enter"
        self.client.send((json.dumps(self.data)).encode("utf-8"))
        self.msg = json.loads((self.client.recv(50960)).decode("utf-8"))
        print(self.msg)
        if self.msg["result"] == "OK":
            self.showprogress()
            self.msg_list.append("服务器连接成功")
            self.msg_list.append("server: " + self.msg["reason"])
            if self.msg["number"] == 0:
                self.msg_list.append("system: " + username + " 成为房主")
                self.username_lab1.setText(username)
                if self.msg["room_content"] == 0:
                    pass
                elif self.msg["room_content"] == 1:
                    pass
                elif self.msg["room_content"] == 2:
                    self.username_lab2.setText(self.msg["new_user2"])
                    self.msg_list.append("system: " + self.msg["new_user2"] + "成为玩家2")
                elif self.msg["room_content"] == 3:
                    self.username_lab2.setText(self.msg["new_user2"])
                    self.msg_list.append("system: " + self.msg["new_user2"] + "成为玩家2")
                    self.username_lab3.setText(self.msg["new_user3"])
                    self.msg_list.append("system: " + self.msg["new_user3"] + "成为玩家3")
            else:
                self.msg_list.append("system: " + username + " 成为玩家" + 
                                    str(self.msg["number"] + 1))
                if self.msg["room_content"] == 0:
                    pass
                elif self.msg["room_content"] == 1:
                    pass
                elif self.msg["room_content"] == 2:
                    self.username_lab1.setText(self.msg["new_roomer"])
                    self.msg_list.append("system: " + self.msg["new_roomer"] + " 是房主")
                    self.username_lab2.setText(self.msg["new_user2"])
                    self.username_lab3.setText("")
                elif self.msg["room_content"] == 3:
                    self.username_lab1.setText(self.msg["new_roomer"])
                    self.msg_list.append("system: " + self.msg["new_roomer"] + " 是房主")
                    self.username_lab2.setText(self.msg["new_user2"])
                    self.msg_list.append("system: " + self.msg["new_user2"] + " 是玩家2")
                    self.username_lab3.setText(self.msg["new_user3"])

        elif self.msg["result"] == "refuse":
            self.showprogress()
            self.msg_list.append("服务器连接失败")
            self.msg_list.append("error: " + self.msg["reason"])
        
        chat = threading.Thread(target=self.manage, args=())
        chat.start()

    def manage(self):
        # 消息监听
        while True:
            self.rec = self.client.recv(40960)
            print(self.rec)
            self.rec = json.loads((self.rec).decode("utf-8"))
            print(self.rec)
            if self.rec["result"] == "OK":
                if self.rec["behavior"] == "add new user":
                    print("加入新的玩家")
                    self.msg_list.append("system: " + "玩家" + 
                                        str(self.rec["new_user_number"] + 1) + 
                                        " " + str(self.rec["new_username"]) + " 加入房间")
                    print("*"*100)
                    if self.rec["room_content"] == 0:
                        self.username_lab1.setText("")
                        self.username_lab2.setText("")
                        self.username_lab3.setText("")
                    elif self.rec["room_content"] == 1:
                        self.username_lab1.setText(self.rec["new_roomer"])
                        self.username_lab2.setText("")
                        self.username_lab3.setText("")
                    elif self.rec["room_content"] == 2:
                        self.username_lab1.setText(self.rec["new_roomer"])
                        self.username_lab2.setText(self.rec["new_user2"])
                        self.username_lab3.setText("")
                    elif self.rec["room_content"] == 3:
                        self.username_lab1.setText(self.rec["new_roomer"])
                        self.username_lab2.setText(self.rec["new_user2"])
                        print("hello world")
                        self.username_lab3.setText(self.rec["new_user3"])
                        print("goodbye world")
                        
                elif self.rec["behavior"] == "user leave":
                    if self.rec["leave_username"] == self.username:
                        self.msg_list.append("system: 本机离开房间")
                    else:
                        self.msg_list.append("system: 玩家"+ 
                                            str(self.rec["leave_user_number"] + 1)+ 
                                            " " + str(self.rec["leave_username"]) + 
                                            " 离开房间")
                        print(self.rec["leave_user_number"])
                        if (self.rec["room_content"]) == 0:
                            self.username_lab1.setText("")
                            self.username_lab2.setText("")
                            self.username_lab3.setText("")
                        elif (self.rec["room_content"]) == 1:
                            self.username_lab1.setText(self.rec["new_roomer"])
                            self.username_lab2.setText("")
                            self.username_lab3.setText("")
                            self.msg_list.setText("system: 房间中剩余玩家为 房主 " + self.rec["new_roomer"] + " 其余玩家已离开")
                        elif (self.rec["room_content"]) == 2:
                            self.username_lab1.setText(self.rec["new_roomer"])
                            self.username_lab2.setText(self.rec["new_user2"])
                            self.username_lab3.setText("")
                        elif (self.rec["room_content"]) == 3:
                            self.username_lab1.setText(self.rec["new_roomer"])
                            self.username_lab2.setText(self.rec["new_user2"])
                            self.username_lab3.setText(self.rec["new_user3"])
                elif self.rec["behavior"] == "roomer leave":
                    self.msg_list.append("system: 房主 " + self.rec["leave_username"] + " 离开房间")
                    if (self.rec["room_content"]) == 0:
                        self.username_lab1.setText("")
                        self.username_lab2.setText("")
                        self.username_lab3.setText("")
                    elif (self.rec["room_content"]) == 1:
                        self.username_lab1.setText(self.rec["new_roomer"])
                        self.username_lab2.setText("")
                        self.username_lab3.setText("")
                        self.msg_list.append("system: " + self.rec["new_roomer"] + " 成为房主")
                    elif (self.rec["room_content"]) == 2:
                        self.username_lab1.setText(self.rec["new_roomer"])
                        self.username_lab2.setText(self.rec["new_user2"])
                        self.username_lab3.setText("")
                        self.msg_list.append("system: " + self.rec["new_roomer"] + " 成为房主")
                        self.msg_list.append("system: " + self.rec["new_user2"] + " 成为玩家2")
                    elif (self.rec["room_content"]) == 3:
                        self.username_lab1.setText(self.rec["new_roomer"])
                        self.username_lab2.setText(self.rec["new_user2"])
                        self.username_lab3.setText(self.rec["new_user3"])
                        self.msg_list.append("system: " + self.rec["new_roomer"] + " 成为房主")
                        self.msg_list.append("system: " + self.rec["new_user2"] + " 成为玩家2")
                        self.msg_list.append("system: " + self.rec["new_user3"] + " 成为玩家3")
                elif self.rec["behavior"] == "ready to begain":
                    self.msg_list.append("system: 房间已满，可以开始游戏了")
                    # 设置开始图标
                    self.wait_btn.setIcon(QIcon("开始.png"))
                    # 添加开始游戏的功能
                    self.wait_btn.clicked.connect(self.start_game)
                elif self.rec["behavior"] == "please wait":
                   self.msg_list.append("system: 房间已满，等待房主开始游戏")
                   self.wait_btn.setIcon(QIcon("等待.png"))
                elif self.rec["behavior"] == "not full":
                    self.msg_list.append("system: 房间未满，等待玩家加入")
                elif self.rec["behavior"] == "game start":
                    self.play_game()
                    break

    def play_game(self):
        self.game = Tetris()
        print(type(self.client))
        self.game.get_connect(self.client, self.username)
        self.game.show()
        self.close()

    def start_game(self):
        # 房主开始游戏
        msg = {
            "behavior": "start game",
            "username": self.username
        }
        msg = (json.dumps(msg)).encode("utf-8")
        self.client.send(msg)
        self.game = Tetris()
        print(type(self.client))
        self.game.get_connect(self.client, self.username)
        self.game.show()
        self.close()

    def showprogress(self):
        # 进度条
        self.progress = QProgressDialog(self)
        self.progress.setWindowTitle("登录")
        self.progress.setLabelText("正在连接中")
        self.progress.setCancelButtonText("取消")
        self.progress.setMinimumDuration(5)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setRange(0, 50000)
        for i in range(50000):
            self.progress.setValue(i)
            if self.progress.wasCanceled():
                QMessageBox.warning(self, "提示", "操作失败")
                break
        else:
            self.progress.setValue(50000)

    def center(self):
        # 界面居中
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())

    # def closeEvent(self, event):
    #     # 关闭提示
    #     reply = QMessageBox.question(self, '三人俄罗斯方块',"你确定要离开吗？",
    #                                  QMessageBox.Yes | QMessageBox.No,
    #                                  QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()


# 游戏模块
class Tetris(QMainWindow):
    # 游戏界面

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):    

        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)

        self.statusbar = self.statusBar()        
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        self.tboard.start()

        self.resize(180, 380)
        self.center()
        self.setWindowTitle('三人俄罗斯方块')
        self.setWindowIcon(QIcon("眼镜蛇.png"))

    def get_connect(self, client, username):
        self.tboard.get_connect(client, username)
        self.setWindowTitle(username + ' 三人俄罗斯方块')

    def closeEvent(self, event):
        # 关闭提示
        reply = QMessageBox.question(self, '三人俄罗斯方块',"你确定要离开吗？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            # self.data["behavior"] = "quit"
            # self.client.sendall((json.dumps(self.data)).encode("utf-8"))
            event.accept()
        else:
            event.ignore()
    
    def center(self):
        # 界面居中
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())
    
    def showprogress(self):
        # 进度条
        self.progress = QProgressDialog(self)
        self.progress.setWindowTitle("加载中")
        self.progress.setLabelText("正在加载游戏")
        self.progress.setCancelButtonText("取消")
        self.progress.setMinimumDuration(5)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setRange(0, 50000)
        for i in range(50000):
            self.progress.setValue(i)
            if self.progress.wasCanceled():
                QMessageBox.warning(self, "提示", "操作失败")
                break
        else:
            self.progress.setValue(50000)

class Board(QFrame):
    
    msg2Statusbar = pyqtSignal(str)

    BoardWidth = 10
    BoardHeight = 22
    Speed = 300

    def __init__(self, parent):
        super().__init__(parent)

        self.initBoard()

    def get_connect(self, client, username):
        self.client = client
        print(type(self.client))
        self.username = username

    def initBoard(self):     
        
        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False

        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()



    def shapeAt(self, x, y):
        return self.board[(y * Board.BoardWidth) + x]


    def setShapeAt(self, x, y, shape):
        self.board[(y * Board.BoardWidth) + x] = shape


    def squareWidth(self):
        return self.contentsRect().width() // Board.BoardWidth


    def squareHeight(self):
        return self.contentsRect().height() // Board.BoardHeight


    def start(self):

        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clearBoard()

        self.msg2Statusbar.emit(str(self.numLinesRemoved))

        self.newPiece()
        self.timer.start(Board.Speed, self)


    def pause(self):

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.msg2Statusbar.emit("paused")

        else:
            self.timer.start(Board.Speed, self)
            self.msg2Statusbar.emit(str(self.numLinesRemoved))

        self.update()


    def paintEvent(self, event):

        painter = QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()

        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.shapeAt(j, Board.BoardHeight - i - 1)

                if shape != Tetrominoe.NoShape:
                    self.drawSquare(painter,
                        rect.left() + j * self.squareWidth(),
                        boardTop + i * self.squareHeight(), shape)

        if self.curPiece.shape() != Tetrominoe.NoShape:

            for i in range(4):

                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                    boardTop + (Board.BoardHeight - y - 1) * self.squareHeight(),
                    self.curPiece.shape())


    def keyPressEvent(self, event):

        if not self.isStarted or self.curPiece.shape() == Tetrominoe.NoShape:
            super(Board, self).keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key_Enter:
            self.pause()
            return

        if self.isPaused:
            return

        elif key == Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)

        elif key == Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)

        elif key == Qt.Key_Up:
            self.tryMove(self.curPiece.rotateLeft(), self.curX, self.curY)

        elif key == Qt.Key_Down:
            self.oneLineDown()

        else:
            super(Board, self).keyPressEvent(event)


    def timerEvent(self, event):

        if event.timerId() == self.timer.timerId():

            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()
            else:
                self.oneLineDown()

        else:
            super(Board, self).timerEvent(event)


    def clearBoard(self):

        for i in range(Board.BoardHeight * Board.BoardWidth):
            self.board.append(Tetrominoe.NoShape)


    def oneLineDown(self):

        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped()


    def pieceDropped(self):

        for i in range(4):

            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.removeFullLines()

        if not self.isWaitingAfterLine:
            self.newPiece()


    def removeFullLines(self):

        numFullLines = 0
        rowsToRemove = []

        for i in range(Board.BoardHeight):

            n = 0
            for j in range(Board.BoardWidth):
                if not self.shapeAt(j, i) == Tetrominoe.NoShape:
                    n = n + 1

            if n == 10:
                rowsToRemove.append(i)

        rowsToRemove.reverse()


        for m in rowsToRemove:

            for k in range(m, Board.BoardHeight):
                for l in range(Board.BoardWidth):
                        self.setShapeAt(l, k, self.shapeAt(l, k + 1))

        numFullLines = numFullLines + len(rowsToRemove)

        if numFullLines > 0:

            self.numLinesRemoved = self.numLinesRemoved + numFullLines
            msg = {
                "behavior":"grade",
                "grade":self.numLinesRemoved,
                "username":self.username
            }
            self.client.send((json.dumps(msg)).encode("utf-8"))

            self.msg2Statusbar.emit(str(self.numLinesRemoved))

            self.isWaitingAfterLine = True
            self.curPiece.setShape(Tetrominoe.NoShape)
            self.update()


    def newPiece(self):

        self.curPiece = Shape()
        self.curPiece.setRandomShape()
        self.curX = Board.BoardWidth // 2 + 1
        self.curY = Board.BoardHeight - 1 + self.curPiece.minY()

        if not self.tryMove(self.curPiece, self.curX, self.curY):

            self.curPiece.setShape(Tetrominoe.NoShape)
            self.timer.stop()
            self.isStarted = False
            self.msg2Statusbar.emit("Game over")



    def tryMove(self, newPiece, newX, newY):

        for i in range(4):

            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)

            if x < 0 or x >= Board.BoardWidth or y < 0 or y >= Board.BoardHeight:
                return False

            if self.shapeAt(x, y) != Tetrominoe.NoShape:
                return False

        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.update()

        return True


    def drawSquare(self, painter, x, y, shape):

        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2, 
            self.squareHeight() - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
            x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1, 
            y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)





class Tetrominoe(object):

    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7




class Shape(object):

    coordsTable = (
        ((0, 0),     (0, 0),     (0, 0),     (0, 0)),
        ((0, -1),    (0, 0),     (-1, 0),    (-1, 1)),
        ((0, -1),    (0, 0),     (1, 0),     (1, 1)),
        ((0, -1),    (0, 0),     (0, 1),     (0, 2)),
        ((-1, 0),    (0, 0),     (1, 0),     (0, 1)),
        ((0, 0),     (1, 0),     (0, 1),     (1, 1)),
        ((-1, -1),   (0, -1),    (0, 0),     (0, 1)),
        ((1, -1),    (0, -1),    (0, 0),     (0, 1))
    )

    def __init__(self):

        self.coords = [[0,0] for i in range(4)]
        self.pieceShape = Tetrominoe.NoShape

        self.setShape(Tetrominoe.NoShape)


    def shape(self):
        return self.pieceShape


    def setShape(self, shape):

        table = Shape.coordsTable[shape]

        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape


    def setRandomShape(self):
        self.setShape(random.randint(1, 7))


    def x(self, index):
        return self.coords[index][0]


    def y(self, index):
        return self.coords[index][1]


    def setX(self, index, x):
        self.coords[index][0] = x


    def setY(self, index, y):
        self.coords[index][1] = y


    def minX(self):

        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])

        return m


    def maxX(self):

        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m


    def minY(self):

        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m


    def maxY(self):

        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])

        return m


    def rotateLeft(self):

        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):

            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))

        return result


    def rotateRight(self):

        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):

            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))

        return result


if __name__ == '__main__':

    app = QApplication(sys.argv)
    login = Login()
    sys.exit(app.exec_())
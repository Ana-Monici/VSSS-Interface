import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QTimer
import game
from field_graphics.field import Field
import math

class Canvas(QtWidgets.QLabel):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        fps = 60
        self.interval = 1000/fps # interval between frames in miliseconds
        timer = QTimer(self, interval = self.interval, timeout = self.paintCanvas)
        timer.start(self.interval)
        self.paintCanvas()
    
    def paintCanvas(self):
        self.category = self.interface.match.category
        self.field = Field(self.category)
        self.scale = 3
        if self.category == "5v5":
            self.scale = 2
        self.field_w = self.field.f_w * self.scale
        self.field_h = self.field.f_h * self.scale
        self.border = 60
        self.center_x = self.border + (self.field_w / 2)
        self.center_y = self.border + (self.field_h / 2)

        pixmap = QtGui.QPixmap(self.field_w + self.border * 2, self.field_h + self.border * 2)
        self.setPixmap(pixmap)
        self.pen_color = QtGui.QColor('white')
        painter = QtGui.QPainter(self.pixmap())
        painter.setRenderHints(painter.Antialiasing)
        self.draw_field(painter)
        self.draw_ball(painter)
        self.draw_robots(painter)
        painter.end()
    
    def draw_field(self, painter):
        p = painter.pen()
        p.setWidth(self.scale)
        p.setColor(self.pen_color)
        painter.setPen(p)

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor("green"))
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        # draw outer lines, center circle and center line
        painter.drawRects(QtCore.QRect(self.border, self.border, self.field_w, self.field_h))
        diameter = self.field.diameter * self.scale
        painter.drawEllipse(self.center_x - diameter/2, self.center_y - diameter/2, diameter, diameter)
        painter.drawLine(self.border + self.field_w / 2, self.border, self.border + self.field_w / 2, self.border + self.field_h)

        # draw goals
        goal_w = self.field.goal_w * self.scale
        goal_h = self.field.goal_h * self.scale
        painter.drawRects(QtCore.QRect(self.border - goal_w, self.center_y - goal_h/2, goal_w, goal_h))
        painter.drawRects(QtCore.QRect(self.border + self.field_w, self.center_y - goal_h/2, goal_w, goal_h))

        # NoBrush
        brush.setStyle(Qt.NoBrush)
        painter.setBrush(brush)

        # draw goal areas
        ga_w = self.field.goal_area_w * self.scale
        ga_h = self.field.goal_area_h * self.scale
        painter.drawRects(QtCore.QRect(self.border, self.center_y - ga_h/2, ga_w, ga_h))
        painter.drawRects(QtCore.QRect(self.border + self.field_w - ga_w, self.center_y - ga_h/2, ga_w, ga_h))

        # draw penalty area (5v5)
        if self.category == "5v5":
            pa_w = self.field.penalty_w * self.scale
            pa_h = self.field.penalty_h * self.scale
            painter.drawRects(QtCore.QRect(self.border, self.center_y - pa_h/2, pa_w, pa_h))
            painter.drawRects(QtCore.QRect(self.border + self.field_w - pa_w, self.center_y - pa_h/2, pa_w, pa_h))
    
    def draw_ball(self, painter):
        p = painter.pen()
        p.setWidth(1)

        # save the current state of the painter
        painter.save()

        # set the center of the coordinate system at the bottom left corner of the field
        painter.translate(self.border, self.border + self.field_h)
        
        # scales the coordinate system so that y axis "points" upwards
        painter.scale(1, -1)

        p.setColor(QtGui.QColor(255, 87, 51))
        painter.setPen(p)

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(255, 87, 51))
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        b_x = self.meter_to_cm(self.interface.match.ball.x) * self.scale
        b_y = self.meter_to_cm(self.interface.match.ball.y) * self.scale
        radius = self.interface.match.ball.r * self.scale
        painter.drawEllipse(b_x - radius, b_y - radius, radius*2, radius*2)

        painter.restore()
    
    def draw_robots(self, painter):
        r_color = self.interface.match.team_color
        if r_color == 'blue':
            r_color_dark = 'darkBlue'
        else:
            r_color_dark = QtGui.QColor(246, 190, 0)

        for r in self.interface.match.robots:
            self.draw_a_robot(painter, r, r_color, r_color_dark)
        
        # draw opposite team's robots
        if r_color == 'blue':
            r_color = 'yellow'
            r_color_dark = QtGui.QColor(246, 190, 0)
        else:
            r_color = 'blue'
            r_color_dark = 'darkBlue'
        
        for r in self.interface.match.opposites:
            self.draw_a_robot(painter, r, r_color, r_color_dark)
    
    def draw_a_robot(self, painter, r, color, dark_color):
        # change coordinate system
        painter.save()
        painter.translate(self.border + (self.meter_to_cm(r.x)*self.scale), self.border + self.field_h - (self.meter_to_cm(r.y)*self.scale))
        painter.scale(1, -1)
        angle = r.theta * (180/math.pi) # rad to degrees
        painter.rotate(angle)
        
        # set pen and brush with appropriate colors
        p = painter.pen()
        p.setWidth(1)
        p.setColor(QtGui.QColor(color))
        painter.setPen(p)

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(color))
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        # Draw robot body
        rx = (-r.l/2)*self.scale
        ry = (-r.l/2)*self.scale
        rl = r.l*self.scale
        painter.drawRect(QtCore.QRect(rx, ry, rl, rl))

        # Draw robot frontal rectangle
        p.setColor(QtGui.QColor(dark_color))
        painter.setPen(p)
        brush.setColor(QtGui.QColor(dark_color))
        painter.setBrush(brush)
        painter.drawRect(QtCore.QRect(-rx - (rl/4), ry, rl/4, rl))

        # write robot ids
        painter.rotate(-angle)
        painter.scale(1, -1)
        if color == 'blue':
            p.setColor(QtGui.QColor('white'))
        else:
            p.setColor(QtGui.QColor('black'))
        painter.setPen(p)
        id_text = (str)(r.robot_id)
        font = QtGui.QFont()
        font.setPointSize(8)
        painter.setFont(font)
        painter.drawText(-self.scale, self.scale, id_text)
        
        painter.restore()
    
    def meter_to_cm(self, m):
        return m*100

class InterfaceButton(QtWidgets.QPushButton):
    def __init__(self, w, h):
        super().__init__()
        self.setFixedSize(QtCore.QSize(w, h))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface

        w = QtWidgets.QWidget()
        l = QtWidgets.QVBoxLayout()
        w.setLayout(l)

        # Adding the game status buttons
        buttons = QtWidgets.QHBoxLayout()
        self.game_status_buttons(buttons)
        l.addLayout(buttons)

        # Adding fault positioning buttons
        # buttons = QtWidgets.QHBoxLayout()
        # self.foul_buttons(buttons)
        # l.addLayout(buttons)

        # Adding the robot attributes buttons
        # buttons = QtWidgets.QHBoxLayout()
        # self.blue_robot_buttons(buttons)
        # l.addLayout(buttons)
        # buttons = QtWidgets.QHBoxLayout()
        # self.yellow_robot_buttons(buttons)
        # l.addLayout(buttons)

        self.canvas = Canvas(interface)
        l.addWidget(self.canvas)

        self.setCentralWidget(w)
    
    def game_status_buttons(self, layout):
        b = InterfaceButton(100, 30)
        b.setText("START")
        b.clicked.connect(self.start_game)
        layout.addWidget(b)

        b = InterfaceButton(100, 30)
        b.setText("HALT")
        b.clicked.connect(self.halt_game)
        layout.addWidget(b)

        b = InterfaceButton(100, 30)
        b.setText("STOP")
        b.clicked.connect(self.stop_game)
        layout.addWidget(b)

        b = InterfaceButton(100, 30)
        b.setText("Change Color")
        b.clicked.connect(self.change_team_color)
        layout.addWidget(b)

        b = InterfaceButton(100, 30)
        b.setText("Change Side")
        b.clicked.connect(self.change_team_side)
        layout.addWidget(b)
    
    # def foul_buttons(self, layout):
    #     b = InterfaceButton(100, 30)
    #     b.setText("Free Ball")
    #     b.clicked.connect(self.free_ball)
    #     layout.addWidget(b)

    #     b = InterfaceButton(100, 30)
    #     b.setText("HALT")
    #     b.clicked.connect(self.halt_game)
    #     layout.addWidget(b)

    #     b = InterfaceButton(100, 30)
    #     b.setText("STOP")
    #     b.clicked.connect(self.stop_game)
    #     layout.addWidget(b)

    #     b = InterfaceButton(100, 30)
    #     b.setText("Change Color")
    #     b.clicked.connect(self.change_team_color)
    #     layout.addWidget(b)

    #     b = InterfaceButton(100, 30)
    #     b.setText("Change Side")
    #     b.clicked.connect(self.change_team_side)
    #     layout.addWidget(b)
    
    # def blue_robot_buttons(self, layout):
    #     text1 = QtWidgets.QLabel("Change blue robots ids:    ")
    #     layout.addWidget(text1)
        
    #     self.blue_r0 = QtWidgets.QLineEdit(self)
    #     self.blue_r0.setFixedWidth(50)
    #     layout.addWidget(self.blue_r0)

    #     self.blue_r1 = QtWidgets.QLineEdit(self)
    #     self.blue_r1.setFixedWidth(50)
    #     layout.addWidget(self.blue_r1)

    #     self.blue_r2 = QtWidgets.QLineEdit(self)
    #     self.blue_r2.setFixedWidth(50)
    #     layout.addWidget(self.blue_r2)

    #     self.blue_r3 = QtWidgets.QLineEdit(self)
    #     self.blue_r3.setFixedWidth(50)
    #     layout.addWidget(self.blue_r3)

    #     self.blue_r4 = QtWidgets.QLineEdit(self)
    #     self.blue_r4.setFixedWidth(50)
    #     layout.addWidget(self.blue_r4)

    #     b = QtWidgets.QPushButton('Submit', self)
    #     b.clicked.connect(self.change_blue_ids)
    #     layout.addWidget(b)
    
    # def yellow_robot_buttons(self, layout):
    #     text1 = QtWidgets.QLabel("Change yellow robots ids:")
    #     layout.addWidget(text1)
        
    #     self.yellow_r0 = QtWidgets.QLineEdit(self)
    #     self.yellow_r0.setFixedWidth(50)
    #     layout.addWidget(self.yellow_r0)

    #     self.yellow_r1 = QtWidgets.QLineEdit(self)
    #     self.yellow_r1.setFixedWidth(50)
    #     layout.addWidget(self.yellow_r1)

    #     self.yellow_r2 = QtWidgets.QLineEdit(self)
    #     self.yellow_r2.setFixedWidth(50)
    #     layout.addWidget(self.yellow_r2)

    #     self.yellow_r3 = QtWidgets.QLineEdit(self)
    #     self.yellow_r3.setFixedWidth(50)
    #     layout.addWidget(self.yellow_r3)

    #     self.yellow_r4 = QtWidgets.QLineEdit(self)
    #     self.yellow_r4.setFixedWidth(50)
    #     layout.addWidget(self.yellow_r4)

    #     b = QtWidgets.QPushButton('Submit', self)
    #     b.clicked.connect(self.change_yellow_ids)
    #     layout.addWidget(b)
    
    def start_game(self):
        # status = "GAME_ON"
        # self.interface.api.send_game_status(self.interface.match, status)
        self.interface.match.game_status = "GAME_ON"
        self.interface.api.send_data(self.interface.match)
        print("START")
    
    def halt_game(self):
        self.interface.match.game_status = "HALT"
        # self.interface.match.game_status = 7
    
    def stop_game(self):
        # self.interface.match.game_status = "STOP"
        # status = "STOP"
        # self.interface.api.send_game_status(self.interface.match, status)
        self.interface.match.game_status = "STOP"
        self.interface.api.send_data(self.interface.match)
        print("STOP")
    
    def change_team_color(self):
        if self.interface.match.team_color == "blue":
            self.interface.match.team_color = "yellow"
            self.interface.match.opposite_team_color = "blue"
        else:
            self.interface.match.team_color = "blue"
            self.interface.match.opposite_team_color = "yellow"
        print(self.interface.match.team_color.upper())
        self.interface.api.send_data(self.interface.match)
    
    def change_team_side(self):
        if self.interface.match.team_side == "left":
            self.interface.match.team_side = "right"
        else:
            self.interface.match.team_side = "left"
        print(self.interface.match.team_side.upper())
        self.interface.api.send_data(self.interface.match)

    # def change_blue_ids(self):
    #     id_list = [self.blue_r0.text(),
    #                 self.blue_r1.text(),
    #                 self.blue_r2.text(),
    #                 self.blue_r3.text(),
    #                 self.blue_r4.text()]
        
    #     if self.interface.match.team_color == "blue":
    #         neon_team = True
    #     else:
    #         neon_team = False
        
    #     aux = 0
    #     for id in id_list:
    #         if id == "":
    #             pass
    #         elif neon_team:
    #             if aux+1 <= len(self.interface.match.robots):
    #                 self.interface.match.robots[aux].robot_id = id
    #             aux = aux + 1
    #         else:
    #             if aux+1 <= len(self.interface.match.opposites):
    #                 self.interface.match.opposites[aux].robot_id = id
    #             aux = aux + 1
    
    # def change_yellow_ids(self):
    #     id_list = [self.yellow_r0.text(),
    #                 self.yellow_r1.text(),
    #                 self.yellow_r2.text(),
    #                 self.yellow_r3.text(),
    #                 self.yellow_r4.text()]
        
    #     if self.interface.match.team_color == "blue":
    #         neon_team = False
    #     else:
    #         neon_team = True
        
    #     aux = 0
    #     for id in id_list:
    #         if id == "":
    #             pass
    #         elif neon_team:
    #             if aux+1 <= len(self.interface.match.robots):
    #                 self.interface.match.robots[aux].robot_id = id
    #             aux = aux + 1
    #         else:
    #             if aux+1 <= len(self.interface.match.opposites):
    #                 self.interface.match.opposites[aux].robot_id = id
    #             aux = aux + 1

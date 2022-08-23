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

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface

        # self.toolbar = 

        self.canvas = Canvas(interface)

        w = QtWidgets.QWidget()
        l = QtWidgets.QVBoxLayout()
        w.setLayout(l)
        l.addWidget(self.canvas)

        self.setCentralWidget(w)

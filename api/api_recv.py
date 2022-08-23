from socket import *

from numpy import mat

from concurrent import futures

import json
import struct

import threading

from game.robot import Robot

class Api_recv(threading.Thread):
    def __init__(self, game, match, address, port):
        super(Api_recv, self).__init__()

        BUFFER_SIZE = 2048

        self.game = game
        self.match = match

        self.address = address
        self.port = port
        self.buffer_size = BUFFER_SIZE
        

    # Receives data
    def run(self):
        self.obj_socket = socket(AF_INET, SOCK_DGRAM)
        self.obj_socket.bind((self.address, self.port))

        print("Starting api_recv...")

        while True:
            data, origem = self.obj_socket.recvfrom(self.buffer_size)
            decoded_data = json.loads(data.decode())
            # Feedback commands from socket (e.g. an interface)
            # print(decoded_data)

            # coach_name = decoded_data.get('COACH_NAME')

            team_color = decoded_data.get('TEAM_COLOR')
            # Change team color
            if team_color != self.match.team_color:
                # self.match.restart(team_color)
                self.match.team_color = team_color
                self.match.update()
            
            if team_color == 'blue':
                opposites_color = 'yellow'
            else:
                opposites_color = 'blue'

            # Update match.robots
            robot_pos = decoded_data.get('TEAM_ROBOTS_POS')
            robot_list = []
            i = 0
            for r in robot_pos:
                id = int(list(list(robot_pos)[i])[0])
                r_pos = (list(robot_pos)[i])[str(id)]
                r_x = r_pos[0]
                r_y = r_pos[1]
                r_theta = r_pos[2]
                robot = Robot(id, r_x, r_y, r_theta, team_color)
                robot_list.append(robot)
                i += 1
            i = 0
            self.match.robots = robot_list

            # Update match.opposites
            robot_pos = decoded_data.get('OPPOSITE_ROBOTS_POS')
            robot_list = []
            for r in robot_pos:
                id = int(list(list(robot_pos)[i])[0])
                r_pos = (list(robot_pos)[i])[str(id)]
                r_x = r_pos[0]
                r_y = r_pos[1]
                r_theta = r_pos[2]
                robot = Robot(id, r_x, r_y, r_theta, opposites_color)
                robot_list.append(robot)
                i += 1
            self.match.opposites = robot_list

            # Change ball position
            ball_pos = decoded_data.get('BALL_POS')
            self.match.ball.x = ball_pos[0]
            self.match.ball.y = ball_pos[1]
            
            # Stop game and game on
            game_status = decoded_data.get('GAME_STATUS')
            if game_status != self.match.game_status:
                self.match.game_status = game_status

            # Change team side
            team_side = decoded_data.get('TEAM_SIDE')
            if team_side != self.match.team_side:
                self.match.team_side = team_side
            
            # Change category
            category = decoded_data.get('CATEGORY')
            if category != self.match.category:
                self.match.category = category

            self.game.update()

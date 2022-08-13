import os
from api import Api
import game

CATEGORIES = {
    '3v3': 3, '5v5': 5
}

#class Match(object):
class Match():
    def __init__(self, interface, team_side = "left", team_color = "blue", coach_name = None, category="3v3"):
        super().__init__()
        self.interface = interface # Interface instance
        
        self.coach_name = os.environ.get('COACH_NAME', coach_name) 
        self.team_side = os.environ.get('TEAM_SIDE', team_side) 
        self.team_color = os.environ.get('TEAM_COLOR', team_color)
        self.category = os.environ.get('CATEGORY', category)
        self.n_robots = CATEGORIES.get(self.category)

        self.opposite_team_color = 'yellow' if self.team_color == 'blue' else 'blue'

        self.game_status = None

        self.ball = game.Ball()
        self.robots = []
        self.opposites = []

        # teste
        r0 = game.Robot(0, 0.2, 0.3, 0, self.team_color)
        r1 = game.Robot(1, 1, 1, 1, self.team_color)
        r2 = game.Robot(2, 1.2, 1.2, 2, self.team_color)
        r3 = game.Robot(3, 1.5, 1.5, 3, self.team_color)
        r4 = game.Robot(4, 1.7, 0.7, -0.5, self.team_color)
        self.robots.append(r0)
        self.robots.append(r1)
        self.robots.append(r2)
        self.robots.append(r3)
        self.robots.append(r4)

        o0 = game.Robot(0, 0.5, 0.5, 0.5, self.team_color)
        o1 = game.Robot(1, 0.7, 0.7, 1.7, self.team_color)
        o2 = game.Robot(2, 1.2, 1.7, 2, self.team_color)
        o3 = game.Robot(3, 1.9, 1.9, -3, self.team_color)
        o4 = game.Robot(4, 1.5, 0.5, 0, self.team_color)
        self.opposites.append(o0)
        self.opposites.append(o1)
        self.opposites.append(o2)
        self.opposites.append(o3)
        self.opposites.append(o4)
    
    def start(self):
        self.opposites = [
            game.Robot(i, self.opposite_team_color) for i in range(self.n_robots)
        ]

        self.robots = [
            game.Robot(i, self.team_color) for i in range(self.n_robots)
        ]

    # def update(self, team_color, coach_name):
    def update(self):
    #     self.team_color = team_color
        self.opposite_team_color = 'yellow' if self.team_color == 'blue' else 'blue'

        # self.opposites = [
        #     game.Robot(i, self.opposite_team_color) for i in range(self.n_robots)
        # ]

        # self.robots = [
        #     game.Robot(i, self.team_color) for i in range(self.n_robots)
        # ]

        # self.coach_name = coach_name

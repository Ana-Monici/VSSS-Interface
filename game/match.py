import os
from api import Api
import game

CATEGORIES = {
    '3v3': 3, '5v5': 5
}

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

        self.game_status = 'STOP'

        self.ball = game.Ball()
        self.robots = []
        self.opposites = []

        # self.start()
    
    def start(self):
        self.opposites = [
            game.Robot(i, 0, 0, 0, self.opposite_team_color) for i in range(self.n_robots)
        ]

        self.robots = [
            game.Robot(i, 0, 0, 0, self.team_color) for i in range(self.n_robots)
        ]

    def update(self, team_color):
        self.team_color = team_color
        self.opposite_team_color = 'yellow' if self.team_color == 'blue' else 'blue'
        # self.coach_name = coach_name

    def set_game_status(self, status):
        self.game_status = status

class Robot():
    def __init__(self, r_id, r_x = 0, r_y = 0, r_theta = 0, team_color = 'blue'):
        self.robot_id = r_id
        self.x = r_x
        self.y = r_y
        self.theta = r_theta
        self.team_color = team_color
        self.l = 7.5 # cm

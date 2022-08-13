class Field():
    def __init__(self, category):
        self.category = category
        if category == "3v3":
            self.f_w = 150
            self.f_h = 130
            self.diameter = 40
            self.goal_w = 10
            self.goal_h = 40
            self.goal_area_w = 15
            self.goal_area_h = 70
        else:
            self.f_w = 220
            self.f_h = 180
            self.diameter = 50
            self.goal_w = 15
            self.goal_h = 40
            self.goal_area_w = 15
            self.goal_area_h = 50
            self.penalty_w = 35
            self.penalty_h = 80

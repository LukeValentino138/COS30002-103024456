from vector2d import Vector2D
from graphics import egi
from random import uniform
from math import radians, cos, sin

class Projectile:
    def __init__(self, start_pos, target_pos, speed, accuracy, is_explosive=False):
        self.pos = start_pos.copy()
        self.target_pos = target_pos
        self.speed = speed
        self.accuracy = accuracy
        self.is_explosive = is_explosive
        self.vel = self.calculate_velocity(start_pos, target_pos, speed, accuracy)

    def calculate_velocity(self, start_pos, target_pos, speed, accuracy):
        desired_velocity = (target_pos - start_pos).normalise() * speed
        if accuracy < 1.0:
            # apply ianccuracy 
            max_deviation = (1 - accuracy) * radians(15)  # max deviation 
            deviation_angle = uniform(-max_deviation, max_deviation)
            cos_angle = cos(deviation_angle)
            sin_angle = sin(deviation_angle)
            # rotate the desired_velocity by the deviation
            rotated_velocity = Vector2D(
                desired_velocity.x * cos_angle - desired_velocity.y * sin_angle,
                desired_velocity.x * sin_angle + desired_velocity.y * cos_angle
            )
            return rotated_velocity.normalise() * speed
        return desired_velocity

    def update(self, delta):
        self.pos += self.vel * delta

    def render(self):
        egi.set_pen_color(name='WHITE')
        egi.circle(self.pos, 2)

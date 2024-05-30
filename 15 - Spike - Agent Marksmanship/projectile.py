from vector2d import Vector2D
from graphics import egi
from random import uniform
from math import radians, cos, sin

class Projectile:
    def __init__(self, start_pos, target, speed, accuracy):
        self.pos = start_pos.copy()
        self.target = target
        self.speed = speed
        self.accuracy = accuracy
        self.vel = self.calculate_velocity(start_pos, target, speed, accuracy)

    def calculate_velocity(self, start_pos, target, speed, accuracy):
        target_pos = self.predict_target(start_pos, target)
        desired_velocity = (target_pos - start_pos).normalise() * speed
        if accuracy < 1.0:
            # apply inaccuracy
            max_deviation = (1 - accuracy) * radians(15)  # Max deviation
            deviation_angle = uniform(-max_deviation, max_deviation)
            cos_angle = cos(deviation_angle)
            sin_angle = sin(deviation_angle)
            # Rotate the desired_velocity by the deviation_angle
            rotated_velocity = Vector2D(
                desired_velocity.x * cos_angle - desired_velocity.y * sin_angle,
                desired_velocity.x * sin_angle + desired_velocity.y * cos_angle
            )
            return rotated_velocity.normalise() * speed
        return desired_velocity

    def predict_target(self, start_pos, target):
        to_target = target.pos - start_pos
        target_speed = target.vel.length()
        closing_speed = self.speed - target_speed
        if closing_speed != 0:
            time_to_target = to_target.length() / closing_speed
            return target.pos + target.vel * time_to_target
        else:
            return target.pos

    def update(self, delta):
        self.pos += self.vel * delta

    def render(self):
        egi.set_pen_color(name='WHITE')
        egi.circle(self.pos, 2)

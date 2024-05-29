'''A 2d world that supports agents with steering behaviour

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

'''

from vector2d import Vector2D
from matrix33 import Matrix33
from graphics import egi


class World(object):

    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.target = Vector2D(cx / 2, cy / 2)
        self.hunter = None
        self.prey = None
        self.agents = []
        self.objects = []
        self.paused = True
        self.show_info = True
        self.selected_param = 'wander'

    def update(self, delta):
        if not self.paused:
            self.calculate_neighbours()
            for agent in self.agents:
                agent.update(delta)

    def render(self):
        for agent in self.agents:
            agent.render()
        
        if self.target:
            egi.red_pen()
            egi.cross(self.target, 10)
        if self.show_info:
                infotext = ', '.join(set(agent.mode for agent in self.agents))
                infotext += f" | Wander: {self.agents[0].wander_amount:.2f}"
                infotext += f" | Separation: {self.agents[0].separation_amount:.2f}"
                infotext += f" | Alignment: {self.agents[0].alignment_amount:.2f}"
                infotext += f" | Cohesion: {self.agents[0].cohesion_amount:.2f}"
                infotext += f" | Selected Parameter: {self.selected_param}"
                egi.white_pen()
                egi.text_at_pos(10, self.cy - 20, infotext)  # Position text at the top of the screen

    def calculate_neighbours(self):
        for agent in self.agents:
            agent.TagNeighbours(self.agents, agent.neighbour_radius)


    def wrap_around(self, pos):
        ''' Treat world as a toroidal space. Updates parameter object pos '''
        max_x, max_y = self.cx, self.cy
        if pos.x > max_x:
            pos.x = pos.x - max_x
        elif pos.x < 0:
            pos.x = max_x - pos.x
        if pos.y > max_y:
            pos.y = pos.y - max_y
        elif pos.y < 0:
            pos.y = max_y - pos.y

    def transform_points(self, points, pos, forward, side, scale):
        ''' Transform the given list of points, using the provided position,
            direction and scale, to object world space. '''
        # make a copy of original points (so we don't trash them)
        wld_pts = [pt.copy() for pt in points]
        # create a transformation matrix to perform the operations
        mat = Matrix33()
        # scale,
        mat.scale_update(scale.x, scale.y)
        # rotate
        mat.rotate_by_vectors_update(forward, side)
        # and translate
        mat.translate_update(pos.x, pos.y)
        # now transform all the points (vertices)
        mat.transform_vector2d_list(wld_pts)
        # done
        return wld_pts
    
    def transform_point(self, point, pos, forward, side):
        ''' Transform the given single point, using the provided position,
        and direction (forward and side unit vectors), to object world space. '''
        # make a copy of the original point (so we don't trash it)
        wld_pt = point.copy()
        # create a transformation matrix to perform the operations
        mat = Matrix33()
        # rotate
        mat.rotate_by_vectors_update(forward, side)
        # and translate
        mat.translate_update(pos.x, pos.y)
        # now transform the point (in place)
        mat.transform_vector2d(wld_pt)
        # done
        return wld_pt
    


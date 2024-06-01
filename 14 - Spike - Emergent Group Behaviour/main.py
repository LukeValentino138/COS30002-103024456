'''Autonomous Agent Movement: Paths and Wandering

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

This code is essentially the same as the base for the previous steering lab
but with additional code to support this lab.

'''
from graphics import egi, KEY
from pyglet import window, clock
from pyglet.gl import *

from vector2d import Vector2D
from world import World
from agent import Agent, AGENT_MODES  # Agent with seek, arrive, flee and pursuit
import random

PARAMETER_KEYS = {
    KEY.F1: 'wander',
    KEY.F2: 'separation',
    KEY.F3: 'alignment',
    KEY.F4: 'cohesion'
}

def on_mouse_press(x, y, button, modifiers):
    if button == 1:  # left
        world.target = Vector2D(x, y)


def on_key_press(symbol, modifiers):
    if symbol == KEY.P:
        world.paused = not world.paused
    elif symbol in AGENT_MODES:
        for agent in world.agents:
            agent.mode = AGENT_MODES[symbol]
    elif symbol in PARAMETER_KEYS:
        world.selected_param = PARAMETER_KEYS[symbol]
    elif symbol == KEY.UP:
        adjust_parameter(world.agents, world.selected_param, 1)
    elif symbol == KEY.DOWN:
        adjust_parameter(world.agents, world.selected_param, -1)
    elif symbol == KEY.A:
        world.agents.append(Agent(world))
    elif symbol == KEY.I:
        for agent in world.agents:
            agent.show_info = not agent.show_info

def adjust_parameter(agents, param, amount):
    for agent in agents:
        if param == 'wander':
            agent.wander_amount += amount
        elif param == 'separation':
            agent.separation_amount += amount
        elif param == 'alignment':
            agent.alignment_amount += amount
        elif param == 'cohesion':
            agent.cohesion_amount += amount

def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy


if __name__ == '__main__':

    # create a pyglet window and set glOptions
    win = window.Window(width=1000, height=1000, vsync=True, resizable=True)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # needed so that egi knows where to draw
    egi.InitWithPyglet(win)
    # prep the fps display
    fps_display = window.FPSDisplay(win)
    # register key and mouse event handlers
    win.push_handlers(on_key_press)
    win.push_handlers(on_mouse_press)
    win.push_handlers(on_resize)

    # create a world for agents
    world = World(1000, 1000)

    for x in range(5):
        world.agents.append(Agent(world))

    # unpause the world ready for movement
    world.paused = False

    while not win.has_exit:
        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # show nice FPS bottom right (default)
        delta = clock.tick()
        world.update(delta)
        world.render()
        fps_display.draw()
        # swap the double buffer
        win.flip()


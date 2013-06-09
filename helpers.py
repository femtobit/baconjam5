import math
import random

import sfml as sf

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

def collision_rectangle(Actor):
    return sf.Rectangle((Actor.position.x, Actor.position.y), Actor.size)
    
def norm(v):
    return math.sqrt(v.x * v.x + v.y * v.y)

def normalize(v):
    if v != sf.Vector2():
        return v / norm(v)
    else:
        return sf.Vector2()

def random_unit_vector():
    """
    Returns a vector of length 1 with random direction.
    """
    return normalize(sf.Vector2(random.randint(0,100) - 50, random.randint(0,100) - 50))

def vector2to3(vec2, z = 0):
    return sf.Vector3(vec2.x, vec2.y, z)

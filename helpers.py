import math

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

def collision_radius(object):
    return object.sprite.size.x / 2
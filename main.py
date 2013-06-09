#!/usr/bin/env python2
#-*- encoding: utf-8 -*-
import datetime
import math
import random
import sys

import sfml as sf

from actors import *
from constants import *
from drawables import *
from states import *
from helpers import *

def main():
    random.seed(datetime.datetime.now())

    window = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), "A Walk In The Dark")
    
    def end_game():
        window.close()

    state_counter = 0
    current_state = IntroState(window)

    step_timer = sf.Clock()

    while window.is_open:
        if current_state.has_ended:
            if current_state.next_state is None:
                window.close()
            else:
                current_state = current_state.next_state(window)

        dt = step_timer.elapsed_time.milliseconds / 16.0
        step_timer.restart()
        
        current_state.step(dt)

        window.clear()
        current_state.draw()
        window.display()


if __name__ == "__main__":
    main()

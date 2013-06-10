#!/usr/bin/env python3
#-*- encoding: utf-8 -*-
import datetime
import math
import random
import sys

import sfml as sf

from actors import *
from constants import *
from drawables import *
import sound
from states import *
from helpers import *

def main():
    random.seed(datetime.datetime.now())

    window = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), "A Walk In The Dark")
    sound.ambient.loop = True
    sound.ambient.volume = 10
    sound.ambient.play()

    state_counter = 0
    current_state = IntroState(window)
    last_state = None

    step_timer = sf.Clock()

    while window.is_open:
        dt = step_timer.elapsed_time.milliseconds / 16.0
        step_timer.restart()
        
        current_state.step(dt)

        window.clear()
        current_state.draw()
        window.display()

        if current_state.has_ended:
            old_current_state = current_state
            if current_state.next_state is None:
                window.close()
            elif current_state.next_state == State.PREVIOUS_STATE:
                print("restoring previous state")
                current_state = last_state
            else:
                current_state = current_state.next_state(window)
            last_state = old_current_state
            last_state.has_ended = False

if __name__ == "__main__":
    main()

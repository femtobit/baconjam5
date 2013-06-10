A Walk In The Dark
==================

Gameplay
--------

You try to survive in a dark and scary world to find a treasure. Run away from the
monsters and especially try to avoid the big one. You can sprint by pressing shift.
However, each time you sprint you lose stamina which regenerates slowly. If your
stamina reaches zero, you will have to stand still for a few seconds.

If you turn out your light by pressing X, the ghosts will only see you when they're
really close. But without light you won't see a thing as well (and the boss will see
and hunt you anyway).

The tresure spawns after two minutes, together with the boss, who will hunt you down
restlessly. Find the treasure before he catches you.

Installation
------------

You need Python 3 (tested with 3.2 and 3.3), SFML 2 and the PySFML bindings.

### Linux ###

First, you need to obtain the above mentioned dependencies. How to do
that obviously depends on your distribution. Bellow are two examples:

#### ArchLinux ####

    # pacman -S python-sfml

#### Ubuntu ####

You need to install the newest stable version of (Py)SFML from a PPA.
To get all the required dependencies, use the following commands:

    $ sudo apt-add-repository ppa:sonkun/sfml-stable
    $ sudo apt-get update
    $ sudo apt-get install python3 python3-sfml git

#### Start the Game ####

Now you can download the game and run it with

    $ git clone https://github.com/picobyte/baconjam5.git walk-in-the-dark
    $ cd walk-in-the-dark
    $ ./main.py

### Windows and Mac OS X ###

To install PySFML, follow the instructions at <http://www.python-sfml.org/download.html>.
Then get the game from [GitHub](https://github.com/picobyte/baconjam5) and run main.py.

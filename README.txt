This repository contains a toy implementation of an in-memory Key Column Value store which was assigned as an interview test.

There are four levels of the assigned problem and all are implemented here.

There are two implementations for the first two levels. One which makes use
of nested dictionary data structures and one which uses a simple binary tree.

The tests are all configurable against either of these implementations but
are currently set to my preferred implementation of the nested dictionary.

You can run all of the functional and unit tests by running nosetests.

The implementation for level 3: persistence is currently only configured
against the nested dict implementation but can easily be applied to the
binary tree implementation.

Level 4 is implemented as a small Flask application which can be run
by running python run_server.py in the root of the repository.

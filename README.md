# Python Fireplace

A simple and cozy fireplace in Python.

## Installation and running

The code relies on some external modules:
* `numpy`
* `matplotlib`
* `pyaudio`

For convenience, a `Pipfile` for [pipenv](https://github.com/pypa/pipenv) is
supplied. The packages can be installed using

    pipenv install

To start any script (e. g. `fireplace.py`), use

    pipenv run fireplace.py

## Fire animation (`fire.py`)

For a nice explanation see
[this video](https://www.youtube.com/watch?v=_SzpMBOp1mE) and read through the
comments.

The basic idea is to use a two-dimensional array and fill the bottom line with
random numbers between 0 and 100:

|   |    |    |   |    |   |
|:-:|:--:|:--:|:-:|:--:|:-:|
| 0 |  0 |  0 | 0 |  0 | 0 |
| 0 |  0 |  0 | 0 |  0 | 0 |
| 0 |  0 |  0 | 0 |  0 | 0 |
| 0 |  0 |  0 | 0 |  0 | 0 |
| 0 | 18 | 27 | 9 | 89 | 0 |

The values in the next row are determined by using the 3 values right below of
each cell and calculate their mean:

|   | 2 |   |
|:-:|:-:|:-:|
| 1 | 2 | 3 |

In every frame, (some of) the values in the bottom line are changed. Different
flame effects can be achieved by varying parts of this procedure. For
example, if the changes are propagated from bottom to top in every frame, the
flame will look static and change instantaneously. If updates are performed from
top to bottom, changes will slowly propagate upwards.

Some modifications for more realistic flames are
* the inclusion of the value of the current cell when determining the mean
value,
* the usage of a random number of elements from the row below (especially
different numbers to the left and right).

For better performance, the patterns for exchanging the bottom rows can be
calculated before the animation starts. In this case, only the index of the
pattern to be used has to be random.

Another really nice method to create fire animations is described [here](
  https://matzjb.se/2014/05/13/fire-simulation-using-cellular-automata/
). However, this method is not (yet) used here.

## Fire sound (`sound.py`)

A simple sound with a wide range of applications is coloured noise. In case of
fire, brown noise gives a pretty nice result. An algorithm to generate coloured
noise is described in [Timmer, J. and Koenig, M., "On generating power law
noise", Astron. Astrophys. 300, 707-710 (1995)](
    http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.29.5304
). A Python implementation of this algorithm can be found [here](
    https://github.com/felixpatzelt/colorednoise/blob/master/colorednoise.py
).

Here, a modified algorithm for the generation of brown noise from
[python-acoustics](
    https://github.com/python-acoustics/python-acoustics
) is used.
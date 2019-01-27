# encoding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Settings
resolution = (60, 100)
intensity = 5
glow_fraction = 0.33
number_glow_patterns = 100

# Prepare values
flame = np.zeros(resolution)
rows = np.arange(resolution[0]-2, -1, -1)
cols = np.arange(1, resolution[1]-1)
damping = 10/intensity

# Prepare fireplace
fireplace = plt.figure(figsize=plt.figaspect(flame))
fireplace.add_axes([0,0,1,1])
fire = plt.imshow(
    flame,
    cmap="afmhot",
    vmin=0,
    vmax=100,
)

# Prepare glowing patterns
glow_size = int(resolution[1]*glow_fraction)
glow_patterns = [
    np.random.choice(cols, size=glow_size, replace=False)
    for _ in range(number_glow_patterns)
]

def glow(wood):
    glowing = glow_patterns[np.random.randint(number_glow_patterns)]
    for col in glowing:
        wood[col] = np.abs(100*np.random.randn())

# Animation
def burn(_):
    glow(flame[-1])

    for row in rows:
        for col in cols:
            left = col - min(col, np.random.randint(0, 2))
            right = col + min(resolution[1] - col, np.random.randint(0, 2))
            sample = flame[row+1][left:right+1]
            value = (sum(sample) + flame[row][col])/(len(sample) + 1)
            flame[row][col] = value - damping

    fire.set_array(flame)
    return [fire]

burning = FuncAnimation(fireplace, burn, interval=1, blit=True)
plt.show()
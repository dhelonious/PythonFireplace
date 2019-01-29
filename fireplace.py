# encoding: utf-8

# TODO: use namedtuples to structure variables

import threading
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyaudio

class Fireplace():

    def __init__(
            self,
            width,
            height,
        ):

        # Settings
        self.intensity = 5
        self.damping = 10/self.intensity
        self.glow_fraction = 0.33
        self.number_glow_patterns = 100
        self.wood_distance = 3
        self.volume = 0.2
        self.duration = 10
        self.rate = 2000

        # Prepare the fireplace
        self.width, self.height = width, height
        self.rows = np.arange(self.height-2, -1, -1)
        self.cols = np.arange(1, self.width-1)

        self.flame = np.zeros((self.height, self.width))
        self.sound = pyaudio.PyAudio()
        self.stream = self.sound.open(
            format = pyaudio.paFloat32,
            channels = 1,
            rate = self.rate,
            output = True,
        )
        self.noise = self._brown(self.duration*self.rate).astype(np.float32)
        self.burning = False
        self.burning_sound = None

        self.prepare_chimney(self.flame)
        self.prepare_glow_patterns()

    def __del__(self):
        self.extinguish()

    def prepare_chimney(self, flame):
        plt.rcParams["toolbar"] = "None"
        self.chimney = plt.figure(
            figsize = plt.figaspect(flame),
        )
        self.chimney.add_axes([0, 0, 1, 1])
        self.fire = plt.imshow(
            flame,
            cmap="afmhot",
            vmin=0,
            vmax=100,
        )

        plt.axis("off")
        plt.get_current_fig_manager().window.resizable(False, False)
        self.chimney.canvas.mpl_connect(
            "close_event", lambda evt: self.extinguish()
        )

    def prepare_glow_patterns(self):
        self.glow_patterns = [
            np.random.choice(
                self.cols[self.wood_distance:-self.wood_distance],
                size = int(self.width*self.glow_fraction),
                replace = False
            ) for _ in range(self.number_glow_patterns)
        ]

    def _brown(self, N):
        state = np.random.RandomState()
        uneven = N % 2
        X = state.randn(N//2 + 1 + uneven) + 1j*state.randn(N//2 + 1 + uneven)
        S = (np.arange(len(X)) + 1)
        y = (np.fft.irfft(X/S)).real
        if uneven:
            y = y[:-1]
        return y/np.sqrt((np.abs(y)**2).mean())

    def wood(self):
        return self.flame[-1]

    def glow(self):
        wood = self.wood()
        glowing = self.glow_patterns[
            np.random.randint(self.number_glow_patterns)
        ]
        for col in glowing:
            wood[col] = np.abs(100*np.random.randn())

    def burn(self):
        self.glow()

        for row in self.rows:
            for col in self.cols:
                left = col - min(col, np.random.randint(0, 2))
                right = col + min(self.width - col, np.random.randint(0, 2))
                sample = self.flame[row+1][left:right+1]
                value = (sum(sample) + self.flame[row][col])/(len(sample) + 1)
                self.flame[row][col] = value - self.damping

        self.fire.set_array(self.flame)
        return [self.fire]

    def ignite(self):
        def sound():
            while self.burning:
                self.stream.write((self.volume*self.noise).tobytes())

        self.burning = True
        self.burning_sound = threading.Thread(target=sound)
        self.burning_sound.start()
        self.burning = FuncAnimation(
            self.chimney,
            lambda x: self.burn(),
            interval=1,
            blit=True
        )
        plt.show()

    def extinguish(self):
        self.burning = False
        self.burning_sound = None
        self.stream.stop_stream()
        self.stream.close()
        self.sound.terminate()

fireplace = Fireplace(100, 60)
fireplace.ignite()
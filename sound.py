# encoding: utf-8

import numpy as np
import pyaudio

def brown(N):
    """
      Timmer, J. and Koenig, M., "On generating power law noise",
      Astron. Astrophys. 300, 707-710 (1995)

      Implementations:
      * https://github.com/python-acoustics/python-acoustics
      * https://github.com/felixpatzelt/colorednoise/blob/master/colorednoise.py
    """
    state = np.random.RandomState()
    uneven = N % 2
    X = state.randn(N//2 + 1 + uneven) + 1j*state.randn(N//2 + 1 + uneven)
    S = (np.arange(len(X)) + 1)
    y = (np.fft.irfft(X/S)).real
    if uneven:
        y = y[:-1]
    return y/np.sqrt((np.abs(y)**2).mean())

# Settings
volume = 0.2
duration = 10
samplerate = 2

# Prepare audio
p = pyaudio.PyAudio()

stream = p.open(
    format = pyaudio.paFloat32,
    channels = 1,
    rate = samplerate*1000,
    output = True,
)

samples = brown(duration*samplerate*1000).astype(np.float32)

# Play sound
while True:
    stream.write((volume*samples).tobytes())

# Close audio
stream.stop_stream()
stream.close()

p.terminate()
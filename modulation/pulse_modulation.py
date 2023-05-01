import numpy as np
import matplotlib.pyplot as plt
from .util import *

def PPM(inputs):
    samples_per_sec = 1000
    [fc,fm,Am,Ac,message_type,ppm_ratio] = inputs
    print(fc,fm,Am,Ac)
    duration = 1
    x = np.linspace(0, duration, int(duration * samples_per_sec))
    carrier = Ac*np.sin(2 * np.pi * fc * x)
    if message_type == "sin":
        message = Am*np.sin(2 * np.pi * fm * x)
    elif message_type == "cos":
        message = Am*np.cos(2 * np.pi * fm * x)
    ppm_mod = np.zeros(len(x))
    for i in range(len(x)):
        if message[i] > 0:
            ppm_mod[i] = carrier[i] * (1 + ppm_ratio)
        else:
            ppm_mod[i] = carrier[i] * (1 - ppm_ratio)

    a = plot_graph(x, message,color="red", title="message_signal")
    b = plot_graph(x, carrier,color="green", title="carrier_wave")
    c = plot_graph(x, ppm_mod,color="pink", title="Modulated_wave")
    
    return [a,b,c]

def PCM(inputs):
    pass

def PAM(inputs):
    [Am,Ac,fm,fc,message_type,fs] = inputs
    N  = 1000
    x = np.linspace(0, N/fs, N)
    if message_type == "sin":
        message = Am*np.sin(2 * np.pi * fm * x)
    elif message_type == "cos":
        message = Am*np.cos(2 * np.pi * fm * x)
    
    carrier = Ac * np.sin(2*np.pi*fc*x)
    k = Ac / Am  # Modulation index
    modulated = Ac * (1 + k * message) * np.sin(2*np.pi*fc*x)

    a = plot_graph(x, message, title="message",condition="plot",color="red")
    b = plot_graph(x, carrier, title="carrier",condition="plot",color="green")
    c = plot_graph(x, modulated, title="modulated",condition="plot",color="blue")

    return [a,b,c]

def quantizatin(inputs):
    pass

def sampling(inputs):
    pass

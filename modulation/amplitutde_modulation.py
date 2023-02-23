import matplotlib.pyplot as plt
import numpy as np
from util import *

def AM_main_graph(x,inputs):
    [Am,Ac,fm,fc,message_signal] = inputs
    carrier = Ac*np.cos(2*np.pi*fc*x)
    if(message_signal=="sin"):
        message = Am*np.sin(2*np.pi*fm*x)
        demodulated_wave = Ac*Am*np.sin(2*np.pi*fm*x)
    elif message_signal=='cos':
        demodulated_wave = Ac*Am*np.cos(2*np.pi*fm*x)
        message = Am*np.cos(2*np.pi*fm*x)
    elif message_signal=='tri':
        message = triangular(x, Am)
        demodulated_wave = triangular(x, 0.01*Am*Ac)
    modulated_wave = carrier+message*np.cos(2*np.pi*fc*x)
        
    plot_graph(x = x, y = modulated_wave, title = "Modulated wave",color='r', name="AM_modulated1.png")
    plot_graph(x = x, y = message, title = "Message Signal",color='y', name="AM_message.png")
    plot_graph(x = x, y = carrier, title = "Carrier Signal",color='g', name="AM_carrier.png")
    plot_graph(x = x, y = demodulated_wave, title="demodulated wave", name="AM_demodulated.png")


def AM_double_sideband_modulation(x,inputs):
    [Am,Ac,fm,fc,message_signal,phi] = inputs
    carrier = Am*np.cos(2*np.pi*fc*x)
    if message_signal=="sin":
        demodulated_wave = Ac**2/2*np.cos(phi)*np.sin(2*np.pi*fm*x)
        message = Am*np.sin(2*np.pi*fm*x)
    elif message_signal=='tri':
        message = triangular(x, Am)
        demodulated_wave = triangular(x, 0.01*Am*Ac)
    elif message_signal=='cos':
        demodulated_wave = Ac**2/2*np.cos(phi)*np.cos(2*np.pi*fm*x)
        message = Am*np.cos(2*np.pi*fm*x)

    modulated_wave = message*carrier


    plot_graph(x = x, y = modulated_wave, title = "Modulated wave", color ='r', name = "AM_modulated1.png")
    plot_graph(x = x, y = message, title = "Message Signal", color = 'y', name = "AM_message.png")
    plot_graph(x = x, y = carrier, title = "Carrier Signal", color = 'g', name = "AM_carrier.png")
    plot_graph(x = x, y = demodulated_wave, title="demodulated wave", color = 'm', name = "AM_demodulated.png")



def AM_ssb_modulation(x,inputs):
    [Am,Ac,fm,fc,message_signal] = inputs
    carrier = Ac*np.cos(2*np.pi*fc*x)
    if message_signal=="sin":
        demodulated_wave = (Am*Ac**2*np.sin(2*np.pi*fm*x))/4
        message = Am*np.sin(2*np.pi*fm*x)
        modulated_positive = message*carrier + Am*np.cos(2*np.pi*fm*x)*carrier
        modulated_negative = message*carrier - Am*np.cos(2*np.pi*fm*x)*carrier
    elif message_signal=="cos":
        message = Am*np.cos(2*np.pi*fm*x)
        demodulated_wave = Am*Ac**2*np.cos(2*np.pi*fm*x)/4
        modulated_positive = message*carrier + Am*np.sin(2*np.pi*fm*x)*carrier
        modulated_negative = message*carrier - Am*np.sin(2*np.pi*fm*x)*carrier
    elif message_signal =="tri":
        message = triangular(x, A)
        demodulated_wave = triangular(x, 0.01*Am*Ac)
        modulated_positive = message*carrier + triangular(x, A)
        modulated_negative = message*carrier - triangular(x, A)

    y2 = (Am*np.cos(2*np.pi*fc*x))
    
    plot_graph(x = x, y = modulated_positive,color='r', title = "Modulated wave 1", name="AM_modulated1.png")
    plot_graph(x = x, y = modulated_negative,color='b', title = "Modulated wave 2", name="AM_modulated2.png")
    plot_graph(x = x, y = message,color='g', title = "Message Signal", name="AM_message.png")
    plot_graph(x = x, y = carrier,color='m', title = "Carrier Signal", name="AM_carrier.png")
    plot_graph(x = x, y=demodulated_wave,color='r', title="demodulated wave", name="AM_demodulated.png")


def AM_QAM(x,inputs):
    [Am,Ac,fm,fc,message_signal,message_signal_2] = inputs
    c1 = Ac*np.cos(2*np.pi*fc*x)
    c2 = Ac*np.sin(2*np.pi*fc*x)

    if message_signal=="sin":
        m1 = Am*np.sin(2*np.pi*fm*x)
    elif message_signal=="cos":
        m1 = Am*np.cos(2*np.pi*fm*x)
    elif message_signal=="tri":
        m1 = triangular(x, Am)
    
    if message_signal_2 == "sin":
        m2 = Am*np.sin(2*np.pi*fm*x)
    elif message_signal_2 == "cos":
        m2 = Am*np.cos(2*np.pi*fm*x)
    elif message_signal_2 == "tri":
        m1 = triangular(x, Am)
    
    modulated_wave = m1*Ac*np.cos(2*np.pi*fc*x) + m2*Ac*np.sin(2*np.pi*fc*x)
     
    
    plot_graph(x = x, y = modulated_wave,color='r', title = "Modulated wave 1", name="AM_modulated1.png")
    plot_graph(x = x, y = m1,color='b', title = "Message Signal", name="AM_message.png")
    plot_graph(x = x, y = m2,color='g', title = "Message Signal", name="AM_message_1.png")
    plot_graph(x = x, y = c1,color='m', title = "Carrier Signal", name="AM_carrier.png")
    plot_graph(x = x, y = c2,color='y', title = "Carrier Signal", name="AM_carrier_1.png")
    plot_graph(x = x, y=m1,color='r', title="demodulated wave", name="AM_demodulated.png")
    plot_graph(x = x, y=m2,color='c', title="demodulated wave", name="AM_demodulated_1.png")

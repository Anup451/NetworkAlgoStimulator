import matplotlib.pyplot as plt
import numpy as np
from .util import *

def AM_main_graph(inputs):
    graphs = []

    [Am,Ac,fm,fc,message_signal] = inputs
    condition = "scatter"
    x_carrier = create_domain_AM(fc)
    x_message = create_domain_AM(fm)
    x_modulated = x_carrier if(len(x_carrier)<len(x_message)) else x_message

    carrier = Ac*np.cos(2*np.pi*fc*x_carrier)

    if(message_signal=="sin"):
        message = Am*np.sin(2*np.pi*fm*x_message)
        demodulated_wave = Ac*Am*np.sin(2*np.pi*fm*x_message)
    elif message_signal=='cos':
        demodulated_wave = Ac*Am*np.cos(2*np.pi*fm*x_message)
        message = Am*np.cos(2*np.pi*fm*x_message)
    elif message_signal=='tri':
        message = triangular(x, Am)
        demodulated_wave = triangular(x, 0.01*Am*Ac)
    
    #add new modulated equation
    # modulated_wave = carrier+message*np.cos(2*np.pi*fc*x_modulated)
    modulated_wave = carrier
        
    a = plot_graph(condition = condition, x = x_message, y = message, title = "Message Signal",color='y')
    b = plot_graph(condition = condition, x = x_carrier, y = carrier, title = "Carrier Signal",color='g')
    c = plot_graph(condition = condition, x = x_carrier, y = modulated_wave, title = "Modulated wave",color='r')
    d = plot_graph(condition = condition, x = x_message, y = demodulated_wave, title="demodulated wave")

    return [a,b,c,d]


def AM_double_sideband_modulation(inputs):
    [Am,Ac,fm,fc,message_signal,phi] = inputs
    condition = "scatter"

    x_carrier = create_domain_AM(fc)
    x_message = create_domain_AM(fm)
    x_modulated = x_carrier if(len(x_carrier)<len(x_message)) else x_message


    carrier = Am*np.cos(2*np.pi*fc*x_carrier)
    if message_signal=="sin":
        demodulated_wave = Ac**2/2*np.cos(phi)*np.sin(2*np.pi*fm*x_message)
        message = Am*np.sin(2*np.pi*fm*x_message)
    elif message_signal=='tri':
        message = triangular(x, Am)
        demodulated_wave = triangular(x, 0.01*Am*Ac)
    elif message_signal=='cos':
        demodulated_wave = Ac**2/2*np.cos(phi)*np.cos(2*np.pi*fm*x_message)
        message = Am*np.cos(2*np.pi*fm*x_message)

    modulated_wave = message*carrier


    a = plot_graph(condition = condition, x = x_message, y = message, title = "Message Signal", color = 'y')
    b = plot_graph(condition = condition, x = x_carrier, y = carrier, title = "Carrier Signal", color = 'g')
    c = plot_graph(condition = condition, x = x_modulated, y = modulated_wave, title = "Modulated wave", color ='r')
    d = plot_graph(condition = condition, x = x_message, y = demodulated_wave, title="demodulated wave", color = 'm')

    return [a,b,c,d]



def AM_ssb_modulation(x,inputs):
    [Am,Ac,fm,fc,message_signal] = inputs
    condition = "scatter"
    
    x_carrier = create_domain_AM(fc)
    x_message = create_domain_AM(fc)
    x_modulated = x_carrier if(len(x_carrier)<len(x_message)) else x_message    
    
    carrier = Ac*np.cos(2*np.pi*fc*x_carrier)

    if message_signal=="sin":
        demodulated_wave = (Am*Ac**2*np.sin(2*np.pi*fm*x_message))/4
        message = Am*np.sin(2*np.pi*fm*x_message)
        modulated_positive = message*carrier + Am*np.cos(2*np.pi*fm*x_modulated)*carrier
        modulated_negative = message*carrier - Am*np.cos(2*np.pi*fm*x_modulated)*carrier
    elif message_signal=="cos":
        message = Am*np.cos(2*np.pi*fm*x)
        demodulated_wave = Am*Ac**2*np.cos(2*np.pi*fm*x)/4
        modulated_positive = message*carrier + Am*np.sin(2*np.pi*fm*x_modulated)*carrier
        modulated_negative = message*carrier - Am*np.sin(2*np.pi*fm*x_modulated)*carrier
    elif message_signal =="tri":
        message = triangular(x, A)
        demodulated_wave = triangular(x, 0.01*Am*Ac)
        modulated_positive = message*carrier + triangular(x, A)
        modulated_negative = message*carrier - triangular(x, A)

    y2 = (Am*np.cos(2*np.pi*fc*x))
    
    a = plot_graph(condition = condition, x = x_message, y = message,color='g', title = "Message Signal")
    b = plot_graph(condition = condition, x = x_carrier, y = carrier,color='m', title = "Carrier Signal")
    c = plot_graph(condition = condition, x = x_modulated, y = modulated_positive,color='r', title = "Modulated wave 1")
    d = plot_graph(condition = condition, x = x_modulated, y = modulated_negative,color='b', title = "Modulated wave 2")
    e = plot_graph(condition = condition, x = x_message, y=demodulated_wave,color='r', title="demodulated wave")
    
    return [a,b,c,d,e]

def AM_QAM(inputs):
    [Am,Ac,fm,fc,message_signal,message_signal_2] = inputs
    condition="scatter"
    x_carrier = create_domain_AM(fc)
    x_message = create_domain_AM(fc)
    x_modulated = x_carrier if(len(x_carrier)<len(x_message)) else x_message


    c1 = Ac*np.cos(2*np.pi*fc*x_carrier)
    c2 = Ac*np.sin(2*np.pi*fc*x_carrier)

    if message_signal=="sin":
        m1 = Am*np.sin(2*np.pi*fm*x_message)
    elif message_signal=="cos":
        m1 = Am*np.cos(2*np.pi*fm*x_message)
    elif message_signal=="tri":
        m1 = triangular(x, Am)
    
    if message_signal_2 == "sin":
        m2 = Am*np.sin(2*np.pi*fm*x_message)
    elif message_signal_2 == "cos":
        m2 = Am*np.cos(2*np.pi*fm*x_message)
    elif message_signal_2 == "tri":
        m1 = triangular(x, Am)
    
    modulated_wave = m1*Ac*np.cos(2*np.pi*fc*x_modulated) + m2*Ac*np.sin(2*np.pi*fc*x_modulated)

    a = plot_graph(condition = condition,x = x_message, y = m1,color='b', title = "Message Signal-1")
    b = plot_graph(condition = condition,x = x_message, y = m2,color='g', title = "Message Signal-2")
    c = plot_graph(condition = condition,x = x_carrier, y = c1,color='m', title = "Carrier Signal-1")
    d = plot_graph(condition = condition,x = x_carrier, y = c2,color='y', title = "Carrier Signal-2")
    e = plot_graph(condition = condition,x = x_modulated, y = modulated_wave,color='r', title = "Modulated wave -1")
    f = plot_graph(condition = condition,x = x_message, y=m1,color='r', title="demodulated wave - 1")
    g = plot_graph(condition = condition,x = x_message, y=m2,color='c', title="demodulated wave - 2")
    
    return [a,b,c,d,e,f,g]
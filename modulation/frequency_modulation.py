import matplotlib.pyplot as plt
import numpy as np
from .util import *

def FM_MAIN(x,inputs):
    Am,Ac,fm,fc,message_signal,K = inputs.values()
    if(message_signal=="sin"):
        y3= Ac*(np.cos((2*np.pi*fc*x))+((K*Am/fm)*np.sin(2*np.pi*fm*x)))
        y1 = Am*np.sin(2*np.pi*fm*x)#message signal
    else:
        y3= Ac*(np.cos(2*np.pi*fc*x)+((K*Am/fm)*np.cos(2*np.pi*fm*x)))
        y1 = Am*np.cos(2*np.pi*fm*x)
    y2 = Ac*np.cos(2*np.pi*fc*x)#carrier signal need to change into scatterplot
        
    a = plot_graph(x = x, y = y1,color="red", title = "Message Signal")
    b = plot_graph(x = x, y = y2,color="blue", title = "Carrier Signal")
    c = plot_graph(x = x, y = y3,color="green", title = "Modulated wave")
    return [a,b,c]
    
    
def PHASE_MAIN(x,inputs):
    Am,Ac,fm,fc,message_signal,K = inputs.values()
    if(message_signal=="sin"):
        y= Ac*np.cos(2*np.pi*fc*x+(K*Am)*np.cos(2*np.pi*fm*x))
        y1 = Am*np.sin(2*np.pi*fm*x)#message signal
    else:
        y= Ac*np.cos(2*np.pi*fc*x+(K*Am)*np.cos(2*np.pi*fm*x))
        y1 = Am*np.cos(2*np.pi*fm*x)       
    
    y2 = Ac*np.cos(2*np.pi*fc*x)#carrier signal need to change into scatterplot
        
    a = plot_graph(x = x, y = y1, title = "Message Signal",color="red")
    b = plot_graph(x = x, y = y, title = "Modulated wave",color="blue")
    c = plot_graph(x = x, y = y2, title = "Carrier Signal",color="green")    
    return [a,b,c]

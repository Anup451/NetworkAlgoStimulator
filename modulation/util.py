import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

def triangular(x,A):
    return np.absolute(np.fmod(np.absolute(x),2*A)-A)
    

def plot_graph(x,y,title,xlabel="Volts",ylabel="Frequncy",color="b",condition="scatter",text=""):
    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    fig = plt.figure(figsize=(20,3))
    plot_axis(fig,ax)
    s = [3 for i in x]
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if text!="":
        plt.text(-210, 5, text, fontsize=14, ha='center', va='center',rotation=90)
    if(condition=="scatter"):
        plt.scatter(x,y,c=color,s=s)        
    else: 
        plt.plot(x,y,c=color)

    fig.tight_layout()
    data = BytesIO()
    fig.savefig(data,format="png")
    data.seek(0)
    encoded_image = data.getvalue().hex()
    plt.close()
    return encoded_image

def plot_axis(fig,ax):
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

def create_domain_AM(frequency):
    x= np.linspace(-200,200,10000)
    if frequency>=50 and frequency<=2000:
        x = np.linspace(-200,200,10000)
    elif frequency<50:
        x = np.linspace(-200,200,1000) 
    elif frequency>2000:
        x = np.linspace(-200,200,12000)
    return x

def destructure_dict(d, *keys):
    return (d[k] for k in keys)

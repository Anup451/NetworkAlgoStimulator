from flask import Flask,render_template,request,redirect,url_for
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


app=Flask(__name__,static_url_path='/static')

def plot_graph(x,y,title,name,xlabel="Volts",ylabel="Frequncy"):
    fig, ax = plt.subplots()
    fig = plt.figure(figsize=(20,6))
    s = [1 for i in x]
    plt.style.use('seaborn')
    plot_axis(fig)    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.scatter(x,y,s)
    fig.tight_layout()
    plt.savefig(f'static/results/{name}',bbox_inches='tight')
    fig.clear()


def plot_axis(fig):
    ax = fig.add_subplot(2, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')


def AM_main_graph(x,x1,inputs):
    [Am,Ac,fm,fc,message_signal] = inputs
    if(message_signal=="sin"):
        y= Ac*(1+((Am/Ac)*np.sin(2*np.pi*fm*x)))*np.cos(2*np.pi*fc*x)
        y1 = Am*np.sin(2*np.pi*fm*x1)#message signal
    else:
        y= Ac*(1+((Am/Ac)*np.cos(2*np.pi*fm*x)))*np.cos(2*np.pi*fc*x)
        y1 = Am*np.cos(2*np.pi*fm*x1)
    y2 = Ac*np.cos(2*np.pi*fc*x1)#carrier signal need to change into scatterplot

    plot_graph(x = x, y = y, title = "Modulated wave", name="AM_modulated1.png")
    plot_graph(x = x1, y = y1, title = "Message Signal", name="AM_message.png")
    plot_graph(x = x1, y = y2, title = "Carrier Signal", name="AM_carrier.png")


def AM_double_sideband_modulation(x,x1,inputs):
    [Am,Ac,fm,fc,message_signal] = inputs
    if message_signal=="sin":
        y = (Am*np.sin(2*np.pi*fm*x))*(Ac*np.cos(2*np.pi*fc*x))
        y1 = (Am*np.sin(2*np.pi*fm*x1))#message signal
    else:
        y = (Am*np.cos(2*np.pi*fm*x))*(Ac*np.cos(2*np.pi*fc*x))
        y1 = (Am*np.cos(2*np.pi*fm*x1))#message signal
    y2 = (Am*np.cos(2*np.pi*fc*x1))#carrier signal
    plot_graph(x = x, y = y, title = "Modulated wave", name="AM_modulated1.png")
    plot_graph(x = x1, y = y1, title = "Message Signal", name="AM_message.png")
    plot_graph(x = x1, y = y2, title = "Carrier Signal", name="AM_carrier.png")



def AM_ssb_modulation(x,x1,inputs):
    [Am,Ac,fm,fc,message_signal] = inputs
    if message_signal=="sin":
        y_positive = (Am*np.sin(2*np.pi*fm*x))*(Ac*np.cos(2*np.pi*fc*x)) + Am*np.cos(2*np.pi*fm*x)*Ac*np.cos(2*np.pi*fc*x)
        y_negative = (Am*np.sin(2*np.pi*fm*x))*(Ac*np.cos(2*np.pi*fc*x)) - Am*np.cos(2*np.pi*fm*x)*Ac*np.cos(2*np.pi*fc*x)
        y1 = (Am*np.sin(2*np.pi*fm*x1))#message signal
    else:
        y_positive = (Am*np.cos(2*np.pi*fm*x))*(Ac*np.cos(2*np.pi*fc*x)) + Am*np.sin(2*np.pi*fm*x)*Ac*np.cos(2*np.pi*fc*x)
        y_negative = (Am*np.cos(2*np.pi*fm*x))*(Ac*np.cos(2*np.pi*fc*x)) - Am*np.sin(2*np.pi*fm*x)*Ac*np.cos(2*np.pi*fc*x)
        y1 = (Am*np.cos(2*np.pi*fm*x1))#message signal
    y2 = (Am*np.cos(2*np.pi*fc*x1))#carrier signal
    
    plot_graph(x = x, y = y_positive, title = "Modulated wave", name="AM_modulated1.png")
    plot_graph(x = x, y = y_positive, title = "Modulated wave", name="AM_modulated2.png")
    plot_graph(x = x1, y = y1, title = "Message Signal", name="AM_message.png")
    plot_graph(x = x1, y = y2, title = "Carrier Signal", name="AM_carrier.png")



def AM_QAM(x,x1,inputs):
    if message_signal=="sin":
        y_positive = (Am*np.sin(2*np.pi*fm*x))*(Ac*cos(2*np.pi*fc*x)) + Am*np.cos(2*np.pi*fm*x)*Ac*np.cos(2*np.pi*fc*x)
        y_negative = (Am*np.sin(2*np.pi*fm*x))*(Ac*cos(2*np.pi*fc*x)) - Am*np.cos(2*np.pi*fm*x)*Ac*np.cos(2*np.pi*fc*x)
        y11 = (Am*np.sin(2*np.pi*fm*x1))#message signal
        y12 = (Am*np*sin(2*np*fm*x1))
    else:
        y = (Am*np.cos(2*np.pi*fm*x))*(Ac*cos(2*np.pi*fc*x))
        y1 = (Am*np.cos(2*np.pi*fm*x1))#message signal
    y2 = (Am*np.cos(2*np.pi*fc*x1))#carrier signal



@app.route('/',methods=['GET'])
def home():
    return redirect(url_for("AM_page"))

@app.route('/AM',methods=['GET'])
def AM_page():
    return render_template('Amplitude_Modulation.html')

@app.route('/AM/<index>',methods=['GET','POST'])
def Amplitutde_Modulation(index):   
    index = int(index)
    title = {1:"Amplitutde Modulation",2:"SSB Modulation",3:"DSB Modulation",4:"QAM Modulation"}
    global y,y1,y2,y11,y12,y_positive,y_negative
    if (request.method=='POST'):
        fm=int (request.form['fm'])
        fc=int (request.form['fc'])
        Am=int (request.form['Am'])
        Ac=int (request.form['Ac'])
        message_signal = str(request.form['message_signal'])
        inputs = [Am,Ac,fm,fc,message_signal]
        x = np.linspace(-200,200,10000) #domain for the modulated_wave
        x1 = np.linspace(-200,200,20000) #domain for the carrier and message signal
        s = [1 for i in x]
        s1 = [1 for i in x1]

        if index == 1:
            AM_main_graph(x, x1, inputs)
        elif index == 2:
            AM_ssb_modulation(x, x1, inputs)
        elif index == 3:
            AM_double_sideband_modulation(x, x1, inputs)
        elif index == 4:
            AM_QAM(x,x1,inputs) 
    return render_template('AM_graphs.html',index=index,title=title[index])


if __name__ == "__main__":
    app.run(debug=True)
    
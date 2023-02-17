from flask import Flask,render_template,request,redirect,url_for
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


app=Flask(__name__,static_url_path='/static')

def plot_graph(x,y,title,name,xlabel="Volts",ylabel="Frequncy",color="b",condition="scatter"):
    fig, ax = plt.subplots()
    fig = plt.figure(figsize=(20,6))
    s = [1 for i in x]
    plt.style.use('seaborn')
    plot_axis(fig)    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if condition=="scatter":
        plt.scatter(x,y,s,c=color)
    elif condition=="plot":
        plt.plot(x,y,s,c=color)
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


def AM_main_graph(x,inputs):
    [Am,Ac,fm,fc,message_signal] = inputs
    carrier = Ac*np.cos(2*np.pi*fc*x)
    if(message_signal=="sin"):
        message = Am*np.sin(2*np.pi*fm*x)
        demodulated_wave = Ac*Am*np.sin(2*np.pi*fm*x)
        y= Ac*(1+((Am/Ac)*np.sin(2*np.pi*fm*x)))*np.cos(2*np.pi*fc*x)
    else:
        demodulated_wave = Ac*Am*np.cos(2*np.pi*fm*x)
        message = Am*np.cos(2*np.pi*fm*x)
        y= Ac*(1+((Am/Ac)*np.sin(2*np.pi*fm*x)))*np.cos(2*np.pi*fc*x)
    modulated_wave = carrier+message*np.cos(2*np.pi*fc*x)
        
    plot_graph(x = x, y = y, title = "Modulated wave",color='r', name="AM_modulated1.png")
    plot_graph(x = x, y = message, title = "Message Signal",color='y', name="AM_message.png")
    plot_graph(x = x, y = carrier, title = "Carrier Signal",color='g', name="AM_carrier.png")
    plot_graph(x = x, y = demodulated_wave, title="demodulated wave", name="AM_demodulated.png")


def AM_double_sideband_modulation(x,x1,inputs):
    [Am,Ac,fm,fc,message_signal,phi] = inputs
    carrier = Am*np.cos(2*np.pi*fc*x1)
    if message_signal=="sin":
        demodulated_wave = Ac**2/2*np.cos(phi)*np.sin(2*np.pi*fm*x)
        message = Am*np.sin(2*np.pi*fm*x)
    else:
        demodulated_wave = Ac**2/2*np.cos(phi)*np.cos(2*np.pi*fm*x)
        message = Am*np.cos(2*np.pi*fm*x)
    modulated_wave = message*carrier

    plot_graph(x = x, y = modulated_wave, title = "Modulated wave",color='r', name="AM_modulated1.png")
    plot_graph(x = x, y = message, title = "Message Signal",color='y', name="AM_message.png")
    plot_graph(x = x, y = carrier, title = "Carrier Signal",color='g', name="AM_carrier.png")
    plot_graph(x=x, y=demodulated_wave, title="demodulated wave",color='m', name="AM_demodulated.png")




def AM_ssb_modulation(x,inputs):
    [Am,Ac,fm,fc,message_signal] = inputs
    if message_signal=="sin":
        demodulated_wave = (Am*Ac**2*np.sin(2*np.pi*fm*x))/4
        y_positive = (Am*np.sin(2*np.pi*fm*x))*(Ac*np.cos(2*np.pi*fc*x)) + Am*np.cos(2*np.pi*fm*x)*Ac*np.cos(2*np.pi*fc*x)
        y_negative = (Am*np.sin(2*np.pi*fm*x))*(Ac*np.cos(2*np.pi*fc*x)) - Am*np.cos(2*np.pi*fm*x)*Ac*np.cos(2*np.pi*fc*x)
        y1 = (Am*np.sin(2*np.pi*fm*x))#message signal
    else:
        demodulated_wave = Am*Ac**2*np.cos(2*np.pi*fm*x)/4
        y_positive = (Am*np.cos(2*np.pi*fm*x))*(Ac*np.cos(2*np.pi*fc*x)) + Am*np.sin(2*np.pi*fm*x)*Ac*np.cos(2*np.pi*fc*x)
        y_negative = (Am*np.cos(2*np.pi*fm*x))*(Ac*np.cos(2*np.pi*fc*x)) - Am*np.sin(2*np.pi*fm*x)*Ac*np.cos(2*np.pi*fc*x)
        y1 = (Am*np.cos(2*np.pi*fm*x))#message signal
    y2 = (Am*np.cos(2*np.pi*fc*x))#carrier signal
    
    plot_graph(x = x, y = y_positive,color='r', title = "Modulated wave 1", name="AM_modulated1.png")
    plot_graph(x = x, y = y_negative,color='b', title = "Modulated wave 2", name="AM_modulated2.png")
    plot_graph(x = x, y = y1,color='g', title = "Message Signal", name="AM_message.png")
    plot_graph(x = x, y = y2,color='m', title = "Carrier Signal", name="AM_carrier.png")
    plot_graph(x=x, y=demodulated_wave,color='r', title="demodulated wave", name="AM_demodulated.png")


def AM_QAM(x,inputs):
    [Am,Ac,fm,fc,message_signal,message_signal_2] = inputs
    if message_signal=="sin" and message_signal_2=="sin":
        y_positive = (Am*np.sin(2*np.pi*fm*x))*(Ac*cos(2*np.pi*fc*x)) + Am*np.cos(2*np.pi*fm*x)*Ac*np.cos(2*np.pi*fc*x)
        y_negative = (Am*np.sin(2*np.pi*fm*x))*(Ac*cos(2*np.pi*fc*x)) - Am*np.cos(2*np.pi*fm*x)*Ac*np.cos(2*np.pi*fc*x)
        y11 = (Am*np.sin(2*np.pi*fm*x))#message signal
        y12 = (Am*np*sin(2*np*fm*x))
    else:
        y = (Am*np.cos(2*np.pi*fm*x))*(Ac*cos(2*np.pi*fc*x))
        y1 = (Am*np.cos(2*np.pi*fm*x))#message signal
    y2 = (Am*np.cos(2*np.pi*fc*x))#carrier signal



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
        x = np.linspace(-200,200,30000) #domain for the modulated_wave
        x1 = np.arange(-200,200,.001)
        s = [1 for i in x]

        if index == 1:
            AM_main_graph(x, inputs)
        elif index == 2:
            AM_ssb_modulation(x, inputs)
        elif index == 3:
            phi  = float(request.form['phi'])
            inputs.append(phi)
            AM_double_sideband_modulation(x, inputs)
        elif index == 4:
            message_signal_2 = request.form['message_signal_2']
            inputs.append(message_signal_2)
            AM_QAM(x,x1,inputs) 
    return render_template('AM_graphs.html',index=index,title=title[index])


if __name__ == "__main__":
    app.run(debug=True)
    
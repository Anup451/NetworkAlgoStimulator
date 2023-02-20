from flask import Flask,render_template,request,redirect,url_for
import pandas as pd
import sys
import matplotlib
matplotlib.use('WebAgg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os


app=Flask(__name__,static_url_path='/static')

if __name__ == "__main__":
    app.run(debug=True)

def triangular(x,A):
    return np.absolute(np.fmod(np.absolute(x),2*A)-A)


def plot_graph(x,y,title,name,xlabel="Volts",ylabel="Frequncy",color="b",condition="scatter"):
    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    fig = plt.figure(figsize=(20,3))
    plot_axis(fig,ax)
    s = [1 for i in x]
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if condition=="scatter":
        plt.scatter(x,y,s,c=color)
    elif condition=="plot":
        plt.plot(x,y,s,c=color)
    fig.tight_layout()
    plt.savefig(f'static/results/{name}',bbox_inches='tight')
    plt.close()


def plot_axis(fig,ax):
    ax = fig.add_subplot(1, 1, 1)
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
    c1 = Ac*np.cos(2*np.pi*fc*x)
    c2 = Ac*np.sin(2*np.pi*fc*x)

    if message_signal=="sin":
        m1 = Am*np.sin(2*np.pi*fm*x)
    else:
        m1 = Am*np.cos(2*np.pi*fm*x)
    
    if message_signal_2 == "sin":
        m2 = Am*np.sin(2*np.pi*fm*x)
    else:
        m2 = Am*np.cos(2*np.pi*fm*x)

    modulated_wave = m1*Ac*np.cos(2*np.pi*fc*x) + m2*Ac*np.sin(2*np.pi*fc*x)
    
    plot_graph(x = x, y = modulated_wave,color='r', title = "Modulated wave 1", name="AM_modulated1.png")
    plot_graph(x = x, y = m1,color='b', title = "Message Signal", name="AM_message.png")
    plot_graph(x = x, y = m2,color='g', title = "Message Signal", name="AM_message_1.png")
    plot_graph(x = x, y = c1,color='m', title = "Carrier Signal", name="AM_carrier.png")
    plot_graph(x = x, y = c2,color='y', title = "Carrier Signal", name="AM_carrier_1.png")
    plot_graph(x = x, y=m1,color='r', title="demodulated wave", name="AM_demodulated.png")
    plot_graph(x = x, y=m2,color='c', title="demodulated wave", name="AM_demodulated_1.png")

@app.route('/',methods=['GET'])
def home():
    return redirect(url_for("AM_page"))

@app.route('/AM',methods=['GET'])
def AM_page():
    return render_template('Amplitude_Modulation.html')

@app.route('/AM/<am_type>',methods=['GET','POST'])
def Amplitutde_Modulation(am_type):  
    
    root_dir = os.path.dirname(os.getcwd()) 
    res_dir = os.path.join(root_dir,"static","results")
    results = os.listdir('./static/results')

    for images in results:
        if images.endswith(".png"):
            os.remove(os.path.join('./static/results', images))
    
    title = {"MAIN":"Amplitutde Modulation","SSB":"SSB Modulation","DSBSC":"DSB Modulation","QAM":"QAM Modulation"}

    if (request.method=='POST'):
        fm=int (request.form['fm'])
        fc=int (request.form['fc'])
        Am=int (request.form['Am'])
        Ac=int (request.form['Ac'])
        message_signal = str(request.form['message_signal'])
        inputs = [Am,Ac,fm,fc,message_signal]
        x = np.linspace(-200,200,10000) #domain for the modulated_wave

        if am_type == "MAIN":
            AM_main_graph(x, inputs)
        elif am_type == "SSB":
            AM_ssb_modulation(x, inputs)
        elif am_type == "DSBSC":
            phi  = float(request.form['phi'])
            inputs.append(phi)
            AM_double_sideband_modulation(x, inputs)
        elif index == "QAM":
            message_signal_2 = request.form['message_signal_2']
            inputs.append(message_signal_2)
            AM_QAM(x,inputs) 
    return render_template('AM_graphs.html',am_type=am_type,title=title[am_type])


if __name__ == "__main__":
    app.run(debug=True)
    
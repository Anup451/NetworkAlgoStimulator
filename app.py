from flask import Flask,render_template,request
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def hello_world():
    if (request.method=='POST'):
        print('psot')
        fm=int (request.form['fm'])
        fc=int (request.form['fc'])
        Am=int (request.form['Am'])
        Ac=int (request.form['Ac'])
        message_signal = str(request.form['message_signal'])
        # s = pd.Series([f1, f2, 5])
        fig, ax = plt.subplots()
        print((message_signal))
        # s.plot.bar()
        x = np.linspace(-200,200,500)
        if(message_signal=="sin"):
            y= Ac*(1+((Am/Ac)*np.sin(2*np.pi*fm*x)))*np.cos(2*np.pi*fc*x)
            y1 = Am*np.sin(2*np.pi*fm*x)
        else:
            y= Ac*(1+((Am/Ac)*np.cos(2*np.pi*fm*x)))*np.cos(2*np.pi*fc*x)
            y1 = Am*np.cos(2*np.pi*fm*x)

        y2 = Ac*np.cos(2*np.pi*fc*x)#carrier signal need to change into scatterplot

        
        # setting the axes at the centre
        fig = plt.figure(figsize=(20,6))
        ax = fig.add_subplot(2, 1, 1)
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        # plot the function
        plt.plot(x,y, 'r')
        plt.savefig('static/my_plot.png')
        fig.savefig('static/my_plot.png')
        fig.clear()

         # plot the function
        plt.plot(x,y1, 'r')
        plt.savefig('static/my_plot1.png')
        fig.savefig('static/my_plot1.png')
        fig.clear()

         # plot the function
        plt.plot(x,y2, 'r')
        for i in range(len(x)):
            print("[",x[i],y[i],"]")
        plt.savefig('static/my_plot2.png')
        fig.savefig('static/my_plot2.png')
        fig.clear()
    # return 'HELLO, World'
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
    
from flask import Flask,render_template,request
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def hello_world():
    if (request.method=='POST'):
        print('psot')
        fm=int (request.form['fm'])
        fc=int (request.form['fc'])
        Am=int (request.form['Am'])
        Ac=int (request.form['Ac'])
        # s = pd.Series([f1, f2, 5])
        fig, ax = plt.subplots()
        # s.plot.bar()
        x = np.linspace(-50,50,10000)
        y= Ac*(1+((Am/Ac)*np.cos(2*np.pi*fm*x)))*np.cos(2*np.pi*fc*x)

        # setting the axes at the centre
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
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
    # return 'HELLO, World'
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
    
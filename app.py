from dotenv import load_dotenv
from flask import Flask,render_template,request,redirect,url_for
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
from amplitutde_modulation import *
from digital_modulation import *
from util import *
import logging

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

matplotlib.use('WebAgg')

load_dotenv()

app=Flask(__name__,static_url_path='/static')


@app.route('/',methods=['GET'])
def home():
    return "hello world"
    return render_template('home.html')

# ---------- Analog Modulation -------------------
@app.route('/AM',methods=['GET'])
def AM_page():
    return render_template('Analog_Modulation.html')

@app.route('/AM/<am_type>',methods=['GET','POST'])
def Amplitutde_Modulation(am_type):  
    root_dir = os.path.dirname(os.getcwd()) 
    res_dir = os.path.join(root_dir,"static","results")
    results = os.listdir('./static/results')
    for images in results:
        if images.endswith(".png"):
            os.remove(os.path.join('./static/results', images))
    
    title = {"MAIN":"Amplitutde Modulation","SSB":"SSB Modulation","DSBSC":"DSB Modulation","QAM":"QAM Modulation"}
    print(am_type)
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
        elif am_type == "QAM":
            message_signal_2 = request.form['message_signal_2']
            inputs.append(message_signal_2)
            AM_QAM(x,inputs) 
    return render_template('AM_graphs.html',am_type=am_type.upper(),title=title[am_type])

@app.route('/FM/<index>',methods=['GET','POST'])
def FM(index):
    results = os.listdir('./static/results')
    for images in results:
        if images.endswith(".png"):
            os.remove(os.path.join('./static/results', images))
    index = int(index)
    title={1:"Frequency modulation",2:"Phase modulation"}
    if request.method == 'POST':
        fm=int (request.form['fm'])
        fc=int (request.form['fc'])
        Am=int (request.form['Am'])
        Ac=int (request.form['Ac'])
        message_signal = str(request.form['message_signal'])
        K = int(request.form['K'])
        inputs = [Am,Ac,fm,fc,message_signal,K]
        x = np.linspace(-200,200,10000) #domain for the modulated_wave
        s = [1 for i in x]
        if(index==1):
            FM_MAIN(x,inputs)
            
        elif(index==2):
            PHASE_MAIN(x,inputs)   
            
        # elif(index==3):
        #     PULSE_MAIN(x,inputs) 
    return render_template('fm_graphs.html',title=title[index],index=index)

# ---------- End of Analog Modulation ------------


# ---------- Digital Modulation ---------------------

@app.route('/DM',methods=['GET'])
def DM_page():
    return render_template('Digital_modulation.html')


@app.route('/DM/<dmtype>', methods=['GET','POST'])
def DigitalModulation(dmtype):
    title = {"BPSK":"BPSK Modulation","BFSK":"BFSK Modulation","BASK":"BASK Modulation","QPSK":"QPSK Modulation"}
    if (request.method=='POST'):
      Tb=float (request.form['Tb'])
      fc=int (request.form['fc'])
      binaryInput = str(request.form['inputBinarySeq'])
      fc2=1
      if(dmtype=='BFSK'):
          fc2=int (request.form['fc2'])

      # Change Binary string to array
      inputBinarySeq = np.array(list(binaryInput), dtype=int)

      if dmtype.upper() == 'BASK':
          BASK(Tb, fc, inputBinarySeq)
      elif dmtype.upper() == 'BFSK':
          BFSK(Tb, fc, fc2, inputBinarySeq)
      elif dmtype.upper() == 'BPSK':
          BPSK(Tb, fc, inputBinarySeq)
      elif dmtype.upper() == 'QPSK':
          QPSK(Tb, fc, inputBinarySeq)

    return render_template('DM_graphs.html',dmtype=dmtype.upper(),title=title[dmtype])

# ------------ End of Digital Modulation -------------

def create_app():
    from waitress import serve
    PORT = int(os.environ.get("PORT",8000))
    serve(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    create_app()
from dotenv import load_dotenv
from flask import Flask,render_template,request,redirect,url_for
from flask_cors import CORS
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import base64
from modulation import *
from binascii import unhexlify
import logging

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

matplotlib.use('WebAgg')

load_dotenv()

app=Flask(__name__,static_url_path='/static')
CORS(app)

@app.template_filter('decode_hex')
def decode_hex(s):
    return unhexlify(s)


@app.template_filter('b64encode')
def b64encode(s):
    return base64.b64encode(s).decode('utf-8')

@app.route('/',methods=['GET'])
def home():
    return render_template('home.html')

# ---------- Analog Modulation -------------------
@app.route('/AM',methods=['GET'])
def AM_page():
    return render_template('Analog_Modulation.html')

@app.route('/AM/<am_type>',methods=['GET','POST'])
def Amplitutde_Modulation(am_type):  
    
    title = {"MAIN":"Amplitutde Modulation","SSB":"SSB Modulation","DSBSC":"DSB Modulation","QAM":"QAM Modulation"}
    print(am_type)
    images = []
    x_message = []
    x_carrier = []
    content_type = request.headers.get('Content-Type')    
    if (request.method=='POST'):
        if (content_type == 'application/json'):
            content = request.json
        else:
            content = request.form
        print(content)
        fm=int (content['fm'])
        fc=int (content['fc'])
        Am=int (content['Am'])
        Ac=int (content['Ac'])
        message_signal = str(content['message_signal'])
        inputs = [Am,Ac,fm,fc,message_signal]            

        if am_type == "MAIN":
            images = AM_main_graph(inputs)
        elif am_type == "SSB":
            images = AM_ssb_modulation(inputs)
        elif am_type == "DSBSC":
            phi  = float(request.form['phi'])
            inputs.append(phi)
            images = AM_double_sideband_modulation(inputs)
        elif am_type == "QAM":
            message_signal_2 = request.form['message_signal_2']
            inputs.append(message_signal_2)
            images = AM_QAM(inputs) 
    return render_template('AM_graphs.html',am_type=am_type.upper(),title=title[am_type],images = images)

@app.route('/FM/<index>',methods=['GET','POST'])
def FM(index):
    images = []
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
            images = FM_MAIN(x,inputs)
            
        elif(index==2):
            images = PHASE_MAIN(x,inputs)   
            
        # elif(index==3):
        #     PULSE_MAIN(x,inputs) 
    return render_template('fm_graphs.html',title=title[index],index=index,images=images)

# ---------- End of Analog Modulation ------------


# ---------- Digital Modulation ---------------------

@app.route('/DM',methods=['GET'])
def DM_page():
    return render_template('Digital_Modulation.html')


@app.route('/DM/<dmtype>', methods=['GET','POST'])
def DigitalModulation(dmtype):
    title = {"BPSK":"BPSK Modulation","BFSK":"BFSK Modulation","BASK":"BASK Modulation","QPSK":"QPSK Modulation"}
    plots = []

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
          plots = BASK(Tb, fc, inputBinarySeq)
      elif dmtype.upper() == 'BFSK':
          plots = BFSK(Tb, fc, fc2, inputBinarySeq)
      elif dmtype.upper() == 'BPSK':
          plots = BPSK(Tb, fc, inputBinarySeq)
      elif dmtype.upper() == 'QPSK':
          plots = QPSK(Tb, fc, inputBinarySeq)

    return render_template('DM_graphs.html',dmtype=dmtype.upper(),title=title[dmtype], plots=plots)

@app.route('/DM2/<dmtype>', methods=['GET','POST'])
def GMSK_Modulation(dmtype):
    title = {"GMSK":"GMSK Modulation"}
    plots = []

    if (request.method=='POST'):
        fm=int (request.form['fm'])
        am=int (request.form['am'])
        pm=int (request.form['pm'])

        fc=int (request.form['fc'])
        ac=int (request.form['ac'])
        pc=int (request.form['pc'])

        # --
        if dmtype.upper() == 'GMSK':
            plots = GMSK(fm, am, pm, fc, ac, pc)
    
    return render_template('GMSK_graphs.html',dmtype=dmtype.upper(),title=title[dmtype], plots=plots)


# ------------ End of Digital Modulation -------------

def create_app():
    from waitress import serve
    PORT = int(os.environ.get("PORT",8000))
    serve(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    create_app()
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
import json


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
    f = open('./data.json')
    data = json.load(f)["Home"]
    return render_template('home.html',data=data)

@app.route('/references',methods=['GET'])
def references():
    return render_template('references.html')

@app.route('/theory/<modulation_type>',methods=["GET"])
def theory(modulation_type):
    return render_template(f'theory/{modulation_type}.html')

# ---------- Analog Modulation -------------------
@app.route('/AM',methods=['GET'])
def AM_page():
    f = open('./data.json')
    data = json.load(f)["AM"]
    return render_template('Analog_Modulation.html',data=data)

@app.route('/AM/<am_type>',methods=['GET','POST'])
def Amplitutde_Modulation(am_type):  
    
    title = {"MAIN":"Amplitutde Modulation","SSB":"SSB Modulation","DSBSC":"DSB Modulation","QAM":"QAM Modulation"}
    plots = []
    x_message = []
    x_carrier = []
    if (request.method=='POST'):
        content = request.form
        fm=int(content['fm'])
        fc=int(content['fc'])
        Am=int(content['Am'])
        Ac=int(content['Ac'])
        message_signal = str(content['message_signal'])
        
        inputs = {"Am":Am,"Ac":Ac,"fm":fm,"fc":fc,"message_signal":message_signal}
        
        if am_type == "MAIN":
            plots = AM_main_graph(inputs)
        elif am_type == "SSB":
            plots = AM_ssb_modulation(inputs)
        elif am_type == "DSBSC":
            phi  = float(request.form['phi'])
            inputs["phi"] = phi
            plots = AM_double_sideband_modulation(inputs)
        elif am_type == "QAM":
            message_signal_2 = request.form['message_signal_2']
            inputs["message_signal_2"] = message_signal_2
            plots = AM_QAM(inputs) 
        return render_template('AM_graphs.html',am_type=am_type.upper(),title=title[am_type],plots = plots,inputs=inputs)
    return render_template('AM_graphs.html',am_type=am_type.upper(),title=title[am_type],plots = plots)

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
        inputs = {"Am":Am,"Ac":Ac,"fm":fm,"fc":fc,"message_signal":message_signal,"K":K}
        x = np.linspace(-200,200,10000) #domain for the modulated_wave
        s = [1 for i in x]
        if(index==1):
            images = FM_MAIN(x,inputs)           
        elif(index==2):
            images = PHASE_MAIN(x,inputs)   
        return render_template('fm_graphs.html',title=title[index],index=index,plots=images,inputs=inputs)
    return render_template('fm_graphs.html',title=title[index],index=index,plots=images)

# ---------- End of Analog Modulation ------------


# ---------- Digital Modulation ---------------------

@app.route('/DM',methods=['GET'])
def DM_page():
    f = open('./data.json')
    data = json.load(f)["DM"]
    return render_template('Digital_Modulation.html',data=data)


@app.route('/DM/<dmtype>', methods=['GET','POST'])
def DigitalModulation(dmtype):
    title = {"BPSK":"BPSK Modulation","BFSK":"BFSK Modulation","BASK":"BASK Modulation","QPSK":"QPSK Modulation"}
    plots = []

    if (request.method=='POST'):
      Tb=float (request.form['Tb'])
      fc=int (request.form['fc'])
      binaryInput = str(request.form['inputBinarySeq'])
      inputs = {"Tb":Tb,"fc":fc,"binaryInput":binaryInput}
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
      return render_template('DM_graphs.html',dmtype=dmtype.upper(),title=title[dmtype], plots=plots,inputs=inputs)
    return render_template('DM_graphs.html',dmtype=dmtype.upper(),title=title[dmtype], plots=plots)

@app.route('/DM2/<dmtype>', methods=['GET','POST'])
def GMSK_Modulation(dmtype):
    title = {"GMSK":"GMSK Modulation"}
    plots = []

    if (request.method=='POST'):
        a= str (request.form['data_stream'])
        fc= int (request.form['fc'])
        osmp_factor= int (request.form['osmp_factor'])
        bt_prod= float (request.form['bt_prod'])

        inputs = {"fm":fm,"fc":fc,"Ac":am,"Am":ac,"Pc":pc}
        if dmtype.upper() == 'GMSK':
            plots = GMSK(a, fc, osmp_factor, bt_prod)
    
        return render_template('GMSK_graphs.html',dmtype=dmtype.upper(),title=title[dmtype], plots=plots,inputs=inputs)    


@app.route('/DM3/<dmtype>', methods=['GET','POST'])
def DPSK_Modulation(dmtype):
    title = {"DPSK":"DPSK Modulation"}
    plots = []

    if (request.method=='POST'):
        fm= int (request.form['fm'])
        Am= int (request.form['am'])
        phi_m= int (request.form['phi_m'])
        fc= int (request.form['fc'])
        Ac= int (request.form['ac'])
        phi_c= int (request.form['phi_c'])

        # --
        if dmtype.upper() == 'DPSK':
            plots = DPSK(fm, Am, phi_m, fc, Ac, phi_c)
    
    return render_template('DPSK_graphs.html',dmtype=dmtype.upper(),title=title[dmtype], plots=plots)


# ------------ End of Digital Modulation -------------

# ---------- Pulse Modulation ---------------------

# @app.route('/PM',methods=['GET'])
# def PM_page():
#     f = open('./data.json')
#     data = json.load(f)["PM"]
#     return render_template('Pulse_Modulation.html',data=data)


# @app.route('/PM/<pmtype>', methods=['GET','POST'])
# def PulseModulation(pmtype):
#     title = {"Sampling":"Sampling",
#              "Quantization":"Quantization",
#              "PAM":"Pulse Amplitude Modulation",
#              "PPM":"Pulse Phase Modulation",
#              "PCM":"Pulse Position Modulation",
#              "PWM":"Pulse Width Modulation"
#              }
#     plots = []
#     inputs = []
#     print(request.form)
#     if (request.method=='POST'):
#         fm = int (request.form['fm'])
#         am = int (request.form['am'])
#         fc = int (request.form['fc'])
#         ac = int (request.form['ac'])
#         message_type = str(request.form["message_signal"])
#         inputs = [am,ac,fm,fc,message_type]

#       # Change Binary string to array
#         print(pmtype)
#         if pmtype.upper() == 'PPM':
#             ppm_ratio = float(request.form['ppm_ratio'])        
#             inputs.append(ppm_ratio)
#             plots = PPM(inputs)
#         elif pmtype.upper() == 'PAM':
#           inputs.append(int(request.form['fs']))
#           plots = PAM(inputs)
#         elif pmtype.upper() == 'BPSK':
#           plots = BPSK(Tb, fc, inputBinarySeq)
#         elif pmtype.upper() == 'QPSK':
#           plots = QPSK(Tb, fc, inputBinarySeq)

#     return render_template('PM_graphs.html',pmtype=pmtype.upper(),title=title[pmtype], plots=plots)




def create_app():
    from waitress import serve
    PORT = int(os.environ.get("PORT",8000))
    serve(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    create_app()
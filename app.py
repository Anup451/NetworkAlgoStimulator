from flask import Flask,render_template,request,redirect,url_for
import pandas as pd
import sys
import matplotlib
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from amplitutde_modulation import *
from util import *
matplotlib.use('WebAgg')

app=Flask(__name__,static_url_path='/static')

if __name__ == "__main__":
    app.run(debug=True)


def FM_MAIN(x,inputs):
    [Am,Ac,fm,fc,message_signal,K] = inputs
    if(message_signal=="sin"):
      y= Ac*np.cos(2*np.pi*fc*x+(K*Am/fm)*np.sin(2*np.pi*fm*x))
      y1 = Am*np.sin(2*np.pi*fm*x)#message signal
    else:
      y= Ac*np.cos(2*np.pi*fc*x+(K*Am/fm)*np.sin(2*np.pi*fm*x))
      y1 = Am*np.cos(2*np.pi*fm*x)
    y2 = Ac*np.cos(2*np.pi*fc*x)#carrier signal need to change into scatterplot
        
    plot_graph(x = x, y = y, title = "Modulated wave", name="FM_modulated1.png")
    plot_graph(x = x, y = y1, title = "Message Signal", name="FM_message.png")
    plot_graph(x = x, y = y2, title = "Carrier Signal", name="FM_carrier.png")
    
    
def PHASE_MAIN(x,inputs):
    [Am,Ac,fm,fc,message_signal,K] = inputs
    if(message_signal=="sin"):
        y= Ac*np.cos(2*np.pi*fc*x+(K*Am)*np.cos(2*np.pi*fm*x))
        y1 = Am*np.sin(2*np.pi*fm*x)#message signal
    else:
        y= Ac*np.cos(2*np.pi*fc*x+(K*Am)*np.cos(2*np.pi*fm*x))
        y1 = Am*np.cos(2*np.pi*fm*x)       
    
    y2 = Ac*np.cos(2*np.pi*fc*x)#carrier signal need to change into scatterplot
        
    plot_graph(x = x, y = y, title = "Modulated wave", name="FM_modulated1.png")
    plot_graph(x = x, y = y1, title = "Message Signal", name="FM_message.png")
    plot_graph(x = x, y = y2, title = "Carrier Signal", name="FM_carrier.png")    
    


# ------- BASK - Binary Amplitude Shift Keying ---------
def BASK(Tb, fc, inputBinarySeq):

  t = np.arange(0, 1+Tb/100, Tb/100)
  c = np.sqrt(2/Tb)*np.sin(2*np.pi*fc*t)  # Equation for the carrier signal as a function of time

  # Generate the message signal
  # N = 8  # Set the number of data elements N
  # m = np.random.rand(N)
  # m = np.array([1,0,1,0,0,1,0])

  m = inputBinarySeq
  N = len(m)

  t1 = 0
  t2 = Tb

  for i in range(N):
      t = np.arange(t1, t2+0.01, 0.01)  # To obtain each data element, generate a random number m in [0,1]
      if m[i] > 0.5:  # If m > 0.5 assign value of m=1, else assign m=0
          m[i] = 1
          m_s = np.ones(len(t))
      else:
          m[i] = 0
          m_s = np.zeros(len(t))

      message = np.zeros((N, len(t)))
      message[i, :] = m_s

      # Product of carrier and message
      ask_sig = c * m_s  # The modulated signal is the product of the message signal level (dc level) and the carrier signal level (analog level)

      t1 = t1 + (Tb + 0.01)
      t2 = t2 + (Tb + 0.01)

      # Plotting the message signal
      plt.subplot(5, 1, 2)
      plt.axis([0, N, -2, 2])
      plt.plot(t, message[i, :], 'r')
      plt.title('message signal')
      plt.xlabel('t')
      plt.ylabel('m(t)')
      plt.grid(True)

      # Plotting the BASK signal (modulated signal)
      plt.subplot(5, 1, 4)
      plt.axis([0, N, -2, 2])
      plt.plot(t, ask_sig)
      plt.title('Amplitude Shift Keying')
      plt.xlabel('t --->')
      plt.ylabel('s(t)')
      plt.grid(True)


  # Save Message & Modulated Signal
  plt.savefig(f'static/results/BASK_msg_mod.png',bbox_inches='tight')
  plt.figure()

  # Plotting the carrier signal
  plt.figure()
  plt.subplot(5, 1, 3)
  plt.plot(t, c)
  plt.title('carrier signal')
  plt.xlabel('t')
  plt.ylabel('c(t)')
  plt.grid(True)
  plt.savefig(f'static/results/BASK_carrier.png',bbox_inches='tight') # Save
  plt.figure()
  # plt.show()

# ------- BFSK - Binary Frequency Shift Keying ----------
def BFSK(Tb, fc1, fc2 ,inputBinarySeq):

  # Binary Information
  x = inputBinarySeq.reshape(-1, 1)
  # bp = 0.000001  # bit period
  bp = Tb

  print(' Binary information at Transmitter :')
  print(x.T)

  # Representation of transmitting binary information as digital signal
  bit = np.array([])
  for n in range(len(x)):
      if x[n] == 1:
          se = np.ones(100)
      else:
          se = np.zeros(100)
      bit = np.concatenate((bit, se))

  t1 = np.arange(bp/100, 100*len(x)*(bp/100)+bp/100, bp/100)
  plt.subplot(3, 1, 1)
  plt.plot(t1, bit, 'b', linewidth=2.5)
  plt.grid(True)
  plt.axis([0, bp*len(x), -0.5, 1.5])
  plt.ylabel('Amplitude (V)')
  plt.xlabel('Time (s)')
  plt.title('Message signal')
  plt.grid(True)
  plt.savefig(f'static/results/BFSK_msg.png',bbox_inches='tight') # Save
  plt.figure()

  # Binary-FSK modulation
  A = np.sqrt(2/Tb)  # Amplitude of carrier signal
  br = 1/bp  # bit rate
  f1 = br*8  # carrier frequency for information as 1
  f2 = br*2  # carrier frequency for information as 0
  # f1 = fc1
  # f2 = fc2
  t2 = np.arange(bp/99, bp+bp/99, bp/99)
  m = np.array([])
  for i in range(len(x)):
      if x[i] == 1:
          y = A*np.cos(2*np.pi*f1*t2)
      else:
          y = A*np.cos(2*np.pi*f2*t2)
      m = np.concatenate((m, y))

  t3 = np.arange(bp/99, bp*len(x)+bp/99, bp/99)
  plt.subplot(3, 1, 2)
  plt.axis([0, bp*len(x), -A-5, A+5])
  plt.plot(t3, m, 'r')
  plt.grid(True)
  plt.xlabel('Time (s)')
  plt.ylabel('Amplitude (V)')
  plt.title('Modulated Wave')
  plt.grid(True)
  plt.savefig(f'static/results/BFSK_mod.png',bbox_inches='tight') # Save
  plt.figure()

# ------------- BPSK - Binary Phase Shift Keying ---------
def BPSK(Tb, fc ,inputBinarySeq):

  # x = np.array([1, 0, 0, 1, 1, 0, 1])  # Binary Information
  x = inputBinarySeq.reshape(-1, 1)
  # bp = 0.000001  # bit period
  bp = Tb

  print("Binary information at Transmitter:")
  print(x)

  # Transmitting binary information as digital signal
  bit = np.array([])
  for n in range(len(x)):
      if x[n] == 1:
          se = np.ones(100)
      else:
          se = np.zeros(100)
      bit = np.concatenate([bit, se])

  t1 = np.arange(bp/100, 100*len(x)*(bp/100)+bp/100, bp/100)
  plt.subplot(3, 1, 1)
  plt.plot(t1, bit, linewidth=2.5)
  plt.grid(True)
  plt.axis([0, bp*len(x), -0.5, 1.5])
  plt.ylabel('Amplitude(Volt)')
  plt.xlabel('Time(sec)')
  plt.title('Message Signal')
  plt.grid(True)
  plt.savefig(f'static/results/BPSK_msg.png',bbox_inches='tight') # Save
  plt.figure()

  # Binary-PSK modulation
  A = np.sqrt(2/Tb)  # Amplitude of carrier signal
  br = 1/bp  # bit rate
  f = br*2  # carrier frequency
  t2 = np.arange(bp/99, bp+bp/99, bp/99)
  ss = len(t2)
  m = np.array([])
  for i in range(len(x)):
      if x[i] == 1:
          y = A*np.cos(2*np.pi*f*t2)
      else:
          y = A*np.cos(2*np.pi*f*t2+np.pi)
      m = np.concatenate([m, y])

  t3 = np.arange(bp/99, bp*len(x)+bp/99, bp/99)
  plt.subplot(3, 1, 2)
  plt.plot(t3, m,'r')
  plt.axis([0, bp*len(x), -A-5, A+5])
  plt.xlabel('Time(sec)')
  plt.ylabel('Amplitude(Volt)')
  plt.title('Modulated Wave')
  plt.grid(True)
  plt.savefig(f'static/results/BPSK_mod.png',bbox_inches='tight') # Save
  plt.figure()


# ------- QPSK ---------------
def QPSK(Tb, fc, inputBinarySeq):
  t = np.linspace(0,1,100)  # Time

  c1 = np.sqrt(2/Tb)*np.cos(2*np.pi*fc*t)  # carrier frequency cosine wave
  c2 = np.sqrt(2/Tb)*np.sin(2*np.pi*fc*t)  # carrier frequency sine wave

  plt.subplot(3,1,2)
  plt.plot(t, c1)
  plt.xlabel('Time (Number of samples)')
  plt.ylabel('Cos Wave')
  plt.title('Carrier Wave 1 (Cosine)')
  plt.grid(True)
  plt.savefig(f'static/results/QPSK_carrier1.png',bbox_inches='tight') # Save
  plt.figure()

  plt.subplot(3,1,2)
  plt.plot(t, c2)
  plt.xlabel('Time (Number of samples)')
  plt.ylabel('Sine Wave')
  plt.title('Carrier Wave 2 (Sine)')
  plt.grid(True)
  plt.savefig(f'static/results/QPSK_carrier2.png',bbox_inches='tight') # Save
  plt.figure()


  m = inputBinarySeq.reshape(-1,1)
  t1 = 0
  t2 = Tb

  ## modulation
  odd_sig = np.zeros((len(m),100))
  even_sig = np.zeros((len(m),100))

  plt.subplot(3,1,2)
  for i in range(0,len(m),2):
      t = np.linspace(t1,t2,100)
      if (m[i]>0.5):
          m[i] = 1
          m_s = np.ones((1,len(t)))
      else:
          m[i] = 0
          m_s = (-1)*np.ones((1,len(t)))

      odd_sig[i,:] = c1*m_s

      if (m[i+1]>0.5):
          m[i+1] = 1
          m_s = np.ones((1,len(t)))
      else:
          m[i+1] = 0
          m_s = (-1)*np.ones((1,len(t)))

      even_sig[i,:] = c2*m_s

      qpsk = odd_sig + even_sig   # modulated wave = oddbits + evenbits

      plt.plot(t,qpsk[i,:])
      t1 = t1 + (Tb+0.01)
      t2 = t2 + (Tb+0.01)


  plt.title('Modulated Wave')
  plt.grid(True)
  plt.savefig(f'static/results/QPSK_mod.png',bbox_inches='tight') # Save
  
  # Message Signal
  plt.figure()
  plt.subplot(3,1,2)
  plt.stem(range(len(m)), m,use_line_collection=True)
  plt.ylabel('16 bits data')
  plt.title('Message signal (Binary)')
  plt.grid(True)
  plt.savefig(f'static/results/QPSK_msg.png',bbox_inches='tight') # Save
  plt.figure()


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


@app.route('/DM',methods=['GET'])
def DM_page():
    return render_template('Digital_Modulation.html')


# ---------- Digital Modulation ---------------------

@app.route('/DM/<dmtype>', methods=['GET','POST'])
def DigitalModulation(dmtype):
    
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

    return render_template('Digital_Modulation.html',dmtype=dmtype.upper())

# ------------ End of Digital Modulation -------------


if __name__ == "__main__":
    app.run(debug=True)
    
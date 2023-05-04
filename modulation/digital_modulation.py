# ------- BASK - Binary Amplitude Shift Keying ---------
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

def BASK(Tb, fc, inputBinarySeq):

  t = np.arange(0, 1+Tb/100, Tb/100)
  c = np.sqrt(2/Tb)*np.sin(2*np.pi*fc*t)  # Equation for the carrier signal as a function of time

  # Generate the message signal
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
  data = BytesIO()
  plt.savefig(data,format="png", bbox_inches='tight')
  data.seek(0)
  msg_mod = data.getvalue().hex()
  plt.figure()

  # Plotting the carrier signal
  plt.subplot(5, 1, 3)
  plt.plot(t, c)
  plt.title('carrier signal')
  plt.xlabel('t')
  plt.ylabel('c(t)')
  plt.grid(True)
  # Save
  data = BytesIO()
  plt.savefig(data,format="png",bbox_inches='tight' )
  data.seek(0)
  carrier = data.getvalue().hex()
  plt.figure()

  return [msg_mod, carrier]

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
  # Save
  data = BytesIO()
  plt.savefig(data,format="png",bbox_inches='tight' )
  data.seek(0)
  msg = data.getvalue().hex()
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

  # Plotting the carrier signal
  plt.subplot(5, 1, 3)
  plt.plot(t2, y)
  plt.title('carrier signal')
  plt.xlabel('t')
  plt.ylabel('c(t)')
  plt.grid(True)
  # Save
  data = BytesIO()
  plt.savefig(data,format="png",bbox_inches='tight' )
  data.seek(0)
  carrier = data.getvalue().hex()
  plt.figure()

  # Modulated Signal
  t3 = np.arange(bp/99, bp*len(x)+bp/99, bp/99)
  plt.subplot(3, 1, 2)
  plt.axis([0, bp*len(x), -A-5, A+5])
  plt.plot(t3, m, 'r')
  plt.grid(True)
  plt.xlabel('Time (s)')
  plt.ylabel('Amplitude (V)')
  plt.title('Modulated Wave')
  plt.grid(True)
  # Save
  data = BytesIO()
  plt.savefig(data,format="png",bbox_inches='tight' )
  data.seek(0)
  mod = data.getvalue().hex()
  plt.figure()

  return [msg,carrier, mod]

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
   # Save
  data = BytesIO()
  plt.savefig(data,format="png",bbox_inches='tight' )
  data.seek(0)
  msgSignal = data.getvalue().hex()
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

  # Plotting the carrier signal
  plt.subplot(5, 1, 3)
  plt.plot(t2, y)
  plt.title('carrier signal')
  plt.xlabel('t')
  plt.ylabel('c(t)')
  plt.grid(True)
  # Save
  data = BytesIO()
  plt.savefig(data,format="png",bbox_inches='tight' )
  data.seek(0)
  carrier = data.getvalue().hex()
  plt.figure()

  # Modulated
  t3 = np.arange(bp/99, bp*len(x)+bp/99, bp/99)
  plt.subplot(3, 1, 2)
  plt.plot(t3, m,'r')
  plt.axis([0, bp*len(x), -A-5, A+5])
  plt.xlabel('Time(sec)')
  plt.ylabel('Amplitude(Volt)')
  plt.title('Modulated Wave')
  plt.grid(True)
  # Save
  data = BytesIO()
  plt.savefig(data,format="png",bbox_inches='tight' )
  data.seek(0)
  modulatedSignal = data.getvalue().hex()
  plt.figure()

  return [msgSignal,carrier, modulatedSignal]


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
  # Save
  data = BytesIO()
  plt.savefig(data,format="png",bbox_inches='tight' )
  data.seek(0)
  carrier1 = data.getvalue().hex()
  plt.figure()

  plt.subplot(3,1,2)
  plt.plot(t, c2)
  plt.xlabel('Time (Number of samples)')
  plt.ylabel('Sine Wave')
  plt.title('Carrier Wave 2 (Sine)')
  plt.grid(True)
  # Save
  data = BytesIO()
  plt.savefig(data,format="png",bbox_inches='tight' )
  data.seek(0)
  carrier2 = data.getvalue().hex()
  plt.figure()


  m = inputBinarySeq.reshape(-1,1)
  t1 = 0
  t2 = Tb

  ## modulation
  odd_sig = np.zeros((len(m),100))
  even_sig = np.zeros((len(m),100))

  plt.subplot(3,1,2)
  for i in range(0,len(m)-1,2):
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
  # Save
  data = BytesIO()
  plt.savefig(data,format="png",bbox_inches='tight' )
  data.seek(0)
  modSignal = data.getvalue().hex()
  plt.figure()
  
  # Message Signal
  plt.figure()
  plt.subplot(3,1,2)
  plt.stem(range(len(m)), m,use_line_collection=True)
  plt.ylabel('16 bits data')
  plt.title('Message signal (Binary)')
  plt.grid(True)
  # Save
  data = BytesIO()
  plt.savefig(data,format="png",bbox_inches='tight' )
  data.seek(0)
  msgSignal = data.getvalue().hex()
  plt.figure()

  return [msgSignal, carrier1, carrier2, modSignal]


# ------- GMSK ---------------
def GMSK(fm, Am, phi_m, fc, Ac, phi_c):
    Tm = 1/fm
    Tc = 1/fc
    t = np.linspace(0, 2*Tm, 200)

    m = Am*np.sin(2*np.pi*fm*t + phi_m)
    c = Ac*np.sin(2*np.pi*fc*t + phi_c)

    bpsk = np.zeros(len(t))
    prev_bit = 0
    for i in range(len(t)):
        if m[i] > 0:
            if prev_bit == 0:
                bpsk[i] = np.pi
                prev_bit = 1
            else:
                bpsk[i] = 0
                prev_bit = 0
        else:
            bpsk[i] = bpsk[i-1]


    plt.figure(figsize=(10,6))

    plt.subplot(3,1,1)
    plt.plot(t, m, 'b-', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Message Signal')
    # Save
    data = BytesIO()
    plt.savefig(data,format="png",bbox_inches='tight' )
    data.seek(0)
    msgSignal = data.getvalue().hex()
    plt.figure()
    

    plt.subplot(3,1,2)
    plt.plot(t, c, 'r-', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Carrier Signal')
    # Save
    data = BytesIO()
    plt.savefig(data,format="png",bbox_inches='tight' )
    data.seek(0)
    carrierSignal = data.getvalue().hex()
    plt.figure()

    plt.subplot(3,1,3)
    plt.plot(t, Ac*np.sin(2*np.pi*fc*t+bpsk), 'g-', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('DPSK Modulated Signal')
    plt.tight_layout()
    # Save
    data = BytesIO()
    plt.savefig(data,format="png",bbox_inches='tight' )
    data.seek(0)
    modSignal = data.getvalue().hex()
    plt.figure()
    
    return [msgSignal, carrierSignal, modSignal]

import pandas
import numpy as np
import matplotlib.pyplot as plt

# function to plot FFT from a single dataset with different signals in different columns
def plot_FFT_va(data, preheader, param, paramcorr, paramunit, looplist, xlabel, ylabel, title, savename, xtextcorr, ytextcorr, dpi=600):
    plt.figure()
    for va in looplist:
        col_x = preheader +  " (" + param + "=" + str(va) + ") X"
        col_y = preheader +  " (" + param + "=" + str(va) + ") Y"
        plt.semilogx(data[col_x], data[col_y], label=param+ " = " + str(paramcorr*va)+ paramunit)
        #annotations
        max_y = data[col_y][1:].max()
        max_x = data[col_x][data[col_y][1:].idxmax()]
        # print(max_x, max_y)
        plt.annotate(f'{round(max_y, 2)}', 
                xy=(max_x, max_y), 
                xytext=(max_x + xtextcorr, max_y + ytextcorr),
                arrowprops=dict(facecolor='red', arrowstyle='->'))
        
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.savefig(savename, dpi = dpi)

# function to plot time domain signals
def plot_signal_va(data, preheader, param, paramcorr, paramunit, looplist, nsamples, xlabel, ylabel, title, savename, dpi=600):
    plt.figure()
    for va in looplist:
        col_x = preheader +  " (" + param + "=" + str(va) + ") X"
        col_y = preheader +  " (" + param + "=" + str(va) + ") Y"
        plt.plot(data[col_x][:nsamples], 
                 data[col_y][:nsamples], 
                 label=param+ " = " + str(paramcorr*va)+ paramunit)
        
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.savefig(savename, dpi = dpi)

# Amplitude variation wih fixed input frequency - error signal
plot_FFT_va(pandas.read_csv("Oct29_FFT_Ve.csv"), 
         "spectrum_ve", 
         "va",
         1000,
         "mV",
         [0.1, 0.05, 0.02],
         "Frequency (Hz)",
         "Voltage (dB)",
         "Error signal FFT - amplitude variation - fixed frequency.",
         "Plot_FFT_va_ve.png",
         500,
         0)
# Amplitude variation wih fixed input frequency - output code
plot_FFT_va(pandas.read_csv("Oct29_FFT_Out.csv"), 
         "spectrum_Out", 
         "va",
         1000,
         "mV",
         [0.1, 0.05, 0.02],
         "Frequency (Hz)",
         "Decimal Code (dB)",
         "Output FFT - amplitude variation - fixed frequency.",
         "Plot_FFT_va_Out.png",
         500,
         0)

# time domain plots of Input, Output and Error signals
nsamples = 2*round(200e3/683.0)
plot_signal_va(pandas.read_csv("Oct29_In.csv"), 
         "vin", 
         "va",
         1000,
         "mV",
         [0.1, 0.05, 0.02],
         nsamples,
         "Time (s)",
         "Signal (V)",
         "Input Signal - amplitude variation - fixed frequency.",
         "Plot_signal_va_In.png")
plot_signal_va(pandas.read_csv("Oct29_Ve.csv"),  
         "ve", 
         "va",
         1000,
         "mV",
         [0.1, 0.05, 0.02],
         nsamples,
         "Time (s)",
         "Signal (V)",
         "Error Signal - amplitude variation - fixed frequency.",
         "Plot_signal_va_Ve.png")
plot_signal_va(pandas.read_csv("Oct29_Out.csv"),  
         "Out", 
         "va",
         1000,
         "mV",
         [0.1, 0.05, 0.02],
         nsamples,
         "Time (s)",
         "Signal (Code)",
         "Output Signal - amplitude variation - fixed frequency.",
         "Plot_signal_va_Out.png")


# plotting the frequency variation measuremnts
data_341_sig = pandas.read_csv("Oct29_f_341.csv")
data_341_FFT = pandas.read_csv("Oct29_f_341_FFT.csv")
data_683_sig = pandas.read_csv("Oct29_f_683.csv")
data_683_FFT = pandas.read_csv("Oct29_f_683_FFT.csv")
data_1367_sig = pandas.read_csv("Oct29_f_1367.csv")
data_1367_FFT = pandas.read_csv("Oct29_f_1367_FFT.csv")

data_f_Out = pandas.DataFrame()
data_f_vin = pandas.DataFrame()
data_f_ve = pandas.DataFrame()
data_f_Out_FFT = pandas.DataFrame()
data_f_ve_FFT = pandas.DataFrame()

data_f_Out["Out (f=341.8) X"] = data_341_sig["Out X"]
data_f_Out["Out (f=341.8) Y"] = data_341_sig["Out Y"]
data_f_Out["Out (f=683.6) X"] = data_683_sig["Out X"]
data_f_Out["Out (f=683.6) Y"] = data_683_sig["Out Y"]
data_f_Out["Out (f=1367) X"] = data_1367_sig["Out X"]
data_f_Out["Out (f=1367) Y"] = data_1367_sig["Out Y"]

data_f_vin["vin (f=341.8) X"] = data_341_sig["vin X"]
data_f_vin["vin (f=341.8) Y"] = data_341_sig["vin Y"]
data_f_vin["vin (f=683.6) X"] = data_683_sig["vin X"]
data_f_vin["vin (f=683.6) Y"] = data_683_sig["vin Y"]
data_f_vin["vin (f=1367) X"] = data_1367_sig["vin X"]
data_f_vin["vin (f=1367) Y"] = data_1367_sig["vin Y"]

data_f_ve["ve (f=341.8) X"] = data_341_sig["ve X"]
data_f_ve["ve (f=341.8) Y"] = data_341_sig["ve Y"]
data_f_ve["ve (f=683.6) X"] = data_683_sig["ve X"]
data_f_ve["ve (f=683.6) Y"] = data_683_sig["ve Y"]
data_f_ve["ve (f=1367) X"] = data_1367_sig["ve X"]
data_f_ve["ve (f=1367) Y"] = data_1367_sig["ve Y"]

data_f_Out_FFT["spectrum_Out (f=341.8) X"] = data_341_FFT["spectrum_Out X"]
data_f_Out_FFT["spectrum_Out (f=341.8) Y"] = data_341_FFT["spectrum_Out Y"]
data_f_Out_FFT["spectrum_Out (f=683.6) X"] = data_683_FFT["spectrum_Out X"]
data_f_Out_FFT["spectrum_Out (f=683.6) Y"] = data_683_FFT["spectrum_Out Y"]
data_f_Out_FFT["spectrum_Out (f=1367) X"] = data_1367_FFT["spectrum_Out X"]
data_f_Out_FFT["spectrum_Out (f=1367) Y"] = data_1367_FFT["spectrum_Out Y"]

data_f_ve_FFT["spectrum_ve (f=341.8) X"] = data_341_FFT["spectrum_ve X"]
data_f_ve_FFT["spectrum_ve (f=341.8) Y"] = data_341_FFT["spectrum_ve Y"]
data_f_ve_FFT["spectrum_ve (f=683.6) X"] = data_683_FFT["spectrum_ve X"]
data_f_ve_FFT["spectrum_ve (f=683.6) Y"] = data_683_FFT["spectrum_ve Y"]
data_f_ve_FFT["spectrum_ve (f=1367) X"] = data_1367_FFT["spectrum_ve X"]
data_f_ve_FFT["spectrum_ve (f=1367) Y"] = data_1367_FFT["spectrum_ve Y"]

# Frequency variation with fixed amplitude FFT:
plot_FFT_va(data_f_Out_FFT, 
         "spectrum_Out", 
         "f",
         1,
         "Hz",
         [341.8, 683.6, 1367],
         "Frequency (Hz)",
         "Decimal Code (dB)",
         "Output signal FFT - frequency variation - fixed amplitude.",
         "Plot_FFT_f_Out.png",
         0,
         5)

plot_FFT_va(data_f_ve_FFT, 
         "spectrum_ve", 
         "f",
         1,
         "Hz",
         [341.8, 683.6, 1367],
         "Frequency (Hz)",
         "Decimal Code (dB)",
         "Error signal FFT - frequency variation - fixed amplitude.",
         "Plot_FFT_f_ve.png",
         0,
         -5)
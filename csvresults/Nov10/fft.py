import os
import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas
from scipy.fft import fft, fftfreq

# plt rc settings for fonts
plt.rc('text', usetex=True)
font = {'family' : 'serif',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)

def fft_measurements(
        data_fft, savefigname = "default.png",
        start_sample = 0, 
        num_cycles=11, 
        num_points=1024, 
        fsample=2e5, 
        fband=1e3):
       
    """Function to calculate FFT, plot it and save the measurement results."""

    # calculating resolution form minimum step change in samples
    data_delta = np.abs(np.diff(data_fft))
    adc_res = min( data_delta[np.where(data_delta > 0)] )

    #taking num_points samples from the given data and given start point
    samples = data_fft[start_sample: start_sample + num_points]
    fft_coef = fft(samples)

    # removing the DC and then taking the amplitude
    fft_absc = 2.0/num_points * np.abs(fft_coef[1:num_points//2])
    fft_dcbl = 20*np.log10(fft_absc)
    fft_freq = fftfreq(num_points, 1/fsample)[1:num_points//2]

    # fft plot
    plt.figure(figsize=(6,4))
    plt.semilogx(fft_freq, fft_dcbl, label = "FFT")
    plt.xlim(min(fft_freq), fsample/2)
    plt.ylim(min(fft_dcbl) - 10, max(fft_dcbl) + 10)
    plt.plot([min(fft_freq) - 10, fband], [min(fft_dcbl) - 10, min(fft_dcbl) - 10], linewidth=4, label = "Bandwidth")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("FFT Coefficients (dB)")
    plt.grid(True, which="both", ls="--", color='0.8')
    plt.legend()
    plt.tight_layout()
    plt.savefig(savefigname)
    

    # fundamental components and all noise
    fundm_freq = fft_freq[num_cycles - 1]
    signl_coef = fft_absc[num_cycles - 1]
    signl_powr = np.square(signl_coef)
    total_powr = np.sum(np.square(fft_absc))
    noise_powr = total_powr - signl_powr

    # inband measurements
    fft_ibcoff = fft_absc[fft_freq <= fband]
    # fft_ibfreq = fft_freq[fft_freq <= fband]
    total_powr_ib = np.sum(np.square(fft_ibcoff))
    noise_powr_ib = total_powr_ib - signl_powr
    snr_ibdcbl = 10*np.log10(signl_powr / noise_powr_ib)

    # measuremnts dictionary
    measurements = {
        "SignalFrequency" : fundm_freq,
        "SNR" : snr_ibdcbl,
        "SignalPowerdB" : 10*np.log10(signl_powr),
        "TotalNoisePowerdB" : 10*np.log10(noise_powr),
        "InbandNoisePowerdB" : 10*np.log10(noise_powr_ib),
        "ADC Resolution" : adc_res
    }

    return measurements

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FFT calculator and plotter.')
    parser.add_argument('-m', type=int, default=23, help='Number of input cycles.')
    parser.add_argument('-n', type=int, default=32768, help='Number of popints for FFT computation, 2**P.')
    parser.add_argument('-fs', type=float, default=2e5, help='Sampling frequency.')
    parser.add_argument('-fb', type=float, default=1e3, help='Input bandwidth.')
    parser.add_argument('-ss', type=int, default=200, help='Start sample to clip from the data.')
    parser.add_argument('-data', type=str, required=True, help='File name to read the samples from')
    parser.add_argument('-col', type=str, default='vout Y', help='Required column name of the output in the -data file.')

    args = parser.parse_args()

    root_dir = os.path.dirname(os.path.abspath(__file__))
    plot_dir = os.path.join(root_dir, 'Plots')
    os.makedirs(plot_dir, exist_ok=True)

    data = pandas.read_csv(os.path.join(root_dir, args.data))
    savename = os.path.join(plot_dir, args.data[:-4] + "_" + args.col.split()[0] + ".pdf")

    meas = fft_measurements(data_fft=data[args.col], 
                        savefigname=savename,
                        start_sample=args.ss,
                        num_cycles=args.m,
                        num_points=args.n,
                        fsample=args.fs,
                        fband=args.fb)
    
    print(meas)
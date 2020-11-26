import cmath as cmath
import numpy as np
import math as mt
from scipy import signal

def freq2erb(freq):
	erb = 9.265 * mt.log(1 + freq / (24.7 * 9.265))

	return erb

def erb2freq(erb):
	freq = 24.7 * 9.265 * (mt.exp(erb / 9.265) - 1)

	return freq

def gammatoneProcess(data, lowFreqHz, highFreqHz, nChannel, fs ):

	ERBs = np.linspace(freq2erb(lowFreqHz),freq2erb(highFreqHz),nChannel)

	centerFreq = np.zeros(128)
	for i in range(0, len(ERBs)):
		centerFreq[i] = erb2freq(ERBs[i])

	#default parameters
	n = 4
	bw = 1.018

	aParam = np.zeros((nChannel,5),dtype = "complex_")
	bParam = np.zeros((nChannel,1))
	for i in range(0, nChannel):
		b, a = gammatoneFilter(centerFreq[i],fs,n,bw)
		bParam[i] = b
		aParam[i,:] = a

	out = np.zeros((len(data),nChannel))
	for jj in range(0, nChannel):
		filterOut = signal.lfilter(bParam[jj], aParam[jj, :],data)
		out[:,jj] = 2*filterOut.real

	return out

def gammatoneFilter(cf,fs,n,bwERB):

	ERBHz = 24.7 + 0.108 * cf
	bwHz = bwERB * ERBHz

	btmp=1-mt.exp(-2*mt.pi*bwHz/fs)
	z = -complex(2*mt.pi*bwHz, 2*mt.pi*cf)/fs
	atmp=[1.+0.j, -cmath.exp(z)]

	b=1
	a=1

	for i in range(0,n):
		b = np.convolve(btmp, b)
		a = np.convolve(atmp, a)

	return b,a




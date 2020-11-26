from scipy import signal
import numpy as np
import math as mt

def applyWindow(data,win,windowLength,stepLength,nSamples,nFrames):

	start = 0
	finish = windowLength

	frames = np.zeros((windowLength,nFrames))

	for i in range(0, nFrames):
		frame = data[int(start):int(finish)]
		frames[:,i] = frame *win
		start = start + stepLength
		finish = finish + stepLength

	return frames

def ratemapProcess(data,windowDuration,stepDuration,fs,winName,decaySec,scaling):

	windowLength = 2*round(windowDuration*fs/2)
	stepLength = stepDuration*fs
	nSamples,nChannels = data.shape
	nFrames = mt.floor((nSamples-(windowLength-stepLength))/stepLength)
	win = signal.windows.get_window(winName,windowLength)
	out = np.zeros((nFrames,nChannels))
	decay = mt.exp(-(1/(fs * decaySec)))
	gain = 1 - decay
	data = signal.lfilter([gain], [1, -decay],data,0)

	out = np.zeros((nFrames,nChannels))
	for i in range(0,nChannels):
		frames = applyWindow(data[:,i],win, windowLength,stepLength, nSamples, nFrames)

		if scaling == 'magnitude':
			out[:,i] = np.mean(frames, axis=0)
		elif scaling == 'power':
			out[:,i] = np.mean(np.power(frames,2),axis=0)
		else:
			print('Method is not supported')


	return out



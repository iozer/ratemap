from scipy import signal
import numpy as np

class IHCparameters:
	def __init__(self, b, a, cascade, order):
		self.b = b
		self.a = a
		self.cascade = cascade
		self.order = order

def butterwFilter(fs, order, cutOffHz):

	b,a = signal.butter(order, cutOffHz/(0.5*fs),'low')

	return b, a


def getIHCparam(fs, method):

	if method == 'joergensen':
		b, a = butterwFilter(fs,1,150)
		p = IHCparameters(b,a,1,1)
		return p
	elif method == 'dau':
		b, a = butterwFilter(fs,2,1000)
		p = IHCparameters(b,a,1,2)
		return p
	elif method == 'breebart':
		b, a = butterwFilter(fs,1,2000)
		p = IHCparameters(b,a,5,1)
		return p
	elif method == 'bernstein':
		b, a = butterwFilter(fs,2,425)
		p = IHCparameters(b,a,1,2)
		return p
	else:
		return None

def ihcProcess(data, method,ihcp,nChannel):

	if method == 'none':
		return data;
	elif method == 'halfwave':
		return np.where(data<0,0,data)
	elif method == 'fullwave':
		return abs(data)
	elif method == 'square':
		return data*data
	elif method == 'hilbert':
		return abs(signal.hilbert(data,axis=0))
	elif method == 'dau':
		data = np.where(data<0,0,data)
		return filterProcess(ihcp,data)
	elif method == 'joergensen':
		return filterProcess(ihcp, abs(signal.hilbert(data,axis=0)))
	elif method == 'breebart':
		data = np.where(data<0,0,data)
		return filterProcess(ihcp, data)
	elif method == 'bernstein':
		nData = np.power(abs(signal.hilbert(data,axis=0)),-0.77)*data
		nData = np.where(nData<0,0,nData)
		env = np.power(nData,2)
		return filterProcess(ihcp,env)
	else:
		print('Method is not supported')

def filterProcess(ihcp,data):

	if ihcp.cascade == 1:
		out = signal.lfilter(ihcp.b,ihcp.a, data,0)
	else:
		out=data
		for i in range(0,ihcp.cascade):
			out = signal.lfilter(ihcp.b,ihcp.a,out,0)

	return out

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

def ihcProcess(data, method,ihcp,nChannel,fs):

	if method == 'none':
		return data;
	elif method == 'halfwave':
		return np.where(data<0,0,data)
	elif method == 'fullwave':
		return abs(data)
	elif method == 'square':
		return data*data
	elif method == 'meddis':
		return meddis(data,fs)
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

def meddis(data,fs):
    
    numChan, sigLength = data.shape
    # hair cell parameters
    med_y=5.05;
    med_g=2000;
    med_l=2500;
    med_r=6580;
    med_x=66.31;
    med_a=3.0;
    med_b=200;
    med_h=48000;
    med_m=1;
    
    # initialize inner hair cells
    ymdt=med_y*med_m/fs;
    xdt=med_x/fs;
    ydt=med_y/fs;
    lplusrdt=(med_l+med_r)/fs;
    rdt=med_r/fs;
    gdt=med_g/fs;
    hdt=med_h;
    
    out = np.zeros((numChan, sigLength))
    for i in range(0,numChan):
        kt=med_g*med_a/(med_a+med_b);
        hair_c=med_m*med_y*kt/(med_l*kt+med_y*(med_l+med_r));
        hair_q=hair_c*(med_l+med_r)/kt;
        hair_w=hair_c*med_r/med_x;
        
        for j in range(0, sigLength):
            if (data[i,j] + med_a) >0:
                kt=gdt*(data[i,j]+med_a)/(data[i,j]+med_a+med_b);
            else:
                kt=0;
            if hair_q<med_m:
                replenish=ymdt-ydt*hair_q;
            else:
                replenish=0;
            eject=kt*hair_q;
            reuptakeandloss=lplusrdt*hair_c;
            reuptake=rdt*hair_c;
            reprocess=xdt*hair_w;
            hair_q=max(hair_q+replenish-eject+reprocess,0);
            hair_c=max(hair_c+eject-reuptakeandloss,0);
            hair_w=max(hair_w+reuptake-reprocess,0);
            out[i,j]=hair_c*hdt;
    return out
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 02:02:56 2020

@author: iozer
"""

import scipy.io.wavfile as wav
from scipy import signal
import numpy as np
from PIL import Image
import gammatoneProcess as gp
import ratemapProcess as rp
import ihcProcess as ip
import os
import uuid

iteratedFiles = []
np.random.seed(87)
data_folder = 'C:/Users/USTA/PycharmProjects/IHRC-Study/Datasets/emo-db/all/'


def pre_emphasis(data, p_factor):
	out = signal.lfilter([1, -p_factor], 1, data)
	return out


for root, dirs, files in os.walk(data_folder):
	for file in files:
		if file.endswith('.wav'):
			file = os.path.join(root, file)
			iteratedFiles.append(file)

for i in iteratedFiles:
	fs, data = wav.read(i)

	rawDataOutput = pre_emphasis(data, 0.97)
	gpDataOutput = gp.gammatoneProcess(rawDataOutput, 50, 20000, 128, fs)

	ihcMethod = 'dau'
	ihcp = ip.getIHCparam(fs, ihcMethod)
	ihcpDataOutput = ip.ihcProcess(gpDataOutput, ihcMethod, ihcp, 128, fs)

	rpDataOutput = rp.ratemapProcess(ihcpDataOutput, 0.01, 0.004, fs, 'hamming', 8E-3, 'power')

	img = Image.fromarray(rpDataOutput, 'RGB')
	unique_filename = str(uuid.uuid4())
	img.save(unique_filename + ".bmp")

if __name__ == 'preEmphasis':
	pre_emphasis()

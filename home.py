from scipy import signal
from scripts import gammatoneProcess as gp
from scripts import ratemapProcess as rp
from scripts import ihcProcess as ip

import matplotlib.pyplot as plt
import pathlib
import scipy.io.wavfile as wav
import uuid
import os
import shutil

desired_width = 256
data_folder = r"C:\Users\USTA\PycharmProjects\IHRC-Study\Datasets\emo-db\all"
image_folder = r"C:\Users\USTA\Desktop\darasets"

folderNamesList = ['a', 'L', 'n', 'w', 'f', 't', 'e']

shutil.rmtree(image_folder, ignore_errors=True, onerror=None)

os.mkdir(image_folder)

os.chdir(image_folder)

for i in folderNamesList:
	os.mkdir(i)


def pre_emphasis(data, p_factor):
	out = signal.lfilter([1, -p_factor], 1, data)
	return out


for root, dirs, files in os.walk(data_folder):
	for file in files:
		if file.endswith('.wav'):
			file = pathlib.PureWindowsPath(root, file).as_posix()
			x = os.path.basename(os.path.dirname(file))
			# print(os.path.basename(file))

			fs, data = wav.read(file)

			rawDataOutput = pre_emphasis(data, 0.97)

			gpDataOutput = gp.gammatoneProcess(rawDataOutput, 50, 10000, desired_width, fs)

			ihcMethod = 'hilbert'
			ihcp = ip.getIHCparam(fs, ihcMethod)
			ihcpDataOutput = ip.ihcProcess(gpDataOutput, ihcMethod, ihcp, desired_width)

			rpDataOutput = rp.ratemapProcess(ihcpDataOutput, 0.01, 0.004, fs, 'hamming', 8E-3, 'magnitude')

			cmap = plt.cm.jet

			unique_filename = str(uuid.uuid4())
			save_image_path = pathlib.PureWindowsPath(image_folder, x, unique_filename + '.bmp').as_posix()
			print(save_image_path)

			plt.imsave(save_image_path, rpDataOutput, cmap=cmap)

if __name__ == 'preEmphasis':
	pre_emphasis()

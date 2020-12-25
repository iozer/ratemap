from scipy import signal
from PIL import Image, ImageOps
from scripts import gammatoneProcess as gp
from scripts import ratemapProcess as rp
from scripts import ihcProcess as ip

import matplotlib.pyplot as plt
import pathlib
import scipy.io.wavfile as wav
import numpy as np
import uuid
import os
import shutil

np.random.seed(265)
desired_width,desired_height = 256,500

data_folder = ""
image_folder = ""

#image_resized_margin_folder = ""
#output_path = ""

folderNamesList = ['a','L','n','w','f','t','e']

# In[2]:

shutil.rmtree(image_folder,ignore_errors=True,onerror=None)
#shutil.rmtree(image_resized_margin_folder,ignore_errors=True,onerror=None)
#shutil.rmtree(output_path,ignore_errors=True,onerror=None)

#os.mkdir(output_path)
#os.mkdir(image_resized_margin_folder)
#os.mkdir(image_folder)

os.chdir(image_folder)

for i in folderNamesList:
	os.mkdir(i)

#os.chdir(image_resized_margin_folder)

#for i in folderNamesList:
#   os.mkdir(i)

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
			save_image_path = pathlib.PureWindowsPath(image_folder, x, unique_filename + '.png').as_posix()
			print(save_image_path)

			plt.imsave(save_image_path,rpDataOutput,cmap=cmap)



# In[ ]:


"""
for root, dirs, files in os.walk(image_folder):
	for file in files:
		if file.endswith('.png'):
	  
			file = pathlib.PureWindowsPath(root, file).as_posix()
			x = os.path.basename(os.path.dirname(file))
			im = Image.open(file)

			def add_margin(pil_img, color):
				width, height = im.size
				y = desired_height - height
				new_height = height + y
				result = Image.new(pil_img.mode, (width, new_height), color)
				result.paste(pil_img, (0, 0))
				return result

			im_new = add_margin(im, (0, 0, 0))

			unique_filename = str(uuid.uuid4())
			save_image_path = pathlib.PureWindowsPath(image_resized_margin_folder, x, unique_filename + '.png').as_posix()

			im_new.save(fp=save_image_path, format="PNG")
"""


# In[ ]:
"""
for root, dirs, files in os.walk(image_folder):
	for file in files:
		if file.endswith('.png'):

			file = pathlib.PureWindowsPath(root, file).as_posix()
			x = os.path.basename(os.path.dirname(file))
			im = Image.open(file)

			im_new = im.resize((desired_width,desired_height))

			unique_filename = str(uuid.uuid4())
			save_image_path = pathlib.PureWindowsPath(image_resized_margin_folder, x, unique_filename + '.png').as_posix()

			im_new.save(fp=save_image_path, format="PNG")


# In[ ]:

splitfolders.ratio(image_resized_margin_folder, output=output_path, seed=265, ratio=(.9,.1), group_prefix=None)
"""
if __name__ == 'preEmphasis':
	pre_emphasis()

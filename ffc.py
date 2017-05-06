import cv2
from glob import glob
import numpy as np
import os
import sys

'''README - Instructions

1. The program must be run as python 'DIR_SUP' 'color', where 'color' is the color chosen for segmentation (either green or red).
The DIR_SUP is the directory where the time directories are located, i.e. the 
ones with the format m-s-f (minutes, seconds, thousandths). It must satisfy the following
   a. THE DIR_SUP name MUST CONTAIN THE FINAL / .
   b. IT MUST ONLY HAVE THE TIME DIRECTORIES INSIDE IT, It can contains other files but no other directories.
2. The color parameter is not mandatory, if it is not included, the color is set to DEFAULT_COLOR.

Settings:
    1. Declare the DEFAULT_COLOR as green or red.
    2. DECLARE CONSTANTS: Define the desired kernel, scaling factor s, the patterns for each channel, the directory and filenames of the corrections.
'''

# SET HERE THE DIRECTORY FOR THE CORRECTIONS AND THEIR FILENAMES, ALWAYS USE FINAL / FOR DIRECTORIES
dir_corrections = '/home/gutiloluis/Dropbox/71macs/71macs_small_scripts_and_image_corrections/corrections/'

#AVG_DARK_GFP
fname_AVG_Dark = 'AVG_Dark.tif'
#AVG_DARK_RFP
fname_AVG_DarkRed = 'AVG_DARK_RFP.tif'
fname_AVG_TotalGreen = 'AVG_GFP.tif'
fname_AVG_TotalRed = 'AVG_RFP.tif'

# SET HERE THE DEFAULT COLOR FOR THE SEGMENTATION CHANNEL.
DEFAULT_COLOR = 'green'
argc = len(sys.argv)

# Input reading and error handling
if not(argc == 2 or argc == 3):
    print("Enter the correct number of parameters.\nThe program must be run as python 'experiment directory' 'color', where 'color' is the color chosen for segmentation (either green or red)")
    exit()
else:
    dir_sup = sys.argv[1]
    if not dir_sup.endswith('/'):
        print("The directory must contain the final /")
        exit()
    if argc == 3:
        color = sys.argv[2]
        if not(color == 'red' or color == 'green'):
            print('Invalid color, it must be either red or green')
            exit()
    elif argc == 2:
        color = DEFAULT_COLOR

print("Starting FFC, color set as", color)

'''Declare constants'''
###### Para acentuar mas contundentemente el -1 cambiarlo por un numero de mayor valor absoluto o ponerla mas grande.
###### Intentar con una 6x6 o 7x7.
kernel = np.array([[-1,-1,-1,-1,-1],
                   [-1, 2, 2, 2,-1],
                   [-1, 2, 8, 2,-1],
                   [-1, 2, 2, 2,-1],
                   [-1,-1,-1,-1,-1]]) / 8.0

s = 1.0
pattern_seg = '*c1.tif'
pattern_rfp = '*c2.tif'
pattern_gfp = '*c3.tif'

'''Import corrections as images'''
cor_dark_gfp = cv2.imread(dir_corrections+fname_AVG_Dark, -1)
cor_dark_rfp = cv2.imread(dir_corrections+fname_AVG_DarkRed, -1)
cor_rfp = cv2.imread(dir_corrections+fname_AVG_TotalRed, -1)
cor_gfp = cv2.imread(dir_corrections+fname_AVG_TotalGreen, -1)

def list_files(dir_img, pattern):
    '''Return a list of files inside dir_img whose names has the pattern
    Args:
        dir_img (str): The directory in which the files are listed.
        pattern (str): The pattern of the files that are added to the list.
    Returns:
        list: The list containing the filenames
    '''
    img_fnames = []
    for dire,_,_ in os.walk(dir_img):
        img_fnames.extend(glob(os.path.join(dire, pattern)))
    img_fnames.sort()
    return img_fnames

def flat_field_correction(fname_img, cor_dark, cor_fluor, s = 1.0):
    '''Performs the flat field corrections over img
    Args:
        img (numpy.ndarray): The image to be corrected.
        cor_dark (numpy.ndarray): The dark correction image.
        cor_fluor (numpy.ndarray): The fluorescence correction image.
        s (num): Scaling factor. Default 1.0.
    Returns:
        numpy.ndarray: The corrected image.
    '''
    img = cv2.imread(fname_img, -1)
    img_cor = np.zeros_like(img)
    maxi = np.amax(cor_fluor)
    for i in range(len(img)):
        for j in range(len(img[0])):
            if(img[i,j] > cor_dark[i,j]):
                tmp = maxi * ( img[i,j] - cor_dark[i,j] ) / cor_fluor[i,j]
                img_cor[i,j] = s * tmp
    return img_cor

def list_directories(directory):
    '''Returns a list unhidden of directory filenames inside the directory.
    Args:
        directory (str): The directory containing the subdirectories to list.
    Returns:
        list: The list containing the directories.
    '''
    dir_names = [dir for root, dirs, files in os.walk(directory) for dir in dirs if not dir.startswith('.')]
    dir_names.sort()
    return dir_names

def correction_single_dir(dir_img, dir_img_cor):
    '''Makes the corrections of flat field and kernel for the specified (time) directory.
    Args:
        dir_img (str): Directory name where the images are located. PUT THE FINAL /
        dir_img_cor (str): Directory name where the corrected images will be located. PUT THE FINAL /
    '''
    fnames_seg = list_files(dir_img, pattern_seg)
    fnames_rfp = list_files(dir_img, pattern_rfp)
    fnames_gfp = list_files(dir_img, pattern_gfp)
    
    if not os.path.exists(dir_img_cor):
        os.makedirs(dir_img_cor)
    
    for fname_img in fnames_seg:
        
        if color == 'green':
            img_pre_cor = flat_field_correction(fname_img, cor_dark_gfp, cor_gfp, s)
        else:
            img_pre_cor = flat_field_correction(fname_img, cor_dark_rfp, cor_rfp, s)

        img_cor = cv2.filter2D(img_pre_cor, -1, kernel) 
        fname_cor = dir_img_cor + fname_img.split('/')[-1]
        cv2.imwrite(fname_cor, img_cor)
        
    
    for fname_img in fnames_rfp:
        
        img_cor = flat_field_correction(fname_img, cor_dark_rfp, cor_rfp, s)

        fname_cor = dir_img_cor + fname_img.split('/')[-1]
        cv2.imwrite(fname_cor, img_cor)
        
    
    for fname_img in fnames_gfp:
        
        img_cor = flat_field_correction(fname_img, cor_dark_gfp, cor_gfp, s)

        fname_cor = dir_img_cor + fname_img.split('/')[-1]
        cv2.imwrite(fname_cor, img_cor)
        
def image_corrections(dir_sup):
    '''Makes the corrections of flat field and kernel for the specified superior directory. The corrected
     images are stored in a directory with the same prefix as dir_sup but endind in _COR/
    Args:
        dir_sup (str): Name of the directory where the subdirectories with images are located i.e. inside
        it there are located the folders whose names are of the form m-s-f.
            dir_sup MUST HAVE THE FINAL /
            the subdirectories inside dir_sup MUST ONLY BE THE ONES WITH THE IMAGES (FORMAT m-s-f).
    '''
    if color == 'green':
        dir_sup_cor = dir_sup[:-1]+'_COR_green/'
    else:
	    dir_sup_cor = dir_sup[:-1]+'_COR_red/'

    if not os.path.exists(dir_sup_cor):
        os.makedirs(dir_sup_cor)

    dir_names = list_directories(dir_sup)

    for dir_name in dir_names:
        dir_img = dir_sup + dir_name + '/'
        dir_img_cor = dir_sup_cor + dir_name + '/'
        correction_single_dir(dir_img, dir_img_cor)
        
        print("Directory ", dir_name, " done")
    
    print("Corrections done")

image_corrections(dir_sup)



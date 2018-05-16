from matplotlib import pyplot as plt
from matplotlib import colors as colors
import numpy as np

import random

def read_im(fn):
    #Transform an image file into a matrice
    img = np.array(plt.imread(fn))
    return img

def convert_rgb_to_hsv(img):
    return colors.rgb_to_hsv(img)

def display_im(im):
    #Display a matrice im from an image
    plt.figure(figsize=(12, 8))
    plt.imshow(im)
    plt.show

def get_patch(i,j,h,im):
    #todo: gérer les bords, actuellement renvoi rien pour un bord
    
    #return a patch of size h centered on i,j from a matrice im 
    
    #print("i : ", i)
    #print("j : ", j)
    #print("h : ", h)
    #print("De ", (i-h//2), " à ", i+h//2)
    if(h%2 == 0):
        return im[(i-h//2):(i+h//2), (j-h//2):(j+h//2)]
    else:
        return im[(i-h//2):(i+h//2)+1, (j-h//2):(j+h//2)+1]

def convert_patch_into_vectors(patch):
    pass

def flatpixel_to_2d(flatpixel, width): 
    x = flatpixel%width
    y = int((flatpixel - (flatpixel%width))/width)
    return (x,y)
    
#return flatimg and pixels of noise_pixels in 2d
def noise(img,prc,width,height):
    #Noise a prc percent of the image img 
    flatimg = img.reshape(-1, img.shape[-1])
    randnoise = random.sample(range(0, len(flatimg)), int(len(flatimg)*prc))
    for i in randnoise:
        flatimg[i] = np.array([0,0,0])
    return (flatimg.reshape([img.shape[0], img.shape[1], 3]), np.array([flatpixel_to_2d(x,width) for x in randnoise]))

    
def delete_rect(img,i,j,height, width):
    #Delete a rectangle of an image centered on i, j and size height and width
    img[(i-height//2):(i+height//2), (j-width//2):(j+width//2)] = np.zeros((height, width, 3))
    return img

def check_if_noisy_patch(patch):
    #Check if there is at least a noisy pixel in a patch
    for x in patch:
        for y in x:
            if(np.array_equal(y, np.array([0, 0, 0]))):
                return True
    return False
    
def get_patches(img, h, height, width):
    #Return a tuple wich contains the noisy patches and the clean patches (without noisy pixel)
    noisy_patches = []
    clean_patches = []
    
    for i_height in range(h//2, height-h//2):
        for j_width in range(h//2, width-h//2):
            patch = get_patch(i_height, j_width, h, img)
            if(check_if_noisy_patch(patch)):
                noisy_patches.append(patch)
            else:
                clean_patches.append(patch)
                
    return (noisy_patches, clean_patches)

def generate_patch():
    pass

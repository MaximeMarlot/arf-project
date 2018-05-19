from matplotlib import pyplot as plt
from matplotlib import colors as colors
import numpy as np

import random

def read_im(fn):
    #Transform an image file into a matrice
    img = np.array(plt.imread(fn))
    #we force to a real array, otherwise [-1,-1,-1] is automatically changed to [255,255,255]
    data = np.asarray( img, dtype="int32" )
    return data

def convert_rgb_to_hsv(img):
    return colors.rgb_to_hsv(img)

#Display a matrice im from an image    
def display_im(im):
    im2=np.array(im)   
    width = im2.shape[0]
    height = im2.shape[1]
    #convert noisy pixel to a selected color
    im2=im2.reshape(-1, im2.shape[-1]) #flatten all but last dimension
    im2[np.equal(im2, np.array([-1,-1,-1]))] = 0 # 0 = black
    im2 = np.array(im2.reshape(width,height,3))
    #end convert
   
    #convert to  a [0-255] img
    im2 = np.array(im2)
    im2 = im2.astype(np.uint8)

    plt.figure(figsize=(12, 8))
    plt.imshow(im2, interpolation='nearest')
    plt.show
    
#return a patch of size h centered on i,j from a matrice im 
def get_patch(i,j,h,im):
    #todo: gérer les bords, actuellement renvoi rien pour un bord

    if(h%2 == 0):
        return im[(i-h//2):(i+h//2), (j-h//2):(j+h//2)]
    else:
        return im[(i-h//2):(i+h//2)+1, (j-h//2):(j+h//2)+1]

def flatpixel_to_2d(flatpixel, width): 
    x = flatpixel%width
    y = int((flatpixel - (flatpixel%width))/width)
    return (x,y)
    

#return flatimg and pixels of noise_pixels in 2d
def noise(img_,prc,width,height, h):
    img=np.array(img_)
    #Noise a prc percent of the image img 
    flatimg = img.reshape(-1, img.shape[-1])
    flatimg = np.asarray(flatimg)
    randnoise = random.sample(range(0, len(flatimg)), int(len(flatimg)*prc))
    noised_pixels = []
    for pixeli in randnoise:
        i,j = flatpixel_to_2d(pixeli,width)
        #test si c'est sur un bord on fait rien
        if((i-h >= 0) and (j-h >= 0) and (i+h+1 <= width) and (j+h+1 <= height)):
            #sinon on met du noise
            flatimg[pixeli] = np.array([-1,-1,-1])  #pixel bruité
            noised_pixels.append(flatpixel_to_2d(pixeli,width))
        else:
            #TODO gérer les bordures au lieu de juste les supprimer ?
            pass
    return (flatimg.reshape([img.shape[0], img.shape[1], 3]), np.array(noised_pixels))

    
def delete_rect(img,i,j, width, height):
    #Delete a rectangle of an image centered on i, j and size height and width
    img[(i-height//2):(i+height//2)+1, (j-width//2):(j+width//2)+1] = np.zeros((height, width, 3))
    #todo optimiser sans boucles
    deletepixels = []
    for pixeli in range((i-height//2), (i+height//2)+1):
        for pixelj in range((j-width//2), (j+width//2)+1):
            deletepixels.append([pixeli, pixelj])
    
    return (img, deletepixels)

def get_centered_pixel(patch, h):
    patch2 = patch.flatten()
    vector = patch2[((len(patch2)//2)-1):((len(patch2)//2)-1)+3]
    return [int(x) for x in vector]

#testé ok
def check_if_noisy_patch(patch, h):
    centerpixel = get_centered_pixel(patch, h) 
    #Check if center pixel is noisy in a patch
    if(np.array_equal(centerpixel, np.array([-1,-1,-1]))):
        return True
    return False

#version quadrillage
def get_patches(img, h, width, height):
    #Return a tuple wich contains the noisy patches and the clean patches (without noisy pixel)
    noisy_patches = []
    clean_patches = []
    for i_height in range(h//2, height-h//2,h):
        for j_width in range(h//2, width-h//2,h):
            patch = get_patch(i_height, j_width, h, img)
            if(check_if_noisy_patch(patch,h)):
                noisy_patches.append(patch)
            else:
                clean_patches.append(patch)
                
    return (noisy_patches, clean_patches)

#version sans quadrillage #TODO recoder plus propre ?
def get_all_patches(img, h,width, height):
    #Return a tuple wich contains the noisy patches and the clean patches (without noisy pixel)
    noisy_patches = []
    clean_patches = []
    for i_height in range(h//2, height-h//2):
        for j_width in range(h//2, width-h//2):
            patch = get_patch(i_height, j_width, h, img)
            if(check_if_noisy_patch(patch,h)):
                noisy_patches.append(patch)
            else:
                clean_patches.append(patch)
                
    return (noisy_patches, clean_patches)

def generate_patch():
    pass

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
    plt.imshow(im, interpolation='nearest')
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
    
#fonction qui gère les bordures (auquel cas les patchs ne sont pas centrés)
def get_noisy_patch(i,j,h,im):
    width = im.shape[0]
    height = im.shape[1]
    
    #todo gérer coins
    
    #bordure gauche
        
    #bordure droite
    
    #bordure haute
    
    #bordure bas
        
    #point normal
    return get_patch(i,j,h,im)
    

def convert_patch_into_vectors(patch):
    pass

def flatpixel_to_2d(flatpixel, width): 
    x = flatpixel%width
    y = int((flatpixel - (flatpixel%width))/width)
    return (x,y)
    

#return flatimg and pixels of noise_pixels in 2d
def noise(img,prc,width,height, h):
    #Noise a prc percent of the image img 
    flatimg = img.reshape(-1, img.shape[-1])
    randnoise = random.sample(range(0, len(flatimg)), int(len(flatimg)*prc))
    noised_pixels = []
    for pixeli in randnoise:
        i,j = flatpixel_to_2d(pixeli,width)
        #test si c'est sur un bord on fait rien
        if((i-h >= 0) and (j-h >= 0) and (i+h+1 <= width) and (j+h+1 <= height)):
            #sinon on met du noise
            flatimg[pixeli] = np.array([0,0,0])  #noir
            #flatimg[pixeli] = np.array([255,255,255]) #blanc
            noised_pixels.append(flatpixel_to_2d(pixeli,width))
        else:
            print("pixel ", i, " ",j, "=(",pixeli,") is on border")
            pass
    return (flatimg.reshape([img.shape[0], img.shape[1], 3]), np.array(noised_pixels))

    
def delete_rect(img,i,j, width, height):
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

#version quadrillage
def get_patches(img, h, width, height):
    #Return a tuple wich contains the noisy patches and the clean patches (without noisy pixel)
    noisy_patches = []
    clean_patches = []
    
    for i_height in range(h//2, height-h//2,h):
        for j_width in range(h//2, width-h//2,h):
            patch = get_patch(i_height, j_width, h, img)
            if(check_if_noisy_patch(patch)):
                noisy_patches.append(patch)
            else:
                clean_patches.append(patch)
                
    return (noisy_patches, clean_patches)

#version sans quadrillage
def get_all_patches(img, h,width, height):
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

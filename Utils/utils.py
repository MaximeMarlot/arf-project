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
    
#extends an image by h pixels on all edges by mirroring on the edges
def extend_image(im, h):
    width  = im.shape[1]
    height = im.shape[0]
    newim = np.zeros((height+h*2, width+h*2, 3))
    #print("origimg shape:", im.shape)
    #print("newimg shape: ", newimg.shape)
    
    #copy original image in center
    newim[h:height+h, h:width+h] = im
    
    #extract borders to paste
    topborder    = np.array(im[0:h,:])
    bottomborder = np.array(im[height-h:height,:])
    
    #on retourne en mirroir
    topborder    = np.flipud(topborder)
    bottomborder = np.flipud(bottomborder)
    
    #put all noised pixel to -2 so we don't try to correct these
    topborder[topborder == -1] = -2   
    bottomborder[bottomborder == -1] = -2
    
    #on ajoute les bordures sur l'image étendue
    newim[0:h, h:width+h] = topborder
    newim[height+h:height+h*2, h:width+h] = bottomborder
    
    #similaire pour gauche et droite
    leftborder   = np.array(newim[:,h:h*2])
    rightborder  = np.array(newim[:,width:width+h])
    
    leftborder   = np.fliplr(leftborder)
    rightborder  = np.fliplr(rightborder)
    
    leftborder[leftborder == -1] = -2 
    rightborder[rightborder == -1] = -2
    
    newim[:, 0:h] = leftborder
    newim[:, height+h:height+h*2] = rightborder
    
    return newim;
    
#return a patch of size h centered on i,j from a matrice im 
#old version without extand_image()
def get_patch(i,j,h,im):  
    if(h%2 == 0):
        print("get_patch() ERROR : le patch doit etre de taille impaire")
    else:
        return im[(i-h//2):(i+h//2)+1, (j-h//2):(j+h//2)+1] 
    
#return a patch of size h centered on i,j from a matrice im 
#new version 
def get_patch2(i,j,h,im):
    #on étend l'image pour gérer les bords
    im2 = extend_image(im, h)
    i2=i+h
    j2=j+h
    if(h%2 == 0):
        print("get_patch() ERROR : le patch doit etre de taille impaire")
    else:
        return im2[(i2-h//2):(i2+h//2)+1, (j2-h//2):(j2+h//2)+1] 

def flatpixel_to_2d(flatpixel, width): 
    x = flatpixel%width
    y = int((flatpixel - (flatpixel%width))/width)
    return [x,y]
    

#return flatimg and pixels of noise_pixels in 2d
#noise() ne met pas de noise sur les bordures
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
            x,y = flatpixel_to_2d(pixeli,width)
            noised_pixels.append([x,y]) 
        else:
            #TODO gérer les bordures au lieu de juste les supprimer ?
            pass
    return (flatimg.reshape([img.shape[0], img.shape[1], 3]), np.array(noised_pixels))

#noise2 met du noise sur les bordures
def noise2(img_,prc,width,height, h):
    img=np.array(img_)
    #Noise a prc percent of the image img 
    flatimg = img.reshape(-1, img.shape[-1])
    flatimg = np.asarray(flatimg)
    lenimg = len(flatimg)-1
    randnoise = random.sample(range(0, lenimg), int(lenimg*prc))
    noised_pixels = []
    for pixeli in randnoise:
        i,j = flatpixel_to_2d(pixeli,width)
        #sinon on met du noise
        flatimg[pixeli] = np.array([-1,-1,-1])  #pixel bruité
        x,y = flatpixel_to_2d(pixeli,width)
        noised_pixels.append([x,y]) 
    return (flatimg.reshape([img.shape[0], img.shape[1], 3]), np.array(noised_pixels))

# i,j = first pixel (top left corner)
def delete_rect(img,i,j, width, height):
    #Delete a rectangle of an image centered on i, j and size height and width
    #img[(i-height//2):(i+height//2)+1, (j-width//2):(j+width//2)+1] = np.zeros((height, width, 3))
    #todo optimiser sans boucles
    deletepixels = []
    for pixeli in range(i, i+height):
        tmp = []
        for pixelj in range(j, j+width):
            img[pixeli, pixelj] = np.array([-1,-1,-1])
            tmp.append([pixeli, pixelj])
        deletepixels.append(tmp)
    return (img, deletepixels)
    
#i,j = centerpixel but maybe bugs ?
def delete_rect_centered(img,i,j, width, height):
    #Delete a rectangle of an image centered on i, j and size height and width
    #img[(i-height//2):(i+height//2)+1, (j-width//2):(j+width//2)+1] = np.zeros((height, width, 3))
    #todo optimiser sans boucles
    deletepixels = []
    for pixeli in range((i-height//2), (i+height//2)+1):
        tmp = []
        for pixelj in range((j-width//2), (j+width//2)+1):
            img[pixeli, pixelj] = np.array([-1,-1,-1])
            tmp.append([pixeli, pixelj])
        deletepixels.append(tmp)
    return (img, deletepixels)

def get_centered_pixel(patch, h):
    patch2 = patch.flatten()
    length = patch2.shape[0]
    thirddim = int((length-h*h)/(h*h)+1)
    patch2 = patch2.reshape(h,h,thirddim)
    center = patch2[h//2, h//2]
    return center

def get_centered_pixel_2(patch, h):
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

def spyral_transformation(a):
    print(">",len(a.shape))
    if(len(a.shape) != 3):
        print("spyral_transformation(a): tab is not of 3 dimensions, doing nothing")
        return a
    out = []
    while (a.size):
        out.append(a[0])
        a = np.rot90(np.delete(a, 0, 0))
    res = np.concatenate(out) 
    return res

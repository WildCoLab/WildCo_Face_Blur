# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:28:50 2021

Updated Nov 24, 2021

Blurs camera trap images identified as human by Microsoft MegaDetector

M Fennell
mitchfen@mail.ubc.ca

@author: mitchfen
"""
# import the necessary packages (opencv-python installed manually via reticulate)
import numpy as np 
import cv2 
import json
import os 
from PIL import Image

#define faceblur function
def anonymize_face_simple(image, factor=7.0):
	# automatically determine the size of the blurring kernel based
	# on the spatial dimensions of the input image
	(h, w) = image.shape[:2]
	kW = int(w / factor)
	kH = int(h / factor)
	# ensure the width of the kernel is odd
	if kW % 2 == 0:
		kW += 1
	# ensure the height of the kernel is odd
	if kH % 2 == 0:
		kH += 1

	# apply a Gaussian blur to the input image using our computed
	# kernel size
	return cv2.GaussianBlur(image, (kW, kH), 0)


# run blurring loop on through detections JSON

def face_blur(ann_file, imgs_in, imgs_out, blur, conf_lim):
    dat = json.load(open(ann_file, "r")) # read in MD ouput .JSON
        
    for img in range(0,len(dat["images"])):
        tmp = dat["images"][img]
        file = tmp["file"]
        det = tmp["detections"]
        img_with_exif = Image.open(str(imgs_in)+"\\"+file, 'r') # Extract exif data from original
        if len(det) != 0:
            for d in range(0,len(det)):
                tmp2 = det[d]
                bbox = tmp2["bbox"]
                cat = int(tmp2["category"])
                conf = float(tmp2["conf"])
                if cat == 2 and conf >= conf_lim:
                    if d == 0:
                        image = cv2.imread(str(imgs_in)+"\\"+file)
                        (h,w) = image.shape[:2]
                        box = bbox * np.array([w, h, w, h])
                        (startX, startY, boxwide, boxhigh) = box.astype("int")
                        endX = startX + boxwide
                        endY = startY + boxhigh
                        face = image[startY:endY, startX:endX]
                        face = anonymize_face_simple(face, factor=blur)
                        image[startY:endY, startX:endX] = face
                        cv_img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # convert RBG from openCV to RGB for pillow
                        cv_img_as_pil = Image.fromarray(cv_img_rgb) # convert from CV2 array to pillow format
                        cv_img_as_pil.save(str(imgs_out)+"\\"+file, format='JPEG', exif=img_with_exif.info['exif']) # Save and assign exifdata
                        cv2.destroyAllWindows()
                    else:
                        image = cv2.imread(str(imgs_out)+"\\"+file)
                        (h,w) = image.shape[:2]
                        box = bbox * np.array([w, h, w, h])
                        (startX, startY, boxwide, boxhigh) = box.astype("int")
                        endX = startX + boxwide
                        endY = startY + boxhigh
                        face = image[startY:endY, startX:endX]
                        face = anonymize_face_simple(face, factor=blur)
                        image[startY:endY, startX:endX] = face
                        cv_img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        cv_img_as_pil = Image.fromarray(cv_img_rgb)
                        cv_img_as_pil.save(str(imgs_out)+"\\"+file, format='JPEG', exif=img_with_exif.info['exif'])
                        cv2.destroyAllWindows()
                else:
                    if d == 0:
                        image = cv2.imread(str(imgs_in)+"\\"+file)
                        orig = image.copy()
                        cv_img_rgb = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
                        cv_img_as_pil = Image.fromarray(cv_img_rgb)
                        cv_img_as_pil.save(str(imgs_out)+"\\"+file, format='JPEG', exif=img_with_exif.info['exif'])
                        cv2.destroyAllWindows()
                    else:
                        continue 
                    
        else:
            image = cv2.imread(str(imgs_in)+"\\"+file)
            orig = image.copy()
            cv_img_rgb = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
            cv_img_as_pil = Image.fromarray(cv_img_rgb)
            cv_img_as_pil.save(str(imgs_out)+"\\"+file, format='JPEG', exif=img_with_exif.info['exif'])
            cv2.destroyAllWindows()
            
    print("All",len(dat["images"]),"images at site",os.path.basename(imgs_out),"complete")      
    dat.clear()


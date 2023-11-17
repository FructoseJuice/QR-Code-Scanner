#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from picamera2 import Picamera2, Preview
from pyzbar.pyzbar import decode
import cv2 as cv
import numpy as np
import time
import webbrowser

CAM_HEIGHT = 650
CAM_WIDTH = 480

def main(args):
    #Configure and start camera
    picam2 = Picamera2()
    picam2.resolution = (CAM_HEIGHT, CAM_WIDTH)

    picam2.configure(picam2.create_preview_configuration())
    picam2.start_preview(Preview.QTGL, width=800, height=600)
    picam2.start()
    #-----
    
    #opened = False
    image = None
    overlay = None
    
    while True:
        image = picam2.capture_array("main")
        
        #Convert to Gray Scale
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        #Detect qr_codes in image
        qr_codes = decode(image)
        
        #Create empty overlay
        overlay = np.zeros((CAM_WIDTH, CAM_HEIGHT, 4), dtype=np.uint8)
        
        #Loop through each detected QR code
        for qr in qr_codes:
            #Grab corners of qr code
            points = qr.polygon
            
            if len(points) == 4:
                pts = []
                
                #Create numpy array of detected bounding points
                for pt in points:
                    pts.append([pt.x, pt.y])
                
 
                pts = np.array(pts, dtype=int)
                
                #Draw bounding box on preview
                cv.polylines(overlay, [pts], isClosed=True, color=(255,0,0, 255), thickness=2)
            
            #Read and print data    
            print("Data: %s" % qr.data.decode('utf-8'))
            
            '''#Open link
            if not opened:
                webbrowser.open(qr.data.decode('utf-8'))
                opened = True
            
        if opened:
            break
        '''
        
        #Update the overlay
        picam2.set_overlay(np.array(overlay))
        
        
    #Stop
    picam2.stop()
    

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

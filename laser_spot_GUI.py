# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 21:18:07 2022

analysis of a laser focal spot with tk GUI
@author: Shou
"""

import tkinter as tk  
import tkinter.filedialog
from PIL import Image,ImageTk
import cv2 
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import rc
import matplotlib.pyplot as plt
x = [0,1]
y = [0,1]
font = {'family' : 'arial',   
  'weight' : 'normal',  
  'size'   : 15,  
  }  
font_size = 15
rc('font', **font)
plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
plt.rcParams['font.sans-serif']=['arial']
def choosepic():
    num = input1.get()
    if num == 'um/pixel':
        num = '0.1315'
    num = np.float64(num)
    spot_size = input2.get()
    if spot_size == 'plot_size_um':
        spot_size = '50'
    spot_size = np.float64(spot_size)
    laser_energy = input3.get()
    if laser_energy == 'laser_energy_J':
        laser_energy = '20'
    laser_energy = np.float64(laser_energy)
    laser_t = input4.get()
    if laser_t == 'laser_duration_fs':
        laser_t = '26'
    laser_t = np.float64(laser_t)
    background = input5.get()
    if background == 'set_background':
        background = '0'
    background = np.float64(background)
    path_ = tkinter.filedialog.askopenfilename()
    path.set(path_)
    img_open = Image.open(entry.get())
    image = np.array(img_open)
    # convert to unit8
    tracking = image/np.max(image)*255
    tracking = tracking.astype(np.uint8)
    # grayscale threshold values.
    gmn = np.max(tracking)/10
    gmx = 253
    #apply thresholding to grayscale frames. 
    ret, thresh = cv2.threshold(tracking, gmn, gmx, 0)
    
    # find contours in the threshold image
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_TC89_L1)
    
    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt
    # fitting with a ellipse
    ellipse = cv2.fitEllipse(best_cnt)
    xc = np.int32(ellipse[0][1])
    yc = np.int32(ellipse[0][0])
    a = ellipse[1][0]
    b = ellipse[1][1]
    rmax = np.int32(spot_size/num)
    
    tracking2 = image/np.max(image[xc-5:xc+5,yc-5:yc+5])*255
    tracking2 = tracking2.astype(np.uint8)
    # grayscale threshold values.
    gmn = np.max(tracking2)/2.71828/2.71828
    gmx = 255
    #apply thresholding to grayscale frames. 
    ret, thresh = cv2.threshold(tracking2, gmn, gmx, 0)
    
    # find contours in the threshold image
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_TC89_L1)
    
    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt
    # fitting with a ellipse
    ellipse = cv2.fitEllipse(best_cnt)
    xc = np.int32(ellipse[0][1])
    yc = np.int32(ellipse[0][0])
    a = ellipse[1][0]
    b = ellipse[1][1]    
    
    sumr = np.zeros(rmax)
    spot0 = image[xc-rmax:xc+rmax,yc-rmax:yc+rmax]
    # subtract background
    bg = np.mean(image[50:350,50:350])
    out4.set('auto_background='+str(np.round(bg,4)))
    if background != 0: 
        bg = background
    r = np.arange(rmax)
    spot0 = spot0 - bg
    sum0 = np.sum(spot0)
    
    for i in r:
        cv2.circle(spot0,(rmax,rmax),i,(0,0,0),-1)
        sumr[i] = np.sum(spot0)
    
    con = (sum0-sumr)/(sum0-sumr[-1])
    cv2.ellipse(tracking2,ellipse,(255,0,0),1) #image ellipse(x0 y0 a b theta) color thickness
    spot1 = tracking2[xc-rmax:xc+rmax,yc-rmax:yc+rmax]
    spot1 = spot1.astype(np.uint8)
    
    spot0 = image-bg
    cv2.ellipse(spot0,ellipse,(0,0,0),-1)
    sum1 = np.sum(spot0[xc-rmax:xc+rmax,yc-rmax:yc+rmax])
    cone2 = (sum0-sum1)/(sum0-sumr[-1]) 
    # img = ImageTk.PhotoImage(img_open.resize((500,500)))
    # spot1 = np.resize(spot1,(500,500))
    img = Image.fromarray(spot1)
    img = img.resize((500,500))
    img = ImageTk.PhotoImage(img)
    lableShowImage1.config(image=img)
    lableShowImage1.image = img
    out1.set('1/e^2 a='+str(np.round(a*num,2))+' um  b='+str(np.round(b*num,2)) + ' um,'+' concentration='+str(np.round(cone2*100,2))+'%')

    tracking3 = image/np.max(image[xc-5:xc+5,yc-5:yc+5])*255
    tracking3 = tracking3.astype(np.uint8)
    # grayscale threshold values.
    gmn = np.max(tracking3)/2.0
    gmx = 255
    #apply thresholding to grayscale frames. 
    ret, thresh = cv2.threshold(tracking3, gmn, gmx, 0)
    
    # find contours in the threshold image
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_TC89_L1)
    
    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt
    # fitting with a ellipse
    ellipse = cv2.fitEllipse(best_cnt)
    xc = np.int32(ellipse[0][1])
    yc = np.int32(ellipse[0][0])
    a = ellipse[1][0]
    b = ellipse[1][1]
    spot0 = image-bg
    cv2.ellipse(spot0,ellipse,(0,0,0),-1)
    sum1 = np.sum(spot0[xc-rmax:xc+rmax,yc-rmax:yc+rmax])
    confwhm = (sum0-sum1)/(sum0-sumr[-1]) 
    out2.set('FWHM a='+str(np.round(a*num,2))+' um  b='+str(np.round(b*num,2)) + ' um,'+' concentration='+str(np.round(confwhm*100,2))+'%')
    intensity = 4*np.log(2)*laser_energy/np.pi/laser_t*1e15/a/b/num/num*1e8*confwhm/0.5
    out3.set('intensity = ' + str(format(intensity, '.2e')) + 'W/cm^2')

    global x ,y
    x = r*num
    y = con
    f.clear()
    ax = f.add_subplot(111)
    ax.plot(x,y)
    ax.set_ylim(0,1.05)
    ax.set_xlim(0,)
    ax.grid(color='r', linestyle='--', linewidth=1)
    ax.set_xlabel('r (um)',fontdict=font)
    ax.set_ylabel('Concentration',fontdict=font)
    ax.axvline((a+b)*0.25*num,linewidth='2',linestyle=':',alpha=1.0)
    f.subplots_adjust(left=0.12, bottom=0.11, right=0.97, top=0.97,wspace=None, hspace=None)
    canvas.draw_idle()
    
if __name__ == '__main__':
    app = tk.Tk()  
    app.geometry('1024x640') 
    app.title("Laser_spot")  
    can = tk.Canvas(app, bg='white', height=640, width=1024)
    f = Figure(figsize=(5,5), dpi=100)
    a = f.add_subplot(111)
    a.plot(x,y)
    #Entry widget which allows displaying simple text.
    path = tk.StringVar()
    entry = tk.Entry(app, state='readonly', text=path,width = 100)
    entry.grid(columnspan=2)
    lableShowImage1 = tk.Label(app)
    lableShowImage1.grid(row=1,column=0)
    canvas = FigureCanvasTkAgg(f,master=app)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1,column=1)
    buttonSelImage = tk.Button(app, text='open tiff', command=choosepic)
    buttonSelImage.grid(row=2,column=0)
    #buttonSelImage.pack(side=tk.BOTTOM)
    #Call the mainloop of Tk.
    input1 = tk.StringVar(value = 'um/pixel')
    entry1 = tk.Entry(app,text = input1)
    entry1.grid(row=3,column=0)
    out1 = tk.StringVar()
    entry2 = tk.Entry(app, state='readonly', text=out1,width = 50)
    entry2.grid(row=4,column=0)
    input2 = tk.StringVar(value = 'plot_size_um')
    entry3 = tk.Entry(app,text = input2)
    entry3.grid(row=3,column=1)
    out2 = tk.StringVar()
    entry4 = tk.Entry(app, state='readonly', text=out2,width = 50)
    entry4.grid(row=4,column=1)
    input3 = tk.StringVar(value = 'laser_energy_J')
    entry5 = tk.Entry(app,text = input3)
    entry5.grid(row=5,column=0)
    input4 = tk.StringVar(value = 'laser_duration_fs')
    entry6 = tk.Entry(app,text = input4)
    entry6.grid(row=5,column=1)
    out3 = tk.StringVar()
    entry7 = tk.Entry(app, state='readonly', text=out3,width = 50)
    entry7.grid(row=2,column=1)
    input5 = tk.StringVar(value = 'set_background')
    entry8 = tk.Entry(app,text = input5)
    entry8.grid(row=6,column=1)
    out4 = tk.StringVar()
    entry9 = tk.Entry(app, state='readonly', text=out4,width = 50)
    entry9.grid(row=6,column=0)
    app.mainloop()
    
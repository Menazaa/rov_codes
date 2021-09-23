{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np \n",
    "import math\n",
    "import cv2 as cv"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "please enter TL4.7\n"
     ]
    }
   ],
   "source": [
    "#the truth length of the reference\n",
    "tl = float(input('please enter TL'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "#function to round up the output\n",
    "def round_up(n, decimals=0):\n",
    "    multiplier = 10 ** decimals\n",
    "    return math.ceil(n * multiplier) / multiplier\n",
    "\n",
    "#define function to calculate distance\n",
    "def distance (point1 , point2):\n",
    "    x = point1[0]-point2[0]\n",
    "    x2= x**2\n",
    "    y = point1[1]-point2[1]\n",
    "    y2 = y**2\n",
    "    return ((x2)+(y2))**0.5\n",
    "#this function use Matrices in this link https://www.qc.edu.hk/math/Advanced%20Level/circle%20given%203%20points.htm\n",
    "#to get our circle equation to calculate cannon's area\n",
    "def circle_eq(p1,p2,p3):\n",
    "    p_list = [p1,p2,p3]\n",
    "    a1=[];a2=[];a3=[];a4=[]\n",
    "    for i in p_list:\n",
    "        a1.append([i[0],i[1],1])\n",
    "        a2.append([(i[0]**2+i[1]**2),i[1],1])\n",
    "        a3.append([(i[0]**2+i[1]**2),i[0],1])\n",
    "        a4.append([(i[0]**2+i[1]**2),i[0],i[1]])\n",
    "    ad = np.linalg.det(a1)\n",
    "    el1 = -(np.linalg.det(a2)/ad)\n",
    "    el2 = np.linalg.det(a3)/ad\n",
    "    el3 = -(np.linalg.det(a4)/ad)\n",
    "    #circle equation\n",
    "    #x**2+y**2+el1*x+el2*y+el3 =0\n",
    "    return [el1,el2,el3]\n",
    "\n",
    "#define function to get the vectors\n",
    "def get_vector (point1,point2):\n",
    "    return (point2[0]-point1[0],point2[1]-point1[1])\n",
    "#get the mid point \n",
    "\n",
    "def get_mid(point1,point2):\n",
    "    mid = ((point1[0]+point2[0])/2,(point1[1]+point2[1])/2)\n",
    "    return mid\n",
    "#this function get rectangle area by vectors' multiplication  \n",
    "def vectors_multiplication(v1=(0,0),v2=(0,0)):\n",
    "    return abs(v1[0]*v2[1]-v1[1]*v2[0])\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "#define variables used in out put\n",
    "r1=0 ; r2=0 ; r3 =0 \n",
    "l=0 ; creference=0\n",
    "pv1=(0,0) ; pv2=(0,0) ; pv3=(0,0);pv4=(0,0)\n",
    "pt1=(0,0) ; pt2=(0,0) ; pt3=(0,0) ; pt4=(0,0)\n",
    "pc1=(0,0) ; pc2=(0,0) ; pc3=(0,0)\n",
    "prc1=(0,0) ; prc2=(0,0) ; prc3=(0,0)\n",
    "#define variables used as flag\n",
    "vRflag= False \n",
    "vLflag = False\n",
    "rflag= False\n",
    "lflag= False\n",
    "cflag= False\n",
    "c1flag= False"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "#function to draw on the frame\n",
    "def draw_lines(event,x,y,flags,param): \n",
    "    \n",
    "    \n",
    "    global pv1,pv2,pv3,pv4,pt1,pt2,pt3,pt4,vRflag,vLflag,rflag,lflag\n",
    "    \n",
    "    #this event for reference definition\n",
    "    \n",
    "    if event == cv.EVENT_RBUTTONDOWN:\n",
    "        if not vRflag:\n",
    "            if pv1==(0,0):\n",
    "                pv1= x,y\n",
    "            elif pv2==(0,0):\n",
    "                pv2= x,y\n",
    "                vRflag= True\n",
    "        elif not vLflag:\n",
    "            if pv3==(0,0):\n",
    "                pv3= x,y\n",
    "            elif pv4==(0,0):\n",
    "                pv4= x,y\n",
    "                vLflag= True\n",
    "        elif vLflag and vRflag:\n",
    "            pv1=(0,0) ; pv2=(0,0) ; pv3=(0,0) ; pv4=(0,0)\n",
    "            vRflag= False\n",
    "            vLflag= False\n",
    "    \n",
    "    \n",
    "    \n",
    "     #this event for length definition\n",
    "    if event == cv.EVENT_LBUTTONDOWN:\n",
    "        if not rflag:\n",
    "            if pt1==(0,0):\n",
    "                pt1= x,y\n",
    "            elif pt2==(0,0):\n",
    "                pt2= x,y\n",
    "                rflag= True\n",
    "        elif not lflag:\n",
    "            if pt3==(0,0):\n",
    "                pt3= x,y\n",
    "            elif pt4==(0,0):\n",
    "                pt4= x,y\n",
    "                lflag= True\n",
    "        elif lflag and rflag:\n",
    "            pt1=(0,0) ; pt2=(0,0) ; pt3=(0,0) ; pt4=(0,0)\n",
    "            rflag= False\n",
    "            lflag= False\n",
    "\n",
    "\n",
    "            \n",
    "            \n",
    "#function draw circle by three points on it          \n",
    "def draw_circle(event, x,y,flags,params):\n",
    "    global pc1,pc2,pc3,cflag,prc1,prc2,prc3,c1flag\n",
    "    \n",
    "    if event== cv.EVENT_LBUTTONUP:\n",
    "        if pc1==(0,0):\n",
    "            pc1= x,y\n",
    "        elif pc2==(0,0):\n",
    "            pc2=x,y\n",
    "        elif pc3==(0,0):\n",
    "            pc3=x,y\n",
    "            cflag=True\n",
    "        elif cflag:\n",
    "            pc1=(0,0) ; pc2=(0,0) ; pc3=(0,0)\n",
    "            cflag= False\n",
    "            \n",
    "            \n",
    "    elif event== cv.EVENT_RBUTTONUP:\n",
    "        if prc1==(0,0):\n",
    "            prc1= x,y\n",
    "        elif prc2==(0,0):\n",
    "            prc2=x,y\n",
    "        elif prc3==(0,0):\n",
    "            prc3=x,y\n",
    "            c1flag=True\n",
    "        elif cflag:\n",
    "            prc1=(0,0) ; prc2=(0,0) ; prc3=(0,0)\n",
    "            c1flag= False\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "R1 =  2.68\n",
      "R2 =  2.68\n",
      "Length =  23.1\n",
      "Inner raduis =  2.3\n"
     ]
    }
   ],
   "source": [
    "#creat an object \n",
    "cap = cv.VideoCapture(0)\n",
    "#creat a resizable window \n",
    "cv.namedWindow('main_window',cv.WINDOW_NORMAL)\n",
    "R1 = [];R2=[];L=[];inner_raduis_list=[]\n",
    "img = None \n",
    "img_c = None\n",
    "while True :\n",
    "    #read the frame using opencv functions \n",
    "    \n",
    "    ret,frame = cap.read()\n",
    "    key = cv.waitKey(1) & 0XFF\n",
    "    \n",
    "    \n",
    "    #assign imag if pressed \n",
    "    if key == ord('l'):\n",
    "        img = frame \n",
    "        cv.namedWindow('measure',cv.WINDOW_NORMAL)\n",
    "        cv.imwrite('length_image.jpg',img)\n",
    "        cv.setMouseCallback('measure',draw_lines) \n",
    "    if key == ord('s'):\n",
    "        img_c = frame\n",
    "        cv.namedWindow('circles',cv.WINDOW_NORMAL)\n",
    "        cv.imwrite('circles.jpg',img_c)\n",
    "        cv.setMouseCallback('circles',draw_circle) \n",
    "        \n",
    "      \n",
    "    \n",
    "    \n",
    "    if img_c is not None and not(creference ==0) :\n",
    "        cv.imshow('circles',img_c)\n",
    "        if not (pc1 == (0,0)):\n",
    "             cv.circle(img_c,pc1,3,(0,200,0),-1)\n",
    "        if not (pc2 == (0,0)):\n",
    "             cv.circle(img_c,pc2,3,(0,200,0),-1)\n",
    "        if not (pc3 == (0,0)):\n",
    "             cv.circle(img_c,pc3,3,(0,200,0),-1)\n",
    "                \n",
    "                \n",
    "        if not (prc1 == (0,0)):\n",
    "             cv.circle(img_c,prc1,3,(0,0,210),-1)\n",
    "        if not (prc2 == (0,0)):\n",
    "             cv.circle(img_c,prc2,3,(0,0,210),-1)\n",
    "        if not (prc3 == (0,0)):\n",
    "             cv.circle(img_c,prc3,3,(0,0,210),-1) \n",
    "        \n",
    "        \n",
    "                \n",
    "        \n",
    "    if img is not None:\n",
    "        cv.imshow('measure',img)\n",
    "        #all of condtions drawing our lines if they defined\n",
    "        if not(pt1 == (0,0)):\n",
    "            cv.circle(img,pt1,1,(0,200,0),-1)\n",
    "        if not(pt2 == (0,0)):\n",
    "            cv.circle(img,pt2,1,(0,200,0),-1)\n",
    "        if rflag:\n",
    "            cv.line(img,pt1,pt2,(0,255,0),1,cv.LINE_AA)\n",
    "        if not(pt3 == (0,0)):\n",
    "            cv.circle(img,pt3,1,(0,200,0),-1)\n",
    "        if not(pt4 == (0,0)):\n",
    "            cv.circle(img,pt4,1,(0,200,0),-1)\n",
    "        if lflag:\n",
    "            cv.line(img,pt3,pt4,(0,255,0),1,cv.LINE_AA)\n",
    "            \n",
    "                \n",
    "        if not(pv1 == (0,0)):\n",
    "            cv.circle(img,pv1,1,(0,0,210),-1)\n",
    "        if not(pv2 == (0,0)):\n",
    "            cv.circle(img,pv2,1,(0,0,210),-1)\n",
    "        if not(pv3 == (0,0)):\n",
    "            cv.circle(img,pv3,1,(0,0,210),-1)\n",
    "        if vRflag:\n",
    "            cv.line(img,pv1,pv2,(0,0,210),1,cv.LINE_AA)\n",
    "        if vLflag:\n",
    "            cv.line(img,pv3,pv4,(0,0,210),1,cv.LINE_AA)\n",
    "        \n",
    "    #check our flags to check all of lines and vectors are defined then calculate our two radii\n",
    "    if key == ord('c'):\n",
    "        if rflag and lflag and vRflag and vLflag:\n",
    "            if  rflag and lflag:\n",
    "                vl1 = get_vector(pt1,pt2)\n",
    "                vl2 = get_vector(pt2,pt1) \n",
    "                vl3 = get_vector(pt3,pt4)\n",
    "                vl4 = get_vector(pt4,pt3)\n",
    "                lines_vectors_1_1 = [get_vector(pt1,pt3),get_vector(pt1,pt4)]\n",
    "                lines_vectors_1_2 = [get_vector(pt2,pt3),get_vector(pt2,pt4)]\n",
    "                lines_vectors_2_1 = [get_vector(pt3,pt1),get_vector(pt3,pt2)]\n",
    "                lines_vectors_2_2 = [get_vector(pt4,pt1),get_vector(pt4,pt2)]\n",
    "                lift_rectangle_areas = []\n",
    "                right_rectangle_areas = []\n",
    "                for v in lines_vectors_1_1:\n",
    "                    right_rectangle_areas.append(vectors_multiplication(v,vl1))\n",
    "                for v in lines_vectors_1_2:\n",
    "                    right_rectangle_areas.append(vectors_multiplication(v,vl2))\n",
    "                for v in lines_vectors_2_1:\n",
    "                    lift_rectangle_areas.append(vectors_multiplication(v,vl3))\n",
    "                for v in lines_vectors_2_2:\n",
    "                    lift_rectangle_areas.append(vectors_multiplication(v,vl4))\n",
    "\n",
    "                length_list=[]\n",
    "                length_list.append(distance(get_mid(pt1,pt2),get_mid(pt3,pt4)))\n",
    "                for area in lift_rectangle_areas:\n",
    "                    length_list.append(area/distance(pt3,pt4))\n",
    "                for area in right_rectangle_areas:\n",
    "                    length_list.append(area/distance(pt1,pt2))\n",
    "                length_av = np.average(length_list)\n",
    "                r1p = distance(pt1,pt2)\n",
    "                r2p = distance(pt3,pt4)\n",
    "                \n",
    "                \n",
    "            if vRflag and vLflag :\n",
    "                v1 = get_vector(pv1,pv2)\n",
    "                v2 = get_vector(pv2,pv1) \n",
    "                v3 = get_vector(pv3,pv4)\n",
    "                v4 = get_vector(pv4,pv3)\n",
    "                vectors_1_1 = [get_vector(pv1,pv3),get_vector(pv1,pv4)]\n",
    "                vectors_1_2 = [get_vector(pv2,pv3),get_vector(pv2,pv4)]\n",
    "                vectors_2_1 = [get_vector(pv3,pv1),get_vector(pv3,pv2)]\n",
    "                vectors_2_2 = [get_vector(pv4,pv1),get_vector(pv4,pv2)]\n",
    "                lift_rectangle_areas_Reference = []\n",
    "                right_rectangle_areas_Reference = []\n",
    "                for v in vectors_1_1:\n",
    "                    right_rectangle_areas_Reference.append(vectors_multiplication(v,v1))\n",
    "                for v in vectors_1_2:\n",
    "                    right_rectangle_areas_Reference.append(vectors_multiplication(v,v2))\n",
    "                for v in vectors_2_1:\n",
    "                    lift_rectangle_areas_Reference.append(vectors_multiplication(v,v3))\n",
    "                for v in vectors_2_2:\n",
    "                    lift_rectangle_areas_Reference.append(vectors_multiplication(v,v4))\n",
    "\n",
    "                reference_list=[]\n",
    "                reference_list.append((distance(pv1,pv3)+distance(pv2,pv4))/2)\n",
    "                for area in lift_rectangle_areas_Reference:\n",
    "                    reference_list.append(area/distance(pv3,pv4))\n",
    "                for area in right_rectangle_areas_Reference:\n",
    "                    reference_list.append(area/distance(pv1,pv2))\n",
    "                width_av = np.average(reference_list)\n",
    "                \n",
    " \n",
    "                r1 = ((r1p*tl)/width_av)/2\n",
    "                r2 = ((r2p*tl)/width_av)/2\n",
    "                l = (length_av*tl)/width_av\n",
    "                L.append(l)\n",
    "                R1.append(r1)\n",
    "                R2.append(r2)\n",
    "                pv1=(0,0) ; pv2=(0,0) ; pv3=(0,0);pv4=(0,0)\n",
    "                pt1=(0,0) ; pt2=(0,0) ; pt3=(0,0) ; pt4=(0,0)\n",
    "                vRflag= False\n",
    "                vLflag= False \n",
    "                rflag= False\n",
    "                lflag= False\n",
    "                img = cv.imread('Length_image.jpg')\n",
    "            \n",
    "                \n",
    "#             if vflag :\n",
    "#                 if abs(pv1[0]-pv2[0])<abs(pv1[0]-pv3[0]):\n",
    "#                     v1 = get_vector(pv1,pv2)\n",
    "#                     v2= get_vector(pv1,pv3)\n",
    "#                     v1distance= distance(pv1,pv2)\n",
    "#                     width = vectors_multiplication(v1,v2)/v1distance\n",
    "#                 if abs(pv1[0]-pv2[0])>abs(pv1[0]-pv3[0]): \n",
    "#                     v1 = get_vector(pv1,pv3)\n",
    "#                     v2= get_vector(pv1,pv2)\n",
    "#                     v1distance= distance(pv1,pv3)\n",
    "#                     width = vectors_multiplication(v1,v2)/v1distance\n",
    "#                 r1 = ((r1p*tl)/width_av)/2\n",
    "#                 r2 = ((r2p*tl)/width_av)/2\n",
    "#                 l = (length_av*tl)/width_av\n",
    "#                 L.append(l)\n",
    "#                 R1.append(r1)\n",
    "#                 R2.append(r2)\n",
    "#                 pv1=(0,0) ; pv2=(0,0) ; pv3=(0,0)\n",
    "#                 pt1=(0,0) ; pt2=(0,0) ; pt3=(0,0) ; pt4=(0,0)\n",
    "#                 vflag= False \n",
    "#                 rflag= False\n",
    "#                 lflag= False\n",
    "#                 img = cv.imread('Length_image.jpg')\n",
    "                \n",
    "                \n",
    "        elif cflag and c1flag :\n",
    "            c_param = circle_eq(pc1,pc2,pc3)\n",
    "            c1_param = circle_eq(prc1,prc2,prc3)\n",
    "            c_raduis_sq = ((0.5*c_param[0])**2)+((0.5*c_param[1])**2)-c_param[2]\n",
    "            c1_raduis_sq = ((0.5*c1_param[0])**2)+((0.5*c1_param[1])**2)-c1_param[2]\n",
    "            \n",
    "            inner_raduis_list.append(round_up(np.sqrt((creference**2)*(c_raduis_sq/c1_raduis_sq)),2))\n",
    "            cflag= False\n",
    "            c1flag= False\n",
    "            pc1=(0,0) ; pc2=(0,0) ; pc3=(0,0)\n",
    "            prc1=(0,0) ; prc2=(0,0) ; prc3=(0,0)\n",
    "            img_c = cv.imread('circles.jpg')\n",
    "                \n",
    "         \n",
    "    if key == ord('r'):\n",
    "        if img is not None:\n",
    "            pv1=(0,0) ; pv2=(0,0) ; pv3=(0,0);pv4=(0,0)\n",
    "            pt1=(0,0) ; pt2=(0,0) ; pt3=(0,0) ; pt4=(0,0)\n",
    "            vRflag= False\n",
    "            vRflag= False \n",
    "            rflag= False\n",
    "            lflag= False\n",
    "            img = cv.imread('Length_image.jpg')\n",
    "        elif img_c is not None:\n",
    "            pc1=(0,0) ; pc2=(0,0) ; pc3=(0,0)\n",
    "            prc1=(0,0) ; prc2=(0,0) ; prc3=(0,0)\n",
    "            cflag= False\n",
    "            c1flag= False\n",
    "            img_c = cv.imread('circles.jpg')\n",
    "                \n",
    "    if key == 32:   #32 is the space key\n",
    "        if not(len(R1)==0):\n",
    "            r1_av = np.average(R1)\n",
    "            r2_av = np.average(R2)\n",
    "            l_av = np.average(L)\n",
    "            \n",
    "            R1_output = round_up(r1_av,2)\n",
    "            R2_output= round_up(r2_av,2)\n",
    "            L_output = round_up(l_av,2)\n",
    "            creference = r2_av\n",
    "            cv.destroyWindow('measure')\n",
    "            img = None\n",
    "            print ('R1 = ',R1_output)\n",
    "            print ('R2 = ',R2_output)\n",
    "            print('Length = ',L_output)\n",
    "            R1 = [];R2=[];L=[]\n",
    "        elif not(len(inner_raduis_list)==0):\n",
    "            inner_raduis_av = np.average(inner_raduis_list)\n",
    "            inner_raduis = round_up(inner_raduis_av,2)\n",
    "            cv.destroyWindow('circles')\n",
    "            img_c= None\n",
    "            print('Inner raduis = ',inner_raduis)\n",
    "            \n",
    "            inner_raduis_list=[]\n",
    "            creference = 0\n",
    "\n",
    "    if key == ord('q'):\n",
    "            break\n",
    "            \n",
    "    cv.imshow('main_window',frame)\n",
    "cap.release()\n",
    "cv.destroyAllWindows()\n",
    "                "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from pcbnew import *
import re
import sys



#
# Actually create the BOM files...
#
def create_pos(filename):

    board = GetBoard()

    m_place_Offset=board.GetDesignSettings().GetAuxOrigin()




    with open(filename, 'w',encoding="utf-8") as f:
        tt=[]
 
        f.write("Designator,Footprint,Mid X,Mid Y,Layer,Rotation,Comment\n")
        

        for footprint in board.Footprints():
            if(not (footprint.GetAttributes() & FP_EXCLUDE_FROM_POS_FILES )):
                tt.append(footprint)
                tt[-1].SetReference(tt[-1].GetReference().split(',', 1)[0])



        tt.sort(key=sort_by_Reference)
        
        for tmp in tt:
            f.write("\""+ tmp.GetReference()  +"\",") #Designator
            f.write("\""+ str(tmp.GetFPID().GetLibItemName()) +"\",") #Footprint


            footprint_pos=tmp.GetPosition()-m_place_Offset

            # if(tmp.GetLayer()==B_Cu):
            #     footprint_pos.x=-footprint_pos.x

            f.write("\""+ str(ToMM(footprint_pos.x)) +"\",") #Mid X
            f.write("\""+ str(ToMM(-footprint_pos.y)) +"\",") #Mid Y

            if(tmp.GetLayer()==F_Cu):#Layer
                f.write("\"T\",") 
            elif(tmp.GetLayer()==B_Cu):
                f.write("\"B\",") 
            else:
                f.write("\"\",") 
            
            f.write("\"" + str(tmp.GetOrientation()/10) +"\",") #Rotation
            f.write("\""+ tmp.GetValue() +"\"\n") #Comment

            
            
            

        
        f.close()



def sort_key(s):
    #sort_strings_with_embedded_numbers
    re_digits = re.compile(r'(\d+)')
    pieces = re_digits.split(s)  # 切成数字与非数字
    pieces[1::2] = map(int, pieces[1::2])  # 将数字部分转成整数
    return pieces


def sort_by_Reference(elem):
    return sort_key(elem.GetReference())

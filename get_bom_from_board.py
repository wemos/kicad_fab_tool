#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from pcbnew import *
import re
import sys



#
# Actually create the BOM files...
#
def create_bom(filename):

    board = GetBoard()




    with open(filename, 'w',encoding="utf-8") as f:
        tt=[]
 
        f.write("Comment,Description,Designator,Footprint,LibRef,Pins,Quantity\n")
        

        for footprint in board.Footprints():
            if(not (footprint.GetAttributes() & FP_EXCLUDE_FROM_BOM)):
                if len(tt)==0:
                    tt.append(footprint)
                    tt[-1].SetReference(tt[-1].GetReference().split(',', 1)[0])
                    tt[-1].qty=1
                else:

                    for tmp in tt:
                        if(tmp.GetValue()==footprint.GetValue() and tmp.GetFPID().GetLibItemName()==footprint.GetFPID().GetLibItemName()):
                            tmp.SetReference(tmp.GetReference()+","+ footprint.GetReference().split(',', 1)[0])
                            tmp.qty=tmp.qty+1
                            break

                        if(tmp==tt[-1]):
                            tt.append(footprint)
                            tt[-1].SetReference(tt[-1].GetReference().split(',', 1)[0])
                            tt[-1].qty=1
                            break

        tt.sort(key=sort_by_Reference)
        
        for tmp in tt:
            f.write("\""+ tmp.GetValue() +"\",") #Comment
            f.write("\""+ tmp.GetDescription() + "\",") #Description

            f.write("\""+ tmp.GetReference() +"\",") #Designator
            
            # list_ref=tmp.GetReference().split(",")   
            # list_ref=list(set(list_ref))
            # list_ref.sort(key=sort_key)
            # f.write("\""+ ",".join(list_ref) +"\",")

            f.write("\""+ str(tmp.GetFPID().GetLibItemName()) +"\",") #Footprint
            f.write("\"\",") #LibRef
            f.write("\"\",") #Pins
            f.write(str(tmp.qty)+"\n") #Quantity

        
        f.close()



def sort_key(s):
    #sort_strings_with_embedded_numbers
    re_digits = re.compile(r'(\d+)')
    pieces = re_digits.split(s)  # 切成数字与非数字
    pieces[1::2] = map(int, pieces[1::2])  # 将数字部分转成整数
    return pieces


def sort_by_Reference(elem):
    return sort_key(elem.GetReference())

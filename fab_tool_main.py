#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import time
from pcbnew import *
import re
import wx


from .get_bom_from_board import *
from .get_pos_from_board import *
from .plot_from_board import *

from .get_size_from_board import *


import zipfile




#
# Actually create the PCBA files...
#
def create_pcba():

    str_time=time.strftime("%Y%m%d_%H%M%S", time.localtime()) 

    board = GetBoard()
    boardfile = board.GetFileName()
    
    name = os.path.splitext(os.path.basename(boardfile))[0]

    path = os.path.dirname(boardfile)+"/SMT_"+name+"_"+str_time+"/"

    plot_path=path+"plot/"

    file_bom=path + "bom_"+name+".csv"
    file_pos=path + "pos_"+name+".csv"
    file_plot_zip=path + "plot_"+name+".zip"

    if not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(plot_path):
        os.mkdir(plot_path)
    


    bound=GetBoardBound()

    # Set AuxOrigin

    # get_size()
    new_AuxOrigin=wxPoint(bound.GetLeft(),bound.GetBottom()) 
    board.GetDesignSettings().SetAuxOrigin(new_AuxOrigin)

    # Set pdf_scale
    pcb_width=bound.GetWidth()/1000000.0  # mm
    pcb_height=bound.GetHeight()/1000000.0

    A4_width=297.0-30
    A4_height=210.0-30

    pdf_scale=min(A4_width/pcb_width, A4_height/pcb_height)

    # bom file
    create_bom(file_bom)

    # pos file
    create_pos(file_pos)

    # plot files
    create_plot(plot_path, pdf_scale)

    
    # Zip the plot files
    f = zipfile.ZipFile(file_plot_zip,'w',zipfile.ZIP_DEFLATED)
    startdir = plot_path
    for dirpath, dirnames, filenames in os.walk(startdir):
        for filename in filenames:
            file_ext=os.path.splitext(filename)[-1][1:]
            if(file_ext=="gbr" or file_ext=="drl"):
                f.write(os.path.join(dirpath,filename),arcname=os.path.join("plot/"+filename))
    f.close()


    ss="Done!\nPCB Width: "+ str(bound.GetWidth()/1000000.0)+"mm, "
    ss+="Height: "+ str(bound.GetHeight()/1000000.0)+"mm\n"
    wx.MessageDialog(None,  ss).ShowModal()
    


    






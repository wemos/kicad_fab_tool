#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from pcbnew import *
import re
import sys
import wx








# def get_size():

#     board = GetBoard()

#     # offset=board.GetDesignSettings().m_AuxOrigin

#     rect=GetBoardBound()


#     # ss=str(offset)+" x="+str(rect.GetLeft())+ " y="+str(rect.GetBottom()) +"\n"
#     # ss+="Width:"+ str(rect.GetWidth()/1000000.0)+"mm\n"
#     # ss+="Height:"+ str(rect.GetHeight()/1000000.0)+"mm\n"
#     # wx.MessageDialog(None,  ss).ShowModal()
    
#     new_p=wxPoint(rect.GetLeft(),rect.GetBottom())
#     board.GetDesignSettings().m_AuxOrigin=new_p


def GetBoardBound(brd = None, marginLayer = Edge_Cuts):
    ''' Calculate board edge from the margin layer, the default margin layer is Edge_Cuts
        enum all the draw segment on the specified layer, and merge their bound rect
    '''
    if not brd:
        brd = GetBoard()

    rect = None

    for dwg in brd.GetDrawings():
        if dwg.GetLayer() == marginLayer:
            if hasattr(dwg, 'Cast_to_DRAWSEGMENT'):
                d = dwg.Cast_to_DRAWSEGMENT()
            else:
                d = Cast_to_PCB_SHAPE(dwg)
            w = d.GetWidth()
            box = d.GetBoundingBox()

            box.SetX(int(box.GetX() + w/2))
            box.SetY(int(box.GetY() + w/2))
            box.SetWidth(int(box.GetWidth() - w))
            box.SetHeight(int(box.GetHeight() - w))
            if rect:
                rect.Merge(box)
            else:
                rect = box
    w = 200000
    rect.SetX(int(rect.GetX() + w/2))
    rect.SetY(int(rect.GetY() + w/2))
    rect.SetWidth(int(rect.GetWidth() - w))
    rect.SetHeight(int(rect.GetHeight() - w))
    return rect

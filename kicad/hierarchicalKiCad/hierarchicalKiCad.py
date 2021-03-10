#!/usr/bin/env python

import wx
import eeschema
import refTools
import clone
import os

(NAME_COL_ID, COPIES_COL_ID, LR_COL_ID, PINSPERUNIT_COL_ID, COMPS_PER_UNIT_COL_ID,
 REFOFFSET_COL_ID, REFSPACING_COL_ID, POSITION_COL_ID, SIZE_COL_ID,
 PATH_COL_ID) = range(10)



A4 = 11693, 8268              # mils
mils = 0.05                   # pixels per mil
W, H = A4[0]*mils, A4[1]*mils # pixels


PADDING = 800
SHEETLINE = 100
SHEETWIDTH = 1400

class HierarchicalKiCad(wx.Frame):


    def __init__(self, parent, id, projectDir=None, title='Hierarchical KiCad'):
        
        wx.Frame.__init__(self, parent, id, title, size=(1200, 600))
        panel = wx.Panel(self)
        
        
        ### LAYOUT
        #######################################################################
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        
        WIDGETS_PADDING = 2
        
        hbox.Add(vbox1, 1, wx.ALL|wx.EXPAND, WIDGETS_PADDING)
        hbox.Add(vbox2, 0, wx.ALL|wx.EXPAND, WIDGETS_PADDING)
        
        panel.SetSizer(hbox)
            

        ### FIRST COLUMN: SETTING
        #######################################################################
        # First line: list of subschematics
        subschList = wx.ListCtrl(panel, style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VRULES)
        subschList.InsertColumn(NAME_COL_ID           , 'Name', width=100)
        subschList.InsertColumn(COPIES_COL_ID         , 'Units', width=50)
        subschList.InsertColumn(LR_COL_ID             , 'LR', width=50)
        subschList.InsertColumn(COMPS_PER_UNIT_COL_ID , 'Comps./unit', width=85)
        subschList.InsertColumn(PINSPERUNIT_COL_ID    , 'Pins/unit', width=70)
        subschList.InsertColumn(REFOFFSET_COL_ID      , 'Ref. offset', width=75)
        subschList.InsertColumn(REFSPACING_COL_ID     , 'Ref. spacing', width=90)
        subschList.InsertColumn(POSITION_COL_ID       , 'Position', width=100)
        subschList.InsertColumn(SIZE_COL_ID           , 'Size', width=100)
        subschList.InsertColumn(PATH_COL_ID           , 'Path', width=500)
        
        subschList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.modifyItem)
        subschList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.modifyItemIfSelected)
        
        vbox1.Add(subschList, 1, wx.ALL|wx.EXPAND, WIDGETS_PADDING)
        
        # Second line: controls
        hbox13 = wx.BoxSizer(wx.HORIZONTAL)
        addBut  = wx.Button(panel, label='Add')
        delBut  = wx.Button(panel, label='Remove')
        saveBut = wx.Button(panel, label='Save')
        
        addBut.Bind(wx.EVT_BUTTON, self.addSch)
        delBut.Bind(wx.EVT_BUTTON, self.delSch)
        saveBut.Bind(wx.EVT_BUTTON, self.save)
        
        hbox13.Add(addBut, 1, wx.ALL, WIDGETS_PADDING)
        hbox13.Add(delBut, 1, wx.ALL, WIDGETS_PADDING)
        hbox13.Add(saveBut, 1, wx.ALL, WIDGETS_PADDING)
        vbox1.Add(hbox13, 0, wx.ALL|wx.EXPAND, WIDGETS_PADDING)
        
        
        ### SECOND COLUMN: SCHEMATICS PREVIEW AND LOG
        #######################################################################
        schPanel = wx.Panel(panel, size=(W+1, H+1))
        schPanel.SetBackgroundColour('white')
        schPanel.Bind(wx.EVT_PAINT, self.OnPaint)
        
        logText = wx.TextCtrl(panel, value='', style=wx.TE_MULTILINE)
        
        vbox2.Add(schPanel, 0, wx.ALL, WIDGETS_PADDING)
        vbox2.Add(logText, 1, wx.ALL|wx.EXPAND, WIDGETS_PADDING)
        
       
        ### PUBLIC WIDGETS
        ########################################################################
        self.logText = logText
        self.subschList = subschList
        self.schPanel = schPanel

        
        ### PUBLIC DATA
        ########################################################################
        self.subschCount = 0
        self.title = title
        self.selected = None
        
        if projectDir:
            self.topdir = projectDir
        else:
            self.topdir = './'

        
        ### CENTRE AND SHOW 
        ########################################################################
        self.Centre()
        self.Show(True)
        self.log('Program started.')
        


    def addSch(self, event):
        
        dlg = wx.FileDialog(self, "Choose a schematics.", self.topdir, "", "*.sch", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            subschList = self.subschList
            
            directory, fn = dlg.GetDirectory(), dlg.GetFilename()
            self.topdir = directory
            name = '.'.join(fn.split('.')[:-1])
            path = directory+'/'+fn
            itemNum = self.subschCount
            
            newItem = subschList.InsertStringItem(itemNum, name)
            subschList.SetStringItem(newItem, NAME_COL_ID, name)
            subschList.SetStringItem(newItem, PATH_COL_ID, path)
            subschList.SetStringItem(newItem, COPIES_COL_ID, str(1))
            subschList.SetStringItem(newItem, LR_COL_ID, 'R')
            
            sch = eeschema.Sch.load(path)
            pinsCount = len(set( [p.text for p in sch.getTextItems('HLabel')] ))
            subschList.SetStringItem(newItem, PINSPERUNIT_COL_ID, str(pinsCount))
            
            compsCount = len(sch.getComponents())
            subschList.SetStringItem(newItem, COMPS_PER_UNIT_COL_ID, str(compsCount))
                        
            sheetHeight = (pinsCount+2)*SHEETLINE
            subschList.SetStringItem(newItem, SIZE_COL_ID,
                                     '%d, %d' % (SHEETWIDTH, sheetHeight) )

            max_ref_num = refTools.maxRefNumber(sch)
            ref_spacing = refTools.niceRefOffset(max_ref_num)
            subschList.SetStringItem(newItem, REFSPACING_COL_ID, str(ref_spacing))
            
            self.rebuild()
            self.subschCount += 1

        dlg.Destroy()
        self.OnPaint(None)
        
        
        
    def delSch(self, event):
        subschList = self.subschList
        i = subschList.GetFirstSelected()
        if type(i)==int and i>-1 and i<subschList.GetItemCount():
            subschList.DeleteItem(i)
            self.rebuild()
            self.OnPaint(None)



    def modifyItemIfSelected(self, event): 
        selected = self.subschList.GetFirstSelected()
        if self.selected == selected:  
            self.modifyItem(None)
        else:
            self.selected = selected


        
    def modifyItem(self, event):
        subschList = self.subschList

        selected = subschList.GetFirstSelected()

        copies = int(subschList.GetItemText(selected, COPIES_COL_ID))
        dlg = wx.TextEntryDialog(self, 'Number of copies or L/R (l/r)', caption=self.title, defaultValue='')
        
        if dlg.ShowModal() == wx.ID_OK:
            val = dlg.GetValue()
            if val and (val in 'LRlr'):
                subschList.SetStringItem(selected, LR_COL_ID, val.upper())
            elif val.isdigit() and int(val)>0:
                val = int(val)
                subschList.SetStringItem(selected, COPIES_COL_ID, str(val))
                
                pinsCount = int(subschList.GetItemText(selected, PINSPERUNIT_COL_ID))
                sheetHeight = ((pinsCount+1)*val+1)*SHEETLINE
                subschList.SetStringItem(selected, SIZE_COL_ID,
                                        '%d, %d' % (SHEETWIDTH, sheetHeight) )
                
                self.rebuild()
            else:
                self.log('Sorry, I dont know what do do with "%s"...' % val)
            self.OnPaint(None)
            
        dlg.Destroy()
        
    
    
    def OnPaint(self, event):
        subschList = self.subschList
        dc = wx.PaintDC(self.schPanel)
        dc.Clear()

        dc.SetPen(wx.Pen('black'))
        
        #dc.DrawRectangle(0,0,W,H) # draw inside :(
        def rec(x,y,w,h):
            x,y,w,h = map(int, (x,y,w,h))
            dc.DrawLine(x,y,x+w,y)
            dc.DrawLine(x+w,y,x+w,y+h)
            dc.DrawLine(x+w,y+h,x,y+h)
            dc.DrawLine(x,y+h,x,y)
        
        rec(0,0,W,H)
        
        for i in range(subschList.GetItemCount()):
            copies = int(subschList.GetItemText(i, COPIES_COL_ID))
            pinsCount = int(subschList.GetItemText(i, PINSPERUNIT_COL_ID))
            posX, posY = subschList.GetItemText(i, POSITION_COL_ID).split(', ')
            posX, posY = int(posX), int(posY)
            width, height = subschList.GetItemText(i, SIZE_COL_ID).split(', ')
            width, height = int(width), int(height)
            rec(posX*mils, posY*mils, width*mils, height*mils)
            
            posYpin = posY + SHEETLINE
            posXpin = posX
            PIN_LEN = 5
            if subschList.GetItemText(i, LR_COL_ID) == 'R':
                posXpin += SHEETWIDTH-PIN_LEN/mils
                
            for copy_i in range(copies):
                for pin in range(pinsCount):
                    dc.DrawLine(posXpin*mils,posYpin*mils,posXpin*mils+PIN_LEN,posYpin*mils)
                    posYpin += SHEETLINE
                posYpin += SHEETLINE
            
            
            
    def rebuild(self):
        subschList = self.subschList
        free_pos = [PADDING, PADDING]
        ref_offset = 0
        
        for i in range(subschList.GetItemCount()):
            
            copies = int(subschList.GetItemText(i, COPIES_COL_ID))
            pinsCount = int(subschList.GetItemText(i, PINSPERUNIT_COL_ID))
            sheetHeight = ((pinsCount+1)*copies+1)*SHEETLINE

            if free_pos[1] + sheetHeight > A4[1]:
                free_pos[0] += SHEETWIDTH + PADDING
                free_pos[1] = PADDING
                
            subschList.SetStringItem(i, POSITION_COL_ID, '%d, %d' % tuple(free_pos) )
                
            free_pos[1] += sheetHeight + PADDING
            
            subschList.SetStringItem(i, REFOFFSET_COL_ID, str(ref_offset))
            
            ref_spacing = int(subschList.GetItemText(i, REFSPACING_COL_ID))
            ref_offset += ref_spacing*copies
        
        
    def log(self, msg):
        l = self.logText
        l.SetValue(l.GetValue() + str(msg) + '\n')
        
        
    def save(self, event):
        dlg = wx.FileDialog(self, "Save schematics hierarchy.", self.topdir, "", "*.sch", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            subschList = self.subschList
            
            directory, fn = dlg.GetDirectory(), dlg.GetFilename()
                
            self.log('Working directory is "%s".' % directory)
            
            sch = eeschema.Sch()

            for  i in range(subschList.GetItemCount()):
                path = subschList.GetItemText(i, PATH_COL_ID) 
                pos = subschList.GetItemText(i, POSITION_COL_ID) 
                dims = subschList.GetItemText(i, SIZE_COL_ID) 
                name = subschList.GetItemText(i, NAME_COL_ID) 
                copies = int(subschList.GetItemText(i, COPIES_COL_ID)) 
                lr = subschList.GetItemText(i, LR_COL_ID) 
                refoffset = int(subschList.GetItemText(i, REFOFFSET_COL_ID)) 
                refspacing = int(subschList.GetItemText(i, REFSPACING_COL_ID))

                newname = '%s-%dx.sch' % (name, copies)
                newpath = os.path.join(directory, newname)
                # TODO better clonesXY than in row...
                clone.clone(path, newpath, posXY=(1000, 1000), clonesXY=(1, copies),
                      margin=500, ref_offset=refoffset, ref_spacing=refspacing)
                self.log('%s generated.' % newname)
                sheet = eeschema.Sheet()
                sheet.fileName = newname
                sheet.sheetName = '.'.join(newname.split('.')[:-1])
                sheet.pos = [int(i) for i in pos.split(', ')]
                sheet.dims = [int(i) for i in dims.split(', ')]

                subsheet = eeschema.Sch.load(path)
                HLabels = subsheet.getTextItems('HLabel')
                pins = map(lambda label: label.text, HLabels)
                pins = sorted(set(pins))
                sheet.pins = []
                if copies>1:
                    for i in range(copies):
                        for pin_i, p in enumerate(pins):
                            offset=100
                            if pin_i==0 and i>0:
                                offset = 200
                            sheet.addPin('%s%d'%(p, i), leftright=lr, offset=offset)
                elif copies==1:
                    for p in pins:
                        sheet.addPin('%s'%(p), leftright=lr, offset=100)


                sch.items.append(sheet)


                
            
            name = '.'.join(fn.split('.')[:-1])
            path = os.path.join(directory,fn)
            if path.strip()[-4:] != '.sch':
                path += '.sch'
            sch.save(path)
            self.log('Saved to %s.' % path)

        dlg.Destroy()
        
        
    

if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser(description='Hierarchical KiCad utility.')
    parser.add_argument('projectDir', nargs='?', action="store", default=None, help='project directory.')
    args = parser.parse_args()

    projectDir = args.projectDir

    app = wx.App()
    HierarchicalKiCad(None, -1, projectDir)
    app.MainLoop()

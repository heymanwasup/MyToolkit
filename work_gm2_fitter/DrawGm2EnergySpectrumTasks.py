from collections import OrderedDict
from curses.panel import version
import enum
from importlib import reload
from re import X
import PlottingLib as P
import ROOT as R
from collections import OrderedDict
reload(P)



class TaskCenter:
    def __init__(self,inputDir):
        self.fileHandler = FilesHandler(inputDir)
        self.isLogy = False
        self.timeTag = None
        self.version = 1

    def Activate(self):
        self.fileHandler.RetrieveFiles()

    def SetLogy(self,isLogy):
        P.Plotting.isLogy = isLogy


    def DrawRatios(self,energy):
        def retrieveRatios(energy):
            ratios= []
             
            for n in range(1296):                
                nCalo = n//54 + 1
                nXtal = n%54
                hname = self.getHistName(nCalo,nXtal)
                try:
                    hist_official = self.fileHandler.GetHist('official',energy,'inFillGainCorrector',hname)
                except:
                    print ('skip: \t',hname)
                    ratios.append({'primary':1.,'residual':1.,'both':1.})
                    continue
                
                ratios.append({})
                if n == 0:
                    x_start = 1
                    x_end = hist_official.GetXaxis().FindBin(200)                
                int_official = hist_official.Integral(x_start,x_end)

                for threshold in ['primary','residual','both']:
                    hist_opt = self.fileHandler.GetHist(threshold,energy,'inFillGainCorrector',hname)    
                    int_opt = hist_opt.Integral(x_start,x_end)
                    ratio = int_opt/int_official                    
                    ratios[-1][threshold] = (ratio)
            return ratios
            
        def getRatioHits(ratios):
            hists = {}
            for threshold in ['primary','residual','both']:                            
                h_ratio_dist = R.TH1F('ratio_dist_%s_%s'%(threshold,energy),'ratio_dist_xtals',100,0,5)
                h_ratio = R.TH1F('ratio_%s_%s'%(threshold,energy),'ratio_xtals',1296,0-0.5,1296-0.5)
                for n in range(1296):
                    ratio = ratios[n][threshold]
                    h_ratio.SetBinContent(n+1,ratio)
                    h_ratio.SetBinError(n+1,0)
                    h_ratio_dist.Fill(ratio)
                hists[threshold] = [h_ratio_dist,h_ratio]
            return hists

        ratios = retrieveRatios(energy)
        ratio_hists = getRatioHits(ratios)
        css = []

        # draw ratio distribution
        thresholds = ['primary','both']
        namess = {'both':'primary+residual','primary':'primary','official':'official'}

        hists = []
        xranges = {'30':[0,3],'25':[0,3.5],'20':[0,5]}
        for key in thresholds:
            h = ratio_hists[key][0]
            h.SetLineWidth(3)
            h.GetXaxis().SetRangeUser(*xranges[energy])
            hists.append(h)

        colors = [R.kBlue,R.kRed]
        p1 = P.Plotting(1200,900)
        p1.colors = colors
        title = 'Ratio of crystal hits;ratio;Num of xtals'
        names = []
        for n in range(2):
            mean = hists[n].GetMean()
            name = '{0:<} mean={1:.2f}'.format(namess[thresholds[n]]+',',mean)
            names.append(name)
        css.append(p1.DrawHistsCmp(title,hists,names,legArgs=(0.45,0.6,0.9,0.8),drawopt='same'))

        # draw ratio all xtals - primary, residual
        p = P.Plotting(1500,600)
        for n,threshold in enumerate(thresholds):
            h = ratio_hists[threshold][1]
            h.SetLineColor(colors[n])            
            h.SetStats(0)
            cs = p.DrawHist(ratio_hists[threshold][1],'Ratio of crystal hits, optmized %s;Xtal index;Optimized / Default;'%(namess[threshold]))
            css.append(cs)
        
        # draw ratio all xtals - primary

        return css
    def DrawCmpEnergyOnCalos(self,method,threshold,xrange,legArgs):
        rebin = 4
        lineWidth = 2
        histss = []
        titles = []
        for caloNum in range(1,25):
            hname = self.getHistName(caloNum,-1,isClustered=True)
            thresholds = [threshold,threshold,'official']
            energies = ['20','30','0']
            namess = {'both':'primary+residual','primary':'primary','official':'official'}

            hists = []
            names = ['%s @ 20 MeV'%(namess[threshold]),'%s @ 30 MeV'%(namess[threshold]),'official']
            for n in range(3):
                thres = thresholds[n]
                energy = energies[n]
                h = self.fileHandler.GetHist(thres,energy,method,hname)
                h.Rebin(rebin)
                h.GetXaxis().SetRangeUser(*xrange)
                h.SetLineWidth(lineWidth)
                hists.append(h)
            histss.append(hists)
            caloStr = 'Calo %s'%(caloNum) if caloNum!=-1 else 'all calos'
            title =  '%s, %s;Energy [MeV];N'%(namess[threshold],caloStr)
            titles.append(title)
        divided = [6,4,0.0001,0.0001]
        return P.Plotting(3600,2400).DrawHistsCmpDivided(divided,titles,histss,names,legArgs,'same')


    def DrawCmpEnergyOnCalo(self,caloNum,method,threshold,xrange,legArgs):
        rebin = 4
        lineWidth = 3
        hname = self.getHistName(caloNum,-1,isClustered=True)
        thresholds = [threshold,threshold,'official']
        energies = ['20','30','0']
        namess = {'both':'primary+residual','primary':'primary','official':'official'}

        hists = []
        names = ['%s @ 20 MeV'%(namess[threshold]),'%s @ 30 MeV'%(namess[threshold]),'official']
        for n in range(3):
            thres = thresholds[n]
            energy = energies[n]
            h = self.fileHandler.GetHist(thres,energy,method,hname)
            h.Rebin(rebin)
            h.GetXaxis().SetRangeUser(*xrange)
            h.SetLineWidth(lineWidth)
            hists.append(h)            
        caloStr = 'Calo %s'%(caloNum) if caloNum!=-1 else 'all calos'
        title =  'Threshold @ %s, %s;Energy [MeV];N'%(namess[threshold],caloStr)
        
        return P.Plotting(1200,900).DrawHistsCmp(title,hists,names,legArgs,'same')

    def DrawCmpThresholdOnCalo(self,caloNum,method,energy,xrange,legArgs=(0.6,0.6,0.9,0.8),rebin=None):
        if rebin == None:
            rebin = 4
        lineWidth = 3
        hname = self.getHistName(caloNum,-1,isClustered=True)
        thresholds = ['official','primary','both']
        hists = []
        for threshold in thresholds:
            h = self.fileHandler.GetHist(threshold,energy,method,hname)
            h.Rebin(rebin)
            h.GetXaxis().SetRangeUser(*xrange)
            h.SetLineWidth(lineWidth)
            hists.append(h)
        names = ['official','primary','primary+residual']
        title =  'Threshold @ %s MeV, Calo %s;Energy [MeV];N'%(energy,caloNum)
        
        return P.Plotting(1200,900).DrawHistsCmp(title,hists,names,legArgs,'same')

    def DrawCmpThresholdOnXtal(self,method,energy,caloNum,xtalNum,legArgs=(0.6,0.6,0.9,0.8),xrange=None,rebin=None):
        if xrange == None:
            xrange = [0,500]
        if rebin == None:
            rebin = 4

        lineWidth = 3
        hname = self.getHistName(caloNum,xtalNum)
        thresholds = ['official','primary','both']
        hists = []
        for threshold in thresholds:
            h = self.fileHandler.GetHist(threshold,energy,method,hname)
            h.Rebin(rebin)
            h.GetXaxis().SetRangeUser(*xrange)
            h.SetLineWidth(lineWidth)
            hists.append(h)
        names = ['official','primary','primary+residual']
        title =  'Threshold @ %s MeV, Calo %s Xtal %s;Energy [MeV];N'%(energy,caloNum,xtalNum)
        
        return P.Plotting(1200,900).DrawHistsCmp(title,hists,names,legArgs,'same')
    
    def DrawCmpThresholdOnXtals(self,method,energy,caloNum,legArgs=(0.4,0.4,0.95,0.85)):
        xrange = [0,500]
        rebin = 4
        lineWidth = 4
        
        thresholds = ['primary','both','official']
        histss = []
        titles = []
        for xtalNum in range(53,-1,-1):
            hists = []
            hname = self.getHistName(caloNum,xtalNum)
            for threshold in thresholds:
                h = self.fileHandler.GetHist(threshold,energy,method,hname)
                h.Rebin(rebin)
                h.GetXaxis().SetRangeUser(*xrange)
                h.SetLineWidth(lineWidth)
                hists.append(h)
            histss.append(hists)
            names = ['primary','primary+residual','official']
            title =  'Threshold @ %s MeV, Calo %s Xtal %s;Energy [MeV];N'%(energy,caloNum,xtalNum)
            titles.append(title)
            divide = [9,6,0,0]
        return P.Plotting(3600,2400).DrawHistsCmpDivided(divide,titles,histss,names,legArgs,'same')

    def DrawCmpThresholdOnCalos(self,method,energy,xrange,legArgs=(0.6,0.3)):
        rebin = 4
        lineWidth = 5
        
        thresholds = ['primary','both','official']
        histss = []
        titles = []
        for caloNum in range(1,25):
            hists = []
            hname = self.getHistName(caloNum,-1,isClustered=True)
            for threshold in thresholds:
                h = self.fileHandler.GetHist(threshold,energy,method,hname)
                h.Rebin(rebin)
                h.GetXaxis().SetRangeUser(*xrange)
                h.SetLineWidth(lineWidth)
                hists.append(h)
            histss.append(hists)
            names = ['primary','primary+residual','official']
            title =  'Threshold @ %s MeV, Calo %s;Energy [MeV];N'%(energy,caloNum)
            titles.append(title)
            divide = [6,4]
        return P.Plotting(3600,2400).DrawHistsCmpDivided(divide,titles,histss,names,legArgs,'same')

    def getHistName(self,caloNum,xtalNum,isClustered=False):
        hname = 'hist_timewindow'
        
        if not isClustered:
            if self.version == 1:
                hname += '_statusTrue'
            elif self.version == 2:
                hname += '_StatusTrue'
            else:
                print ('setup version %s first'%(self.version))
                raise RuntimeError()
        if self.timeTag != None:
            hname += '_%s'%(self.timeTag)

        if caloNum!=-1:
            hname += '_calo%s'%(caloNum)
            if xtalNum!=-1:
                hname += '_xtal%s'%(xtalNum)
        hname += '_energy'
        return hname        


class FilesHandler:
    def __init__(self,inputDir):
        self.inputDir = inputDir
        self.thresholds = ['official','primary','residual','both']
        self.energies = ['30','25','20']
        self.methods = ['islandFitterDAQ','inFillGainCorrector','hitClusterDAQ','testCoincidenceFinder']

    def GetHist(self,threshold,energy,method,hname):
        key = ''
        if threshold == 'official':
            key = 'official'
        else:
            key = '{0:}_{1:}'.format(threshold,energy)        
        try:
            hist = self.files[key][method].Get(hname).Clone()
        except:
            print (hname)
            print (key,method)
            print (self.files[key][method])
            raise RuntimeError()
        return hist


    def RetrieveFiles(self):
        files = {}
        fs = {}
        energies = ['30','25','20']
        thresholds = ['official','primary','residual','both']
        methods = ['islandFitterDAQ','inFillGainCorrector','hitClusterDAQ','testCoincidenceFinder']
        for threshold in thresholds:
            for energy in energies:
                if energy != '30'  and threshold == 'official':
                    continue
                if threshold == 'official':
                    name_f = 'official'
                else:
                    name_f = '%s_%s'%(threshold,energy)
                if threshold!='official':
                    fname = '%s/hists_%s.root'%(self.inputDir,name_f)
                else:
                    fname = '%s/hists_%s.root'%(self.inputDir,name_f)
                f = R.TFile(fname)
                fs[fname] = f
                files[name_f] = {}
                for method in methods:
                    files[name_f][method] = f.Get(method)
        self.files = files
        self.fs = fs

def Activate():
    pass

if __name__ == '__main__':
    main()
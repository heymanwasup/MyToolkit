import ROOT as R
import random

def bind(instance, func, as_name=None):
    """
    Bind the function *func* to *instance*, with either provided name *as_name*
    or the existing name of *func*. The provided *func* should accept the 
    instance as the first argument, i.e. "self".
    """
    if as_name is None:
        as_name = func.__name__
    bound_method = func.__get__(instance, instance.__class__)
    setattr(instance, as_name, bound_method)
    return bound_method

def DrawAndSave(self,name):
    R.TCanvas.Draw(self)
    self.SaveAs(name)

class Plotting:
    isLogy = False
    def __init__(self,c_wx=None,c_wy=None):
        self.c_wx = c_wx
        self.c_wy = c_wy
        self.colors = [1,4,2,6,9]

    def DrawHist(self,hist,title):
        canvas = self.getCanvas()
        hist.SetTitle(title)
        hist.Draw()
        return [canvas,hist]

    
    def DrawHistsCmpDivided(self,divide,titles,histss,names,legArgs,drawopt='esame'):
        canvas = self.getCanvas()
        canvas.Divide(*divide)
        css = []
        for n,hists in enumerate(histss):
            p = canvas.cd(n+1)
            drawleg = True if n == 0 else False
            css.append(self.printOnCanvas(p,titles[n],hists,names,legArgs,drawopt,drawleg))
        return [canvas,css]

    def getCanvas(self):
        if self.c_wx != None and self.c_wy != None:
            canvas = R.TCanvas('%s'%(random.random()),'1',self.c_wx,self.c_wy)
        else:
            canvas = R.TCanvas()        
        bind(canvas,DrawAndSave)
        return canvas

    def DrawHistsCmp(self,title,hists,names,legArgs,drawopt='esame'):
        canvas = self.getCanvas()
        return self.printOnCanvas(canvas,title,hists,names,legArgs,drawopt)

    
    def printOnCanvas(self,canvas,title,hists,names,legArgs,drawopt,drawleg=True):
        canvas.SetLogy(self.isLogy)
        self.setMaximum(hists)
        canvas.cd()
        leg = R.TLegend(*legArgs)
        for n,h in enumerate(hists):
            h.SetLineColor(self.colors[n])
            h.SetTitle(title)
            h.SetStats(0)            
            h.Draw(drawopt)
            leg.AddEntry(h,names[n],'L')
        if drawleg:
            leg.Draw()
        return [canvas,leg,hists]

    def setMaximum(self,hists):
        maximum = max ([h.GetMaximum() for h in hists ])
        for h in hists:
            h.SetMaximum(maximum*1.2)
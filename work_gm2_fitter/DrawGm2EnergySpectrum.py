#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from importlib import reload
import ROOT as R
import DrawGm2EnergySpectrumTasks as Tasks
import subprocess
reload(Tasks)


# In[ ]:


reload(Tasks)
inputDir = '/Users/cheng/workspace/Data/hadd_readAnaHists_total_cc_makehist_total_0207_v1/'
version = 2
# inputDir = '/Users/cheng/workspace/Data/hadd_readAnaHists_timebin_cc_makehist_891_0119_v2/'
timeTag = 'timeGT30'
outputDir = './output_0207_v1'
subprocess.getstatusoutput('mkdir -p %s'%(outputDir))
tasks = Tasks.TaskCenter(inputDir)
tasks.timeTag = timeTag
tasks.version = version
tasks.Activate()


# Input version log
#     1. old input
#     2. Add timeLT10 and timeGT30, modified bin width

# In[ ]:


caloNum = 1; xtalNum = 30; method = 'inFillGainCorrector'
css = []
tasks.timeTag = 'timeLT10'
for energy in ['30','25','20']:
    cs = tasks.DrawCmpThresholdOnXtal(method,energy,caloNum,xtalNum,xrange=[0,500])
    css.append(cs)
    css[-1][0].DrawAndSave('{0:}/Cmp_xtal_thresholds_{1:}MeV_calo{2:}_xtal{3:}_{4:}.png'.format(outputDir,energy,caloNum,xtalNum,method))


# In[ ]:


caloNum = 1; method = 'inFillGainCorrector'
css = []
for energy in ['30','25','20']:
    cs = tasks.DrawCmpThresholdOnXtals(method,energy,caloNum)
    css.append(cs)
    css[-1][0].DrawAndSave('{0:}/Cmp_xtals_thresholds_{1:}MeV_calo{2:}_{3:}.png'.format(outputDir,energy,caloNum,method))


# In[ ]:


method = 'hitClusterDAQ'
css = []
for energy in ['30','25','20']:
    cs = tasks.DrawCmpThresholdOnCalos(method,energy,[0,2990],legArgs=(0.25,0.6,0.85,0.9))
    css.append(cs)
    css[-1][0].DrawAndSave('{0:}/Cmps_calos_thresholds_{1:}MeV_{2:}.png'.format(outputDir,energy,method))


# In[ ]:


method = 'hitClusterDAQ'
css = []
for energy in ['30','25','20']:
    cs = tasks.DrawCmpThresholdOnCalos(method,energy,[0,500],legArgs=(0.25,0.6,0.85,0.9))
    css.append(cs)
    css[-1][0].DrawAndSave('{0:}/Cmps_calos_thresholds_{1:}MeV_{2:}_lowE.png'.format(outputDir,energy,method))


# In[ ]:



caloNum = 1
method = 'hitClusterDAQ'
isLogy = True
css = []
tasks.SetLogy(isLogy)
for energy in ['30','25','20']:
    cs = tasks.DrawCmpThresholdOnCalo(caloNum,method,energy,[0,2990],legArgs=(0.25,0.1,0.85,0.3))
    css.append(cs)
    css[-1][0].DrawAndSave('{0:}/Cmps_calo_thresholds_{1:}MeV_calo{2:}_{3:}.png'.format(outputDir,energy,caloNum,method))


# In[ ]:



caloNum = 1
method = 'hitClusterDAQ'
isLogy = True
tasks.SetLogy(isLogy)
css = []
for threshold in ['both','primary']:
    cs = tasks.DrawCmpEnergyOnCalo(caloNum,method,threshold,[0,2990],legArgs=(0.3,0.1,0.8,0.3))
    css.append(cs)
    css[-1][0].DrawAndSave('{0:}/Cmps_calo_energies_calo{1:}_{2:}_{3:}.png'.format(outputDir,caloNum,method,threshold))


# In[ ]:



caloNum = -1
method = 'hitClusterDAQ'
isLogy = True
tasks.SetLogy(isLogy)
css = []
for threshold in ['both','primary']:
    cs = tasks.DrawCmpEnergyOnCalo(caloNum,method,threshold,[0,2990],legArgs=(0.3,0.1,0.8,0.3))
    css.append(cs)
    css[-1][0].DrawAndSave('{0:}/Cmps_allcalos_energies_{1:}_{2:}.png'.format(outputDir,method,threshold))


# In[ ]:



caloNum = -1
method = 'hitClusterDAQ'
isLogy = False
tasks.SetLogy(isLogy)
css = []
for threshold in ['both','primary']:
    cs = tasks.DrawCmpEnergyOnCalo(caloNum,method,threshold,[0,200],legArgs=(0.3,0.6,0.8,0.8))
    css.append(cs)
    css[-1][0].DrawAndSave('{0:}/Cmps_calo_energies_calo{1:}_{2:}_{3:}_lowE.png'.format(outputDir,caloNum,method,threshold))


# In[ ]:



caloNum = -1
method = 'hitClusterDAQ'
isLogy = True
tasks.SetLogy(isLogy)
css = []
for threshold in ['both','primary']:
    cs = tasks.DrawCmpEnergyOnCalos(method,threshold,[0,2990],legArgs=(0.3,0.1,0.8,0.3))
    css.append(cs)
    css[-1][0].DrawAndSave('{0:}/Cmps_energies_calos_{1:}_{2:}.png'.format(outputDir,method,threshold))


# In[ ]:



csss = []
for energy in ['30','25','20']:
    css = tasks.DrawRatios(energy)
    names = ['ratio_dist','ratio_primary','ratio_both']
    for n,cs in enumerate(css):
        cs[0].DrawAndSave('{0:}/{1:}_{2:}.png'.format(outputDir,names[n],energy))
    csss.append(css)


# In[ ]:



caloNum = 1
method = 'hitClusterDAQ'
isLogy = False
tasks.timeTag = 'timeLT10'
css = []
tasks.SetLogy(isLogy)
for energy in ['30','25','20']:
    cs = tasks.DrawCmpThresholdOnCalo(caloNum,method,energy,[0,500],legArgs=(0.5,0.7,0.85,0.9))
    css.append(cs)
    css[-1][0].DrawAndSave('{0:}/Cmps_calo_thresholds_{1:}MeV_calo{2:}_{3:}_lowE.png'.format(outputDir,energy,caloNum,method))


# In[ ]:



caloNum = 1
method = 'inFillGainCorrector'
isLogy = False
tasks.timeTag = 'timeLT10'
legArgs=(0.25,0.6,0.85,0.9)
css = []
tasks.SetLogy(isLogy)
for energy in ['30','25','20']:
    cs = tasks.DrawCmpThresholdOnXtals(method,energy,caloNum,legArgs=legArgs)
    css.append(cs)
    css[-1][0].DrawAndSave('{0:}/Cmps_calo_thresholds_{1:}MeV_calo{2:}_{3:}_lowE.png'.format(outputDir,energy,caloNum,method))


# In[ ]:



reload(Tasks)
inputDir = '/Users/cheng/workspace/Data/hadd_readAnaHists_total_cc_makehist_total_0207_v1/'
version = 2
# inputDir = '/Users/cheng/workspace/Data/hadd_readAnaHists_timebin_cc_makehist_891_0119_v2/'
timeTag = 'timeGT30'
outputDir = './output_0207_v1'
subprocess.getstatusoutput('mkdir -p %s'%(outputDir))
tasks = Tasks.TaskCenter(inputDir)
tasks.timeTag = timeTag
tasks.version = version
tasks.Activate()

caloNum = 1;xtalNum=8
method = 'inFillGainCorrector'
isLogy = False
tasks.timeTag = timeTag
css = []
tasks.SetLogy(isLogy)
for energy in ['30','25','20']:
    cs = tasks.DrawCmpThresholdOnXtal(method,energy,caloNum,xtalNum,legArgs=(0.5,0.7,0.85,0.9),xrange=[0,500],rebin=4)
    css.append(cs)
    css[-1][0].DrawAndSave('{0:}/Cmps_calo_thresholds_{1:}MeV_calo{2:}_xtal{3:}_{4:}_lowE.png'.format(outputDir,energy,caloNum,xtalNum,method))


# In[ ]:


caloNum = 1; xtalNum = 30; method = 'inFillGainCorrector'
css = []
tasks.timeTag = 'timeLT10'
for energy in ['30','25','20']:
    cs = tasks.DrawCmpThresholdOnXtal(method,energy,caloNum,xtalNum,xrange=[0,500])
    css.append(cs)
    css[-1][0].DrawAndSave('{0:}/Cmp_xtal_thresholds_{1:}MeV_calo{2:}_xtal{3:}_{4:}.png'.format(outputDir,energy,caloNum,xtalNum,method))


# In[ ]:



reload(Tasks)
inputDir = '/Users/cheng/workspace/Data/hadd_readAnaHists_total_cc_makehist_total_0207_v1/'
version = 2
# inputDir = '/Users/cheng/workspace/Data/hadd_readAnaHists_timebin_cc_makehist_891_0119_v2/'
timeTag = 'timeGT30'
outputDir = './output_0207_v1'
subprocess.getstatusoutput('mkdir -p %s'%(outputDir))
tasks = Tasks.TaskCenter(inputDir)
tasks.timeTag = timeTag
tasks.version = version
tasks.Activate()

caloNum = 1
method = 'hitClusterDAQ'
isLogy = False
tasks.timeTag = timeTag
css = []
tasks.SetLogy(isLogy)
for energy in ['30','25','20']:
    cs = tasks.DrawCmpThresholdOnCalo(caloNum,method,energy,[0,500],legArgs=(0.5,0.7,0.85,0.9),rebin=4)
    css.append(cs)
    css[-1][0].DrawAndSave('{0:}/Cmps_calo_thresholds_{1:}MeV_calo{2:}_{3:}_lowE.png'.format(outputDir,energy,caloNum,method))


# In[ ]:





#Roy Haggerty 6/1/2015
# Code to plot fraction of discharge correlated to spring precip and Max SWE

import pandas as pd
import numpy as np
from datetime import datetime 
from datetime import timedelta
import os
import sys
sys.path.insert(0, 'C:\\code\\maplot\\')
import constants as cst
import imp
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec

def royplot(xf,yf,xf2,yf2,xf_precip,yf_precip,gage_name,select_gage,R2_SWE,R2_PRE):
    fig = plt.figure()
    window = fig.add_subplot(111)
    par = window.twinx()
    colors = np.array(R2_SWE)
    colors_precip = np.array(R2_PRE)
    window.set_ylim(ymax = 1.)
    window.set_ylim(ymin = 0.)
    window.scatter(xf,yf,marker='H',s=60,c=colors, cmap=cm.Blues)
    window.scatter(xf_precip,yf_precip,marker='v',s=60,c=colors_precip, cmap=cm.Reds)
    par.plot(xf2, yf2, 'k')
    #window.legend([line1, line2], ['$Correlation$', '$Discharge$'],loc='best',frameon=False)
    window.set_title(gage_name + ' Gage # '+str(select_gage)+'\n')
    window.set_ylabel("$Fraction\, discharge\, correlated\, to\, Max\, SWE\, or\, F-J\, Precip,$ [-]", fontsize=14)
    window.set_xlabel("$Julian\, Day$", fontsize=14)
    window.set_xlim(150,310)
    par.set_ylabel("$Avg\, Discharge\,$[m$^{\t{3}}$/s]", fontsize=14)
    #plt.show()
    graph_name_png = 'PRE-SWE '+gage_name + ' Gage # '+str(select_gage)+'.png'
    plt.savefig(path_pngs+graph_name_png, format="png", dpi=300)
    plt.close(1)
    #ax.plot(doy_range,mean_discharge)

def fig3plot_wk(doyloop,gage_name,data_and_gage_list,
                 Q_data0,slope_data,p_value,
                 R2,frac,ymax,marker, color, title, label2, label3):
#    fig = plt.figure(1, figsize=(6.4,8.))
    fig = plt.figure(1)
    nf = len(gage_name)
    print nf
    width_ratios=   [1.]*nf
    height_ratios = [1.2]*nf
    wspace = 0.     # horizontal space btwn figs
    hspace = 0.     # vertical space btwn figs

    ###### Figure canvas 
    gs1 = gridspec.GridSpec(nf,1, width_ratios=width_ratios,
                            height_ratios=height_ratios,
                            wspace = wspace)
        
#    gs1.update(left=0.1, right = 2.9, wspace=wspace, hspace = hspace)

    for ifig in range(nf):
        window = fig.add_subplot(gs1[ifig,0])
        x = data_and_gage_list[ifig][:,0]
        y = data_and_gage_list[ifig][:,2]*cst.cfs_to_m3
        window.scatter(x,y,marker=marker,color=color, edgecolor='k')
        x2 = np.array([0.,x.max()])
        y2 = np.array([Q_data0[ifig],slope_data[ifig]*x2[1] + Q_data0[ifig]])
        y2 = y2*cst.cfs_to_m3
        window.plot(x2,y2,'k')
        window.set_xlim(xmin=0.)
        window.set_ylim(ymin = 0.)
        window.set_ylim(ymax = ymax[ifig]*1.6*cst.cfs_to_m3)
        max_yticks = 5
        yloc = plt.MaxNLocator(max_yticks)
        window.yaxis.set_major_locator(yloc)
        props = dict(boxstyle='round', facecolor='white', alpha=0.5, lw=0)        
        window.text(0.05, 0.90, gage_name[ifig]+'\n'+
                    '$discharge fraction\,=\,$'+"{0:.2f}".format(frac[ifig])+', '+
                    '$r^{\t{2}}\,=\,$'+"{0:.2f}".format(R2[ifig])+', '+
                    '$p\,=\,$'+"{0:.3f}".format(p_value[ifig]),
                    verticalalignment='top', horizontalalignment='left',
                    transform=window.transAxes,
                    fontsize=9,bbox=props)

#        window.text(0.05, 0.80, 
#                    '$discharge fraction\,=\,$'+"{0:.2f}".format(frac[ifig])+', '+
#                    '$r^{\t{2}}\,=\,$'+"{0:.2f}".format(R2[ifig])+', '+
#                    '$p\,=\,$'+"{0:.3f}".format(p_value[ifig]),
#                    verticalalignment='top', horizontalalignment='left',
#                    transform=window.transAxes,
#                    fontsize=9)
        yticks = window.yaxis.get_major_ticks()
        yticks[0].label1.set_visible(False)

        if ifig == 0: 
            window.set_title(title+'\n')
        elif ifig == nf/2:
            window.set_ylabel(label2, fontsize=16)
        if ifig == nf-1:
            window.set_xlabel(label3)
        if ifig != nf-1:
            window.set_xticklabels([])
#    window.show()

    graph_name_png = 'Figure 3 '+title+'.png'
    plt.savefig(path_pngs+graph_name_png, format="png", dpi=300)
    plt.close(1)

#    graph_name_png = 'PRE-SWE '+gage_name + ' Gage # '+str(select_gage)+'.png'
#    plt.savefig(path_pngs+graph_name_png, format="png", dpi=300)
#    plt.close(1)
    #ax.plot(doy_range,mean_discharge)


def fig3plot(doyloop,gage_name,snow_and_gage_list,precip_and_gage_list,
                 Q_SWE0,Q_PRE0,slope_SWE,slope_PRE,p_value_SWE,p_value_PRE,
                 R2_SWE,R2_PRE,SWE_frac,PRE_frac):
    
    ymax_snow = [np.max(snow_and_gage_list[i][:,2]) for i in range(len(snow_and_gage_list))]
    ymax_precip = [np.max(precip_and_gage_list[i][:,2]) for i in range(len(precip_and_gage_list))]
    ymax = [np.max([ymax_snow[i],ymax_precip[i]]) for i in range(len(precip_and_gage_list))]
    data_and_gage_list = snow_and_gage_list
    Q_data0 =Q_SWE0
    slope_data =slope_SWE
    p_value =p_value_SWE
    R2 =R2_SWE
    frac = SWE_frac
    marker = 'H'
    color = 'blue'
    title ='Discharge vs Max SWE'
    label2 = '$Discharge \,$[m$^{\t{3}}$/s]'
    label3 ='$Frac\, normal\, Max\, SWE\,$[-]'
    
    fig3plot_wk(doyloop,gage_name,data_and_gage_list,
                 Q_data0,slope_data,p_value,
                 R2,frac,ymax, marker,color, title, label2, label3)
                 
    data_and_gage_list = precip_and_gage_list
    Q_data0 =Q_PRE0
    slope_data =slope_PRE
    p_value =p_value_PRE
    R2 = R2_PRE
    frac = PRE_frac
    marker = 'v'
    color = 'red'
    title ='Discharge vs Spr Precip'
    label2 = '$Discharge \,$[m$^{\t{3}}$/s]'
    label3 ='$Frac\, normal\, spring\, Precip\,$[-]'
    
    fig3plot_wk(doyloop,gage_name,data_and_gage_list,
                 Q_data0,slope_data,p_value,
                 R2,frac,ymax,marker,color, title, label2, label3)



path_gage   = 'C:\\code\usgs-gauges\\gageroutines.py'
path_gage_data = 'C:\\code\\Willamette Basin gauge data\\'
path_snow   = 'C:\\code\usgs-gauges\\snowroutines.py'
path_snow_data = 'C:\\code\\Willamette Basin snotel data\\'
path_precip = 'C:\\code\usgs-gauges\\preciproutines.py'
path_pngs = 'C:\\code\\maplot pngs\\fraction discharge through time\\'
gg = imp.load_source('get_gage_data', path_gage)
gg = imp.load_source('get_gage_info', path_gage)
gg = imp.load_source('get_gage_info_dict', path_gage)
gg = imp.load_source('get_discharge_by_doyrange', path_gage)
gg = imp.load_source('reassign_by_yr', path_gage)
snt =imp.load_source('get_snow_data', path_snow)
snt =imp.load_source('MaxSWE_wy_snow_data', path_snow)
snt =imp.load_source('basin_index_doy', path_snow)
pp = imp.load_source('get_precip_data','C:\\code\\usgs-gauges\\preciproutines.py')
pp = imp.load_source('get_precip_by_moyrange','C:\\code\\usgs-gauges\\preciproutines.py')
pp = imp.load_source('reassign_by_wyr','C:\\code\\usgs-gauges\\preciproutines.py')
pp = imp.load_source('basin_index','C:\\code\\usgs-gauges\\preciproutines.py')
# Get Q through summer
# Calculate correlations through summer
  # 1. Correlations Q to Precip
  # 2. Correlations Q to Max SWE

# Names:
gage_tuple = {
"McK_Belknap"       : 14158850,
"McK_Clear_Lake"    : 14158500,
"McK_Vida"          : 14162500,
"Will_Portland"     : 14211720,
"Will_Salem"        : 14191000,
"So_Sant_Waterloo"  : 14187500,
"Clack_Three_Lynx"  : 14209500,
"Marys"             : 14171000,
"Luckiamute"        : 14190500}
Calapooia = 14173500

#example_gage_names = ['McK_Clear_Lake','McK_Vida','So_Sant_Waterloo','Luckiamute','Will_Portland']
example_gage_names = ['Will_Portland']
significance_cutoff = 0.1

test = False
fig3 = True
select_gage = gage_tuple["Will_Portland"]

# gage info list, dict
gage_info = gg.get_gage_info(local_path= path_gage_data, index_col=[0,1,2,3])
gage_dict = gg.get_gage_info_dict(local_path= path_gage_data)
gage_name = gage_dict[select_gage][0]

if fig3:
    doyloop = 190
    averaging_days = 14
    # snow info, data
    snow_df = snt.get_snow_data(local_path = path_snow_data)
    snow_df = snt.MaxSWE_wy_snow_data(snow_df) #FOR MAX SWE
    snow_basin_index_doy = snt.basin_index_doy(snow_df,doy=270)  # doy 270 = end of Sep
    snow_basin_index = gg.reassign_by_yr(snow_basin_index_doy)

    precip_df = pp.get_precip_data(local_path = 'C:\\code\\Willamette Basin precip data\\')
    precip_by_moyrange = pp.get_value_by_moyrange(precip_df,2,6)
    precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
    precip_basin_index = pp.basin_index(precip_by_wy)
    precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
    precip0_by_moyrange = pp.get_value_by_moyrange(precip_df,10,1)
    precip0_by_wy = pp.reassign_by_wyr(precip0_by_moyrange)
    precip0_basin_index = pp.basin_index(precip0_by_wy)
    precip0_basin_index = gg.reassign_by_yr(precip0_basin_index) #place at end of year
    
    SWE_frac = []
    Q_SWE0 = []
    Q_SWE1= []
    Delta_Q_SWE1 = []
    R2_SWE = []
    p_value_SWE = []
    PRE_frac = []
    Q_PRE0 = []
    Q_PRE1= []
    Delta_Q_PRE1 = []
    R2_PRE = []
    p_value_PRE = []
    mean_discharge = []
    gage_name = []
    snow_and_gage_list = []
    precip_and_gage_list = []
    all_three_list = []
    slope_SWE = []
    slope_PRE = []
    for gage in example_gage_names:
        select_gage = gage_tuple[gage]
        gage_name.append(gage_dict[select_gage][0])
        print 'working on '+ gage_dict[select_gage][0]
        gage_data_df = gg.get_gage_data(select_gage, local_path= path_gage_data).drop(["Gage number","Data-value qualification code"],axis=1) 
        gage_df_doy = gg.get_discharge_by_doyrange(select_gage, doyloop,doyloop+averaging_days, 
             file_name = '', index_col = 2, 
             local_path = path_gage_data)
        gage_df = gg.reassign_by_yr(gage_df_doy)
        snow_and_gage_df = pd.concat([snow_basin_index,gage_df],axis=1)
        snow_and_gage = np.array(snow_and_gage_df.dropna(axis=0, how='any'))
        snow_and_gage_list.append(snow_and_gage)
        precip_and_gage_df = pd.concat([precip_basin_index,gage_df],axis=1)
        precip_and_gage = np.array(precip_and_gage_df.dropna(axis=0, how='any'))
        precip_and_gage_list.append(precip_and_gage)
        ##########################
        from sklearn import linear_model
        from statsmodels.formula.api import ols
        all_three_df = pd.concat([snow_basin_index,precip_basin_index,precip0_basin_index,gage_df],axis=1)
        all_three_df.drop("Gage number",axis=1,inplace=True)
        SWE = all_three_df[0]
        precipSpr = all_three_df[1]
        precipFW = all_three_df[2]
        gage = all_three_df["Discharge (cfs)"]
        all_three_df.columns = ["SWE","precipSpr","precipFW","gage"]
        formula = 'gage ~ SWE + precipSpr + precipFW + precipSpr*precipFW'
        lm = ols(formula, all_three_df).fit()
        print lm.summary()
        assert False
        ##############################
        # slope, intercept, r_value, p_value, std_err
        regression_stats_sg = stats.linregress(snow_and_gage[:,0],snow_and_gage[:,2]) 
        slope = regression_stats_sg[0]
        slope_SWE.append(slope)
        p_value = regression_stats_sg[3]
        regression_stats_sg_precip = stats.linregress(precip_and_gage[:,0],precip_and_gage[:,2]) 
        slope_precip = regression_stats_sg_precip[0]
        slope_PRE.append(slope_precip)
        slope_precip = regression_stats_sg_precip[0]
        p_value_precip = regression_stats_sg_precip[3]
        mean_discharge.append(gage_df_doy["Discharge (cfs)"].mean())
        Q_SWE0.append(regression_stats_sg[1])
        Delta_Q_SWE1.append(slope)
        Q_SWE1.append(slope + regression_stats_sg[1])
        R2_SWE.append(regression_stats_sg[2]*regression_stats_sg[2])
        p_value_SWE.append(regression_stats_sg[3])
        SWE_frac.append(Delta_Q_SWE1[-1]/Q_SWE1[-1])
        Q_PRE0.append(regression_stats_sg_precip[1])
        Delta_Q_PRE1.append(slope_precip)
        Q_PRE1.append(slope_precip + regression_stats_sg_precip[1])
        R2_PRE.append(regression_stats_sg_precip[2]*regression_stats_sg_precip[2])
        p_value_PRE.append(regression_stats_sg_precip[3])
        PRE_frac.append(Delta_Q_PRE1[-1]/Q_PRE1[-1])
        print 'Delta ',slope_precip, 'Q_PRE1 ', slope_precip + regression_stats_sg_precip[1]
    
    fig3plot(doyloop,gage_name,snow_and_gage_list,precip_and_gage_list,
             Q_SWE0,Q_PRE0,slope_SWE,slope_PRE,p_value_SWE,p_value_PRE,
             R2_SWE,R2_PRE,SWE_frac,PRE_frac)
    assert False
    
if not test:
    snow_df = snt.get_snow_data(local_path = path_snow_data)
    snow_df = snt.MaxSWE_wy_snow_data(snow_df) #FOR MAX SWE
    snow_basin_index_doy = snt.basin_index_doy(snow_df,doy=270)  # doy 270 = end of Sep
    snow_basin_index = gg.reassign_by_yr(snow_basin_index_doy)

    precip_df = pp.get_precip_data(local_path = 'C:\\code\\Willamette Basin precip data\\')
    precip_by_moyrange = pp.get_value_by_moyrange(precip_df,2,6)
    precip_by_wy = pp.reassign_by_wyr(precip_by_moyrange)
    precip_basin_index = pp.basin_index(precip_by_wy)
    precip_basin_index = gg.reassign_by_yr(precip_basin_index) #place at end of year
    for select_gage in gage_dict:
#    for idummy in range(0,1):
        gage_name = gage_dict[select_gage][0]
        print 'working on '+ gage_name
        # get info, data for specific gage
        gage_data_df = gg.get_gage_data(select_gage, local_path= path_gage_data).drop(["Gage number","Data-value qualification code"],axis=1) 
        doy_plot = []
        doy_plot_precip = []
        day_start = cst.day_of_year_jun1 
        day_end =   cst.day_of_year_oct31
        doy_range = range(day_start,day_end)
        SWE_frac = []
        Q_SWE0 = []
        Q_SWE1= []
        Delta_Q_SWE1 = []
        R2_SWE = []
        p_value_SWE = []
        PRE_frac = []
        Q_PRE0 = []
        Q_PRE1= []
        Delta_Q_PRE1 = []
        R2_PRE = []
        p_value_PRE = []
        mean_discharge = []
        for doyloop in doy_range:
            mth_name = 'DOY '+ str(doyloop)
            gage_df_doy = gg.get_discharge_by_doyrange(select_gage, doyloop,doyloop+1, 
                 file_name = '', index_col = 2, 
                 local_path = path_gage_data)
            gage_df = gg.reassign_by_yr(gage_df_doy)
            snow_and_gage_df = pd.concat([snow_basin_index,gage_df],axis=1)
            snow_and_gage = np.array(snow_and_gage_df.dropna(axis=0, how='any'))
            precip_and_gage_df = pd.concat([precip_basin_index,gage_df],axis=1)
            precip_and_gage = np.array(precip_and_gage_df.dropna(axis=0, how='any'))
            # slope, intercept, r_value, p_value, std_err
            regression_stats_sg = stats.linregress(snow_and_gage[:,0],snow_and_gage[:,2]) 
            slope = regression_stats_sg[0]
            p_value = regression_stats_sg[3]
            regression_stats_sg_precip = stats.linregress(precip_and_gage[:,0],precip_and_gage[:,2]) 
            slope_precip = regression_stats_sg_precip[0]
            p_value_precip = regression_stats_sg_precip[3]
            mean_discharge.append(gage_df_doy["Discharge (cfs)"].mean())
            if p_value <= significance_cutoff: 
                Q_SWE0.append(regression_stats_sg[1])
                Delta_Q_SWE1.append(slope)
                Q_SWE1.append(slope + regression_stats_sg[1])
                R2_SWE.append(regression_stats_sg[2]*regression_stats_sg[2])
                p_value_SWE.append(regression_stats_sg[3])
                SWE_frac.append(Delta_Q_SWE1[-1]/Q_SWE1[-1])
                doy_plot.append(doyloop)
            if p_value_precip <= significance_cutoff: 
                Q_PRE0.append(regression_stats_sg_precip[1])
                Delta_Q_PRE1.append(slope_precip)
                Q_PRE1.append(slope_precip + regression_stats_sg_precip[1])
                R2_PRE.append(regression_stats_sg_precip[2]*regression_stats_sg_precip[2])
                p_value_PRE.append(regression_stats_sg_precip[3])
                PRE_frac.append(Delta_Q_PRE1[-1]/Q_PRE1[-1])
                doy_plot_precip.append(doyloop)
    
        # Number of samplepoints
        if len(SWE_frac) > 0 or len(PRE_frac) > 0:
            print '# stat sig = ',str(len(SWE_frac)), str(len(PRE_frac))
            yf = SWE_frac
            xf = doy_plot
            yf_precip = PRE_frac
            xf_precip = doy_plot_precip
            yf2 = np.array(mean_discharge)*cst.cfs_to_m3
            xf2 = doy_range
            royplot(xf,yf,xf2,yf2,xf_precip,yf_precip,gage_name,select_gage,R2_SWE,R2_PRE)
else:
    data_tmp = np.array(np.genfromtxt('testdata.csv', delimiter=',',skip_header=1)) # Read csv file
    xf = data_tmp[:,0]
    xf = xf[np.logical_not(np.isnan(xf))]
    yf = data_tmp[:,1]
    yf = yf[np.logical_not(np.isnan(yf))]
    R2_SWE = data_tmp[:,2]
    R2_SWE = R2_SWE[np.logical_not(np.isnan(R2_SWE))]
    xf2 = data_tmp[:,3]
    yf2 = data_tmp[:,4]*cst.cfs_to_m3
#    xf = range(150,300)
#    yf = np.random.random(len(xf))
#    xf2 = xf
#    yf2 = np.array(xf)/2.
    #royplot(xf,yf,xf2,yf2,xf,yf,gage_name,select_gage,R2_SWE)

    fig3plot(xf,yf,xf2,yf2,xf_precip,yf_precip,gage_name,select_gage,R2_SWE,R2_PRE)

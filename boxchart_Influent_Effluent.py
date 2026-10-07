# -*- coding: utf-8 -*-
"""
Created on Sun May 31 17:56:03 2026
Boxplot for comparing the PFAS composition obtained in present study with other data published over the world.


@author: xiang
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import matplotlib.patches as mpatches
from matplotlib.patches import Patch



#setup the font type ans size in plot.
plt.rcParams["font.family"]="Times New Roman"
plt.rcParams.update({"font.size":10})



def autopct_if_big(pct):
    return f'{pct:.1f}%' if pct >= 1.5 else ''




#def function
def remove_zero (list_i):
    """
    remove zero from a list.

    Parameters
    ----------
    list_i : list
        a list containing zero.

    Returns
    -------
    a list without zero

    """
    
    new_list=[i for i in list_i if float (i) != 0.0]
    return new_list




#----------------------------------
#Step 1: extract the data.
#----------------------------------

matrix='Effluent' #select Influent or Effluent.


#import the PFAS data
input_file="C:\Aphd_PFAS in WWTP\DataAnalysis\sample_collection\{0} data summary.csv".format(matrix)
PFAS_df = pd.read_csv(input_file,header=0, index_col=0)
PFAS_df=PFAS_df.fillna(0)


#------------------------
#Extract the data.
#-----------------------
collected_data_df = PFAS_df[PFAS_df['country'] != 'present study']
present_data_df = PFAS_df[PFAS_df['country'] == 'present study']
selected_PFAS=['PFBA', 'PFPeA', 'PFBS', 'PFOA', 'PFOS']
#print(score_present_study_df)

boxchart_data_list=[]
for PFAS_i in selected_PFAS:
    list_i = PFAS_df[PFAS_i].tolist()
    list_i = remove_zero(list_i)
    boxchart_data_list +=[list_i]

#print(len(boxchart_data_list[1]))


scatter_collecteddata_list=[]
for PFAS_i in selected_PFAS:
    list_i = collected_data_df[PFAS_i].tolist()
    list_i = remove_zero(list_i)
    scatter_collecteddata_list +=[list_i]

scatter_presentdata_list=[]
for PFAS_i in selected_PFAS:
    list_i = present_data_df[PFAS_i].tolist()
    list_i = remove_zero(list_i)
    scatter_presentdata_list +=[list_i]

#----------------------------------
#ploting the box chart with scatter
#----------------------------------
color_list=['grey', 'red']
label_list=['Collected data', 'Data of the present study']

fig, axe = plt.subplots(figsize=(4.0, 4.0))
#adjust spline line width
for spine in axe.spines.values():
    spine.set_linewidth(0.7)


   
    
#plot scatter plots.
#add all datapoints
#define the mean marker and properties.
meanprops={'marker':'o', 'markerfacecolor':'blue', 'markeredgecolor':'blue', 'markersize':2.0, 'linewidth':0.5, 'zorder':1}
# define outlier properties
flierprops = dict(marker='o', markersize=1.5, markeredgewidth=0.2, markeredgecolor='black', markerfacecolor='red')
x_tick_index=[i+1 for i in range(len(selected_PFAS))]


for i, g in enumerate(scatter_collecteddata_list):
    y = g
    x = np.random.normal(x_tick_index[i], 0.06, size=len(y))  # spread points
    if i < 4:
        plt.scatter(x, y, color='gray', s=0.6, zorder=3)
    else:
        plt.scatter(x, y, color='gray', s=0.6, label=label_list[0], zorder=3)
    
    
for i, g in enumerate(scatter_presentdata_list):
    y = g
    x = np.random.normal(x_tick_index[i], 0.06, size=len(y))  # spread points
    if i < 4:
        plt.scatter(x, y, color='red', s=1.5, zorder=3)
    else:
        plt.scatter(x, y, color='red', s=1.5, label=label_list[1], zorder=3)


    
#plot box plot
bplot=plt.boxplot(boxchart_data_list, positions=x_tick_index, widths=0.5, patch_artist=True, showmeans=True, meanprops=meanprops, showfliers=False, boxprops={'linewidth':0.5, 'zorder':1}, whiskerprops=dict(linewidth=0.5, zorder=1), capprops=dict(linewidth=0.5, zorder=1), medianprops=dict(color='black', zorder=1, linewidth=0.5))
for patch, color in zip(bplot['boxes'], ['lightblue']*len(selected_PFAS)):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)
    
    
   
if matrix =='Influent':
    plt.legend(fontsize=9, loc='upper left',  ncol=2, frameon=False, bbox_to_anchor=(0.0, 0.1))



axe.set_xticks(x_tick_index)
axe.set_xticklabels(selected_PFAS, fontsize=9, rotation=0)


plt.yscale('log')
axe.set_ylim(0.01, 15000)
#axe.set_yticks([-1, 0, 1, 2, 3, 4])
axe.set_ylabel('Concentration (ng L'+'\u207b'+'\u00b9)', fontsize=9)




# Adjust layout to prevent titles and labels from overlapping
plt.savefig("{0}_PFAS composition_comparison_boxplot.jpg".format(matrix), dpi=900, bbox_inches='tight')
# Display the plot
plt.show()










print("The end of this program.")
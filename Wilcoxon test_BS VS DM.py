# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 08:15:03 2026

Wilcoxon rank-sum test/Wilcoxon signed-rank test for the study: PFAS in WWTP.
Wilcoxon rank-sum test for paried groups of independent; Wilcoxon signed-rank test for paried groups of related.
Test the difference between BS and DM in terms of influent, effluent, and biosolid.
@author: xiang
"""

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from scipy.stats import mannwhitneyu





dataset_file="C:\Aphd_PFAS in WWTP\DataAnalysis\significance test\Wilcoxon\Source Data Table_PFAS in BS and DM WWTP.csv"
PFAS_df = pd.read_csv(dataset_file,header=0, index_col=0)



short_PFAS=['PFBA', 'PFPeA', 'PFHxA', 'PFHpA', 'PFBS', 'PFPeS']
long_PFAS=['PFOA', 'PFNA', 'PFDA', 'PFUdA', 'PFDoA', 'PFHxS', 'PFHpS', 'PFOS', 'PFDS']
precursors=['6:2FTS', 'N-MeFOSAA', 'N-EtFOSAA']
total_PFAS=[*short_PFAS, *long_PFAS, *precursors]


#calculate the total short-chain, long-chain, and precursors.
#Here we treat all the qualitative data D and ND as zero for the convenience of calculation.
PFAS_df['Sum_short_PFAS']=PFAS_df[short_PFAS].sum(axis=1)
PFAS_df['Sum_long_PFAS']=PFAS_df[long_PFAS].sum(axis=1)
PFAS_df['Sum_precursor']=PFAS_df[precursors].sum(axis=1)
PFAS_df['Sum_PFAS']=PFAS_df[total_PFAS].sum(axis=1)

PFAS_df=PFAS_df.set_index('Sample')


#print(PFAS_df['Sum_PFAS'])


#---------------------------------------------------
#test the difference between BS VS, DM, using Wilcoxon signed-rank test.
#--------------------------------------------------
para_list=['Sum_PFAS', 'Sum_short_PFAS', 'Sum_long_PFAS', 'Sum_precursor']
IN_list=['BS1', 'DM1']
EF_list=['BS7', 'DM7']
BIO_list=['BS8', 'DM8']

Wilcoxon_results={}
P_list=[]
statistic_list=[]
id_list=[]
 
for WWTP_i in ['IN', "EF", 'BIO']:
    if WWTP_i =='IN':
        WWTP_list=IN_list
    elif WWTP_i =='EF':
        WWTP_list=EF_list
    elif WWTP_i =='BIO':
        WWTP_list=BIO_list
        
    for para_i in para_list:
        BS_df=PFAS_df.loc[WWTP_list[0], :]
        DM_df=PFAS_df.loc[WWTP_list[1], :]
        
        BS_para_i = BS_df[para_i].to_numpy()
        DM_para_i = DM_df[para_i].to_numpy()
        
        #print(BS_para_i)
        
        statistic_i, p_value_i = mannwhitneyu(BS_para_i, DM_para_i, alternative='two-sided')
        sample_i='BS VS DM '+ WWTP_i + " "+ para_i
        
        P_list +=[round(p_value_i, 4)]
        statistic_list +=[statistic_i]
        id_list +=[sample_i]
        

Wilcoxon_results['sample']=id_list
Wilcoxon_results['p_value']=P_list
Wilcoxon_results['statistic']=statistic_list

Wilcoxon_results_df=pd.DataFrame(Wilcoxon_results)

Wilcoxon_results_df.to_csv('Wilcoxon signed-rank test_BS VS DM.csv')


print(Wilcoxon_results_df)
    


print('The end of this program.')
        
        



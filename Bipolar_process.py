#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import math
import os

import warnings
warnings.filterwarnings("ignore")


def cad_genotype_code(x1, x2, x3, y):
    if y == x1:
        return 2  #2
    elif y == x2:
        return 1  #1
    elif y == x3:
        return 0  #0
    else :
        return np.NaN


xls = pd.ExcelFile('Bipolar PRS calci.xlsx')
df = pd.read_excel(xls, 'Sheet1')


xls = pd.ExcelFile('BIPOLAR DEMO DATA.xlsx')
Bipolar_samples_df = pd.read_excel(xls, 'Sheet1')

df = df.dropna()
col_list = ['condition name',
 'genes',
 'uniqueid',
 'RAF',
 'OR',
 'Risk Allele',
 'Genotpye call Dose 2',
 'Genotpye call Dose 1',
 'Genotpye call Dose 0']

template_df = df[col_list]

for sample_id in list(Bipolar_samples_df.columns):
    print(sample_id)
    temp_df = pd.concat([template_df, Bipolar_samples_df[sample_id]], axis=1).dropna()
    temp_df["CAD Genotype code_cal"] = temp_df[['Genotpye call Dose 2', 'Genotpye call Dose 1', 'Genotpye call Dose 0', sample_id]].apply(lambda x: cad_genotype_code(x['Genotpye call Dose 2'], x["Genotpye call Dose 1"], x["Genotpye call Dose 0"], x[sample_id]), axis=1)
    temp_df["Beta_cal"]              = temp_df["OR"].apply(lambda x: math.log(x))
    temp_df["Population score_cal"]  = temp_df[["Beta_cal", 'RAF']].apply(lambda x: (x['Beta_cal'] * x['RAF']), axis = 1)
    temp_df["Zero center score_cal"] = temp_df[["Beta_cal", "CAD Genotype code_cal", 'Population score_cal']].apply(lambda x: ((x["Beta_cal"] * x["CAD Genotype code_cal"])-x['Population score_cal']), axis = 1)
    temp_df["z score_cal"] = temp_df["Zero center score_cal"]/(temp_df["Population score_cal"].std())
    temp_df["Population score_std"] = temp_df["Population score_cal"].std()
    temp_df["z score avg"] = temp_df["z score_cal"].mean()
    
    path = "Bipolar_Outputs"
    if not os.path.exists(path):
        os.makedirs(path)
    sample_file_name = path + "/" + "Bipolar_" + str(sample_id) + ".csv"
    temp_df.to_csv(sample_file_name, index= False)


# In[ ]:





import numpy as np
import pandas as pd
import scipy.stats as stats
import math
from scipy.stats import norm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def Multivar_AB_Testing(dataframe, page_name, group, target):
    
    dataframe = Data_Prep(dataframe, group, target)
    
    # extract unique groups
    groups = []
    for g in dataframe[group].unique():
        df = dataframe[dataframe[group]==g]
        groups.append(df[target].values)
    
    # perform one-way ANOVA
    anova = stats.f_oneway(*groups)
    
    if anova[1] < 0.05: # if p<0.05, then at least one of the mean values is significantly different
        
        # perform Tukey's test
        tukey = pairwise_tukeyhsd(endog=dataframe[target],
                                  groups=dataframe[group],
                                  alpha=0.05)
        df_tukey = pd.DataFrame(data=tukey._results_table.data[1:], 
                                columns=tukey._results_table.data[0])
        
        # fetch the info about the groups and merge
        df_info = pd.read_csv("static/pages_info_legacy.csv", usecols=["page.version", "group.codes"])
        df_info = df_info[df_info['page.version'].str.contains(page_name.lower())]
        df_info['page.version.num'] = df_info['page.version'].str.split('.').str[1]
        df = df_tukey.merge(df_info, left_on="group1", right_on="page.version.num").merge(df_info, left_on="group2", right_on="page.version.num")
        df = df[["group1", "group.codes_x", "group2", "group.codes_y", "meandiff", "lower", "upper", "p-adj", "reject"]]
        df = df.rename({'group.codes_x': 'group1.codes', 'group.codes_y': 'group2.codes'}, axis=1)
        
        df1 = dataframe.groupby('group', as_index=False)[target].mean()
        df2 = dataframe.groupby('group', as_index=False).size()
        df3 = dataframe.groupby('group', as_index=False)[target].std()
        
        df = (df.merge(df1, left_on="group1", right_on="group")
               .merge(df1, left_on="group2", right_on="group")
               .merge(df2, left_on='group1', right_on="group")
               .merge(df2, left_on='group2', right_on="group")
               .merge(df3, left_on='group1', right_on="group")
               .merge(df3, left_on='group2', right_on="group"))
        
        df = df.drop(['group_x', 'group_y', 'group_x', 'group_y', 'group_x', 'group_y'], axis=1)
        df.columns = ['group1', 'group1.codes', 'group2', 'group2.codes', 'meandiff', 'lower', 'upper',
               'p-adj', 'reject', 'mean.group1', 'mean.group2', 'size.group1', 'size.group2',
               'std.group1', 'std.group2']
        sd_pooled = math.sqrt((df['mean.group1'].std()**2 + df['mean.group2'].std()**2)/2)
        
        df['effect_size'] = df.meandiff / sd_pooled
        df['power_size'] = np.round(norm.cdf(-1.96 + df['effect_size'] / 
                             np.sqrt(df['std.group1']**2 / df['size.group1'] + 
                                       df['std.group2']**2 / df['size.group2'])), 5)
        df = df[["group1", "group1.codes", "group2", "group2.codes",
                 "meandiff", "lower", "upper", "p-adj", "reject", "effect_size", "power_size"]]
        
    else:  # if p>0.05
        return "There is no significant difference across the means"

    return df

def Data_Prep(dataframe, group, target):
    
    dataframe[group] = dataframe[group].apply(str)
    
    def is_outlier(s):
        Q1 = s.quantile(0.25)
        Q3 = s.quantile(0.75)
        IQR = Q3 - Q1
        lower_limit = Q1 - 1.5 * IQR
        upper_limit = Q3 + 1.5 * IQR
        
        return ~s.between(lower_limit, upper_limit)
    
    # Remove outliers
    dataframe = dataframe[~dataframe.groupby(group)[target].apply(is_outlier)]
    dataframe.reset_index(drop=True, inplace=True)
    
    return dataframe
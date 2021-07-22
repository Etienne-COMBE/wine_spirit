import pandas as pd
from scipy.stats import zscore, iqr

def cleaning_web_df(web_df):
    web_df_clean = web_df.dropna(axis=1, how = 'all')

    web_df_clean = web_df_clean.drop(columns=['virtual', 'downloadable',
                                              'rating_count', 'average_rating',
                                              'post_parent', 'menu_order', 'comment_count'])          
    web_clean = web_df_clean.drop_duplicates(subset='sku')

    web_clean = web_clean.dropna(axis = 0, how = 'all')
    
    web_clean = web_clean.drop(columns='post_mime_type')
    return web_clean

def merge_tables(erp_df, liaison_df, web_df):
    fusion_1 = erp_df.merge(liaison_df, on='product_id')
    fusion = fusion_1.merge(web_df, left_on = ('id_web'), right_on = ('sku'))
    return fusion

def outliers_zscore(fusion, column):
    fusion['z_score'] = zscore(fusion[column])
    outliers_zscore = fusion.query('-2 <= z_score >= 2')
    return outliers_zscore

def outliers_iqr(fusion, column):
    temp = fusion.copy()
    temp['iqr'] = iqr(temp[column])
    temp['q1'] = temp[column].quantile(0.25)
    temp['q3'] = temp[column].quantile(0.75)
    outliers_iqr = temp.query('(q1 - 1.5*iqr) <= price >= (q3 + 1.5*iqr)')
    return outliers_iqr
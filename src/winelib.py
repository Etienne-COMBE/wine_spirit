import pandas as pd

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
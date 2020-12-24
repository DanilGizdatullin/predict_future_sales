import os

import pandas as pd
import numpy as np

PATH_TO_DATA = './processed_data/'


def add_shops_items_category_features(df):
    items = pd.read_csv(os.path.join(PATH_TO_DATA, 'items_preprocessed.csv'))
    categories = pd.read_csv(os.path.join(PATH_TO_DATA, 'item_categories_preprocessed.csv'))
    shops = pd.read_csv(os.path.join(PATH_TO_DATA, 'shops_preprocessed.csv'))

    df = pd.merge(df, shops, on='shop_id', how='left')
    df = pd.merge(df, items, on='item_id', how='left')
    df = pd.merge(df, categories, on='item_category_id', how='left')

    df['shop_city'] = df['shop_city'].astype(np.int8)
    df['shop_category'] = df['shop_category'].astype(np.int8)
    df['item_category_id'] = df['item_category_id'].astype(np.int8)
    df['type_code'] = df['type_code'].astype(np.int8)
    df['subtype_code'] = df['subtype_code'].astype(np.int8)
    return df


def add_lag_feature(df, lags, col):
    temp = df[['date_block_num', 'shop_id', 'item_id', col]]
    for i in lags:
        shifted = temp.copy()
        shifted.columns = ['date_block_num', 'shop_id', 'item_id', col + '_lag_' + str(i)]
        shifted['date_block_num'] += i
        df = pd.merge(df, shifted, on=['date_block_num', 'shop_id', 'item_id'], how='left')
    return df


def add_mean_encoded_features(df):
    # date mean lag 1
    group = df.groupby(['date_block_num']).agg({'item_cnt_month': ['mean']})
    group.columns = ['date_avg_item_cnt']
    group.reset_index(inplace=True)
    df = pd.merge(df, group, on=['date_block_num'], how='left')
    df['date_avg_item_cnt'] = df['date_avg_item_cnt'].astype(np.float16)
    df = add_lag_feature(df, [1], 'date_avg_item_cnt')
    df.drop(['date_avg_item_cnt'], axis=1, inplace=True)

    # date item mean lag 1, 2, 3
    group = df.groupby(['date_block_num', 'item_id']).agg({'item_cnt_month': ['mean']})
    group.columns = ['date_item_avg_item_cnt']
    group.reset_index(inplace=True)
    df = pd.merge(df, group, on=['date_block_num', 'item_id'], how='left')
    df['date_item_avg_item_cnt'] = df['date_item_avg_item_cnt'].astype(np.float16)
    df = add_lag_feature(df, [1, 2, 3], 'date_item_avg_item_cnt')
    df.drop(['date_item_avg_item_cnt'], axis=1, inplace=True)

    # date shop mean lag 1, 2, 3
    group = df.groupby(['date_block_num', 'shop_id']).agg({'item_cnt_month': ['mean']})
    group.columns = ['date_shop_avg_item_cnt']
    group.reset_index(inplace=True)
    df = pd.merge(df, group, on=['date_block_num', 'shop_id'], how='left')
    df['date_shop_avg_item_cnt'] = df['date_shop_avg_item_cnt'].astype(np.float16)
    df = add_lag_feature(df, [1, 2, 3], 'date_shop_avg_item_cnt')
    df.drop(['date_shop_avg_item_cnt'], axis=1, inplace=True)

    # date mean item_category_id lag 1
    group = df.groupby(['date_block_num', 'item_category_id']).agg({'item_cnt_month': ['mean']})
    group.columns = ['date_cat_avg_item_cnt']
    group.reset_index(inplace=True)
    df = pd.merge(df, group, on=['date_block_num', 'item_category_id'], how='left')
    df['date_cat_avg_item_cnt'] = df['date_cat_avg_item_cnt'].astype(np.float16)
    df = add_lag_feature(df, [1], 'date_cat_avg_item_cnt')
    df.drop(['date_cat_avg_item_cnt'], axis=1, inplace=True)

    # date (shop X item_category_id) lag 1
    group = df.groupby(['date_block_num', 'shop_id', 'item_category_id']).agg({'item_cnt_month': ['mean']})
    group.columns = ['date_shop_cat_avg_item_cnt']
    group.reset_index(inplace=True)
    df = pd.merge(df, group, on=['date_block_num', 'shop_id', 'item_category_id'], how='left')
    df['date_shop_cat_avg_item_cnt'] = df['date_shop_cat_avg_item_cnt'].astype(np.float16)
    df = add_lag_feature(df, [1], 'date_shop_cat_avg_item_cnt')
    df.drop(['date_shop_cat_avg_item_cnt'], axis=1, inplace=True)

    # date (shop X subtype) lag 1
    group = df.groupby(['date_block_num', 'shop_id', 'subtype_code']).agg({'item_cnt_month': ['mean']})
    group.columns = ['date_shop_subtype_avg_item_cnt']
    group.reset_index(inplace=True)
    df = pd.merge(df, group, on=['date_block_num', 'shop_id', 'subtype_code'], how='left')
    df['date_shop_subtype_avg_item_cnt'] = df['date_shop_subtype_avg_item_cnt'].astype(np.float16)
    df = add_lag_feature(df, [1], 'date_shop_subtype_avg_item_cnt')
    df.drop(['date_shop_subtype_avg_item_cnt'], axis=1, inplace=True)

    # date shop_city lag 1
    group = df.groupby(['date_block_num', 'shop_city']).agg({'item_cnt_month': ['mean']})
    group.columns = ['date_city_avg_item_cnt']
    group.reset_index(inplace=True)
    df = pd.merge(df, group, on=['date_block_num', 'shop_city'], how='left')
    df['date_city_avg_item_cnt'] = df['date_city_avg_item_cnt'].astype(np.float16)
    df = add_lag_feature(df, [1], 'date_city_avg_item_cnt')
    df.drop(['date_city_avg_item_cnt'], axis=1, inplace=True)

    # date (item X shop_city) lag 1
    group = df.groupby(['date_block_num', 'item_id', 'shop_city']).agg({'item_cnt_month': ['mean']})
    group.columns = ['date_item_city_avg_item_cnt']
    group.reset_index(inplace=True)
    df = pd.merge(df, group, on=['date_block_num', 'item_id', 'shop_city'], how='left')
    df['date_item_city_avg_item_cnt'] = df['date_item_city_avg_item_cnt'].astype(np.float16)
    df = add_lag_feature(df, [1], 'date_item_city_avg_item_cnt')
    df.drop(['date_item_city_avg_item_cnt'], axis=1, inplace=True)

    # date (shop X item) lag 1
    group = df.groupby(['date_block_num', 'shop_id', 'item_id']).agg({'item_cnt_month': ['mean']})
    group.columns = ['date_shop_item_avg_item_cnt']
    group.reset_index(inplace=True)
    df = pd.merge(df, group, on=['date_block_num', 'shop_id', 'item_id'], how='left')
    df['date_shop_item_avg_item_cnt'] = df['date_shop_item_avg_item_cnt'].astype(np.float16)
    df = add_lag_feature(df, [1], 'date_shop_item_avg_item_cnt')
    df.drop(['date_shop_item_avg_item_cnt'], axis=1, inplace=True)
    return df


def add_trend_features(df, train):
    # add revenue feature
    train['revenue'] = train['item_price'] * train['item_cnt_day']

    # mean item price whole dataset
    group = train.groupby(['item_id']).agg({'item_price': ['mean']})
    group.columns = ['item_avg_item_price']
    group.reset_index(inplace=True)
    df = pd.merge(df, group, on=['item_id'], how='left')
    df['item_avg_item_price'] = df['item_avg_item_price'].astype(np.float16)

    # mean item price by date
    group = train.groupby(['date_block_num', 'item_id']).agg({'item_price': ['mean']})
    group.columns = ['date_item_avg_item_price']
    group.reset_index(inplace=True)
    df = pd.merge(df, group, on=['date_block_num', 'item_id'], how='left')
    df['date_item_avg_item_price'] = df['date_item_avg_item_price'].astype(np.float16)

    lags = [1, 2, 3]
    df = add_lag_feature(df, lags, 'date_item_avg_item_price')

    for i in lags:
        df['delta_price_lag_' + str(i)] = ((df['date_item_avg_item_price_lag_'+str(i)]
                                            - df['item_avg_item_price']) / df['item_avg_item_price'])

    def select_trend(row):
        for lag in lags:
            if row['delta_price_lag_' + str(lag)]:
                return row['delta_price_lag_' + str(lag)]
        return 0

    df['delta_price_lag'] = df.apply(select_trend, axis=1)
    df['delta_price_lag'] = df['delta_price_lag'].astype(np.float16)
    df['delta_price_lag'].fillna(0, inplace=True)

    features_to_drop = ['item_avg_item_price', 'date_item_avg_item_price']
    for i in lags:
        features_to_drop += ['date_item_avg_item_price_lag_' + str(i)]
        features_to_drop += ['delta_price_lag_' + str(i)]

    df.drop(features_to_drop, axis=1, inplace=True)

    group = train.groupby(['date_block_num', 'shop_id']).agg({'revenue': ['sum']})
    group.columns = ['date_shop_revenue']
    group.reset_index(inplace=True)

    df = pd.merge(df, group, on=['date_block_num', 'shop_id'], how='left')
    df['date_shop_revenue'] = df['date_shop_revenue'].astype(np.float32)

    group = group.groupby(['shop_id']).agg({'date_shop_revenue': ['mean']})
    group.columns = ['shop_avg_revenue']
    group.reset_index(inplace=True)

    df = pd.merge(df, group, on=['shop_id'], how='left')
    df['shop_avg_revenue'] = df['shop_avg_revenue'].astype(np.float32)

    df['delta_revenue'] = (df['date_shop_revenue'] - df['shop_avg_revenue']) / df['shop_avg_revenue']
    df['delta_revenue'] = df['delta_revenue'].astype(np.float16)

    df = add_lag_feature(df, [1], 'delta_revenue')

    df.drop(['date_shop_revenue', 'shop_avg_revenue', 'delta_revenue'], axis=1, inplace=True)

    return df


def add_month_and_days_in_month(df):
    df['month'] = df['date_block_num'] % 12

    days = pd.Series([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    df['days'] = df['month'].map(days).astype(np.int8)

    df['item_shop_first_sale'] = df['date_block_num'] - df.groupby(['item_id', 'shop_id'])['date_block_num'].transform('min')
    df['item_first_sale'] = df['date_block_num'] - df.groupby('item_id')['date_block_num'].transform('min')

    return df

if __name__ == '__main__':
    complete_df = pd.read_csv(os.path.join(PATH_TO_DATA, 'complete_dataframe.csv'))

    complete_df['date_block_num'] = complete_df['date_block_num'].astype(np.int8)
    complete_df['shop_id'] = complete_df['shop_id'].astype(np.int8)
    complete_df['item_id'] = complete_df['item_id'].astype(np.int16)

    complete_df = add_shops_items_category_features(complete_df)
    complete_df = add_lag_feature(complete_df, [1, 2, 3], 'item_cnt_month')
    complete_df = add_mean_encoded_features(complete_df)

    train = pd.read_csv(os.path.join(PATH_TO_DATA, 'sales_train_preprocessed.csv'))
    complete_df = add_trend_features(complete_df, train)

    complete_df = add_month_and_days_in_month(complete_df)

    complete_df.to_csv(os.path.join(PATH_TO_DATA, 'complete_dataframe_with_features.csv'), index=False)

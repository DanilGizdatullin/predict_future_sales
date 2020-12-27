import os

import numpy as np
import pandas as pd

PATH_TO_DATA = './processed_data/'
PATH_TO_VALID = './train_validation_test_split/'
PATH_TO_TEST = './train_test_split/'


def final_preparations(df):
    columns_to_fill = {
        'item_cnt_month_lag_1', 'item_cnt_month_lag_2', 'item_cnt_month_lag_3', 'date_avg_item_cnt_lag_1',
        'date_item_avg_item_cnt_lag_1', 'date_item_avg_item_cnt_lag_2', 'date_item_avg_item_cnt_lag_3',
        'date_shop_avg_item_cnt_lag_1', 'date_shop_avg_item_cnt_lag_2', 'date_shop_avg_item_cnt_lag_3',
        'date_cat_avg_item_cnt_lag_1', 'date_shop_cat_avg_item_cnt_lag_1', 'date_shop_subtype_avg_item_cnt_lag_1',
        'date_city_avg_item_cnt_lag_1', 'date_item_city_avg_item_cnt_lag_1', 'date_shop_item_avg_item_cnt_lag_1'
    }
    df = df[df['date_block_num'] > 3].copy()

    def fill_na(df_n):
        for col in df_n.columns:
            if (col in columns_to_fill) and (df_n[col].isnull().any()):
                if col in columns_to_fill:
                    df_n[col] = df_n[col].fillna(0)

    fill_na(df)
    return df


def split_train_valid_test(df):
    x_train = df[df['date_block_num'] < 32].copy().drop(['item_cnt_month'], axis=1)
    y_train = df.loc[df['date_block_num'] < 32, 'item_cnt_month']
    x_valid = df[df['date_block_num'] == 32].copy().drop(['item_cnt_month'], axis=1)
    y_valid = df.loc[df['date_block_num'] == 32, 'item_cnt_month']
    x_test = df[df['date_block_num'] == 33].copy().drop(['item_cnt_month'], axis=1)
    y_test = df.loc[df['date_block_num'] == 33, 'item_cnt_month']
    return x_train, y_train, x_valid, y_valid, x_test, y_test


def split_train_test(df):
    x_train = df[df['date_block_num'] < 34].copy().drop(['item_cnt_month'], axis=1)
    y_train = df.loc[df['date_block_num'] < 34, 'item_cnt_month']
    x_test = df[df['date_block_num'] == 34].copy().drop(['item_cnt_month'], axis=1)
    return x_train, y_train, x_test


complete_df_with_features = pd.read_csv(os.path.join(PATH_TO_DATA, 'complete_dataframe_with_features.csv'))
complete_df_with_features = final_preparations(complete_df_with_features)

x_train, y_train, x_valid, y_valid, x_test, y_test = split_train_valid_test(complete_df_with_features)
np.save(os.path.join(PATH_TO_VALID, 'x_train.npy'), x_train)
np.save(os.path.join(PATH_TO_VALID, 'y_train.npy'), y_train)
np.save(os.path.join(PATH_TO_VALID, 'x_valid.npy'), x_valid)
np.save(os.path.join(PATH_TO_VALID, 'y_valid.npy'), y_valid)
np.save(os.path.join(PATH_TO_VALID, 'x_test.npy'), x_test)
np.save(os.path.join(PATH_TO_VALID, 'y_test.npy'), y_test)

x_train, y_train, x_test = split_train_test(complete_df_with_features)
np.save(os.path.join(PATH_TO_TEST, 'x_train.npy'), x_train)
np.save(os.path.join(PATH_TO_TEST, 'y_train.npy'), y_train)
np.save(os.path.join(PATH_TO_TEST, 'x_test.npy'), x_test)

import os

import pandas as pd

PATH_TO_DATA = './data'
PATH_TO_SAVE_PROCESSED_DATA = './processed_data'


def train_test_preprocess():
    train = pd.read_csv(os.path.join(PATH_TO_DATA, 'sales_train.csv'))
    test = pd.read_csv(os.path.join(PATH_TO_DATA, 'test.csv')).set_index('ID')

    # remove outliers
    train = train[train.item_price < 100000]
    train = train[train.item_cnt_day < 1000]
    train = train[train.item_price > 0].reset_index(drop=True)

    # if item_cnt_day less than 1, change it to 0
    train.loc[train.item_cnt_day < 1, 'item_cnt_day'] = 0

    # several shops have the similar name, so merge them into one shop
    train.loc[train.shop_id == 0, 'shop_id'] = 57
    test.loc[test.shop_id == 0, 'shop_id'] = 57
    # Якутск ТЦ "Центральный"
    train.loc[train.shop_id == 1, 'shop_id'] = 58
    test.loc[test.shop_id == 1, 'shop_id'] = 58
    # Жуковский ул. Чкалова 39м²
    train.loc[train.shop_id == 11, 'shop_id'] = 10
    test.loc[test.shop_id == 11, 'shop_id'] = 10

    train.loc[train.shop_id == 40, 'shop_id'] = 39
    test.loc[test.shop_id == 40, 'shop_id'] = 39

    train.to_csv(os.path.join(PATH_TO_SAVE_PROCESSED_DATA, 'sales_train_preprocessed.csv'), index=False)
    test.to_csv(os.path.join(PATH_TO_SAVE_PROCESSED_DATA, 'test_preprocessed.csv'), index=False)

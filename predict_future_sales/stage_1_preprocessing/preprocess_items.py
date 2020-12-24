import os
import re

import pandas as pd
from sklearn.preprocessing import LabelEncoder

PATH_TO_DATA = './data'
PATH_TO_SAVE_PROCESSED_DATA = './processed_data'


def items_preprocess():
    items = pd.read_csv(os.path.join(PATH_TO_DATA, 'items.csv'))

    _, items['item_type'] = items['item_name'].str.split('[', 1).str
    _, items['item_subtype'] = items['item_name'].str.split('(', 1).str

    items['item_type'] = items['item_type'].str.replace('[^A-Za-z0-9А-Яа-я]+', ' ').str.lower()
    items['item_subtype'] = items['item_subtype'].str.replace('[^A-Za-z0-9А-Яа-я]+', ' ').str.lower()
    items = items.fillna('0')

    def name_correction(x):
        x = x.lower()
        x = x.partition('[')[0]
        x = x.partition('(')[0]
        x = re.sub('[^A-Za-z0-9А-Яа-я]+', ' ', x)
        x = x.replace('  ', ' ')
        x = x.strip()
        return x

    items['item_name'] = items['item_name'].apply(lambda x: name_correction(x))
    items['item_type'] = items.item_type.apply(lambda x: x[:-1] if x != '0' else '0')

    items['type'] = items.item_type.apply(lambda x: x[0:8] if x.split(' ')[0] == 'xbox' else x.split(' ')[0])
    items.loc[(items.type == 'x360') | (items.type == 'xbox360'), 'type'] = 'xbox 360'
    items.loc[items.type == '', 'type'] = 'mac'
    items.type = items.type.apply(lambda x: x.replace(' ',''))
    items.loc[(items.type == 'pc') | (items.type == 'pс') | (items.type == 'рс'), 'type'] = 'pc'
    items.loc[(items.type == 'рs3'), 'type'] = 'ps3'

    drop_list = ['5c5', '5c7', '5f4', '6dv', '6jv', '6l6', 'android', 'hm3', 'j72', 'kf6', 'kf7', 'kg4',
                 'ps2', 's3v', 's4v', 'англ', 'русская', 'только', 'цифро']

    items.item_type = items.type.apply(lambda x: 'etc' if x in drop_list else x)
    items = items.drop(['type'], axis=1)

    items['item_type'] = LabelEncoder().fit_transform(items['item_type'])
    items['item_subtype'] = LabelEncoder().fit_transform(items['item_subtype'])
    items.drop(['item_name'], axis=1, inplace=True)
    items.to_csv(os.path.join(PATH_TO_SAVE_PROCESSED_DATA, 'items_preprocessed.csv'), index=False)

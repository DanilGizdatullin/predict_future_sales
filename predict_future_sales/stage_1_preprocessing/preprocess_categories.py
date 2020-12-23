import os

import pandas as pd
from sklearn.preprocessing import LabelEncoder

PATH_TO_DATA = './data'
PATH_TO_SAVE_PROCESSED_DATA = './processed_data'


def categories_preprocess():
    categories = pd.read_csv(os.path.join(PATH_TO_DATA, 'item_categories.csv'))

    categories['type'] = categories.item_category_name.apply(lambda x: x.split(' ')[0]).astype(str)
    categories.loc[(categories.type == 'Игровые') | (categories.type == 'Аксессуары'), 'type'] = 'Игры'
    categories.loc[categories.type == 'PC', 'type'] = 'Музыка'
    valid_category = ['Игры', 'Карты', 'Кино', 'Книги', 'Музыка', 'Подарки', 'Программы', 'Служебные', 'Чистые']
    categories['type'] = categories.type.apply(lambda x: x if (x in valid_category) else 'etc')
    categories['type_code'] = LabelEncoder().fit_transform(categories['type'])

    categories['split'] = categories['item_category_name'].apply(lambda x: x.split('-'))
    categories['subtype'] = categories['split'].map(lambda x: x[1].strip() if len(x) > 1 else x[0].strip())
    categories['subtype_code'] = LabelEncoder().fit_transform(categories['subtype'])

    categories = categories[['item_category_id', 'type_code', 'subtype_code']]
    categories.to_csv(os.path.join(PATH_TO_SAVE_PROCESSED_DATA, 'item_categories_preprocessed.csv'), index=False)

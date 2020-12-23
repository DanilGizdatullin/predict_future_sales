import os
from itertools import product

import numpy as np
import pandas as pd

PATH_TO_DATA = './processed_data/'


def make_complete_dataframe():
    train = pd.read_csv(os.path.join(PATH_TO_DATA, 'sales_train_preprocessed.csv'))
    test = pd.read_csv(os.path.join(PATH_TO_DATA, 'test_preprocessed.csv'))

    matrix = []
    cols = ['date_block_num', 'shop_id', 'item_id']

    # prepare sales for each shop for each item by each day
    for i in range(34):
        sales = train[train.date_block_num == i]
        matrix.append(np.array(list(product([i], sales.shop_id.unique(), sales.item_id.unique())), dtype='int16'))

    matrix = pd.DataFrame(np.vstack(matrix), columns=cols)
    matrix['date_block_num'] = matrix['date_block_num'].astype(np.int8)
    matrix['shop_id'] = matrix['shop_id'].astype(np.int8)
    matrix['item_id'] = matrix['item_id'].astype(np.int16)
    matrix.sort_values(cols, inplace=True)

    # group by days
    group = train.groupby(cols).agg({'item_cnt_day': ['sum']})
    group.columns = ['item_cnt_month']
    group.reset_index(inplace=True)

    # add item_cnt_month to matrix
    matrix = pd.merge(matrix, group, on=cols, how='left')
    matrix['item_cnt_month'] = (matrix['item_cnt_month']
                                .fillna(0)
                                .clip(0, 20)
                                .astype(np.float16))

    test['date_block_num'] = 34
    test['date_block_num'] = test['date_block_num'].astype(np.int8)
    test['shop_id'] = test['shop_id'].astype(np.int8)
    test['item_id'] = test['item_id'].astype(np.int16)

    matrix = pd.concat([matrix, test], ignore_index=True, sort=False, keys=cols)
    matrix.fillna(0, inplace=True)
    matrix.to_csv(os.path.join(PATH_TO_DATA, 'complete_dataframe.csv'), index=False)

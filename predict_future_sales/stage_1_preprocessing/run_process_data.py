from predict_future_sales.stage_1_preprocessing.preprocess_categories import categories_preprocess
from predict_future_sales.stage_1_preprocessing.preprocess_items import items_preprocess
from predict_future_sales.stage_1_preprocessing.preprocess_shops import shops_preprocess
from predict_future_sales.stage_1_preprocessing.preprocess_train_test_data import train_test_preprocess
from predict_future_sales.stage_1_preprocessing.preprocess_complete_dataframe import make_complete_dataframe

train_test_preprocess()
categories_preprocess()
items_preprocess()
shops_preprocess()
make_complete_dataframe()
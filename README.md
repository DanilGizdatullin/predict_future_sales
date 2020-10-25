# predict_future_sales
solution https://www.kaggle.com/c/competitive-data-science-predict-future-sales

Change **LOCAL_DATA** variable in *Makefile* to a full path to competition data on your computer.
## 1. Data Preprocessing.
```bash
make build
make process_data
```
or
```bash
python predict_future_sales/stage_1_preprocessing/run_process_data.py
```

1. Process train and test data (*stage_1_preprocessing/preprocess_train_test_data.py*)
    * remove outliers (item_price >= 100000 or item_cnt_day >= 1000 or item_price <= 0)
    * if item_cnt_day less than 1, change it to 0
    * merge some shops into one (because they have similar names)
2. Process categories (*stage_1_preprocessing/preprocess_categories.py*)  
Create type and subtype from *'item_category_name'*. Valid type values are {'Игры', 'Карты', 'Кино', 'Книги', 'Музыка', 'Подарки', 'Программы', 'Служебные', 'Чистые', 'etc'}.  
3. Process items (*stage_1_preprocessing/preprocess_items.py*)
    * get only letters and numbers from *item_name*
    * try to get item type by process *item_name* column
4. Process shops (*stage_1_preprocessing/preprocess_shops.py*)  
Get shop category from *shop_name* column and process shop city.
5. Process complete dataframe (*stage_1_preprocessing/preprocess_complete_dataframe.py*)  
    * create a dataframe with 34 days and for each day we have the Cartesian product of all shop_id and item_id. We call this dataframe **complete**
    * group train data by day, shop id and item_id and join this dataframe with complete dataframe
    * 

It creates new files in *processed_data* directory:
* item_categories_preprocessed.csv
* sales_train_preprocessed.csv
* test_preprocessed.csv
* items_preprocessed.csv
* shops_preprocessed.csv  

## 2. 

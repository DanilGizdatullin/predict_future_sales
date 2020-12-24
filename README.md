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
   * create 'type' and 'subtype' from *'item_category_name'*. Valid type values are {'Игры', 'Карты', 'Кино', 'Книги', 'Музыка', 'Подарки', 'Программы', 'Служебные', 'Чистые', 'etc'}. 
   * use label encoder on 'type' and 'subtype' to get int values instead of string
   
3. Process items (*stage_1_preprocessing/preprocess_items.py*)
   * get only letters and numbers from *item_name*
   * get 'item_type' and 'item_subtype' by process *item_name* column
   * use label encoder on 'item_type' and 'item_subtype' columns

4. Process shops (*stage_1_preprocessing/preprocess_shops.py*)  
   * get 'shop_category' from 'shop_name' column
   * process 'city' column into new one 'shop_city'
   * use label encoder on 'shop_city' and 'shop_category'
   
5. Process complete dataframe (*stage_1_preprocessing/preprocess_complete_dataframe.py*)  
    * create a dataframe with 34 days and for each day we have the Cartesian product of all shop_id and item_id. We call this dataframe **complete**
    * group train data by day, shop id and item_id and join this dataframe with complete dataframe

As a result we have new files in *processed_data* directory:
* item_categories_preprocessed.csv
* sales_train_preprocessed.csv
* test_preprocessed.csv
* items_preprocessed.csv
* shops_preprocessed.csv  
* complete_dataframe.csv  

## 2. Feature Engineering.
```bash
make feature_engineering
```
or
```bash
python predict_future_sales/stage_2_feature_engineering/run_feature_engineering.py
```

1. Add shop, item and categories features (add_shops_items_category_features)
   * Join complete dataframe with shop, items and categories dataframes
   
2. Add lag features for 'item_cnt_month' (add_lag_feature)
   * Join complete dataframe with itself, but use 'item_cnt_month' value from last month, two months ago and three months ago
   
3. Add mean encoded features (add_mean_encoded_features)
   * Add mean 'item_cnt_month' for a previous month
   * Add mean 'item_cnt_month' for each 'item_id' for the previous three months
   * Add mean 'item_cnt_month' for each 'shop_id' for the previous three months
   * Add mean 'item_cnt_month' for each 'item_category_id' for the previous month
   * Add mean 'item_cnt_month' for each ('shop_id', 'item_category_id') pair for the previous month
   * Add mean 'item_cnt_month' for each ('shop_id', 'subtype_code') pair for the previous month
   * Add mean 'item_cnt_month' for each 'shop_city' for the previous month
   * Add mean 'item_cnt_month' for each ('item_id', 'shop_city') pair for the previous month
   * Add mean 'item_cnt_month' for each ('shop_id', 'item_id') pair for the previous month
   
4. Add trend features (add_trend_features)
   * Add lag features for average month item price (average item price for the previous three months)
   * Add 'delta_price_lag' price from previous (one, two, three months, it depends on which month data is accessible) minus global mean item price and divide it by global mean item price
   * Add delta shop revenue for the previous three months:
      * Revenue is 'item_price' multiply by 'item_cnt_day'
      * Then we get 'date_shop_revenue' is a sum revenue of each shop by one month
      * Then we compute 'shop_avg_revenue' is an average revenue for each shop by whole dataset
      * We can compute 'delta_revenue' by this formula ('date_shop_revenue' - 'shop_avg_revenue') 'shop_avg_revenue'
      * Finally, by applying lag function we get delta_revenue for previous three months
   
5. Add (add_month_and_days_in_month)
   * Add 'month' by dividing 'date_block_num' modulo 12
   * Add number of days in each month ('days' column)
   * Add 'item_shop_first_sale' - how long months ago first sale of current item in current shop was made
   * Add 'item_first_sale' -  how long months ago first sale of current item was made

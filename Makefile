PROJECT_PATH = $(shell pwd)
PROJECT_NAME = predict_future_sales

LOCAL_DATA = /home/danil/projects/courses/how_to_win_kaggle/data
MOUNT_DIR_DATA = $(LOCAL_DATA):/var/www/predict_future_sales/data

LOCAL_MAIN_PATH = $(PROJECT_PATH)/predict_future_sales
MOUNT_DIR_MAIN = $(LOCAL_MAIN_PATH):/var/www/predict_future_sales/predict_future_sales

LOCAL_PROCESSED_DATA = $(PROJECT_PATH)/processed_data
MOUNT_DIR_PROCESSED_DATA = $(LOCAL_PROCESSED_DATA):/var/www/predict_future_sales/processed_data

LOCAL_TRAIN_TEST_DATA = $(PROJECT_PATH)/train_test_split
MOUNT_DIR_TRAIN_TEST_DATA = $(LOCAL_TRAIN_TEST_DATA):/var/www/predict_future_sales/train_test_split

LOCAL_TRAIN_VALIDATION_TEST_DATA = $(PROJECT_PATH)/train_validation_test_split
MOUNT_DIR_TRAIN_VALIDATION_TEST_DATA = $(LOCAL_TRAIN_VALIDATION_TEST_DATA):/var/www/predict_future_sales/train_validation_test_split

build:
	docker build --no-cache -t $(PROJECT_NAME) --file $(PROJECT_PATH)/Dockerfile $(PROJECT_PATH)

CONTAINER_NAME = $(PROJECT_NAME)_container

process_data:
	docker run --rm --name $(CONTAINER_NAME) \
	-v $(MOUNT_DIR_MAIN) \
	-v $(MOUNT_DIR_PROCESSED_DATA) \
	-v $(MOUNT_DIR_DATA) \
	-v $(MOUNT_DIR_TRAIN_TEST_DATA) \
	-v $(MOUNT_DIR_TRAIN_VALIDATION_TEST_DATA) \
	$(PROJECT_NAME) process_data

feature_engineering:
	docker run --rm --name $(CONTAINER_NAME) \
	-v $(MOUNT_DIR_MAIN) \
	-v $(MOUNT_DIR_PROCESSED_DATA) \
	-v $(MOUNT_DIR_DATA) \
	-v $(MOUNT_DIR_TRAIN_TEST_DATA) \
	-v $(MOUNT_DIR_TRAIN_VALIDATION_TEST_DATA) \
	$(PROJECT_NAME) feature_engineering

train_valid_test_split:
	docker run --rm --name $(CONTAINER_NAME) \
	-v $(MOUNT_DIR_MAIN) \
	-v $(MOUNT_DIR_PROCESSED_DATA) \
	-v $(MOUNT_DIR_DATA) \
	-v $(MOUNT_DIR_TRAIN_TEST_DATA) \
	-v $(MOUNT_DIR_TRAIN_VALIDATION_TEST_DATA) \
	$(PROJECT_NAME) train_validation_test_split

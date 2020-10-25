#!/usr/bin/env bash

set -o errexit      # make your script exit when a command fails.
set -o nounset      # exit when your script tries to use undeclared variables.

case "$1" in
  process_data)
    python predict_future_sales/stage_1_preprocessing/run_process_data.py
    ;;
esac
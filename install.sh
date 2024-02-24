#!/bin/bash

# Default values
gpu=false

while getopts ":g:" opt; do
  case $opt in
    g)
      case $OPTARG in
        true|false)
          gpu=$OPTARG
          ;;
        *)
          echo "Invalid value for --gpu. Use 'true' or 'false'."
          exit 1
          ;;
      esac
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

echo "GPU: $gpu"

git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

make LLAMA_CUBLAS=1
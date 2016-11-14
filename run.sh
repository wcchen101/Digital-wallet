#!/usr/bin/env bash

# example of the run script for running the fraud detection algorithm with a python file
# I'll execute my programs, with the input directory paymo_input and output the files in the directory paymo_output
dir=$(PWD)
echo "current path: $dir"
cd $dir/src
python antifraud.py


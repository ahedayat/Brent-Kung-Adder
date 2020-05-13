#!/bin/bash

# Output File Path
out_path='./outputs/64'

# Adder Type
adder_type='brent_kung'

# Bitwidth
bitwidth=64

python main.py  --adder-type $adder_type \
                --path $out_path \
                --bitwidth $bitwidth
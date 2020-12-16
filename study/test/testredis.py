#-*- coding:utf-8 -*-
import argparse
parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--conf_path', type=str, default = None)
parser.add_argument('--scheme_path', type=str, default = None)
parser.add_argument('--package_path', type=int, default=32)
args = parser.parse_args()
print(args.conf_path)

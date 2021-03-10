#!/usr/bin/env python

from eeschema import Sch, Component, TextItem, Sheet

import argparse

parser = argparse.ArgumentParser(description='Insert template schematics to taget schematics.')

parser.add_argument('-t', '--template-sch', action="store", required=True, help='Template to inject.')
parser.add_argument('-i', '--target-sch', action="store", required=True, help='Target schema.')
parser.add_argument('-o' ,'--output-sch', action="store", default=None, help='Output schema.')
parser.add_argument('-p' ,'--posXY', nargs=2, action="store", default=(1000, 1000), help='Position in target.')
parser.add_argument('-s' ,'--sizeXY', nargs=2, action="store", default=(1600, None), help='Size in target.')

args = parser.parse_args()

template_fn = args.template_sch
target_fn, output_fn = args.target_sch, args.output_sch
pos, size = args.posXY, args.sizeXY

if not output_fn:
    output_fn = target_fn

template_fn_short = template_fn.split('/')[-1]


target = Sch.load(target_fn)
target.insertSubsheet('.'.join(template_fn_short.split('.')[:-1]), template_fn_short, pos, size)
target.save(output_fn)
    
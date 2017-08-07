#!/bin/bash

filename=$1
width=$2
height=$3
outfile=$4

a=`echo $filename | awk -F '.' '{print $1"."$2}'`;
b=`echo $filename | awk -F '.' '{print $6}'`
x=`echo $b | awk -F 'x' '{print $2}' | awk -F '_' '{print $1}'`;
y=`echo $b | awk -F 'y' '{print $2}' | awk -F '-' '{print $1}'`;

/home/tkurc/programs/openslide-340/bin/openslide-write-png $a.svs $x $y 0 $width $height $outfile

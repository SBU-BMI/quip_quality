#!/bin/bash

set -x

segfile=$1
svsfile=$2
width=$3
height=$4
outfile=$5

bname=$(basename $segfile)

b=`echo $bname | awk -F '.' '{print $6}'`
x=`echo $b | awk -F 'x' '{print $2}' | awk -F '_' '{print $1}'`;
y=`echo $b | awk -F 'y' '{print $2}' | awk -F '-' '{print $1}'`;

/home/tkurc/programs/openslide-340/bin/openslide-write-png $svsfile $x $y 0 $width $height $outfile

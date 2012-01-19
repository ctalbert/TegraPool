#!/bin/bash
cd $1/temp
tar -jxf $2
unzip -o $3 'bin*'
unzip -o $3 'certs*'
cp -R bin/* firefox/.
cp -R certs firefox/.
mv firefox $1/ffxbin

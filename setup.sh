#!/bin/bash

rm -r clang+llvm-7.0.1-x86_64-linux-sles11.3*

wget http://releases.llvm.org/7.0.1/clang+llvm-7.0.1-x86_64-linux-sles11.3.tar.xz
tar -xvf clang+llvm-7.0.1-x86_64-linux-sles11.3.tar.xz

cd clang+llvm-7.0.1-x86_64-linux-sles11.3

wget http://releases.llvm.org/7.0.1/cfe-7.0.1.src.tar.xz
tar -xvf cfe-7.0.1.src.tar.xz --strip-components=1


source exports.sh


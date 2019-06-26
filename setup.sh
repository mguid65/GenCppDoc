#!/bin/bash

rm -r clang+llvm-7.0.1-x86_64-linux-sles11.3*
rm -r clang_llvm_7.0.1

mkdir clang_llvm_7.0.1
cd clang_llvm_7.0.1

wget http://releases.llvm.org/7.0.1/clang+llvm-7.0.1-x86_64-linux-sles11.3.tar.xz --strip-components=1
tar -xvf clang+llvm-7.0.1-x86_64-linux-sles11.3.tar.xz

wget http://releases.llvm.org/7.0.1/cfe-7.0.1.src.tar.xz
tar -xvf cfe-7.0.1.src.tar.xz --strip-components=1

cd include

cp -r ./c++/c1/* ./

cd ../..

cat exports.sh >> ~/.bashrc



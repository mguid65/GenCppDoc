export PATH=$PWD/clang+llvm-7.0.1-x86_64-linux-sles11.3/bin:$PATH
export LD_LIBRARY_PATH=$(llvm-config --libdir):$LD_LIBRARY_PATH
export PYTHONPATH=$PWD/clang+llvm-7.0.1-x86_64-linux-sles11.3/bindings/python:$PYTHONPATH

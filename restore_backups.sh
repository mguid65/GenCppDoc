#!/bin/bash

for name in $(ls *.bak); do
  orig=${name%.bak};
  echo 'Restoring '$name' to '$orig;
  mv $name $orig
done

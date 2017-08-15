#!/bin/bash

for d in build/Kindle/*; do
  if [ -d "${d}" ]; then
    if [ ! -f "build/${d##*/}.mobi" ]; then
      kindlegen "${d}/${d##*/}.opf"
      echo "${d}/${d##*/}.mobi"
      mv "${d}/${d##*/}.mobi" build/.
    fi
  fi
done

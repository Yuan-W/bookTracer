#!/bin/bash

for d in Kindle/*; do
  if [ -d "${d}" ]; then
    if [ ! -f "${d##*/}.mobi" ]; then
      kindlegen "${d}/${d##*/}.opf"
      echo "${d}/${d##*/}.mobi"
      mv "${d}/${d##*/}.mobi" .
    fi
  fi
done

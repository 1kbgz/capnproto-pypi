#!/bin/bash

mkdir -p build
cmake -B build src -DBUILD_TESTING=OFF -DCMAKE_CXX_STANDARD=17 -DCMAKE_INSTALL_PREFIX=capnproto
cmake --build build --config Release -j 3
cmake --install build
rm -rf build

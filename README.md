# CWIPC for Android

This repository contains facilities necessary to cross-compile CWIPC-related
software for the Android operating system, i.e. smartphones and VR headsets
like the Meta Quest.

## Preliminaries

Before getting started, make sure to cross-compile the PCL library for Android.
Instructions and scripts for the process can be found at
[troeggla/pcl-for-android](https://github.com/troeggla/pcl-for-android).

## Building

Once PCL and its dependencies are compiled, call the `build_cwipc_android.sh`
script, passing in the desired target architecture (i.e. `armv7`, `armv8`,
`x86` or `x86_64`) as a command line argument.

    $ bash build_cwipc_android.sh armv8

Building for `armv8` should cover most devices nowadays. A smaller number of
legacy devices require `armv7` builds. The `x86` architectures are only
required for emulator support.

Upon successful completion, you will find the resulting artifacts in a folder
named `dist/[ARCH]` in your current working directory, where `ARCH` is the name
of the target architecture that you passed to `build_cwipc_android.sh`.

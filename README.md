# Introduction

Deepsight Face is a binary SDK that runs as an HTTP service.  It encapsulates Deep learning models for face detection, gender/age classification, face recognition and provides a REST api for easy inference.  Each model is a separate plugin that can be upgraded as new updates are pushed.  

![deepsight](https://j.gifs.com/Xo23k8.gif)

Since all inference is made offline, there are no limits on the number of API hits.

This repository consists of a collection of example programs written in python demonstrating the capabilities of the SDK.

## Getting Started and Installation

Deepsight Face is extremely easy to setup and is available for free.

Deepsight Face is currently supported in `Linux` and `Windows` Operating Systems on `x64` platform.  
It is available with or without `GPU Acceleration`.  The free version comes without it.

Visit [this link](https://www.baseapp.com/deepsight-image-recognition-sdk/deepsight-face-sdk-download/) and download a suitable version for your platform

### Windows

1. Run the setup file and install to a location that will **NOT** require **admin privileges** for writing. The default `C:\Deepsight_Face` is safe.

#### Install Dependencies

The setup package installs necessary dependencies.  However, in case that didn't happen, install these present in the `redist` folder.

1. VC++ 2017 Runtime (`vc_redist.x64.exe`)
1. Intel MKL BLAS Runtime  (`c_wproc*.exe`)

#### Run

1. The setup should've created start menu links. Launch `Deepsight Face` from the start menu link. (or `dsFace.exe` from the installed folder)
2. The application should start with a bunch of messages and finally say `SERVER READY`.
3. At this point you can start the Demo app using your browser and pointing it to `localhost:5000`.

### Linux

1. Open a terminal and `cd` into a directory with non-root access.
2. Copy the shell installer into this directory.
3. Run the script using 
    ```sh
    chmod +x Deepsight_Face-xxx-Linux.sh
    ./Deepsight_Face-xxx-Linux.sh
    ```
4. Press the space bar to read the EULA and enter `y` to accept it
5. Continue through the prompt until extraction is complete.

#### Install Dependencies

Deepsight on `Linux` requires the [OpenBLAS](http://www.openblas.net/) library.  It should be available in your distribution repository.

```sh
# On Ubuntu
sudo apt-get update
sudo apt-get install libopenblas-dev
```

#### Run

1. `cd` into the directory `Deepsight_Face` and use `./dsFace` to launch the program 
2. The application should start with a bunch of messages and finally say `SERVER READY`.
3. At this point you can start the Demo app using your browser and pointing it to `localhost:5000`.

### Usage

* The application accepts arguments as follows

```sh
$ ./dsFace -h
Deepsight Face is a Deep Learning powered face recognition SDK that runs locally as a http service
Usage:
  DeepSight Face [OPTION...]

  -v, --verbose    Print lots of messages; vv increases verbosity
  -b, --benchmark  Run benchmark to evaluate speed
  -k, --key        Prompts license key
  -u, --usage      Print usage stats
  -h, --help       Prints help
  -p, --port arg   specify port at which to serve; default is 5000
```

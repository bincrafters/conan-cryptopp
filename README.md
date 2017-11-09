[ ![Download](https://api.bintray.com/packages/bincrafters/public-conan/CryptoPP%3Abincrafters/images/download.svg?version=5.6.5%3Astable) ](https://bintray.com/bincrafters/public-conan/CryptoPP%3Abincrafters/5.6.5%3Astable/link)
[![Build Status](https://travis-ci.org/bincrafters/conan-CryptoPP.svg?branch=stable%2F5.6.5)](https://travis-ci.org/bincrafters/conan-CryptoPP)
[![Build status](https://ci.appveyor.com/api/projects/status/a5snyovachh6e8nh?svg=true)](https://ci.appveyor.com/project/BinCrafters/conan-CryptoPP)



[Conan.io](https://conan.io) package for [CryptoPP](https://github.com/someauthor/CryptoPP) project

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/bincrafters/public-conan/CryptoPP%3Abincrafters).

## For Users: Use this package

### Basic setup

    $ conan install CryptoPP/5.6.5@bincrafters/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    CryptoPP/5.6.5@bincrafters/stable

    [generators]
    txt

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.

## For Packagers: Publish this Package

The example below shows the commands used to publish to bincrafters conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly.

## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create bincrafters/stable

## Add Remote

    $ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"

## Upload

    $ conan upload CryptoPP/5.6.5@bincrafters/stable --all -r bincrafters

## License
[LICENSE_TYPE](LICENSE)

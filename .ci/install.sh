#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    brew update || brew update
    brew outdated pyenv || brew upgrade pyenv
    brew install pyenv-virtualenv
    brew install cmake || true

    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi

<<<<<<< HEAD:.ci/install.sh
    pyenv install 3.7.0
    pyenv virtualenv 3.7.0 conan
=======
    pyenv install 3.7.1
    pyenv virtualenv 3.7.1 conan
>>>>>>> testing/7.0.0:.ci/install.sh
    pyenv rehash
    pyenv activate conan
fi

pip install conan --upgrade
pip install conan_package_tools bincrafters_package_tools

conan user

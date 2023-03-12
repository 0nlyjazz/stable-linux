#!/bin/bash

#
# Satellite script to handle the env variable setup which 
# python apparently cannot handle
#
# Author: Sarbojit Ganguly
# Bugs/Suggestions: onlyjazz.16180@gmail.com



run_cargo_env () {
    source "$HOME/.cargo/env"
    echo "all done"
}

setup_path () {
    echo "removing old rust dir from path"
    RUSTDIR="/home/$USER/.cargo/bin"
    # backup incase anything messes up :-)
    ORIGINAL_PATH=$PATH


    # this will convert the delimiters to newline so that grep can search
    NEWPATH=$(echo $PATH|tr ':' '\n' | grep -v $RUSTDIR | tr "\n" ':')
    # convert delimiters back to their original form
    NEWPATH=$(echo $NEWPATH|sed 's/.$//')
    
    
    # export it
    export PATH=$NEWPATH
    echo path=$PATH

    echo "all done"
}


if [ -z "$1" ]
    then
        echo "no args supplied"
fi

if [ $1 = "setpath" ]; then
        setup_path
fi

if [ $1 = "cargoenv" ]; then
        run_cargo_env
fi




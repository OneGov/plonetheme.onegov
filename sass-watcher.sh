#!/usr/bin/env sh

command -v sass 2>&1 > /dev/null
has_sass=$?

command -v rbenv 2>&1 > /dev/null
has_rbenv=$?


if [[ $has_sass -eq 1 ]]; then
    echo 'It seems you do not have "sass" installed yet.'

    if [[ $has_rbenv -eq 0 ]]; then
        echo "You have rbenv installed."
        rbenv local 2>&1 > /dev/null
        rbenv_enabled=$?
        if [[ $rbenv_enabled -eq 1 ]]; then
            echo "rbenv is not enabled, enable it with:"
            echo " $ rbenv local 1.9.3-p194"
        else
            echo "Install sass with:"
            echo " $ gem install sass"
        fi
    fi

    exit 1;
fi

sass --watch plonetheme/onegov/resources/sass/main.scss:plonetheme/onegov/resources/css/main.css

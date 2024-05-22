#!/usr/bin/env sh

# Removes any smart characters automatically added by macOS/ iOS.

function replace_unwanted_characters_in_file() {
    sed -i '' s/'\xe2\x80\x98'/\'/g  ${1} # Smart open single-quote
    sed -i '' s/'\xe2\x80\x99'/\'/g  ${1} # Smart close single-quote 
    sed -i '' s/'\xe2\x80\x9c'/\"/g  ${1} # Smart open double-quote
    sed -i '' s/'\xe2\x80\x9d'/\"/g  ${1} # Smart close double-quote
    sed -i '' s/'\xe2\x80\x94'/--/g  ${1} # Smart dash
    sed -i '' s/'\xe2\x80\xa6'/.../g ${1} # Smart ellipsis
}

export -f replace_unwanted_characters_in_file

find ./_static \
    -name '*.md' \
    -exec bash -c 'replace_unwanted_characters_in_file "$0"' {} \;
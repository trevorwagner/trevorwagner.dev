#!/usr/bin/env sh

printf $'Removing smart characters and unnecessary formatting from markdown files...\n'

function replace_unwanted_characters_in_file() {
    sanitized_md=$( cat ${1}              \
    | sed  s/'\xe2\x80\x98'/\'/g          \
    | sed  s/'\xe2\x80\x99'/\'/g          \
    | sed  s/'\xe2\x80\x9c'/\"/g          \
    | sed  s/'\xe2\x80\x9d'/\"/g          \
    | sed  s/'\xe2\x80\x94'/--/g          \
    | sed  s/'\xe2\x80\xa6'/.../g         \
    | sed -e 's/\([.?!*-_]\) \{2,\}/\1 /g' \
    | sed -e s/' \{1,\}$//g'              \
    | grep -A1 . - | grep -v "^--$"       \
    )
    printf "%s" "${sanitized_md}" > ${1}
}

export -f replace_unwanted_characters_in_file

find ./_static \
    -name '*.md' \
    -exec bash -c 'replace_unwanted_characters_in_file "$0"' {} \;

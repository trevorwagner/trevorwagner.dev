#!/usr/bin/env sh

function remove_unwanted_characters() {
    result=$(echo "${1}"                                    \
    | sed  s/'\xe2\x80\x98'/\'/g                            \
    | sed  s/'\xe2\x80\x99'/\'/g                            \
    | sed  s/'\xe2\x80\x9c'/\"/g                            \
    | sed  s/'\xe2\x80\x9d'/\"/g                            \
    | sed  s/'\xe2\x80\x94'/--/g                            \
    | sed  s/'\xe2\x80\xa6'/.../g                           \
    )
    
    echo "${result}"
}


function reformat_markdown() {
    result=$(echo "${1}"                                    \
    | sed    's/[[:blank:]]+$//'                            \
    | sed -e 's/\([\.\?\!\*\_\-\"]\)[[:blank:]]\{2,\}/\1 /' \
    | cat -s                                                \
    )

    echo "${result}"
}


function process_file_contents() {
    md_raw="$(echo "${1}")"
    md_sanitized="$(remove_unwanted_characters "${md_raw}")"
    md_reformatted="$(reformat_markdown "${md_sanitized}")"

    echo "${md_reformatted}"
}


function run_main() {
    f_contents="$(cat ${1})"
    result="$(process_file_contents "${f_contents}")"

    printf "%s" "${result}" > ${1}
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]
then
  run_main ${1}
fi
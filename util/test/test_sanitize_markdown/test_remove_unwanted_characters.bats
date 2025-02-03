load '../test_helper/bats-support/load'
load '../test_helper/bats-assert/load'

profile_script="./util/bin/sanitize_markdown.sh"


@test ".removes left smart apostrophe" {
    needle='‘'
    source ${profile_script}

    hay='beginning of literal'
    content="${needle}${hay}"
    
    expected="'${hay}"
    run remove_unwanted_characters "${content}"

    assert_output "${expected}"
}

@test ".removes right smart apostrophe" {
    needle='’'
    source ${profile_script}

    hay='end of literal'
    content="${hay}${needle}"
    
    expected="${hay}'"
    run remove_unwanted_characters "${content}"

    assert_output "${expected}"
}

@test ".removes left smart quotes" {
    needle='“'
    source ${profile_script}

    hay='beginning of literal'
    content="${needle}${hay}"
    
    expected="\"${hay}"
    run remove_unwanted_characters "${content}"

    assert_output "${expected}"
}

@test ".removes right smart quotes" {
    needle='”'
    source ${profile_script}

    hay='end of literal'
    content="${hay}${needle}"
    
    expected="${hay}\""
    run remove_unwanted_characters "${content}"

    assert_output "${expected}"
}

@test ".removes smart double dash" {
    needle='—'
    source ${profile_script}

    hay='something to follow'
    content="${hay}${needle}"

    expected="${hay}--"
    run remove_unwanted_characters "${content}"

    assert_output "${expected}"
}

@test ".removes smart ellipsis" {
    needle='…'
    source ${profile_script}

    hay='it keeps going'
    content="${hay}${needle}"

    expected="${hay}..."
    run remove_unwanted_characters "${content}"

    assert_output "${expected}"
}
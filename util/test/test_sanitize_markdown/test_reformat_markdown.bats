load '../test_helper/bats-support/load'
load '../test_helper/bats-assert/load'

profile_script="./util/bin/sanitize_markdown.sh"


# @test ".strips space characters from empty lines" {
#     needle="   "
#     source ${profile_script}
# 
#     hay='LINES WITH STRAY SPACE CHARS.'
# 
#     content="${hay}"$'\n'"${needle}"$'\n'
#     expected="${hay}"$'\n\n'
# 
#     run reformat_markdown "${content}"
# 
#     assert_output "${expected}"
# }

# @test ".strips tab characters from empty lines" {
#     needle=$'\t'
#     source ${profile_script}
# 
#     hay='LINES WITH STRAY TAB CHARS.'
# 
#     content="$(echo ${hay}$'\n'${needle}$'\n')"
#     expected="$(echo ${hay}$'\n\n')"
# 
#     run reformat_markdown "${content}"
# 
#     assert_output "${expected}"
# }

# @test ".removes trailing whitespace before newline" {
#     needle="  "
#     source ${profile_script}
# 
#     hay="here is a line with trailing whitespace"
# 
#     content=$(echo ${hay}${needle}$'\n')
#     expected=$(echo ${hay}$'\n')
# 
#     run reformat_markdown "${content}"
# 
#     assert_output "${expected}"
# }

# @test ".condenses multiple whitespace-only lines to empty line" {}

@test ".condenses multiple space characters following period to one" {
    needle="  "
    source ${profile_script}

    hay='This is the end of the sentence.'
    content="${hay}${needle}Plus"
    
    expected="${hay} Plus"
    run reformat_markdown "${content}"

    assert_output "${expected}"
}

@test ".condenses multiple space characters following question mark to one" {
    needle="  "
    source ${profile_script}

    hay='Is this the end of the sentence?'
    content="${hay}${needle}Plus"
    
    expected="${hay} Plus"
    run reformat_markdown "${content}"

    assert_output "${expected}"
}

@test ".condenses multiple space characters following exclamation mark to one" {
    needle="  "
    source ${profile_script}

    hay='This is the end of an exciting sentence!'
    content="${hay}${needle}Plus"
    
    expected="${hay} Plus"
    run reformat_markdown "${content}"

    assert_output "${expected}"

}

# @test ".condenses multiple space characters following dash to one" {
#    needle="  "
#    source ${profile_script}
# 
#    hay='Dear Recipient-'
#    content="${hay}${needle}You"
#     
#     expected="${hay} You"
#     run reformat_markdown "${content}"
# 
#     assert_output "${expected}"
# }

@test ".removes multiple space characters following underscore" {
    needle="  "
    source ${profile_script}

    hay='_This is some italicized text_'
    content="${hay}${needle}Plus"
    
    expected="${hay} Plus"
    run reformat_markdown "${content}"

    assert_output "${expected}"
}

@test ".removes multiple space characters following asterisk" {
    needle="  "
    source ${profile_script}

    hay='**This is some bold text**'
    content="${hay}${needle}Plus"
    
    expected="${hay} Plus"
    run reformat_markdown "${content}"

    assert_output "${expected}"
}

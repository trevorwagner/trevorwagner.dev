#!/usr/bin/env sh

set -eo pipefail

HLJS_VERSION="11.9.0"
HLJS_THEME="default-dark"
PHPMAILER_VERSION="6.9.1"


function fetch_phpmailer() {
    f_php_private=./_dist/html/private
    mkdir -p "${f_php_private}/lib/phpmailer/"

    echo "PHPMailer v${PHPMAILER_VERSION}: Downloading Exception.php..."
    curl --create-dirs -# -o "${f_php_private}/lib/phpmailer/Exception.php" \
        "https://raw.githubusercontent.com/PHPMailer/PHPMailer/v${PHPMAILER_VERSION}/src/Exception.php"

    echo "PHPMailer v${PHPMAILER_VERSION}: Downloading LICENSE..."
    curl --create-dirs -# -o "${f_php_private}/lib/phpmailer/LICENSE" \
        "https://raw.githubusercontent.com/PHPMailer/PHPMailer/v${PHPMAILER_VERSION}/LICENSE"

    echo "PHPMailer v${PHPMAILER_VERSION}: Downloading PHPMailer.php..."
    curl --create-dirs -# -o "${f_php_private}/lib/phpmailer/PHPMailer.php" \
        "https://raw.githubusercontent.com/PHPMailer/PHPMailer/v${PHPMAILER_VERSION}/src/PHPMailer.php"

    echo "PHPMailer v${PHPMAILER_VERSION}: Downloading SMTP.php..."
    curl --create-dirs -# -o "${f_php_private}/lib/phpmailer/SMTP.php" \
        "https://raw.githubusercontent.com/PHPMailer/PHPMailer/v${PHPMAILER_VERSION}/src/SMTP.php"
}


function fetch_highlight_js() {
    f_js_lib='./_dist/html/js/lib'

    echo "highlight.js ${HLJS_VERSION}: Downloading highlight.min.js..."
    curl --create-dirs -# -o "${f_js_lib}/highlightjs/${HLJS_VERSION}/js/highlight.min.js" \
        "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/${HLJS_VERSION}/highlight.min.js"

    echo "highlight.js ${HLJS_VERSION}: Downloading js LICENSE..."
    curl --create-dirs -# -o "${f_js_lib}/highlightjs/${HLJS_VERSION}/js/LICENSE" \
        "https://raw.githubusercontent.com/highlightjs/highlight.js/${HLJS_VERSION}/LICENSE"

    echo "highlight.js ${HLJS_VERSION}: Downloading gherkin.min.js..."
    curl --create-dirs -# -o "${f_js_lib}/highlightjs/${HLJS_VERSION}/js/gherkin.min.js" \
        "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/${HLJS_VERSION}/languages/gherkin.min.js"

    echo "highlight.js ${HLJS_VERSION}: Downloading ${HLJS_THEME}.css..."
    curl --create-dirs -# -o "${f_js_lib}/highlightjs/${HLJS_VERSION}/css/${HLJS_THEME}.css" \
        "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/${HLJS_VERSION}/styles/base16/${HLJS_THEME}.css"        
        
}


fetch_phpmailer
fetch_highlight_js
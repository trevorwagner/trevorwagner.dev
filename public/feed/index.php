<?php
    $attachment_location = $_SERVER["DOCUMENT_ROOT"] . "/blog/feed/rss.xml";

    if (file_exists($attachment_location)) {

        header($_SERVER["SERVER_PROTOCOL"] . " 200 OK");
        header("Cache-Control: public"); // needed for internet explorer
        header("Content-Type: application/rss+xml");
        header("Content-Transfer-Encoding: Binary");
        header("Content-Length:".filesize($attachment_location));
        header("Content-Disposition: attachment; filename=rss.xml");
        readfile($attachment_location);
        die();
    } else {
        http_response_code(404);
        die()
?>
<?php
$queryString = $_SERVER['QUERY_STRING'];
parse_str($queryString, $queryParams);

$jsonFile = file_get_contents("./posts/posts.json");
$postsList = json_decode($jsonFile, true)['posts'];

function handle_not_found()
{
  $html = file_get_contents($_SERVER['DOCUMENT_ROOT'] . "/404/index.html");
  header($_SERVER["SERVER_PROTOCOL"] . " 404 Not Found");
  echo $html;
}

if (array_key_exists('p', $queryParams) && is_numeric($queryParams['p'])):
  if ($queryParams['p'] > count($postsList)):
    handle_not_found();
    die();
  endif;
  
  if (strlen($postsList[$queryParams['p'] - 1]['slug']) == 0):
    handle_not_found();
    die();
  endif;

  $path = "/blog/posts/" . $postsList[$queryParams['p'] - 1]['slug'] . "/";
  header("location: $path");
  http_response_code(301);
  die();

endif;
?>
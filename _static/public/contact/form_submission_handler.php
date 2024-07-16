<?php
require_once '../private/lib/phpmailer/PHPMailer.php';
require_once '../private/lib/phpmailer/Exception.php';
require_once '../private/lib/phpmailer/SMTP.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;
use PHPMailer\PHPMailer\SMTP;

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = htmlspecialchars($_POST['name']);
    $email = htmlspecialchars($_POST['email']);
    $message = htmlspecialchars($_POST['message']);

    $mail = new PHPMailer(true);

    try {
        //Server settings
        $mail->isSMTP();
        $mail->Host       = '<%SMTP_HOST%>';
        $mail->SMTPAuth   = true;
        $mail->Username   = '<%SMTP_USERNAME%>';
        $mail->Password   = '<%SMTP_PW%>';
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_SMTPS;
        $mail->Port       = '<%SMTP_PORT%>';

        //Recipients
        $mail->setFrom('<%SMTP_USERNAME%>', "{$name} (via trevorwagner.dev)");
        $mail->addAddress('<%MESSAGE_RECIPIENT%>');
        $mail->addReplyTo($email, $name);

        //Content
        $mail->isHTML(true);
        $mail->Subject = "New Contact Form Submission from {$name}";
        $mail->Body    = "New Contact Form Submission from trevorwagner.dev.<br/><b>Name:</b> {$name}<br/><b>Email:</b> {$email}<br/><b>Message:</b> {$message}";
        $mail->AltBody = "New Contact Form Submissionfrom trevorwagner.dev.\n\nName:    {$name}\n\nEmail:   {$email}\n\nMessage: {$message}";

        $mail->send();
        echo '<p class="notice success">Message has been sent. Thank you!</p>';
    } catch (Exception $e) {
        echo "<p class=\"notice error\">Message could not be sent (Mailer Error).</p>";
    }
}
?>
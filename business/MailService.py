import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailService:
    @staticmethod
    def send_activation_code_email(recipient_email, activation_code):
        try:
            smtp_server = "smtp.gmail.com"
            port = 587
            sender_email = "your-email@example.com"
            password = "your-email-password"

            message = MIMEMultipart("alternative")
            message["Subject"] = "Aktivasyon Kodu"
            message["From"] = sender_email
            message["To"] = recipient_email

            text = f"Hesabınızı etkinleştirmek için aşağıdaki aktivasyon kodunu kullanın: {activation_code}"
            html = f"""\
                <html>
                    <body>
                        <p>Hesabınızı etkinleştirmek için aşağıdaki aktivasyon kodunu kullanın:</p>
                        <p>{activation_code}</p>
                    </body>
                </html>
            """

            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            message.attach(part1)
            message.attach(part2)

            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, recipient_email, message.as_string())

            print("E-posta başarıyla gönderildi.")
        except Exception as ex:
            print("E-posta gönderme hatası:", ex)
from django.core.mail import EmailMultiAlternatives


def emailSender(data):
    name=data.get("name","user")
    try:
        subject = "Reeloid : Account Registration Successful"
        from_email = "appteam@omr.co.in"  # Replace with your Gmail
        to_email = [data.get("email")]  # Replace with recipient's email

        # Plain text version (fallback)
        text_content = ""

        # HTML content as a string
        html_content = f"""
                    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 600px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #D4AF37; text-align: center;">Welcome to <span style="font-weight: bold;">Reeloid</span>: Naye Zamane Ka Vertical Content Provider!</h2>
                <p style="font-size: 16px; color: #333;">Dear {name},</p>
                
                <p style="font-size: 16px; color: #333;">
                    We are excited to inform you that you have been successfully 
                    <b style="color: #D4AF37;">registered</b> with us.
                </p>
                
                <p style="font-size: 16px; color: #333;">
                    Now you can use your credentials to <b style="color: #D4AF37;">log in</b> and enjoy 
                    high-quality <b style="color: #D4AF37;">entertainment videos</b> anytime, anywhere.
                </p>

                <div style="text-align: center; margin: 20px 0;">
                    <a href="https://demo.reeloid.app/" 
                    style="background: #D4AF37; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-size: 16px; font-weight: bold;">
                    Login Now
                    </a>
                </div>

                <p style="font-size: 16px; color: #333; text-align: center;">
                    <b>- Rohit Gupta (C.E.O)</b><br>
                    <i style="color: #D4AF37;">Reeloid: Vertical Movies and Series on the Go</i>
                </p>
            </div>
        </body>
    </html>

                    """

        # Create Email Object
        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()
        return "email sent successfully"
    except Exception as err:
        raise ValueError(str(err))

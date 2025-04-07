from django.core.mail import EmailMultiAlternatives


def forgotPasswordEmailSender(data):
    name = data.get("name", "User")
    email = data.get("email")
    otp = data.get("otp")  # Ensure a password reset link is passed in the data

    if not otp:
        raise ValueError("Error: Missing otp")
    if not email:
        raise ValueError("Error: no email found")
        # return "Error: Missing password reset link."
    try:
        subject = "Reeloid: Password Reset Request"
        from_email = "appteam@omr.co.in"  # Replace with your email
        to_email = [data.get("email")]  # Recipient email

        # Plain text version (fallback)
        text_content = f"""
        Hi {name},

        We received a request to reset your password. Use the otp to change the password:

        {otp}

        If you did not request this, please ignore this email.

        Regards,
        Reeloid Support Team
        """

        # HTML Content
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 600px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #D4AF37; text-align: center;">Reset Your Password</h2>
                <p style="font-size: 16px; color: #333;">Dear {name},</p>
                
                <p style="font-size: 16px; color: #333;">
                    We received a request to reset your password. Use the otp to change the password (valid for 15 minutes only):
                </p>

                <div style="text-align: center; margin: 20px 0;">
                    <a  
                    style="background: #D4AF37; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-size: 16px; font-weight: bold;">
                    {otp}
                    </a>
                </div>

                <p style="font-size: 16px; color: #333;">
                    If you did not request this, you can safely ignore this email.
                </p>

                <p style="font-size: 16px; color: #333; text-align: center;">
                    <b>- Reeloid Support Team</b>
                </p>
            </div>
        </body>
        </html>
        """

        # Create Email Object
        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        print(email.send())
        return "Email sent successfully"

    except Exception as err:
        print(err)
        raise ValueError(f"Error sending email: {str(err)}")

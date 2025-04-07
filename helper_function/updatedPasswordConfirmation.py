from django.core.mail import EmailMultiAlternatives

def updatedPasswordConfirmation(data):
    name = data.get("name", "User")
    recipient_email = data.get("email")

    if not recipient_email:
        raise ValueError("Missing recipient email.")

    try:
        subject = "Reeloid: Your Password Was Successfully Changed"
        from_email = "appteam@omr.co.in"
        to_email = [recipient_email]

        # Plain text fallback
        text_content = f"""
        Hi {name},

        This is a confirmation that your password has been successfully changed.

        If you did not make this change, please contact our support team immediately.

        Regards,
        Reeloid Support Team
        """

        # HTML version
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 600px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #4CAF50; text-align: center;">Password Changed Successfully</h2>
                <p style="font-size: 16px; color: #333;">Dear {name},</p>
                
                <p style="font-size: 16px; color: #333;">
                    This is a confirmation that your password was changed successfully.
                </p>

                <p style="font-size: 16px; color: #333;">
                    If you didn’t perform this action, please contact our support team immediately.
                </p>

                <p style="font-size: 16px; color: #333; text-align: center;">
                    <b>- Reeloid Support Team</b>
                </p>
            </div>
        </body>
        </html>
        """

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return "Password change confirmation email sent."

    except Exception as err:
        raise ValueError(f"Error sending email: {err}")

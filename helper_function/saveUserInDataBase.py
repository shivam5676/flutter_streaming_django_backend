from streaming_app_backend.mongo_client import (
    users_collection,
    checkInPoints,
    dailyCheckInTask_collection,
)
from django.http import JsonResponse
from datetime import datetime, timezone, timedelta
from django.core.mail import EmailMultiAlternatives


def saveUserInDataBase(data):

    try:
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        current_time = datetime.now(timezone.utc)

        today = datetime.today()

        # Add 7 days to today's date
        new_date = today + timedelta(days=7)
        next_allocation = new_date.strftime("%d/%m/%Y")
        current_date = datetime.today()
        userResponse = users_collection.insert_one(
            {
                "name": name,
                "email": email,
                "password": password,
                "loggedInBefore": False,
                "gender": "null",
                "mobile": "null",
                "createdAt": current_time,  # created_at field
                "updatedAt": current_time,  # updated_at field
                # "next_Allocation": next_allocation,
            }
        )
        user_id = userResponse.inserted_id

        # userResponse["_id"]=str(userResponse["_id"])

        if userResponse:
            checkInResponse = list(checkInPoints.find({}, {"_id": 1}).limit(7))

            allotedTask = []
            for index, checkInData in enumerate(checkInResponse):
                print(checkInData, "cdata")
                new_task = {
                    "assignedTaskId": str(checkInData.get("_id")),
                    "assignedUser": str(user_id),
                    "status": "Pending",
                    "obtainable": (current_date + timedelta(days=index)).strftime(
                        "%d/%m/%Y"
                    ),
                }
                allotedTask.append(new_task)

            if allotedTask:
                dailyAllocationResponse = dailyCheckInTask_collection.insert_many(
                    allotedTask
                )
                if dailyAllocationResponse:
                    users_collection.find_one_and_update(
                        {"_id": user_id},
                        {
                            "$set": {
                                "assignedCheckInTask": 7,
                                "next_Allocation": next_allocation,
                            }
                        },
                    )
                # we will use this asigned task later at the time of assigning task to user for off limit to next 7 task
#                 subject = "Reeloid : Account Registration Successful"
#                 from_email = "appteam@omr.co.in"  # Replace with your Gmail
#                 to_email = ["techking08@gmail.com"]  # Replace with recipient's email

#                 # Plain text version (fallback)
#                 text_content = (
#                     ""
#                 )

#                 # HTML content as a string
#                 html_content = """
#                 <html>
#     <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
#         <div style="max-width: 600px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
#             <h2 style="color: #D4AF37; text-align: center;">Welcome to <span style="font-weight: bold;">Reeloid</span>: Naye Zamane Ka Vertical Content Provider!</h2>
#             <p style="font-size: 16px; color: #333;">Dear User,</p>
            
#             <p style="font-size: 16px; color: #333;">
#                 We are excited to inform you that you have been successfully 
#                 <b style="color: #D4AF37;">registered</b> with us.
#             </p>
            
#             <p style="font-size: 16px; color: #333;">
#                 Now you can use your credentials to <b style="color: #D4AF37;">log in</b> and enjoy 
#                 high-quality <b style="color: #D4AF37;">entertainment videos</b> anytime, anywhere.
#             </p>

#             <div style="text-align: center; margin: 20px 0;">
#                 <a href="https://demo.reeloid.app/" 
#                    style="background: #D4AF37; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-size: 16px; font-weight: bold;">
#                    Login Now
#                 </a>
#             </div>

#             <p style="font-size: 16px; color: #333; text-align: center;">
#                 <b>- Rohit Gupta (C.E.O)</b><br>
#                 <i style="color: #D4AF37;">Reeloid: Vertical Movies and Series on the Go</i>
#             </p>
#         </div>
#     </body>
# </html>

#                 """

#                 # Create Email Object
#                 email = EmailMultiAlternatives(
#                     subject, text_content, from_email, to_email
#                 )
#                 email.attach_alternative(html_content, "text/html")
#                 email.send()
                return userResponse

        else:
            print("no user response")
            raise ValueError(" something went wrong while creating user")

    except Exception as err:
        print(err)
        raise ValueError((err))

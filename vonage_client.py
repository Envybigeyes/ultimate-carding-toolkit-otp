import os
import vonage

auth = vonage.Auth(
    application_id=os.getenv("VONAGE_APPLICATION_ID"),
    private_key=os.getenv("VONAGE_PRIVATE_KEY")
)

voice = vonage.Voice(auth=auth)

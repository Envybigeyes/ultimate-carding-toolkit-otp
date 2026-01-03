SCRIPTS = {
    "capital_one": {
        "intro": (
            "This is an automated fraud prevention call from Capital One. "
            "We detected a suspicious transaction attempt on your account."
        ),
        "otp_prompt": (
            "To protect your account, we have sent a six digit verification code "
            "to the phone number associated with your account. "
            "Please enter the six digit code now."
        ),
        "verified_prompt": (
            "Thank you. Your identity has been verified. "
            "If you recognize and authorized this transaction, press 1. "
            "If you did not authorize this transaction, press 2."
        ),
        "confirm_yes": (
            "Thank you. The transaction has been confirmed as authorized. "
            "Your account remains secure and no further action is required."
        ),
        "confirm_no": (
            "Thank you. The transaction has been blocked and your account is secure. "
            "Our fraud team is monitoring your account. No further action is required."
        ),
        "failure": (
            "We were unable to verify your identity. "
            "For your protection, this case will be reviewed by our fraud team."
        )
    },

    "citi_bank": {
        "intro": (
            "This is an automated security alert from Citi Bank. "
            "We detected unusual activity on your account."
        ),
        "otp_prompt": (
            "A six digit verification code has been sent to your registered phone number. "
            "Please enter the code now to verify your identity."
        ),
        "verified_prompt": (
            "Verification successful. "
            "If this transaction was made by you, press 1. "
            "If this transaction was not made by you, press 2."
        ),
        "confirm_yes": (
            "Thank you. The transaction has been approved and your account is secure."
        ),
        "confirm_no": (
            "Thank you. The transaction has been declined and your account is protected."
        ),
        "failure": (
            "We could not verify your identity. "
            "This matter will be escalated to our fraud department."
        )
    },

    "chase": {
        "intro": (
            "This is an automated fraud alert from Chase Bank. "
            "We noticed a potentially suspicious transaction."
        ),
        "otp_prompt": (
            "We sent a six digit verification code to your phone. "
            "Please enter the code now."
        ),
        "verified_prompt": (
            "Identity confirmed. "
            "Press 1 if you authorized this transaction. "
            "Press 2 if you did not."
        ),
        "confirm_yes": (
            "Thank you. The transaction is confirmed and your account is safe."
        ),
        "confirm_no": (
            "Thank you. The transaction has been blocked and your account is secured."
        ),
        "failure": (
            "We could not verify your identity. "
            "Your account will remain protected and monitored."
        )
    },

    "wells_fargo": {
        "intro": (
            "This is a Wells Fargo fraud prevention call. "
            "We detected a suspicious transaction attempt."
        ),
        "otp_prompt": (
            "Please enter the six digit verification code we sent to your phone."
        ),
        "verified_prompt": (
            "Verification complete. "
            "Press 1 to confirm this transaction. "
            "Press 2 if this transaction was not made by you."
        ),
        "confirm_yes": (
            "Thank you. The transaction has been approved."
        ),
        "confirm_no": (
            "Thank you. The transaction has been declined and your account is secure."
        ),
        "failure": (
            "Verification failed. A fraud specialist will review this activity."
        )
    },

    "pnc": {
        "intro": (
            "This is an automated fraud alert from P N C Bank."
        ),
        "otp_prompt": (
            "Enter the six digit verification code sent to your phone to continue."
        ),
        "verified_prompt": (
            "Verification successful. "
            "Press 1 if the transaction was authorized. "
            "Press 2 if it was not."
        ),
        "confirm_yes": (
            "Thank you. Your account remains safe."
        ),
        "confirm_no": (
            "Thank you. The transaction has been blocked."
        ),
        "failure": (
            "We could not verify your identity."
        )
    },

    "amex": {
        "intro": (
            "This is an automated security call from American Express."
        ),
        "otp_prompt": (
            "Please enter the six digit verification code sent to your mobile device."
        ),
        "verified_prompt": (
            "Thank you for verifying. "
            "Press 1 to confirm this charge. "
            "Press 2 if you do not recognize this charge."
        ),
        "confirm_yes": (
            "Thank you. The charge has been approved."
        ),
        "confirm_no": (
            "Thank you. The charge has been declined and your account is protected."
        ),
        "failure": (
            "Verification failed. This case will be reviewed."
        )
    },

    "paypal": {
        "intro": (
            "This is an automated security alert from PayPal."
        ),
        "otp_prompt": (
            "Enter the six digit security code sent to your phone."
        ),
        "verified_prompt": (
            "Verification complete. "
            "Press 1 if this payment was authorized. "
            "Press 2 if it was not."
        ),
        "confirm_yes": (
            "Thank you. The payment is confirmed."
        ),
        "confirm_no": (
            "Thank you. The payment has been blocked."
        ),
        "failure": (
            "We could not verify your identity."
        )
    },

    "coinbase": {
        "intro": (
            "This is an automated security call from Coinbase regarding your account."
        ),
        "otp_prompt": (
            "Please enter the six digit verification code sent to your phone."
        ),
        "verified_prompt": (
            "Verification successful. "
            "Press 1 if this transaction was initiated by you. "
            "Press 2 if it was not."
        ),
        "confirm_yes": (
            "Thank you. The transaction has been approved."
        ),
        "confirm_no": (
            "Thank you. The transaction has been blocked for your security."
        ),
        "failure": (
            "Verification failed. A security review will follow."
        )
    },

    "kraken": {
        "intro": (
            "This is an automated security notification from Kraken."
        ),
        "otp_prompt": (
            "Enter the six digit verification code now."
        ),
        "verified_prompt": (
            "Identity verified. "
            "Press 1 if you authorized this transaction. "
            "Press 2 if you did not."
        ),
        "confirm_yes": (
            "Transaction confirmed."
        ),
        "confirm_no": (
            "Transaction blocked and account secured."
        ),
        "failure": (
            "Verification unsuccessful."
        )
    },

    "bank_of_america": {
        "intro": (
            "This is an automated fraud alert from Bank of America."
        ),
        "otp_prompt": (
            "Please enter the six digit verification code sent to your phone."
        ),
        "verified_prompt": (
            "Thank you. "
            "Press 1 if you recognize this transaction. "
            "Press 2 if you do not."
        ),
        "confirm_yes": (
            "Thank you. Your account remains secure."
        ),
        "confirm_no": (
            "Thank you. The transaction has been stopped."
        ),
        "failure": (
            "We could not verify your identity."
        )
    }
}

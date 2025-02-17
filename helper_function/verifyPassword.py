import bcrypt

def verifyPassword(password, hashedPassword):
    try:
        verifiedPassword = bcrypt.checkpw(
            password.encode("utf-8"), hashedPassword.encode("utf-8")
        )
        if not verifyPassword:
            raise ValueError("incorrect password")
        return verifiedPassword
    except Exception as err:
        raise ValueError(str(err))

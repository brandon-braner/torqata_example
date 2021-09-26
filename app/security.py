from passlib.context import CryptContext

# passlib context https://passlib.readthedocs.io/en/stable/narr/quickstart.html#creating-and-using-a-cryptcontext

pwd_context = CryptContext(
    # Replace this list with the hash(es) you wish to support.
    # this example sets pbkdf2_sha256 as the default,
    # with additional support for reading legacy des_crypt hashes.
    schemes=["bcrypt"],

    # Automatically mark all but first hasher in list as deprecated.
    # (this will be the default in Passlib 2.0)
    deprecated="auto",

    # Optionally, set the number of rounds that should be used.
    # Appropriate values may vary for different schemes,
    # and the amount of time you wish it to take.
    # Leaving this alone is usually safe, and will use passlib's defaults.
    ## pbkdf2_sha256__rounds = 29000,
)


def hash_password(password: str):
    """Hash password using passlib context set in app.security"""
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    """Verify the hashsed password."""
    return pwd_context.verify(password, hashed_password)

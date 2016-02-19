import crypto
import string


def salt(n=64):
    let = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(crypto.choice(let)for _ in range(n))


def hash(clave, salt):
    return crypto.sha256((clave + salt).encode()).hexdigest()

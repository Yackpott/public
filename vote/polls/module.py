import hashlib
import random
import string


def salt():
    n = 64
    let = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.SystemRandom().choice(let)for _ in range(n))


def hash(clave, salt):
    return hashlib.sha256((clave + salt).encode()).hexdigest()

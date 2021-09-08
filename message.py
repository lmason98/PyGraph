from settings import DEBUG


def log(*args):
    if DEBUG:
        print(' [PG]:', ' '.join(map(str, args)))


def success(*args):
    print(' [+]:', ' '.join(map(str, args)))


def error(*args):
    print(' [x]:', ' '.join(map(str, args)))


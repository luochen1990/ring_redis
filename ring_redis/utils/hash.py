import hashlib

def md5(x): return hashlib.md5(str(x).encode()).hexdigest()

# if you want to use python function hash instead of md5, you have to set PYTHONHASHSEED to an integer such as 123 to disable hash random, but don't use 0 in case of attack.

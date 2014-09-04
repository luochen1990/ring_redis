import hashlib
import zlib

def md5(x): return hashlib.md5(str(x).encode()).hexdigest()
def crc32(x): return zlib.crc32(("%.53f" % x) if type(x) == float else str(x))


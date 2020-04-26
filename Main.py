import Md5 as md
import binascii
import Sender as sd
import Email as em

mined_email = sd.mine("Tesjfsejfse", 15)

nounce, hashe = mined_email

zeros = sd.check_zeros(hashe)
zeros
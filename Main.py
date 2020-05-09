import Md5 as md
import binascii
import Sender as sd
import Email as em
import Receiver as rs

mined_email = sd.mine("Tesjfsejfse", 2)

nounce, hashe = mined_email

email_status = rs.receiver("Tesjfsejfse", nounce, "2020-05-9 14:25:30", "luvi@germanos.ws", hashe)
print(email_status)
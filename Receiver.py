import json
from datetime import datetime, timedelta
import dateutil.parser
import Md5 as md


class Receiver:
    def __init__(self, msg, nounce, timestamp, sender, md5Hash):
        with open('contacts.json', 'r') as infile:
            self.contacts_info = json.load(infile)
        self.msg = msg
        self.nounce = nounce
        self.timestamp = dateutil.parser.parse(timestamp)
        self.sender = sender
        self.md5Hash = md5Hash
        self.dificulty = 5
        self.days = 2
    
    def check_zeros(self, bynary_string):
        bynary_string = bin(int(bynary_string, 16))[2:].zfill(128)
        counter = 0
        for bit in bynary_string:
            if bit == "0":
                counter += 1
            if bit == "1":
                break
        return counter

    def check_date(self, timestamp):
        timedelta = datetime.now() - timestamp
        return timedelta.days <= 2
            
    def check_contacts(self, sender):
        return sender in self.contacts_info["contacts"]
    
    def check_hash_list(self, md5Hash):
        return not(md5Hash in self.contacts_info["hashes"])
    
    def check_hash(self, md5Hash):
        if self.dificulty <= self.check_zeros(md5Hash):
            if self.check_hash_list(md5Hash):
                self.contacts_info["hashes"].append(md5Hash)

                with open('contacts.json', 'w') as outfile:
                    json.dump(self.contacts_info, outfile)

            return True

        else:

            return False

    def mine_check(self, msg, nounce):
        receiver_md5Hash = md.md5_hash(msg+str(nounce))
        return receiver_md5Hash == self.md5Hash

    
    def status(self):
        preliminary_status = self.check_date(self.timestamp) & self.check_contacts(self.sender) & self.check_hash_list(self.md5Hash) & self.check_hash(self.md5Hash)
        if (preliminary_status == False):
            return False
        else:
            return self.mine_check(self.msg, self.nounce)


        
def receiver(msg, nounce, timestamp, sender, md5Hash):
    receiver = Receiver(msg, nounce, timestamp, sender, md5Hash)
    return receiver.status()
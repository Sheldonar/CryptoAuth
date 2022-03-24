from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA3_512
import base64

pk = RSA.generate(1024)
print("PK", pk)
#pub = bytes_to_long(pk.publickey().exportKey("PEM"))
pub = pk.publickey()
print("pub", pub)
#SHA = SHA3_512.new(long_to_bytes(id) + long_to_bytes(v))
SHA = SHA3_512.new(b'FLAG;oerjhgiop[WEHGIOHWer[0irghiowSEHIOGHweio[hgio[WEHGIO[Hwe[oighIO[WEGHIO[werhg[iowEH[IOGHwe[iogho[iwEHGOIWeho[ighwO[EIGHIO9Wehi[oghW')
SHA2 = SHA3_512.new(b'ssssssss')
print(SHA)
cert = pkcs1_15.new(pk).sign(SHA)

print(11)
#pub = RSA.importKey(long_to_bytes(int(str(self.pub))))
print(pkcs1_15.new(pub).verify(SHA, cert))
try:
    pkcs1_15.new(pub).verify(SHA2, cert)
    print("УРРРРАААААА")
except ValueError:
    print("BLET")
    
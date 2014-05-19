import hashlib
#convert user_password into sha1 encoded string
def gen_password(user_password):
    return hashlib.sha1(user_password.encode("utf-8")).hexdigest()
text='abc%03d'
for i in range(1,399+1):
    print(text%(i)+':'+gen_password(text%(i))+':'+text%(i)+'@gmail.com:'+text%(i)+'@gmail.com:'+'user')
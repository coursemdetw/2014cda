import math
count = 0
text='%04d'
for i in range(100,200+10):
    print(text%round(math.log(i/100,10)*10000,0),end='-')
    count += 1
    if(count == 10):
        print()
        count = 0
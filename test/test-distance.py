import math


def rad(d):
    return (d * math.pi) / 180


def distance( latitude1,longitude1, latitude2, longitude2):
    l1 = rad(latitude1)
    l2 = rad(latitude2)
    a = l1 - l2
    b = rad(longitude1) - rad(longitude2)
    s = 2 * math.asin(math.sqrt((math.sin(a / 2) ** 2) + (math.cos(l1) * math.cos(l2) * (math.sin(b / 2) ** 2))))
    s *= 6378137.0
    return s


def distance2(longitude1, latitude1):
    longitude2 = longitude1 + 0.2
    latitude2 = latitude1 + 0.2
    return distance(longitude1, latitude1, longitude2, latitude2)


x = 2000
y = 4000
str1 = str(x)+' '+str(y)
bytes(str1, encoding="utf8")
print(bytes(str1, encoding="utf8"))

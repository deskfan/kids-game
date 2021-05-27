#shake method
#https://github.com/kidscancode/gamedev/blob/master/tutorials/examples/shake.py



import math
from itertools import repeat

#determining collisions
def isCollision(playerX,playerY,objX,objY,threshold=45):
    distance = math.sqrt(math.pow(playerX-objX,2) + math.pow(playerY-objY,2))
    if distance < threshold:
        return True
    else:
        return False

# 'offset' will be our generator that produces the offset
# in the beginning, we start with a generator that 
# yields (0, 0) forever
offset = repeat((0, 0))

# this function creates our shake-generator
# it "moves" the screen to the left and right
# three times by yielding (-5, 0), (-10, 0),
# ... (-20, 0), (-15, 0) ... (20, 0) three times,
# then keeps yieling (0, 0)
def shake():
    s = -1
    for _ in range(0, 3):
        for x in range(0, 20, 5):
            yield (x*s, 0)
        for x in range(20, 0, 5):
            yield (x*s, 0)
        s *= -1
    while True:
        yield (0, 0)
# Game "Flow" functions

import math, numpy

def max_enemy(score):
    # Computes the maximum number of enemies that can spawn
    if score < 2:
        return 1
    else:
        limit = math.log(score)*2
        if limit >= 7: # Caps the limit at 7
            return 7
        else:
            return limit

def sd_subtractor(score):
    # Calculates the subtractor of the spawn delay (sd_s) based on score
    if score == 0:
        return 0
    else:
        sd_s = math.pow(score, 2)
        return numpy.clip(sd_s, 0, 1250)

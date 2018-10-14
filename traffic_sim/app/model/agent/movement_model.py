from const import LARGE_NUMBER, SAFE_GAP, SAFE_TIME_HEADWAY, ACC_EXP, S1
from math import sqrt


def intelligent_driver_model(vel, vel_max, acc_max, dec_max, vel_front=LARGE_NUMBER, gap_front=LARGE_NUMBER,
                             s0=SAFE_GAP, acc_exp=ACC_EXP, s1=S1, safe_time_headway=SAFE_TIME_HEADWAY):

    gap_front = LARGE_NUMBER if gap_front == 0 else gap_front

    if gap_front == LARGE_NUMBER:
        acc = acc_max * (1 - ((vel / vel_max) ** acc_exp))
        return round(acc, 2)

    min_gap_des = s0 + \
                  (s1 * (sqrt(vel / vel_max))) + \
                  (safe_time_headway * vel) + \
                  ((vel * (vel - vel_front)) / (2 * sqrt(acc_max * dec_max)))

    acc = acc_max * (1 - ((vel / vel_max) ** acc_exp) - (min_gap_des / gap_front) ** 2)

    return round(acc, 2)

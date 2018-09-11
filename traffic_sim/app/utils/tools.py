PX2M_DEFAULT = .18


def to_m(px):
    return round(px * PX2M_DEFAULT, 2)


def to_px(m):
    return round(int(float(m) / PX2M_DEFAULT), 2)

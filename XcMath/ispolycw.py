def ispolycw(x, y):
    """
    Given equal sized arrays of points,
    returns True if the polygonal contour vertices represented by x and y
    are ordered in the clockwise direction.
    """

    l = len(x)
    if l < 3:
        raise ValueError("ispolycw::X length is less than 3")

    if len(y) < 3:
        raise ValueError("ispolycw::Y length is less than 3")

    if l != len(y):
        raise ValueError("ispolycw::Non-equal sized arrays")

    s = 0.0
    for k in range(0, l):
        kn = (k + 1) % l

        s += (x[kn] - x[k]) * (y[kn] + y[k])

    return (s > 0.0, 0.5*s) # CW flag, signed area of the polygon


if __name__ == "__main__":
    x = [0, 1, 1, 0, 0]
    y = [0, 0, 1, 1, 0]
    print(ispolycw(x, y))
    print(ispolycw(x[::-1], y[::-1]))
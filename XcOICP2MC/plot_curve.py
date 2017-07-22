#%%
import os
import matplotlib.pyplot as plt


def read_curve(fname: str):
    """
    Read single MC curve and return (iw, ow) tuple
    """
    if fname is None:
        return None

    with open(fname) as f:

        lines = f.readlines()

        rw = list()
        zw = list()
        for line in lines:
            s = line.rstrip('\n').split(' ')
            s = [x for x in s if x] # remove empty lines
            zw.append(float(s[0]))
            rw.append(float(s[1]))

        return (zw, rw)

    return None


dir = "."
cup = "R8O3IL05"

fnameC = os.path.join(dir, cup + "_KddCurve" + "C" + ".txt")
zowO, rowO = read_curve(fnameC)

fnameB = os.path.join(dir, cup + "_KddCurve" + "B" + ".txt")
ziwO, riwO = read_curve(fnameB)

fnameA = os.path.join(dir, cup + "_KddCurve" + "A" + ".txt")
zowI, rowI = read_curve(fnameA)

l_outerO, = plt.plot(zowO, rowO, label="O outer")
l_innerO, = plt.plot(ziwO, riwO, label="O inner")

l_outerI, = plt.plot(zowI, rowI, label="I outer")

plt.legend([l_outerO, l_innerO, l_outerI], ['O outer', 'O inner', 'I outer'])
plt.grid()
plt.show()

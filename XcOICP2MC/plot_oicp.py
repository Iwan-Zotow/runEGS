#%%
import matplotlib.pyplot as plt

from OCPICP import readICP, readOCP

#ziwO, riwO, zowO, rowO = readICP("D:/Ceres/Resource/PlanEngine/R8/Cup/R8O1IS01.icp")
#ziwO, riwO, zowO, rowO = readICP("R8O1.ocp")
RU, OC, dist, ziwO, riwO, zowO, rowO = readOCP("OICPparam/Cup.New/R8O1.ocp")

l_innerO, = plt.plot(ziwO, riwO, label="innerO")
l_outerO, = plt.plot(zowO, rowO, label="outerO")

RU, OC, IC, ziwN, riwN, zowN, rowN = readICP("OICPparam/Cup.New/R8O1IS01.icp")

l_innerN, = plt.plot(ziwN, riwN, label="innerN")
l_outerN, = plt.plot(zowN, rowN, label="outerN")

plt.legend([l_innerO, l_outerO, l_innerN, l_outerN], ['InnerO', 'OuterO', 'InnerN', 'OuterN'])
plt.grid()
plt.show()

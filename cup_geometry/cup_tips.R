library(data.table)

dt <- fread("cup_tipM.txt")
print(dt)

dt[, Diff := Curve-Drawing]
print(dt)

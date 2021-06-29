import pandas as pd
import numpy as np

df = pd.read_csv("UFC_Fight_data_new.csv")

df = pd.crosstab(df.F1, df.F2)
idx = df.columns.union(df.index)
df = df.reindex(index = idx, columns=idx, fill_value=0)

p1 = df.to_numpy()
psym = p1 + p1.T

p = np.linalg.matrix_power(p1, 3)
pdiag = np.diagonal(p)
print(pdiag)

triangles = sum(pdiag[pdiag>0])
# totaltri = do the same code as above but for the undirected graph
def check_symmetric(a, rtol=1e-05, atol=1e-08):
    return np.allclose(a, a.T, rtol=rtol, atol=atol)
#print(check_symmetric(p))

psymp = np.linalg.matrix_power(psym, 3)
psymdiag = np.diagonal(psymp)


trianglessym = sum(psymdiag[psymdiag>0])

ratio = ((trianglessym/6) -(triangles/3))/((trianglessym/6))
print(ratio)


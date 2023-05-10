import numpy as np
import data2latex as dtol

data = np.random.uniform(0, 10, (6, 16))

dtol.plot(data[0:3], data[3:6], line="-")

dtol.table([[1, 2], [3, 4]])

dtol.finish()

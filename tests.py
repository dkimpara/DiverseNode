import pandas as pd
data = [1,2,3,34]
df = pd.DataFrame(data)
df.name = 'Sayama'
df.to_pickle("./tests/df_" + df.name)

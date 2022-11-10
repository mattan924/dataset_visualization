import pandas as pd
from util import *
import math

index_file = "./index.csv"

create_index_file(index_file)

df = pd.read_csv(index_file, index_col=0)

df.at['data', 'config_file'] = "test.csv"

print(df.at['data', 'traking_file'])


if math.isnan(df.at['data', 'traking_file']):
    print("True")
else:
    print("False")
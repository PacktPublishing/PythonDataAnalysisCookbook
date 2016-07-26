from dautil import data
from dautil import report
import pandas as pd
import numpy as np
from tabulate import tabulate


df = data.Weather.load()
headers = [data.Weather.get_header(header) 
           for header in df.columns.values.tolist()]
df = df.describe()


writer = report.RSTWriter()
writer.h1('Weather Statistics')
writer.add(tabulate(df, headers=headers, 
        tablefmt='grid', floatfmt='.2f'))
writer.divider()

builder = report.DFBuilder(df.columns)
builder.row(df.iloc[7].values - df.iloc[3].values)
builder.row(df.iloc[6].values - df.iloc[4].values)
df = builder.build(['ptp', 'iqr'])

writer.h1('Peak-to-peak and Interquartile Range')
headers = [data.Weather.get_header(header) 
           for header in df.columns.values.tolist()]
writer.add(tabulate(df, headers=headers, 
        tablefmt='grid', floatfmt='.2f'))
writer.write('slides.rst')
generator = report.Generator('slides.rst', 'weather_report.html')
generator.generate()

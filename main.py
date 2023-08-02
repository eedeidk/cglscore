from tools.helpers import *
from tools.parsers import *

softinfo = 'CGLSCORE'
author = 'https://github.com/eedeidk/cglscore'

print(f'Welcome to {softinfo}')

url = str(input("Paste scorecard URL: "))	
resp = getpage(url=url)
exam=str(input('Is this CGL? (y/n)'))
if not exam.lower() == 'y':
    p = float(input('Positive Marks: '))
    n = float(input('Negative Marks: '))
    if n<0:
        n=n*(-1)
Parseme(resp=resp, pos=p, neg=n).main()

print(f'For improvements/suggestions {softinfo}')
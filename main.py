from tools.helpers import *
from tools.parsers import *

url = str(input("INPUT SSC CGL digialm url: "))	
resp = getpage(url=url)
Parseme(resp=resp).main()
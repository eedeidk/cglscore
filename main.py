import requests
import os
from bs4 import BeautifulSoup as bs
import ua_generator

		

def getpage(url):
	rawua = ua_generator.generate(device='desktop', browser='firefox')
	header = {'User-Agent': str(rawua)}
	try:
		r = requests.get(url, headers=header)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return None

url = str(input("INPUT SSC CGL digialm url: "))	
resp = getpage(url=url)

class Parseme:
	def __init__(self, resp:str) -> None:
		self.soup = bs(resp, 'lxml')
	
	def parse1(self):
		self.ci_cont = self.soup.find('div', class_='main-info-pnl')
		self.ci_info = self.ci_cont.find('tbody')
		self.response_area = self.soup.find('div', class_='grp-cntnr')
	
	def candi_info(self):
		table = self.ci_info
		# Initialize an empty dictionary
		self.data_dict = {}

		# Iterate through each row in the table
		for row in table.find_all('tr'):
			columns = row.find_all('td')
			if len(columns) == 2:
				key = columns[0].text.strip()
				value = columns[1].text.strip()
				self.data_dict[key] = value
		
		for key in self.data_dict:
			print(key, self.data_dict[key])
	
	@staticmethod
	def update_counts(target_dict, source_dict):
		for key, value in source_dict.items():
			target_dict[key] += value
		return target_dict

	def qa_calc(self):
		#find sections:
		sections = self.response_area.find_all('div', class_='section-cntnr')
		c = {'r': 0, 'w': 0, 'u': 0}
		for section in sections:
			secvalues, secname = self.parse_section(section)
			self.score_card(secvalues, secname)
			c = self.update_counts(c, secvalues)
		
		# final:
		self.score_card(c, 'Total')
	
	def parse_section(self, section:bs):
		# section info:
		label = section.find('div', class_='section-lbl').get_text(strip=True)
		questions = section.find_all('div', class_='question-pnl')
		c = {
			'r': 0,
			'w': 0,
			'u': 0
			}
		for q in questions:
			a = self.parse_question(q)
			c[a] += 1
		return c, label
	
	def parse_question(self, q:bs):
		# generate score:
		tc = q.find('table', class_='questionPnlTbl')
		# tc has two table:
		# first table is question:
		qtable = tc.find('table', class_='questionRowTbl')
		atable = tc.find('table', class_='menu-tbl')
		# correct response:
		rt_c = qtable.find('td', class_='rightAns').get_text(strip=True)
		rt_o = str(rt_c).split('.')[0]
		# given resp:
		my_c = atable.find_all('td')
		my_c = my_c[-1].get_text(strip=True)
		# now calculate:
		if my_c=='--':
			s = 'u'
		elif my_c==rt_o:
			s = 'r'
		else:
			s = 'w'
		return s

	def score_card(self,v:dict, n:str):
		# final calc
		sq_total = v['r']*2 - v['w']*0.3333
		sq_acc = v['r']/(v['r']+v['w'])*100
		toprint = f'''{n}
		Score: {sq_total}, Accuracy: {sq_acc}
		Right/Wrong/NA: {v['r']}/{v['w']}/{v['u']}'''
		print(toprint)
	
	def main(self):
		self.parse1()
		self.candi_info()
		self.qa_calc()

Parseme(resp=resp).main()
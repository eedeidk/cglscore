from bs4 import BeautifulSoup as bs

class Parseme:
	def __init__(self, resp:str, pos:2, neg:0.5) -> None:
		self.soup = bs(resp, 'lxml')
		self.answer_column = None
		self.sq_pos = pos
		self.sq_neg = neg
	
	def parse1(self):
		self.ci_cont = self.soup.find('div', class_='main-info-pnl')
		if self.ci_cont:
			self.ci_info = self.ci_cont.find('tbody')
		else:
			self.ci_info = None
		self.response_area = self.soup.find('div', class_='grp-cntnr')
	
	def candi_info(self):
		if not self.ci_info:
			print('No candidate info present')
			return None
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
		c = {'r': 0,'w': 0,'u': 0}
		# some scorecard does not show questions:
		if len(questions)==0:
			# question not present type:
			table = section.find('table')
			if table:
				headers = table.thead.find_all('th')
				##
				if not self.answer_column:
					#
					a = ''
					for each in headers:
						a+= each.get_text(strip=True)+'||'
					print(f'Rows:\n{a}')
					self.answer_column = int(input('Which one is answer column: '))
					self.response_column = int(input('Which one is response column: '))
				##
				qs = table.tbody.find_all('tr')
				for q in qs:
					a = self.parse_qnp(q)
					c[a] += 1
			else:
				raise ValueError('This website is not supported kindly'
				'submit scorecard url to Issue section of https://github.com/eedeidk/cglscore')
		for q in questions:
			a = self.parse_question(q)
			c[a] += 1
		return c, label
	
	def parse_qnp(self, q:bs):
		cq = q.find_all('td')
		aq = cq[self.answer_column-1].get_text(strip=True)
		rq = cq[self.response_column-1].get_text(strip=True)
		## score logic:
		if rq == aq:
			t = 'r'
		elif rq.isdigit():
			t = 'w'
		else:
			t = 'u'
		return t

	
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
		sq_total = v['r']*self.sq_pos - v['w']*self.sq_neg
		sq_acc = v['r']/(v['r']+v['w'])*100
		toprint = f'''{n}
		Score: {sq_total}, Accuracy: {sq_acc}
		Right/Wrong/NA: {v['r']}/{v['w']}/{v['u']}'''
		print(toprint)
	
	def main(self):
		self.parse1()
		self.candi_info()
		self.qa_calc()
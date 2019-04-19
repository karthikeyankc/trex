import json
import re
from pandas import DataFrame, Index

stage = {}

with open('export.json', 'r') as f:
	f = json.load(f)
	cards = f['cards']
	for card in cards:
		title = card['name']
		description = card['desc']
		custom_fields = card['customFieldItems']
		values = []

		#Regex Magic!
		r = re.search(r'\d{10}', title)
		phone = r.group(0) if r else "None"
		r = re.search(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', description)
		email = r.group(0) if r else "None"

		for items in custom_fields:
			for item, value in items.items():
				try:
					values.append(value['text'])
				except:
					pass
		metadata = [phone, email, description, ", ".join(values)]
		stage[title] = metadata


df = DataFrame.from_dict(stage)
df.index = Index(['Phone', 'Email', 'Description', 'Custom Field Data'], name='Title')
df = df.transpose()
df.to_excel("trexxed.xlsx")
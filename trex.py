import json
import re
from pandas import DataFrame, Index

row = {}

with open('export.json', 'r') as f:
	f = json.load(f)
	cards = f['cards']
	for card in cards:
		title = card['name']
		description = card['desc']
		custom_fields = card['customFieldItems']
		url = card['url']
		custom_field_data = []

		#Regex Magic!
		r = re.search(r'\d{10}', title)
		phone = r.group(0) if r else "None"
		r = re.search(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', description)
		email = r.group(0) if r else "None"

		for items in custom_fields:
			for value in items.values():
				try:
					custom_field_data.append(value['text'])
				except:
					pass
		metadata = [phone, email, description, ", ".join(custom_field_data), url]
		row[title] = metadata


df = DataFrame.from_dict(row)
df.index = Index(['Phone', 'Email', 'Description', 'Custom Field Data', 'Card URL'], name='Title')
df = df.transpose()
df.to_excel("trexxed.xlsx")
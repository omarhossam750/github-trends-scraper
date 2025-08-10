import requests, csv
from bs4 import BeautifulSoup

root_url = "https://github.com"
url = "https://github.com/trending?spoken_language_code=en" # Change it to any spoken language!
file_name = "data.csv" # Change it to anything you want 
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

main = soup.find("main")
if main:
	Box = main.find("div", class_="Box")
	rows = Box.find_all("article", class_="Box-row")
	with open(file_name, "w", encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow(["Author", "Name", "description", "lang", "stars", "link"])
		
		for row in rows:
			row_h2 = row.find("h2")
			row_title = row_h2.find("a", class_="Link")
			title_array = row_title.text.strip().split("/") # <a></a> -> contains author + repo name
			
			author = title_array[0].strip()
			name = title_array[1].replace("\n", "").strip()
			stars = row.find("a", attrs={"href": f"/{author}/{name}/stargazers"}).text.strip()
			programming_lang = row.find("span", attrs={"itemprop": "programmingLanguage"})
			if programming_lang:
				programming_lang = programming_lang.text.strip() 
			else:
				programming_lang = None
			p_els = row.find_all("p", recursive=False)
			description = p_els[0] if p_els else p_els # <p> elements -> p_els
			if description:
				description = description.text.strip()
			else:
				description = None
			link = f"{root_url}/{author}/{name}"
			writer.writerow([author, name, description, programming_lang, stars, link])
			
		print("Succesfully Wrote to CSV File!")
	
	

from io import open_code
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

download_dir = "C:\\Users\\gupta\\Documents\\ACMPapers2" # for linux/*nix, download_dir="/usr/Public"
options = webdriver.ChromeOptions()

profile = {
	"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
    "download.default_directory": download_dir , 
	"download.extensions_to_open": "applications/pdf",
	"download.prompt_for_download": False, #To auto download the file
	"download.directory_upgrade": True,
	"plugins.always_open_pdf_externally": True
}
options.add_experimental_option("prefs", profile)

driver = webdriver.Chrome('C:\\Users\\gupta\\Research Work\\ACM Parser\\chromedriver.exe', options=options)

# driver.get('https://dl-acm-org.proxy2.library.illinois.edu/conference/comm/proceedings')
driver.get('https://dl-acm-org.proxy2.library.illinois.edu/conference/comm/proceedings')


# Login
username = WebDriverWait(driver,30).until(
	EC.presence_of_element_located((By.ID, "j_username"))
)

password = WebDriverWait(driver,30).until(
	EC.presence_of_element_located((By.ID, "j_password"))
)

username.send_keys("")
password.send_keys("")

submit = WebDriverWait(driver,30).until(
	EC.presence_of_element_located((By.NAME, "_eventId_proceed"))
)

submit.click()

'''
downloads all of the pdfs that are on the page
identifies the links and then downloads the ones that look like pdfs
'''
def download_links_on_single_card():
	for a in driver.find_elements_by_tag_name("a"):
		print("a tag")
		link = a.get_attribute("href")

		# identifies this link as a paper that needs to be downloaded
		if "/doi/pdf/10.1145/" in link:
			# actually download the paper
			driver.get(link)
def go_back_one_page():
	driver.execute_script("window.history.go(-1)")

'''
looks at a single webpage,
one by one opens the dropdown arrows,
downloads all of the papers in the dropdown
'''
def download_pdfs_from_single_page():
	# download all of the pdfs
	'''
	make a while loop that loops until all of the arrow elements are clicked
	it checks the array of arrows and clicks the first one that has an attribute of aria-expanded = "false"
	then it waits until the page reloads

	what this does is individually load all of the dropdowns (we never really need them all open at once)
	as they are open, we can download all of the content from them at that time
	'''
	ids_already_clicked = []
	while True:
		# identifies the arrows on the page
		a_tags = driver.find_elements_by_tag_name("a")
		arrows = []

		for a_tag in a_tags:
			if '/doi/proceedings/10.1145/3452296?tocHeading=heading' in a_tag.get_attribute("href"):
				arrows.append(a_tag)

		# makes sure that the page has loaded
		Elem = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'issue-item__content')))
		# identifies the arrow to click
		arrow_to_click = None
		for a in arrows:
			if a.get_attribute("aria-expanded") == "false" and a.get_attribute("id") not in ids_already_clicked:
				arrow_to_click = a
				ids_already_clicked.append(a.get_attribute("id"))
				break
		# if the work is done
		if arrow_to_click == None:
			print("Breaking out of loop")
			break
		else:
			driver.get(arrow_to_click.get_attribute("href"))
			download_links_on_single_card()


'''
the same way that we navigated the dropdowns on individual pages will be used to navigate the huge dropdowns on the main page
'''
 # we are not allowed to just list the links that we have to click and go to them one by one,
 # we need to actually simulate clicking each one

def open_headings_on_main_page():
	last_element = WebDriverWait(driver,30).until(
		EC.presence_of_element_located((By.XPATH, '//*[@id="pb-page-content"]/div/main/div/div[2]/div[2]/div/ul/li[21]/a'))
	)
	a_tags = driver.find_elements_by_tag_name("a")
	large_headings = []
	for a in a_tags:
		if a.get_attribute("class") == "accordion-tabbed__control proceedings-browse__control":
			large_headings.append(a)

	# open all headings one by one
	for i in range(1, len(large_headings)):
		heading = large_headings[i]
		driver.execute_script("arguments[0].click();", heading)

		# to make sure that the screen has loaded properly
		last_element = WebDriverWait(driver,30).until(
			EC.presence_of_element_located((By.XPATH, '//*[@id="pb-page-content"]/div/main/div/div[2]/div[2]/div/ul/li[21]/a'))
		)

	# identify the earliest large heading that we have not FULLY explored yet
	a_tags = driver.find_elements_by_tag_name("a")
	small_headings = []
	for a in a_tags:
		if a.get_attribute("class") == "accordion-tabbed__control loadAjax":
			small_headings.append(a)

	# open all headings one by one
	for i in range(1, len(small_headings)):
		heading = small_headings[i]
		driver.execute_script("arguments[0].click();", heading)
		# to make sure that the screen has loaded properly
		last_element = WebDriverWait(driver,30).until(
			EC.presence_of_element_located((By.XPATH, '//*[@id="pb-page-content"]/div/main/div/div[2]/div[2]/div/ul/li[21]/a'))
		)

# last_element = WebDriverWait(driver,30).until(
# 		EC.presence_of_element_located((By.XPATH, '//*[@id="pb-page-content"]/div/main/div[4]/div/div[2]/div[1]/div/div/div/div[8]'))
# )

card_titles_visited = []
def visit_each_card(extra_num):
	print("supposed to be visiting each card!!!!")
	load_checker = WebDriverWait(driver,30).until(
		EC.presence_of_element_located((By.XPATH, '//*[@id="pb-page-content"]/div/main/div[4]/div/div[2]/div[1]/div'))
	)
	print("THE LOAD CHECKER IS COMPLETED")
	# this array contains all of the papers on the screen, their links that are neccessary
	while True:
		a_tags = []
		for a in driver.find_elements_by_tag_name("a"):
			if "/doi/10.1145/" + extra_num  in a.get_attribute("href"):
				if a.text not in card_titles_visited:
					a_tags.append(a)
		print(len(a_tags))
		if len(a_tags) > 0:
			card_titles_visited.append(a_tags[0].text)
			# parent = a_tags[0].find_element_by_xpath("..")
			# parent.click()
			a_tags[0].click()
			scrape_data_from_card_page()
		else:
			break

# this successfully does everything necessary on a card page
def scrape_data_from_card_page():
	# make sure that the page has properly loaded
	# title
	title_element = WebDriverWait(driver,30).until(
		EC.presence_of_element_located((By.CLASS_NAME, 'citation__title'))
	)
	title = title_element.text
	# list of authors
	try:
		expand_button = driver.find_element_by_class_name("removed-items-count")
		expand_button.click()
	except:
		pass

	author_elements = driver.find_elements_by_class_name("author-name")
	authors = []
	for a in author_elements:
		authors.append(a.get_attribute("title"))
	# time of writing
	date = driver.find_element_by_class_name("epub-section__date")
	date_txt = date.text
	# get the link
	link = driver.find_element_by_class_name("issue-item__doi")
	link_txt = link.text
	# add all of the data to the json file
	information_dict = {"title":title, "authors": authors, "published":date_txt, "link":link_txt}
	with open("paper_information2.json", "r") as f:
		papers = json.load(f)
	papers.append(information_dict)
	with open("paper_information2.json", "w") as f:
		json.dump(papers, f)

	# actually download the pdf
	pdf_button = driver.find_element_by_xpath('//*[@id="pb-page-content"]/div/main/div[2]/article/div[1]/div[2]/div/div/div[6]/div/div[2]/ul[2]/li[2]/a')
	pdf_button.click()

	go_back_one_page()

proceedings_visited = []
def main():
	while True:
		open_headings_on_main_page()
		# wait until the bottom one is open
		load_checker = WebDriverWait(driver,30).until(
			EC.presence_of_element_located((By.XPATH, '//*[@id="conferenceW-3"]/div/ul/li/a'))
		)
		try:
			cookies = WebDriverWait(driver,30).until(
				EC.presence_of_element_located((By.XPATH, '//*[@id="pb-page-content"]/div/div/div[2]/a'))
			)
		except:
			pass
		print("all tabs opened")
		a_tags = []
		for a in driver.find_elements_by_tag_name('a'):
			if '/doi/proceedings/10.1145' in a.get_attribute("href") and a.text not in proceedings_visited:
				a_tags.append(a)
		proceedings_visited.append(a_tags[0].text)
		a_tags[0].click()
		print("SHOULD HAVE CLICKED THE BUTTON")
		print('PRINTING:' + a_tags[0].get_attribute("href").replace('https://dl-acm-org.proxy2.library.illinois.edu/doi/proceedings/10.1145/',''))
		visit_each_card(a_tags[0].get_attribute("href").replace('https://dl-acm-org.proxy2.library.illinois.edu/doi/proceedings/10.1145/',''))
		driver.execute_script("window.history.go(-1)")
		# for l in links_to_click:
		# 	if l.text not in proceedings_visited:
		# 		a_tags.append(l)
		# if len(a_tags) > 0:
		# 	proceedings_visited.append(a_tags[0].text)
		# 	a_tags[0].click()
		# 	visit_each_card()
		# else:
		# 	break
 

main()
# visit_each_card()



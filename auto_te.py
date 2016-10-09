from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys
import time

def get_course_and_teacher_elements(driver):
	dropdown_elements = driver.find_elements_by_tag_name("select")
	for el in dropdown_elements:
		el_name = el.get_attribute("name")
		if el_name == "ddlcourse":
			course_select = el
		elif el_name == "ddlteacher":
			teacher_select = el
	return course_select, teacher_select


def do_auto_te(uname, passwd):

	delay = 5
	driver = webdriver.Chrome("chromedriver")

	driver.get("http://www.dss.nitc.ac.in")

	try:
	    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'TABLE1')))
	    # print "Page is ready!"
	except TimeoutException:
	    print "page not loaded...\nexiting..."
	    sys.exit()


	driver.maximize_window()
	page_links = driver.find_elements_by_tag_name("a")
	for link in page_links:
		if link.text.find("COURSE REGISTRATION") != -1:
			link.click()
			break

	try:
	    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'bottomstrip1')))
	    # print "Page is ready!"
	except TimeoutException:
	    print "page not loaded...\nexiting..."
	    sys.exit()

	input_elements = driver.find_elements_by_tag_name("input")
	for el in input_elements:
		el_name = el.get_attribute("name")
		if el_name == "user":
			uname_input = el
		elif el_name == "passwd":
			passwd_input = el
		elif el_name == "Submit1":
			submit_btn = el

	uname_input.send_keys(uname)
	passwd_input.send_keys(passwd)
	submit_btn.click()

	try:
		if driver.switch_to_alert().text.find("Invalid Login!") != -1:
			return "Incorrect Username/Password"
	except NoAlertPresentException:
		pass
	
	driver.switch_to_frame("contents")

	try:
	    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'TreeView1')))
	except TimeoutException:
	    print "page not loaded...\nexiting..."
	    sys.exit()

	page_links = driver.find_elements_by_tag_name("a")
	for link in page_links:
		if link.text.find("Teacher Evaluation") != -1:
			link.click()
			break

	driver.switch_to_default_content()
	driver.switch_to_frame("main")

	while True:
		try:
		    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'Label2')))
		    completed_notification = driver.find_element_by_id('Label2')
		    if completed_notification.text.find("You have completed the Teacher Evaluation") != -1:
			    print "Evaluation is complete. Bye!!"
			    sys.exit()
		except TimeoutException:
		    pass
		get_teacher_btn = driver.find_element_by_id("Button3")
		course_select = get_course_and_teacher_elements(driver)[0]
		course_option = course_select.find_elements_by_tag_name("option")[0]
		course_option.click()
		get_teacher_btn.click()
		time.sleep(1)
		try:
			driver.switch_to_alert().accept()
		except NoAlertPresentException:
			pass

		teacher_select = get_course_and_teacher_elements(driver)[1]
		teacher_option = teacher_select.find_elements_by_tag_name("option")[0]
		teacher_option.click()
		# teacher_select.select_by_index(0)

		next_btn = driver.find_element_by_id("Button1")
		next_btn.click()
		try:
		    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'Form1')))
		except TimeoutException:
		    print "page not loaded...\nexiting..."
		    sys.exit()

		dropdown_elements = driver.find_elements_by_tag_name("select")
		# print len(dropdown_elements)
		for el in dropdown_elements:
			first_option = el.find_elements_by_tag_name("option")[1]
			first_option.click()

		submit_btn = driver.find_element_by_id("Button1")
		submit_btn.click()

if __name__ == '__main__':
	args = sys.argv[1:]
	uname = None
	passwd = None
	for arg in args:
		if arg[0:7] == "-uname=":
			uname = arg[7:]
		elif arg[0:8] == "-passwd=":
			passwd = arg[8:]

	if uname and passwd:
		print do_auto_te(uname, passwd)
	else:
		print "Username and/or Password not provided"
	sys.exit()

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

class webEngine(object):
	def __init__(self,commadnType=0):
		os.system('TASKKILL /F /IM firefox.exe')
		firefox_profile = webdriver.FirefoxProfile(r"C:\\Users\\bengou\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\uk6bzv9q.default")
		self.driver = webdriver.Firefox(firefox_profile=firefox_profile)
		self.waitTime = 5
		#0为jquery查找方式，1为xpath查找方式，2为js查找方式
		self.commandType = commadnType
		self.driver.implicitly_wait(30)

	def fastExcuJs(self,command):
		self.driver.execute_script(command)

	def excuJs(self,command,waitTime=0):
		if waitTime > self.waitTime:
			return 200
		result=None
		if not 'return ' in command:
			command = 'return '+command+'.text();'
		try:
			result = self.driver.execute_script(command)
			self.log(results)
		except:
			checkCommand = command.split(')')[0]+").text();"
			result = self.driver.execute_script(checkCommand)
		self.log(result)
		if result == None or result == "":
			time.sleep(0.5)
			waitTime += 1
			return self.excuJs(command,waitTime)
		else:
			self.switchToWindow()
			self.log(command)
			return result

	def excuXpath(self,content,tagType="0",waitTime=0):
		tag={"0":By.ID,"1":By.CLASS_NAME}
		if waitTime > self.waitTime:
			return 200
		try:
			element = self.driver.find_element(tag.get(tagType),content)
			print(content + " success"+":"+tag.get(tagType))
			return element
		except Exception as e:
			time.sleep(0.5)
			return self.excuXpath(content,tagType,waitTime+1)

	def open(self,url):
		self.log(url)
		self.driver.get(url)

	def type(self, tagId, data, commandTag="ID"):
		if self.commandType == 0:
			command = "return $('#"+tagId+"').val("+data+")"
			if self.excuJs(command) == 200:
				self.logError()
		elif self.commandType == 1:
			element = self.excuXpath(tagId)
			if element == 200:
				self.logError()
			else:
				element.send_keys(data)

	def click(self, tagId, tagType="0"):
		if self.commandType == 0:
			command = "return $('#"+tagId+"').click()"
			if excuJs(command) == 200:
				self.logError()
		elif self.commandType == 1:
			element = self.excuXpath(tagId,tagType)
			if element == 200:
				self.logError()
			else:
				element.click()
				time.sleep(2)
	def switchToWindow(self):
		handles = self.driver.window_handles
		if len(handles) > 1:
			self.driver.close()
			self.driver.switch_to_window(handles[1])

	def log(self,content):
		localTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
		print(localTime + ":" +content)

	def quit(self):
		self.driver.quit()

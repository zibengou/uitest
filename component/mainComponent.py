from library.setfile import *
from library.webEngine import *
class mainComopent(object):
	def __init__(self,configPath):
		config = readConfig(configPath)
		if isinstance(config['root']['component'],list):
			self.componentList = config['root']['component']
		else:
			self.componentList=[]
			self.componentList.append(config['root']['component'])
		self.driver = webEngine(1)
		self.excu={"0":self.driver.excuJs,"1":self.driver.open,"2":self.driver.fastExcuJs,"3":self.driver.click,"5":self.driver.click}
	def excuComponent(self,component):
		if isinstance(component['action'],list):
			for action in component['action']:
				if action['@type'] == "4":
					self.driver.type(action["@command"],action["@data"])
				elif action['@type'] >= "5":
					self.excu.get(action['@type'])(action['@command'],action['@tagType'])
				else:
					self.excu.get(action['@type'])(action['@command'])
		else:
			action = component['action']
			if action['@type'] == "4":
				self.driver.type(action["@command"],action["@data"])
			elif action['@type'] >= "5":
				self.excu.get(action['@type'])(action['@command'],action['@tagType'])
			else:
				self.excu.get(action['@type'])(action['@command'])
	def doDriver(self):
		for component in self.componentList:
			print(component['@name'])
			if '@reTry' in component.keys():
				for i in range(int(component['@reTry'])):
					print("------------in")
					self.excuComponent(component)
			else:
				self.excuComponent(component)
		# self.driver.quit()


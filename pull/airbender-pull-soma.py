import os,sys

sys.path.append("/opt/livingdata/lib")
sys.path.append("/opt/SoMA/python/lib")
from livdattable import *
from libsoma import *
import pygsheets
from bs4 import BeautifulSoup

class AirBender(SoMACyborg):
	def __init__(self,configfile,headless=False):
		config=ConfigParser.ConfigParser()
		config.read(configfile)
		self.config=config
		try:
			self.fbusr = config.get("User","fbusername")
			self.fbpwd = config.get("User","fbpassword")
		except:
			print "Cyborg did not have an FB id configured"
		try:
			self.googleusr = config.get("User","googleusername")
			self.googlepwd = config.get("User","googlepassword")
		except:
			print "Cyborg did not have an Google id configured"
		try:
			self.outhstore = config.get("Google","outhstore")
			self.outhfile = config.get("Google","outhfile")
		except:
			print "Cyborg did not get a google client secret"
			
		
		self.airvedausername = config.get("Airveda","username")
		self.airvedapassword = config.get("Airveda","password")
		self.airvedadevicelist = config.get("Airveda","devicelist")
		self.gc=pygsheets.authorize(outh_file=self.outhfile,outh_nonlocal=True,outh_creds_store=self.outhstore)
		self.airvedadevsheet=self.gc.open_by_key(self.airvedadevicelist)
		
		
		self.datapath=config.get("System","datapath")
		sessionpathprefix=config.get("System","sessionpathprefix")
		ts=datetime.now()
		sessiondir=sessionpathprefix+"-"+ts.strftime("%Y%b%d-%H%M%S")
		self.sessionpath=os.path.join(self.datapath,sessiondir)
		self.sessiondownloaddir=os.path.join(self.sessionpath,"downloads")
		self.sessionjsonpath=os.path.join(self.sessionpath,"json")
		if not os.path.exists(self.datapath):
			os.mkdir(self.datapath)
		if not os.path.exists(self.sessionpath):
			os.mkdir(self.sessionpath)
		if not os.path.exists(self.sessiondownloaddir):
			os.mkdir(self.sessiondownloaddir)
		if not os.path.exists(self.sessionjsonpath):
			os.mkdir(self.sessionjsonpath)
		
		if headless==True:
			os.environ['MOZ_HEADLESS'] = '1'
		
		firefox_profile = webdriver.FirefoxProfile()
		firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
		firefox_profile.set_preference("browser.download.dir", self.sessiondownloaddir);

		firefox_profile.set_preference("browser.download.folderList", 2);


		firefox_profile.set_preference("browser.download.manager.showWhenStarting", False);

		firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, text/csv",)
		
		driver = webdriver.Firefox(firefox_profile=firefox_profile)
		self.driver=driver
	def airveda_get_dev_data(self,dev):
		if os.path.exists(os.path.join(self.sessiondownloaddir,str(dev)+".csv")):
			os.rename(os.path.join(self.sessiondownloaddir,str(dev)+".csv"),os.path.join(self.sessiondownloaddir,str(dev)+"-prev.csv"))
		self.goto_url("http://api.airveda.com/core/download/")
		time.sleep(10)
		self.driver.find_element_by_id("checkbox2").click()
		self.driver.find_element_by_id("checkbox3").click()
		self.driver.find_element_by_id("checkbox4").click()
		self.driver.find_element_by_id("checkbox5").click()
		self.driver.find_element_by_id("checkbox6").click()
		self.driver.find_element_by_name("average").click()
		self.driver.find_element_by_class_name("select2-search__field").click()
		self.driver.find_element_by_class_name("select2-search__field").send_keys(dev)
		self.driver.find_element_by_class_name("select2-search__field").send_keys(Keys.RETURN)
		time.sleep(3)
		self.driver.find_element_by_id("download_button").click()
		time.sleep(20)
		os.rename(os.path.join(self.sessiondownloaddir,"airveda_data.csv"),os.path.join(self.sessiondownloaddir,str(dev)+".csv"))
		return os.path.join(self.sessiondownloaddir,str(dev)+".csv")
	def airveda_update(self):
		devsheetdf=self.airvedadevsheet.worksheet_by_title("Sheet1").get_as_df()
		for dev in devsheetdf.devname:
			print self.airveda_get_dev_data(dev)
	
if __name__=="__main__":
	airvedaurl="http://api.airveda.com/core/download/"
	sks=AirBender("/home/arjun/ids/sks.conf",headless=True)
	sks.goto_url("http://api.airveda.com/core/download/")
	time.sleep(10)
	sks.driver.find_element_by_name("username").send_keys(sks.airvedausername)
	sks.driver.find_element_by_name("password").send_keys(sks.airvedapassword)
	sks.driver.find_element_by_name("username").send_keys(Keys.RETURN)
		

devicedatawsheet=devdatasheet.worksheet_by_title(str(dev))
df=pandas.read_csv(os.path.join(sks.sessiondownloaddir,str(dev)+".csv"))
devdatadf=devicedatawsheet.get_as_df()
df.columns=devdatadf.columns
df2=devdatadf.append(df).drop_duplicates()
devicedatawsheet.set_dataframe(df2,(1,1))
history
devicedatawsheet=devdatasheet.worksheet_by_title(str(dev))
df=pandas.read_csv(os.path.join(sks.sessiondownloaddir,str(dev)+".csv"))
devdatadf=devicedatawsheet.get_as_df()
df.columns=devdatadf.columns
df2=devdatadf.append(df).drop_duplicates()
devicedatawsheet.set_dataframe(df2,(1,1))
history
devicedatawsheet=devdatasheet.worksheet_by_title(str(dev))
df=pandas.read_csv(os.path.join(sks.sessiondownloaddir,str(dev)+".csv"))
devdatadf=devicedatawsheet.get_as_df()
df.columns=devdatadf.columns
df2=devdatadf.append(df).drop_duplicates()
devicedatawsheet.set_dataframe(df2,(1,1))
sks.airveda_update()
sks=SoMACyborg("/home/arjun/ids/sks.conf")
%run airbender-pull-soma.py
sks.airveda_update()
devicedatawsheet=devdatasheet.worksheet_by_title(str(dev))
df=pandas.read_csv(os.path.join(sks.sessiondownloaddir,str(dev)+".csv"))
devdatadf=devicedatawsheet.get_as_df()
df.columns=devdatadf.columns
df2=devdatadf.append(df).drop_duplicates()

devicedatawsheet.set_dataframe(df2,(1,1))
cat /home/arjun/ids/sks/SoMASession-2018Jan23-011724/downloads/1211170143.csv
dev
sks.sessiondownloaddir
df
df2
devicedatawsheet=devdatasheet.worksheet_by_title(str(dev))
df=pandas.read_csv(os.path.join(sks.sessiondownloaddir,str(dev)+".csv"))
devdatadf=devicedatawsheet.get_as_df()
df.columns=devdatadf.columns
df2=devdatadf.append(df).drop_duplicates()

devicedatawsheet.set_dataframe(df2,(1,1))
devdatasheet.worksheets
devdatasheet.worksheets()
a=devdatasheet.worksheets()
a[0].sheetname
b=a[0]
b.title
for sheets in a:
    sheetnames.append(sheets.title)
sheetnames=[]
sheets=devdatasheet.worksheets()
for sheet in sheets:
    sheetnames.append(sheet.title)
sheetnames
if str(dev) in sheetnames:
    print "Hell"
if str(dev) in sheetnames:
    print "Hell"
    else:
if str(dev) in sheetnames:
    print "Hell"
else:
    devdatasheet.add_worksheet(str(dev))
for dev in devlist.devname:
    if str(dev) in sheetnames:
        print "Sheet exists"
    else:
        print "No sheet"
columns=df.columns
columns=list(df.columns)
for dev in devlist.devname:
    if str(dev) in sheetnames:
        print "Sheet exists"
    else:
        print "No sheet"
        devdatasheet.add_worksheet(str(dev))
        dsheet=devdatasheet.worksheet_by_title(str(dev))
        dsheet.update_row(1,columns)
for dev in devlist.devname:
    if str(dev) in sheetnames:
        print "Sheet exists"
    else:
        print "No sheet"
        devdatasheet.add_worksheet(str(dev))
        dsheet=devdatasheet.worksheet_by_title(str(dev))
        dsheet.update_row(1,columns)
sheetnames=[]
a=devdatasheet.worksheets()
sheets=devdatasheet.worksheets()
for sheet in sheets:
    sheetnames.append(sheet.title)
for dev in devlist.devname:
    if str(dev) in sheetnames:
        print "Sheet exists"
    else:
        print "No sheet"
        devdatasheet.add_worksheet(str(dev))
        dsheet=devdatasheet.worksheet_by_title(str(dev))
        dsheet.update_row(1,columns)
sheets=devdatasheet.worksheets()
sheetnames=[]
for sheet in sheets:
    sheetnames.append(sheet.title)
for dev in devlist.devname:
    if str(dev) in sheetnames:
        print "Sheet exists"
    else:
        print "No sheet"
        devdatasheet.add_worksheet(str(dev))
        dsheet=devdatasheet.worksheet_by_title(str(dev))
        dsheet.update_row(1,columns)
for dev in devlist.devname:
    devicedatawsheet=devdatasheet.worksheet_by_title(str(dev))
    df=pandas.read_csv(os.path.join(sks.sessiondownloaddir,str(dev)+".csv"))
    devdatadf=devicedatawsheet.get_as_df()
    df.columns=devdatadf.columns
    df2=devdatadf.append(df).drop_duplicates()
    devicedatawsheet.set_dataframe(df2,(1,1))
dev
df2
df.columns
df.columns
df.columns
dev
for dev in devlist.devname:
    try:
        devicedatawsheet=devdatasheet.worksheet_by_title(str(dev))
        df=pandas.read_csv(os.path.join(sks.sessiondownloaddir,str(dev)+".csv"))
        devdatadf=devicedatawsheet.get_as_df()
        df.columns=devdatadf.columns
        df2=devdatadf.append(df).drop_duplicates()
        devicedatawsheet.set_dataframe(df2,(1,1))
    except:
        print os.path.join(sks.sessiondownloaddir,str(dev)+".csv")
history

from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests
import time
import json
import selenium
from Station import Station,Line
import copy
import csv
class CarPortal():
    sleepTime=3
    line = Line()
    goWorkList=list()
    def __init__(self,id,pw):
        try:
            self.id = id
            self.pw = pw

        except Exception as e:
            print("init error:",e)

    def loginSite(self):
        try:
            print("login")
            option = webdriver.ChromeOptions()
            option.add_argument('hide_console')
            self.driver = webdriver.Chrome('/Users/yunmi/Downloads/chromedriver_win32/chromedriver3.exe', desired_capabilities=option.to_capabilities(),service_args=["hide_console",])

            self.driver.implicitly_wait(10)

            self.driver.get('http://samsung.u-vis.com/kh')


            self.driver.find_element_by_id('i_userid').send_keys(self.id)
            self.driver.find_element_by_id('n_passwd').send_keys(self.pw)
            self.driver.find_element_by_xpath('/html/body/form/div/div[2]/div/span/input').click()
            self.driver.implicitly_wait(10)

        except Exception as e:
            print(e)
            return -2
        except selenium.common.exceptions.UnexpectedAlertPresentException as e:
            #print("접속 error : ",e)
            # Popup 제거
            alert = self.driver.switch_to.alert
            alert.accept()
            index=e.__str__().find("접속")
            if index != -1:
                return -2
            else:
                return -1
    def getCsv(self):
        try:
            with open('goWor.csv',newline='') as csvfile:
                reader = csv.reader(csvfile,delimiter=' ',quotechar='|')
                for row in reader:
                    self.goWorkList.append(row)

        except Exception as e:
            print(e)


    def getGoWorkDataInfo(self):
        ## 검색 화면 이동
        self.driver.get('http://samsung.u-vis.com:8080/portalm/VISGuide.do?method=main&pickoffice=0000011&scrId=POT002&menuCode=UV0202')
        self.driver.implicitly_wait(5)
        time.sleep(self.sleepTime)
        for nosun in self.goWorkList:
            ## 검색
            self.driver.switch_to.default_content()
            self.driver.find_element_by_id('search_val1').clear()
            self.driver.find_element_by_id('search_val1').send_keys(nosun[0])
            self.driver.find_element_by_xpath('//*[@id="tabArea1"]/a/img').click()
            time.sleep(1)
            ## driver와 requests Cookie 맞추기
            test = self.driver.get_cookies()
            s = requests.Session()
            for cookie in test:
                s.cookies.set(cookie['name'],cookie['value'])

            self.driver.switch_to.frame('station')
            html = self.driver.page_source
            soup = bs(html,'html.parser')
            self.listForGame = soup.select('#busInfo > div > table > tbody > tr > td > a:nth-of-type(1)')
            a= 0


            for list in self.listForGame:
                try:
                    if a%2==0:
                        self.time = list.text
                        a=a+1
                        node = Station(nosun[0],self.time)

                    else:
                        a=a+1
                        first = list.get_attribute_list("href").__str__()
                        paraList = first.split('\'')
                        #rm_idx
                        para1 = paraList[1]
                        #rt_key
                        para2 = paraList[3]
                        #lat
                        para3 = paraList[5]
                        #lon
                        para4 = paraList[7]
                        print("Befor Request")
                        res = s.get('http://samsung.u-vis.com:8080/portalm/VISMapControl.do?method=route&rm_idx='+para1+'&rt_key='+para2+'&lat='+para3+'&lon='+para4+'&i_day=123001')
                        print("After Request")
                        time.sleep(2)
                        jsonData = json.loads(res.text)
                        print(a)
                        for i in jsonData["dataList"]:
                            idx = i["SI_IDX"]
                            name = i["SI_NAME"]
                            longitude = i["SI_LONGITUDE"]
                            latitude = i["SI_LATITUDE"]
                            node.addStation(idx,name,longitude,latitude)
                            node.printItem()
                            #print(idx,name,longitude,latitude)
                        temp = copy.copy(node)

                        self.line.add(temp)
                        node.clearItem()
                except Exception as e:
                    print(e)
        self.line.makeJson()

    def quitDirver(self):
        self.driver.quit()

a = CarPortal('sangyub0608.kim','q7w5r1z8^^')
a.loginSite()
a.getCsv()
a.getGoWorkDataInfo()
#a.quitDirver()
print(a.goWorkList)
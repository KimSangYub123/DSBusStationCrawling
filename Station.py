import json
from pprint import pprint as pp
class Station:
    #
    stationList=[]
    cnt = 0
    def __init__(self,_name,_time):
        self.name=_name
        self.time = _time

    def setName(self,_name,_time):
        self.name=_name
        self.time = _time


    def addStation(self,_id,_stationName,_longitude,_latitude):
        self.stationList.append((_id,_stationName,_longitude,_latitude))
        self.cnt= self.cnt+1

    def returnList(self):
        return self.stationList

    def returnName(self):
        return self.name

    def returnTime(self):
        return self.time

    def printItem(self):
        for i in self.stationList:
            print(i)

    def clearItem(self):
        self.stationList.clear()

class Line:
    stationList=[]
    a = 0
    stationDict = {}
    def __init__(self):
        pass

    def add(self,_station):
        self.stationList.append(_station)
        self.makeDict()
        self.stationList.clear()
        _station.printItem()

    def makeDict(self):


        for i in self.stationList:
            self.stationDict[self.a] = {'NAME':i.returnName(),
                             'TIME':i.returnTime()}
            self.stationDict[self.a]['LIST'] = []
            for j in i.returnList():
                try:
                    #print(j[0],j[1],j[2],j[3])
                    self.stationDict[self.a]['LIST'].append({'ID': j[0],
                                   'STATIONNAME': j[1],
                                   'LONGITUDE': j[2],
                                   'LATITUDE': j[3] })

                except:
                    pass
            self.a += 1
        #pp(self.stationDict)

    def makeJson(self):

        try:
            with open("./stationList.json", 'w+', encoding='utf-8') as fw:
                json.dump(self.stationDict, fw, sort_keys=True, indent=4, ensure_ascii=False)
        except Exception as e:
            print("error: ")
            self.log.error(e)
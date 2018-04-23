from bson.json_util import dumps
#from Controller import VRNHeaderCtrl

class VRNDetailCtrl:
    
    def __init__(self, db):
        self.db = db;
    
    def getVRNDetail(self, vrnId):
        #VRNid request.
        vrnDat = {}
        VRNDetail =  self.db.VRNDetail.find({"VRN": vrnId})
        vrnRetData = []
        for lst in VRNDetail:
            vrnDat['SEALCONDITION'] = lst['SEALCONDITION']
            vrnDat['VEHICLESTATUS'] = lst['VEHICLESTATUS']
            vrnRetData.append(lst)
        
        if VRNDetail.count() >0:
            paramValue = self.db.Params.find({ "$or" : [{
                  "Domain":'SEALCONDITION',
                  "modeNum":vrnDat["SEALCONDITION"],
                  }, {
                  "Domain": 'VEHICLESTATUS',
                  "modeNum":vrnDat["VEHICLESTATUS"]  ,
                  }]})
            if paramValue.count() == 0:
                return dumps(vrnRetData)
            else:
                
                for dtl in vrnRetData:
                    for prm in paramValue:
                        dtl[prm["Domain"]] = prm["modeTxt"]
                    
                return dumps(vrnRetData)
            return dumps(vrnRetData)
        else:
            return dumps({"msgCode":"E", "message":'No VRN number found'})
        
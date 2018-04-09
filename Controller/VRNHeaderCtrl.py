#from flask import request
from bson.json_util import dumps
from _pickle import dumps
#from Controller import VRNHeaderCtrl

class VRNHeaderCtrl:
    
    def __init__(self, db):
        self.db = db;
    
    def createVRN(self, data):
        
        
        return 'create VRN successFully'
    
    
    
    def getVRNHeaderList(self):
        VRNList =  self.db.VRNHeader.find({ "$or": [{ "VRNSTATUS": "R"}, { "VRNSTATUS": "C" }]})
        listCnt = VRNList.count()
        if listCnt >0:
            paramValue = self.db.Params.find({
                    "$or" : [{
                            "Domain":'TrnsprtMode'
                        },{
                            "Domain": 'IDProffList'
                        },{
                            "Domain":'FleetList'
                        }]})
            if paramValue.count() == 0:
                return dumps(VRNList)
            else:
                dataPrm = {};
                for prm in paramValue:
                    dataPrm[prm["Domain"]+prm["modeNum"]] = prm["modeTxt"]
                vrnRetData = []
                for lst in VRNList:
                    lst["TrnsprtMode"] = dataPrm['TrnsprtMode'+lst["MODEOFTRANSPORT"]] if lst["MODEOFTRANSPORT"] != "" else ""
                    lst["IDPROOFTYPE"] = dataPrm['IDProffList'+lst["IDPROOFTYPE"]] if lst["IDPROOFTYPE"] != "" else ""
                    lst["FLEETTYPE"] = dataPrm['FleetList'+lst["FLEETTYPE"]] if lst["FLEETTYPE"] != "" else ""
                    vrnRetData.append(lst)
                return dumps(vrnRetData)
            return dumps(VRNList)
        else:
            return 'No VRN found'
    
    def createVRNCheckIN(self, vrnId):
#         vrnCheckIN= self.db.VRNHeader.findOneAndUpdate({ "VRN": int(vrnId) }, { '$set': { "VRNSTATUS": "C" } }, { "new": True, "upsert": True })
#         if vrnCheckIN.acknowledged:
#             VRNCheckINDetail = self.db.VRNDetail.findOneAndUpdate({ VRN: req.params.VRN }, { '$set': { "VEHICLECHECKINDATE": new Date(), "VRNCHECKINBY": 'Bhaskar'}  }, { "new": True, "upsert": True })
#             if VRNCheckINDetail.acknowledged:
#                 return dumps({ message: 'VRN ' + vrnId + ' checked in succesfully ', "msgCode": "S"})
#         return dumps({ message: 'VRN ' + vrnId + ' is not checked in', "msgCode": "E"})
#     
        return vrnId
    
    def createVRNCheckOUT(self, data):
        return data
        
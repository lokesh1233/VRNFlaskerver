from bson.json_util import dumps
import re
class VRNParamCtrl:
    
    def __init__(self, db):
        self.db = db;
    
    def licenseRegion(self):
        licenseRegion = self.db.LicenseRegion.find({})
        if licenseRegion.count() > 0: 
            return dumps(licenseRegion)
        else:
            return dumps({ 'message': 'No data found', 'msgCode': "E"})
    
    def getParamData(self, domain):
        paramData = self.db.Params.find({"Domain":domain})
        if paramData.count() > 0: 
            return dumps(paramData)
        else:
            return dumps({ 'message': 'No data found', 'msgCode': "E"})
    
    def getTransporters(self, transporterId):
        if len(transporterId) < 3:
            return dumps({ 'message': 'Enter maximum 3 characters', 'msgCode': "E"})
        
        regx = re.compile("^"+transporterId)
        trnsporterData = self.db.Transporter.find({'$or':[{'Name1':regx}, {'Vendor' : regx}]})
        if trnsporterData.count() > 0: 
            return dumps(trnsporterData)
        else:
            return dumps({ 'message': 'No data found', 'msgCode': "E"})
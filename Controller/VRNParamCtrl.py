from bson.json_util import dumps
import re
class VRNParamCtrl:
    
    def licenseRegion(self):
        licenseRegion = self.db.LicenseRegion.find({})
        if licenseRegion.count() > 0: 
            return dumps(licenseRegion)
        else:
            return 'No data found'
    
    def getParamData(self, domain):
        paramData = self.db.Params.find({"Domain":domain})
        if paramData.count() > 0: 
            return dumps(paramData)
        else:
            return 'No data found'
    
    def getTransporters(self, transporterId):
        if len(transporterId) < 3:
            return 'Enter maximum 3 characters'
        
        regx = re.compile("^"+transporterId)
        trnsporterData = self.db.Transporter.find({'$or':[{'Name1':regx}, {'Vendor' : regx}]})
        if trnsporterData.count() > 0: 
            return dumps(trnsporterData)
        else:
            return 'No data found'
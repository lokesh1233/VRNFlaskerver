from bson.json_util import dumps
import json

class VRNLicenseCtrl:
    
    def createLicense(self,data):
        licStr = json.loads(data)
        
        licenseStr = {
            "Licencenumber" : licStr["Licencenumber"],
            "Lastname" : licStr["Lastname"],
            "Validto" : licStr["Validto"],
            "Telephone" : licStr["Telephone"],
            "Rg" : licStr["Rg"]
            }
        licenseDta = self.db.License.insert_one(licenseStr)
        returnMessage = ''
        if licenseDta.acknowledged:
            returnMessage = {"msgCode":"S", "message": licStr["Licencenumber"] + ' license created'}
        else:
            returnMessage = {"msgCode":"E", "message":licStr["Licencenumber"] + ' license not created'}
        return dumps(returnMessage)
    
    def getLicenseData(self, licenseId):
        licenseData = self.db.License.find({"Licencenumber": licenseId})
        if licenseData.count() > 0: 
            return dumps(licenseData)
        else:
            return 'No data found'

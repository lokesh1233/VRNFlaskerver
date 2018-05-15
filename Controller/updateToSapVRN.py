import requests
hstURL = 'http://fiori_test4:Welcome.1@nwgwtgd.rjil.ril.com:8000/sap/opu/odata/sap'
class updateToSapVRN:
    def __init__(self, db):
        self.db = db;
    
    def postSAPData(self, url, pData):
        client = requests.session();
        response = client.get(hstURL+'/Z_FIORI_VRN_IN_LITE_SRV/?saml2=disabled', headers = {"x-csrf-token": "Fetch"})
        token = response.headers["x-csrf-token"]
        headers = {"X-CSRF-Token": token}
        r = client.post(hstURL+url, json = pData, headers = headers)
        print(r.text)
        r.raise_for_status()
    
    def createLicense(self, data):
        LICDta = {
            "DriverName": data["Lastname"],
            "LicenceNum": data["Licencenumber"],
            "MobileNum": data["Telephone"],
            "RegionCode": data["Rg"],
            "ValidUpToDate": data["Validto"] + "T00:00:00"#[:-4] # need to check validto date senario what it is passing
            }
        self.postSAPData('/Z_FIORI_VRN_IN_LITE_SRV/LicenceCreateSet', LICDta)
    
    def createVRNCheckOut(self, data):
        checkOut = {
            "VRNNum": str(data["VRN"]),
            "VRNCREHRDITMNAV": [{
                "CheckType": "O",
                "DepRemarks": data["REMARKS"],
                "LRDate": "0000-00-00T00:00:00",
                "LRNum": '',
                "NoHus": data["NUMOFBOXES"],
                "Reject": "",
                "SealCond": data["SEALCONDITION"],
                "TripNum": "",
                "VRNCREITMDOCNAV": [{ "DocNum": "", "DocType": "" }],
                "VRNNum": str(data["VRN"]),
                "VehicleStatus": data["VEHICLESTATUS"]
                }]
                    }
        self.postSAPData('/Z_FIORI_VRN_OUT_LITE_SRV/VRNCreHdrSet', checkOut)
 
    def createVRNReortAndCheckIn(self, data, ind):
        report = {
            "Indicator": 'X' if data["VRNSTATUS"] == 'C' else "" ,
            "VRNCREHRDVEHNAV": [{
                "VehicleNum": data["VEHICLENUM"] if ind == 'X' else  '',
                "VendorNum": data["TRANSPORTERCODE"] if ind == 'X' else '',
                "FleetType": data["FLEETTYPECODE"] if ind == 'X' else  ''
                }],
            "VRNHDRITEMNAV": [{
                "CheckType": "I",
                "Depremarks": data["REMARKS"],
                "Depseal": data["SEAL1"],
                "DriverName": data["DRIVERNAME"],
                "DriverNum": data["DRIVERNUM"],
                "FleetType": data["FLEETTYPECODE"],
                "IDPrfNum": data["IDPROOFNUM"],
                "IDPrfType": data["IDPROOFTYPE"],
                "LRDate": "0000-00-00T00:00:00",
                "LRNum": data["LRNUM"],
                "LicenceNum": data["LICENSENUM"],
                "NoHus": data["NUMOFBOXES"],
                "Purpose": "VEND_INB",
                "SealCond": data["SEALCONDITION"],
                "TCNNum": "",
                "TransCode": data["TRANSPORTERCODE"],
                "Transporter": data["TRANSPORTER"],
                "VRNITEMDOCNAV": [{ "DocType": "", "DocNo": "" }],
                "VehStatus": data["VEHICLESTATUS"],
                "VehicleNum": data["VEHICLENUM"],
                "VehicleType": data["MODEOFTRANSPORT"]
                }]
                  }
        self.postSAPData('/Z_FIORI_VRN_IN_LITE_SRV/VRNCreateHdrSet', report);
        
 
    def createVRNCheckIn(self, vrn):
        CheckData = {
            "Indicator": "X",
            "VRNNum": str(vrn)
            }
        self.postSAPData('/Z_FIORI_VRN_IN_LITE_SRV/CheckInSet', CheckData);

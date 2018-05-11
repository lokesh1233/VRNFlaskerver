import requests
hstURL = 'http://fiori_test3:Welcome.1@nwgwtgd.rjil.ril.com:8000/sap/opu/odata/sap'
class updateToSapVRN:
    def __init__(self, db):
        self.db = db;
    
    def postSAPData(self, url, pData):
        response = requests.get(hstURL+'/Z_FIORI_VRN_IN_LITE_SRV', headers = {"x-csrf-token": "Fetch"})
        requests.post(hstURL+url, headers = {"x-csrf-token": response.headers["x-csrf-token"]}, data = pData)
    
    def createLicense(self, data):
        LICDta = {
            "DriverName": data["Lastname"],
            "LicenceNum": data["Licencenumber"],
            "MobileNum": data["Telephone"],
            "RegionCode": data["Rg"],
            "ValidUpToDate": data["Validto"][:-4] # need to check validto date senario what it is passing
            }
        updateToSapVRN.postSAPData(self, '/Z_FIORI_VRN_IN_LITE_SRV/LicenceCreateSet', LICDta)
    
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
        updateToSapVRN.postSAPData('/Z_FIORI_VRN_OUT_LITE_SRV/VRNCreHdrSet', checkOut)
 
    def createVRNReortAndCheckIn(self, data, ind):
        report = {
            "Indicator": 'X' if data.CHECKININD == 'X' else "" ,
            "VRNCREHRDVEHNAV": [{
                "VehicleNum": data.VEHICLENUM if ind == 'X' else  '',
                "VendorNum": data.TRANSPORTERCODE if ind == 'X' else '',
                "FleetType": data.FLEETTYPECODE if ind == 'X' else  ''
                }],
            "VRNHDRITEMNAV": [{
                "CheckType": "I",
                "Depremarks": data.REMARKS,
                "Depseal": data.SEAL1,
                "DriverName": data.DRIVERNAME,
                "DriverNum": data.DRIVERNUM,
                "FleetType": data.FLEETTYPECODE,
                "IDPrfNum": data.IDPROOFNUM,
                "IDPrfType": data.IDPROOFTYPE,
                "LRDate": "0000-00-00T00:00:00",
                "LRNum": data.LRNUM,
                "LicenceNum": data.LICENSENUM,
                "NoHus": data.NUMOFBOXES,
                "Purpose": "VEND_INB",
                "SealCond": data.SEALCONDITION,
                "TCNNum": "",
                "TransCode": data.TRANSPORTERCODE,
                "Transporter": data.TRANSPORTER,
                "VRNITEMDOCNAV": [{ "DocType": "", "DocNo": "" }],
                "VehStatus": data.VEHICLESTATUS,
                "VehicleNum": data.VEHICLENUM,
                "VehicleType": data.MODEOFTRANSPORT
                }]
                  }
        updateToSapVRN.postSAPData('/Z_FIORI_VRN_IN_LITE_SRV/VRNCreateHdrSet', report);
        
 
    def createVRNCheckIn(self, vrn):
        CheckData = {
            "Indicator": "X",
            "VRNNum": str(vrn)
            }
        updateToSapVRN.postSAPData('/Z_FIORI_VRN_IN_LITE_SRV/CheckInSet', CheckData);
        
    
    
# 
# 
# 'use strict';
# var mongoose = require('mongoose'),
#   request = require('request'),
#   
# 
# function doCall(url, pData) {
#   var token;
#   var j = request.jar();
# 
#   var postDataToSAP = function () {
#     return new Promise(function (resolve, reject) {
#       request({
#         url: hstURL+"/Z_FIORI_VRN_IN_LITE_SRV",
#         jar: j,
#         headers: {
#           "x-csrf-token": "Fetch"
#         }
#       }, function (error, response, body) {
#         try {
#           token = response.headers["x-csrf-token"];
#           console.log("token csrf " + token);
# 
#           request({
#             url: hstURL + url,
#             method: 'POST',
#             jar: j,
#             headers: {
#               "Content-Type": "application/json",
#               "X-CSRF-Token": token, // set CSRF Token for post or update
#             },
#             json: pData
#           }, function (error, response, body) {
# 
#             console.log("error " );
#             console.log(error);
#             console.log("response " );
#             console.log(response);
#             console.log("body ");
#             console.log(body);
# 
#             resolve();
#           });
#         } catch (err) {
#           console.log("Cannot post data to sap in catch" + err);
#         }
#       });
# 
#     });
#   }
#   postDataToSAP();
# }
# 
# function postSAPData(pth, data) {
#   //fetchCSRFToken(pth, data);
#   doCall(pth, data);
# }
# 
# //0000-00-00T00:00:00
# function dateFormate(myDate) {
#   return myDate.substring(0, myDate.length - 5);
# }
# 
# exports.createLicense = function (data) {
# 
#   var LICDta = {
#     DriverName: data.Lastname,
#     LicenceNum: data.Licencenumber,
#     MobileNum: data.Telephone,
#     RegionCode: data.Rg,
#     ValidUpToDate: dateFormate(data.Validto)
#   }
#   postSAPData('/Z_FIORI_VRN_IN_LITE_SRV/LicenceCreateSet', LICDta);
# 
# }
# 
# exports.createVRNCheckOut = function (data) {
#   var checkOut = {
#     VRNNum: data.VRN.toString(),
#     VRNCREHRDITMNAV: [{
#       CheckType: "O",
#       DepRemarks: data.REMARKS,
#       LRDate: "0000-00-00T00:00:00",
#       LRNum: '',
#       NoHus: data.NUMOFBOXES,
#       Reject: "",
#       SealCond: data.SEALCONDITION,
#       TripNum: "",
#       VRNCREITMDOCNAV: [{ DocNum: "", DocType: "" }],
#       VRNNum: data.VRN.toString(),
#       VehicleStatus: data.VEHICLESTATUS
#     }]
#   }
#   postSAPData('/Z_FIORI_VRN_OUT_LITE_SRV/VRNCreHdrSet', checkOut);
# }
# 
# exports.createVRNReortAndCheckIn = function createVRNReortAndCheckIn(data, ind) {
#   var report = {
#     Indicator: data.CHECKININD == 'X' ? 'X' : '',
#     VRNCREHRDVEHNAV: [{
#       VehicleNum: ind == 'X' ? data.VEHICLENUM : '',
#       VendorNum: ind == 'X' ? data.TRANSPORTERCODE : '',
#       FleetType: ind == 'X' ? data.FLEETTYPECODE : ''
#     }],
#     VRNHDRITEMNAV: [{
#       CheckType: "I",
#       Depremarks: data.REMARKS,
#       Depseal: data.SEAL1,
#       DriverName: data.DRIVERNAME,
#       DriverNum: data.DRIVERNUM,
#       FleetType: data.FLEETTYPECODE,
#       IDPrfNum: data.IDPROOFNUM,
#       IDPrfType: data.IDPROOFTYPE,
#       LRDate: "0000-00-00T00:00:00",
#       LRNum: data.LRNUM,
#       LicenceNum: data.LICENSENUM,
#       NoHus: data.NUMOFBOXES,
#       Purpose: "VEND_INB",
#       SealCond: data.SEALCONDITION,
#       TCNNum: "",
#       TransCode: data.TRANSPORTERCODE,
#       Transporter: data.TRANSPORTER,
#       VRNITEMDOCNAV: [{ DocType: "", DocNo: "" }],
#       VehStatus: data.VEHICLESTATUS,
#       VehicleNum: data.VEHICLENUM,
#       VehicleType: data.MODEOFTRANSPORT
#     }]
#   }
#   postSAPData('/Z_FIORI_VRN_IN_LITE_SRV/VRNCreateHdrSet', report);
# }
# 
# exports.createVRNCheckIn = function (vrn) {
#   var CheckData = {
#     Indicator: "X",
#     VRNNum: vrn.toString()
#   }
#   postSAPData('/Z_FIORI_VRN_IN_LITE_SRV/CheckInSet', CheckData);
# }

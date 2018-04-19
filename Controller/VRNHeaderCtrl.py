#from flask import request
from bson.json_util import dumps
import json
from datetime import datetime
#from Controller import VRNHeaderCtrl

class VRNHeaderCtrl:
    
    def __init__(self, db):
        self.db = db;


    # List of VRNs with status R and C    
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
                    try:
                        lst["TrnsprtMode"] = dataPrm['TrnsprtMode'+lst["MODEOFTRANSPORT"]] if lst["MODEOFTRANSPORT"] != "" else ""
                        lst["IDPROOFTYPE"] = dataPrm['IDProffList'+lst["IDPROOFTYPE"]] if lst["IDPROOFTYPE"] != "" else ""
                        lst["FLEETTYPE"] = dataPrm['FleetList'+lst["FLEETTYPE"]] if lst["FLEETTYPE"] != "" else ""
                        vrnRetData.append(lst)
                    except:
                        vrnRetData.append(lst)
                return dumps(vrnRetData)
            return dumps(VRNList)
        else:
            return 'No VRN found'

    
    # VRN checkin with vrn number
    def createVRNCheckIN(self, vrnId):
        #vrnCheckIN= self.db.VRNHeader.findOneAndUpdate({ "VRN": int(vrnId) }, { '$set': { "VRNSTATUS": "C" } }, { "new": True, "upsert": True })
        vrnCheckIN= self.db.VRNHeader.update_one({ "VRN": int(vrnId) }, { '$set': { "VRNSTATUS": "C" } }, True)
        if vrnCheckIN.acknowledged:
            #VRNCheckINDetail = self.db.VRNDetail.findOneAndUpdate({ "VRN": vrnId }, { '$set': { "VEHICLECHECKINDATE": str(datetime.now()), "VRNCHECKINBY": 'Bhaskar'}  }, { "new": True, "upsert": True })
            VRNCheckINDetail = self.db.VRNDetail.update_one({ "VRN": vrnId }, { '$set': { "VEHICLECHECKINDATE": str(datetime.now()), "VRNCHECKINBY": 'Bhaskar'}  }, True)
            if VRNCheckINDetail.acknowledged:
                return dumps({ "message": 'VRN ' + vrnId + ' checked in succesfully ', "msgCode": "S"})
        return dumps({ "message": 'VRN ' + vrnId + ' is not checked in', "msgCode": "E"})

    
    # VRN checkout with request data
    def createVRNCheckOUT(self, data):
        checkOutStr = json.loads(data)
        #VRNHdr =  self.db.VRNHeader.findOneAndUpdate({ "VRN": checkOutStr["VRN"] }, { '$set': { "VRNSTATUS": "X" } }, { "new": True, "upsert": True })
        VRNHdr =  self.db.VRNHeader.update_one({ "VRN": checkOutStr["VRN"] }, { '$set': { "VRNSTATUS": "X" } }, True)
        if VRNHdr.acknowledged:
            checkOutStr["VEHICLESECURITYDATE"] = str(datetime.now())
            checkOutStr["VEHICLECHECKINDATE"] = str(datetime.now())
            checkOutStr["VRNCHECKINBY"] = "Bhaskar"
            checkOutStr["CHECKINOUT"] = "O"
            vrnDtl = self.db.VRNDetail.insert_one(checkOutStr)
            if vrnDtl.acknowledged:
                return dumps({"message": 'VRN ' + str(checkOutStr["VRN"]) + ' checked out succesfully ', "msgCode": "S"})
        return dumps({ "message": 'VRN ' + str(checkOutStr["VRN"]) + ' is not checked out', "msgCode": "E" });


    # create a VRN 
    def createVRN(self, data):
        crtVRNStr = json.loads(data)
        vhcle = crtVRNStr["VEHICLENUM"]
        if vhcle != '':
            VRNHeaderCtrl.vehicleAvailable(self, vhcle, crtVRNStr)
        else:
            VRNHeaderCtrl.create_new_vrn(self, crtVRNStr)



    def getNextSequenceVlue(self, sequenceName):
        return self.db.VRNCounter.findOneAndUpdate({ "col1": sequenceName },
                                            { "$inc": { "seq": 1 } },
                                            { "new": True, "upsert": True, "fields": {} })





    def vehicleAvailable(self, VEHICLENUM, data):
        vrnHdr = self.db.VRNHeader.find({ "VEHICLENUM": VEHICLENUM , "$or": [{ "VRNSTATUS": 'R' }, { "VRNSTATUS": 'C' }] })
        if vrnHdr.count() > 0:
            return dumps({ "message" :"VRN " + vrnHdr + " is open for vehicle number " + VEHICLENUM });
        VRNHeaderCtrl.create_new_vrn(self, data);


    def create_new_vrn(self, data):
        seqNum = self.getNextSequenceVlue('VRNNum')
        for seq_ls in seqNum:
            seqval = seq_ls["seq"]
        hdrData =  VRNHeaderCtrl.createVRNHeaderData(self, data, seqval)
        dtlData =  VRNHeaderCtrl.createVRNDetailData(self, data, seqval)
        new_vrn = self.db.VRNHeader.insert_one(hdrData)
        if new_vrn.acknowledged:
            dtl_vrn = self.db.VRNDetail.insert_one(dtlData)
            if dtl_vrn.acknowledged:
                self.db.Vehicle.findOneAndUpdate({ "VehicleNumber": hdrData["VEHICLENUM"] }, {
                    '$set': { 'FleetType': hdrData["FLEETTYPECODE"], 'Vendor': hdrData["TRANSPORTERCODE"], 'VendorName': ["TRANSPORTER"] } }, {
                        "new": True, "upsert": True })
                return dumps({ 'message': 'VRN: ' + seqval + ' created sccesfully', 'msgCode': "S" })
        return dumps({ 'message': 'VRN is not created', 'msgCode': "E"})


    # VRN detail data structure
    def createVRNDetailData(self, data, vrno):
        return {
            "CHECKINOUT": "I",
            "NUMOFBOXES": data["NUMOFBOXES"],
            "REMARKS": data["REMARKS"],
            "SEAL1": data["SEAL1"],
            "SEAL2": data["SEAL2"],
            "SEALCONDITION": data["SEALCONDITION"],
            "VEHICLECHECKINDATE": datetime.now() if data["CHECKININD"] == 'X' else "",
            "VEHICLESECURITYDATE": datetime.now(),
            "VEHICLESTATUS": data["VEHICLESTATUS"],
            "VRN": vrno,
            "VRNCHECKINBY": 'Bhaskar' if data["CHECKININD"] == 'X' else ""
        }

    #VRNHeader data structure
    def createVRNHeaderData(self, data, vrno):
        return {
            "CHANGEDBY": "",
            "CHANGEDON": "",
            "CREATEDBY": "Bhaskar",
            "CREATEDON": datetime.now(),
            "DRIVERNAME": data["DRIVERNAME"],
            "DRIVERNUM": data["DRIVERNUM"],
            "FLEETTYPE": data["FLEETTYPECODE"],
            "IDPROOFNUM": data["IDPROOFNUM"],
            "IDPROOFTYPE": data["IDPROOFTYPE"],
            "LICENSENUM": data["LICENSENUM"],
            "LRDATE": '',
            "LRNUM": data["LRNUM"],
            "MODEOFTRANSPORT": data["MODEOFTRANSPORT"],
            "PURPOSE": '',
            "SITE": "",
            "TRANSPORTER": data["TRANSPORTER"],
            "TRANSPORTERCODE": data["TRANSPORTERCODE"],
            "VEHICLENUM": data["VEHICLENUM"],
            "VRN": vrno,
            "VRNSTATUS": data["VRNSTATUS"]
        }

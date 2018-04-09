from bson.json_util import dumps
#from Controller import VRNHeaderCtrl

class VRNVehicleCtrl:
    def __init__(self, db):
        self.db = db;
    
    def createVehicle(self):
        return 'create VRN successFully'
    
    def findVRNVehicle(self, vehicleid):
        vrnHeader = self.db.VRNHeader.find({ "VEHICLENUM": vehicleid, "$or": [{ "VRNSTATUS": 'R' }, { "VRNSTATUS": 'C' }] })
        if vrnHeader.count() >  0:
            return "message: VRN  is open for vehicle number " + vehicleid;
        vehicleDtl =  self.db.Vehicle.find({ "VehicleNumber": vehicleid })
        if vehicleDtl.count() == 0:
            return vehicleid + " is not registered in vehicle master"
        vehicleRetData = []
        for vhcle in vehicleDtl:
            paramValue = self.db.Params.find({
            "Domain": 'FleetList',
            "modeNum": vhcle["FleetType"]
            })
            if paramValue.count() == 0:
                return dumps(vehicleDtl)
            else:
                for prm in paramValue:
                    vhcle['FleetTypeDesc'] = prm["modeTxt"]
                    vehicleRetData.append(vhcle)
                return dumps(vehicleRetData)
            return dumps(vehicleDtl)
        else:
            return vehicleid+'is not registered in vehicle master'
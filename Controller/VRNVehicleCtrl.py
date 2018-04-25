from bson.json_util import dumps
#from Controller import VRNHeaderCtrl

class VRNVehicleCtrl:
    def __init__(self, db):
        self.db = db;
    
    def findVRNVehicle(self, vehicleid):
        vrnHeader = self.db.VRNHeader.find({ "VEHICLENUM": vehicleid, "$or": [{ "VRNSTATUS": 'R' }, { "VRNSTATUS": 'C' }] })
        if vrnHeader.count() >  0:
            for vrns in vrnHeader:
                return dumps({ 'message': "VRN "+vrns['VRN']+" is open for vehicle number " + vehicleid, 'msgCode': "E"})
        vehicleDtl =  self.db.Vehicle.find({ "VehicleNumber": vehicleid })
        if vehicleDtl.count() == 0:
            return dumps([])
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
            return dumps([])
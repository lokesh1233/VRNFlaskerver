from flask import request
from Controller.VRNHeaderCtrl import VRNHeaderCtrl 
from Controller.VRNDetailCtrl import VRNDetialCtrl 
from Controller.VRNVehicleCtrl import VRNVehicleCtrl
from Controller.VRNParamCtrl import VRNParamCtrl
from Controller.VRNLicenseCtrl import VRNLicenseCtrl 

class VRNRouter: 
    
    def __init__(self, app, db):
        
        self.app = app
        self.db = db
        VRNHeaderCtrl(db)
        self.loadAppRouterPath()
    
    def loadAppRouterPath(self):
        app = self.app
        
        #VRN master data    
        @app.route('/VRNMaster',methods = ['POST', 'GET'])
        def VRNMasterList():
            if request.method == 'POST':
                return VRNHeaderCtrl.createVRN(self, request.data)
            else:
                return VRNHeaderCtrl.getVRNHeaderList(self)
        
        #VRN master data    
        @app.route('/VRNCheckIN/<vrnId>',methods = ['PUT'])
        def VRNCheckIN(vrnId):
            if request.method == 'PUT':
                return VRNHeaderCtrl.createVRNCheckIN(self, vrnId)
        
        #VRN master data    
        @app.route('/VRNCheckOUT',methods = ['POST'])
        def VRNCheckOUT(vrnId):
            if request.method == 'POST':
                return VRNHeaderCtrl.createVRNCheckOUT(self, request.data)
            
        #VRN Detail Data
        @app.route('/VRNDetail/<vrnId>',methods = ['GET'])
        def VRNDetail(vrnId):
            if request.method == 'GET':
                return VRNDetialCtrl.getVRNDetail(self, vrnId)
        
        #VRN Vehicle Data
        @app.route('/VRNVehicle/<vehicleId>',methods = ['GET'])
        def findVRNVehicle(vehicleId):
            if request.method == 'GET':
                return VRNVehicleCtrl.findVRNVehicle(self, vehicleId)
        
        #VRN Param Data
        @app.route('/VRNParam/<domainId>',methods = ['GET'])
        def VRNParamData(domainId):
            if request.method == 'GET':
                return VRNParamCtrl.getParamData(self, domainId)
        
        #VRN LicenseRegion Data
        @app.route('/LicenseRegion',methods = ['GET'])
        def VRNLicenseRgn():
            if request.method == 'GET':
                return VRNParamCtrl.licenseRegion(self)
        
        #VRN Transporter Data
        @app.route('/VRNTransporters/<trnsporterId>',methods = ['GET'])
        def VRNTransporter(trnsporterId):
            if request.method == 'GET':
                return VRNParamCtrl.getTransporters(self, trnsporterId)
 
        #VRN Licence Data
        @app.route('/License/<licenseId>',methods = ['GET'])
        def VRNLicense(licenseId):
            if request.method == 'GET':
                return VRNLicenseCtrl.getLicenseData(self, licenseId)
        
        #VRN Licence Data
        @app.route('/License',methods = ['POST'])
        def createVRNLicense():
            if request.method == 'POST':
                return VRNLicenseCtrl.createLicense(self, request.data)

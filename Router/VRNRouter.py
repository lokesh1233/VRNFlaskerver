from flask import request
from Controller.VRNHeaderCtrl import VRNHeaderCtrl 
from Controller.VRNDetailCtrl import VRNDetailCtrl 
from Controller.VRNVehicleCtrl import VRNVehicleCtrl
from Controller.VRNParamCtrl import VRNParamCtrl
from Controller.VRNLicenseCtrl import VRNLicenseCtrl 

class VRNRouter: 
    
    def __init__(self, app, db):
        
        self.app = app
        self.db = db
        self.VRNHeader = VRNHeaderCtrl(db)
        self.VRNDetail = VRNDetailCtrl(db)
        self.VRNVehicle = VRNVehicleCtrl(db)
        self.VRNParam = VRNParamCtrl(db)
        self.VRNLicense = VRNLicenseCtrl()
        self.loadAppRouterPath()
    
    def loadAppRouterPath(self):
        app = self.app
        
        #VRN master data    
        @app.route('/VRNMaster',methods = ['POST', 'GET'])
        def VRNMasterList():
            if request.method == 'POST':
                return self.VRNHeader.createVRN(request.data)
            else:
                return self.VRNHeader.getVRNHeaderList()
        
        #VRN master data    
        @app.route('/VRNCheckIN/<vrnId>',methods = ['PUT'])
        def VRNCheckIN(vrnId):
            if request.method == 'PUT':
                return self.VRNHeader.createVRNCheckIN(vrnId)
        
        #VRN master data    
        @app.route('/VRNCheckOUT',methods = ['POST'])
        def VRNCheckOUT():
            if request.method == 'POST':
                return self.VRNHeader.createVRNCheckOUT(request.data)
            
        #VRN Detail Data
        @app.route('/VRNDetail/<vrnId>',methods = ['GET'])
        def VRNDetail(vrnId):
            if request.method == 'GET':
                return self.VRNDetail.getVRNDetail(vrnId)
        
        #VRN Vehicle Data
        @app.route('/VRNVehicle/<vehicleId>',methods = ['GET'])
        def findVRNVehicle(vehicleId):
            if request.method == 'GET':
                return self.VRNVehicle.findVRNVehicle(vehicleId)
        
        #VRN Param Data
        @app.route('/VRNParam/<domainId>',methods = ['GET'])
        def VRNParamData(domainId):
            if request.method == 'GET':
                return self.VRNParam.getParamData(domainId)
        
        #VRN LicenseRegion Data
        @app.route('/LicenseRegion',methods = ['GET'])
        def VRNLicenseRgn():
            if request.method == 'GET':
                return self.VRNParam.licenseRegion()
        
        #VRN Transporter Data
        @app.route('/VRNTransporters/<trnsporterId>',methods = ['GET'])
        def VRNTransporter(trnsporterId):
            if request.method == 'GET':
                return self.VRNParam.getTransporters(trnsporterId)
 
        #VRN Licence Data
        @app.route('/License/<licenseId>',methods = ['GET'])
        def VRNLicense(licenseId):
            if request.method == 'GET':
                return self.VRNLicense.getLicenseData(licenseId)
        
        #VRN Licence Data
        @app.route('/License',methods = ['POST'])
        def createVRNLicense():
            if request.method == 'POST':
                return self.VRNLicense.createLicense(request.data)

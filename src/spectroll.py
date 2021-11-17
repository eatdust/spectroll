import numpy as np

#everything lies in the linear space, that *is not* RGB gamma
#compressed
#
#the CIE spectral range over which all colors are computed. It should
#be large enough to encompass all response functions and illuminant
#spectra
nmMin= 300
nmMax= 830
nmLength=nmMax-nmMin+1


#data from http://cvrl.ioo.ucl.ac.uk, should match CIE2006
#
#color matching function for XYZ
xyzCMF='data/lin2012xyz2e_1_7sf.dat'

#LMS response function
lmsResponse='data/lms2deg.dat'

#Analytical transform from lms to xyz as reported in
#http://cvrl.ioo.ucl.ac.uk (for test only)
LMS2XYZ = np.array([[1.94735469,-1.41445123,0.36476327],
                   [0.68990272,0.34832189,0.0],
                    [0.0,0.0,1.93485343]])

#Some chromatic coordinates (from
#http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html)
sRGBchromaD65 = {'xr':0.6400,'yr':0.3300,'Yr':0.212656,
                 'xg':0.3000,'yg':0.6000,'Yg':0.715158,
                 'xb':0.1500,'yb':0.060,'Yb':0.072186}

wideGamutRGBD50 = {'xr':0.7350,'yr':0.2650,'Yr':0.258187,
                 'xg':0.1150,'yg':0.8260,'Yg':0.724938,
                 'xb':0.1570,'yb':0.0180,'Yb':0.016875}

class spectrum(object):

    def __init__(self,name='',filename=''):

        self.set_name(name)

        self.nm = np.linspace(nmMin,nmMax,num=nmLength)
        self.spectrum = np.zeros(nmLength)
        self.set_lms_response()
        self.set_xyz_colormatch()

        self.L = -1.
        self.M = -1.
        self.S = -1.

        self.X = -1.
        self.Y = -1.
        self.Z = -1.

        self.RGB2XYZ = np.identity(n=3)
        self.XYZ2RGB = np.identity(n=3)
        
        if filename:
            self.read_spectrum(filename)


    def set_lms_response(self):
        wavelength,l,m,s = np.loadtxt(lmsResponse,dtype='float',unpack=True,usecols=[0,1,2,3])
        
        self.l = np.interp(self.nm,wavelength,l,left=0.,right=0.)
        self.m = np.interp(self.nm,wavelength,m,left=0.,right=0.)
        self.s = np.interp(self.nm,wavelength,s,left=0.,right=0.)

    def set_xyz_colormatch(self):
        wavelength,x,y,z = np.loadtxt(xyzCMF,dtype='float',unpack=True,usecols=[0,1,2,3])

        self.x = np.interp(self.nm,wavelength,x,left=0.,right=0.)
        self.y = np.interp(self.nm,wavelength,y,left=0.,right=0.)
        self.z = np.interp(self.nm,wavelength,z,left=0.,right=0.)
        

    def read_spectrum(self,filename):
        wavelength,intensity = np.loadtxt(filename,dtype='float',unpack=True,usecols=[0,1])

        self.spectrum = np.interp(self.nm,wavelength,intensity,left=0.,right=0.)
        self.irradiance = np.trapz(self.spectrum,self.nm)

#input two equal length numpy arrays        
    def set_spectrum(self,wavelength,intensity):
        self.spectrum = np.interp(self.nm,wavelength,intensity,left=0.,right=0.)
        self.irradiance = np.trapz(self.spectrum,self.nm)
        self.L=-1
        self.M=-1
        self.S=-1
        self.X=-1
        self.Y=-1
        self.Z=-1

        
    def get_spectrum(self):
        return self.nm, self.spectrum
        
    def set_name(self,name):
        self.name = name

    def get_name(self):
        return self.name
    
    def get_irradiance(self):
        return self.irradiance
    
    
    def get_L(self):
        if self.L == -1.:
            self.L = np.trapz(self.l*self.spectrum,self.nm)

        return self.L

    def get_M(self):
        if self.M == -1:
            self.M = np.trapz(self.m*self.spectrum,self.nm)

        return self.M
            
    def get_S(self):
        if self.S == -1:
            self.S = np.trapz(self.s*self.spectrum,self.nm)

        return self.S

    def get_LMS(self):
        return np.array([self.get_L(),self.get_M(),self.get_S()]).transpose()
    
    def get_l(self):
        return self.L/(self.L+self.M+self.S)

    def get_m(self):
        return self.M/(self.L+self.M+self.S)

    def get_s(self):
        return self.S/(self.L+self.M+self.S)


    def get_lms(self):
        return np.array([self.get_l(),self.get_m(),self.get_s()]).transpose()
    
    
    def get_X(self):
        if self.X == -1:
            self.X = np.trapz(self.x*self.spectrum,self.nm)

        return self.X

    def get_Y(self):
        if self.Y == -1:
            self.Y = np.trapz(self.y*self.spectrum,self.nm)

        return self.Y

    def get_Z(self):
        if self.Z == -1:
            self.Z = np.trapz(self.z*self.spectrum,self.nm)

        return self.Z


    def get_XYZ(self):
        return np.array([self.get_X(),self.get_Y(),self.get_Z()]).transpose()

#consistency check is that this should give the same results as
#get_XYZ() when LMS=get_LMS()
    def get_XYZ_from_LMS(self,LMS):
        return np.matmul(LMS2XYZ,LMS)
    
    def get_x(self):
        return self.X/(self.X+self.Y+self.Z)

    def get_y(self):
        return self.Y/(self.X+self.Y+self.Z)

    def get_z(self):
        return self.Z/(self.X+self.Y+self.Z)

    def get_xyz(self):
        return np.array([self.get_x(),self.get_y(),self.get_z()]).transpose()
    

#chroma should be a dictionary (see sRGBchromaD65), Xw,Yw,Zw are
#the white point response. This is the "M" matrix giving XYZ from RGB
    def set_RGB2XYZ_transforms(self,chroma,Xw,Yw,Zw):
        Xr = chroma['xr']/ chroma['yr']
        Yr = 1.0
        Zr = (1.0 - chroma['xr'] - chroma['yr'])/chroma['yr']
        Xg = chroma['xg']/ chroma['yg']
        Yg = 1.0
        Zg = (1.0 - chroma['xg'] - chroma['yg'])/chroma['yg']
        Xb = chroma['xb']/ chroma['yb']
        Yb = 1.0
        Zb = (1.0 - chroma['xb'] - chroma['yb'])/chroma['yb']

        S2W = [[Xr,Xg,Xb],[Yr,Yg,Yb],[Zr,Zg,Zb]]
        W2S = np.linalg.inv(S2W)

        Srgb = np.matmul(W2S,np.array([Xw,Yw,Zw]).transpose())
        Sr = Srgb[0]
        Sg = Srgb[1]
        Sb = Srgb[2]
        
        self.RGB2XYZ=[[Sr*Xr,Sg*Xg,Sb*Xb],[Sr*Yr,Sg*Yg,Sb*Yb],[Sr*Zr,Sg*Zg,Sb*Zb]]
        self.XYZ2RGB = np.linalg.inv(self.RGB2XYZ)

    def get_RGB2XYZ(self):
        return self.RGB2XYZ

    def get_XYZ2RGB(self):
        return self.RGB2XYZ

    def get_RGB(self):
        return np.matmul(self.XYZ2RGB,self.get_XYZ())
        
    def get_RGB_from_XYZ(self,XYZ):
        return np.matmul(self.XYZ2RGB,XYZ)

    def get_XYZ_from_RGB(self,RGB):
        return np.matmul(self.RGB2XYZ,RGB)

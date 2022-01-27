import numpy as np
import spectroll as sp


def sRGB_linear_to_nonlinear(lRGB):
    gRGB=lRGB
    for i in range(len(lRGB)):
        if lRGB[i] <= 0.0031308:
            gRGB[i] = lRGB[i]*12.92
        else:
            gRGB[i]=1.055*lRGB[i]**(1.0/2.4)-0.055
            
    return gRGB
    

D65 = sp.spectrum(name='D65',filename='data/illuminant_D65.dat')

wavelength,white = D65.get_spectrum()

#that is supposed to be white for sRGB
D65_XYZ = D65.get_XYZ()
D65_LMS = D65.get_LMS()

print("D65 illuminant: ")
print("XYZ=",D65_XYZ)
#print("test",D65.get_XYZ_from_LMS(D65_LMS))

Xw = D65.get_X()
Yw = D65.get_Y()
Zw = D65.get_Z()
print("This is our white point:")
print("Xw= Yw= Zw= ",Xw,Yw,Zw)

D65.set_RGB2XYZ_transforms(sp.sRGBchromaD65,Xw,Yw,Zw)

print("D65: RGB= ",D65.get_RGB())
print()

print("Loading rhodopic response...")      
#night vision response
RESP = sp.spectrum(name='RHOD Response',filename='data/rhodopic_response.dat')

#D65 under night vision
RHODW = sp.spectrum(name='RHOD White')
wavelength, rhod = RESP.get_spectrum()

print("Multiplying by D65 spectrum...")
RHODW.set_spectrum(wavelength,rhod*white)
RHODW_XYZ = RHODW.get_XYZ()
RHODW_LMS = RHODW.get_LMS()

print("Rhodopic D65:")
print("XYZ= ",RHODW_XYZ)
#print("test",RHODW.get_XYZ_from_LMS(RHODW_LMS))

print()
print("Setting RGB2XYZ transform based on D65 daylight white point:")
print("Xw= Yw= Zw= ",Xw,Yw,Zw)

RHODW.set_RGB2XYZ_transforms(sp.sRGBchromaD65,Xw,Yw,Zw)
print("XYZ2RGB= ",RHODW.get_XYZ2RGB())

print()
print("White under night vision is: ")
lRGB = RHODW.get_RGB()
print("RHODW: lRGB= ",lRGB)
print("RHODW: gRGB= ",sRGB_linear_to_nonlinear(lRGB))

import numpy as np
import spectroll as sp


#compute XYZ to sRGB(linear) transformation

D65 = sp.spectrum(name='D65',filename='data/illuminant_D65.dat')
wavelength,white = D65.get_spectrum()


#that is supposed to be white for sRGB
D65_XYZ = D65.get_XYZ()

print("D65 illuminant (white point): ")
print("XYZ=",D65_XYZ)
Xw = D65.get_X()
Yw = D65.get_Y()
Zw = D65.get_Z()

print("Setting XYZ <-> sRGB transformation matrices...")
D65.set_RGB2XYZ_transforms(sp.sRGBchromaD65,Xw,Yw,Zw)
XYZ2RGB = D65.get_XYZ2RGB()
print('XYZ2RGB= ',XYZ2RGB)
print("Checking sRGB for D65= ",D65.get_RGB())
print()

#compute XYZ colors from GAIA passband filters

print("Loading Gaia RP, G and BP transmittance filters...")      
gaiaR = sp.spectrum(name='GAIA RP',filename='data/gaia_EDR3_RP.dat')
lambdaR, passbandR = gaiaR.get_spectrum()

gaiaG = sp.spectrum(name='GAIA G',filename='data/gaia_EDR3_G.dat')
lambdaG, passbandG = gaiaG.get_spectrum()

gaiaB = sp.spectrum(name='GAIA BP',filename='data/gaia_EDR3_BP.dat')
lambdaB, passbandB = gaiaB.get_spectrum()

print("Convolving with D65 illuminant...")
gaiaR.set_spectrum(lambdaR,passbandR*white)
gaiaG.set_spectrum(lambdaG,passbandG*white)
gaiaB.set_spectrum(lambdaB,passbandB*white)

gaiaR_XYZ = gaiaR.get_XYZ()
gaiaG_XYZ = gaiaG.get_XYZ()
gaiaB_XYZ = gaiaB.get_XYZ()

print("Gaia R XYZ= ",gaiaR_XYZ)
print("Gaia G XYZ= ",gaiaG_XYZ)
print("Gaia B XYZ= ",gaiaB_XYZ)
print()


gaiaR.set_RGB2XYZ_transforms(sp.sRGBchromaD65,Xw,Yw,Zw)
gaiaG.set_RGB2XYZ_transforms(sp.sRGBchromaD65,Xw,Yw,Zw)
gaiaB.set_RGB2XYZ_transforms(sp.sRGBchromaD65,Xw,Yw,Zw)

#should be all the same
#print("D65_XYZ2RGB =  ",D65.get_XYZ2RGB())
#print("gaiaR_XYZ2RGB= ",gaiaR.get_XYZ2RGB())
#print("gaiaG_XYZ2RGB= ",gaiaG.get_XYZ2RGB())
#print("gaiaB_XYZ2RGB= ",gaiaB.get_XYZ2RGB())

print("gaiaR_RGB= ",gaiaR.get_RGB())
print("gaiaG_RGB= ",gaiaG.get_RGB())
print("gaiaB_RGB= ",gaiaB.get_RGB())
print()
print("Transformation matrix gaia2RGB= ")
print(np.array([gaiaR.get_RGB(),gaiaG.get_RGB(),gaiaB.get_RGB()]).transpose())
print()

print("Check by direct computations: ")
gaia2XYZ = np.array([gaiaR_XYZ,gaiaG_XYZ,gaiaB_XYZ]).transpose()
print("gaia2XYZ= ",gaia2XYZ)
print("gaia2RGB= ")
print(np.matmul(XYZ2RGB,gaia2XYZ))


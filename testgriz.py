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

print("Loading Sloan g', r', i', and z' transmittance curves...")
sloanG = sp.spectrum(name='g',filename='data/corr_g7604B.dat')
lambdaG, passbandG = sloanG.get_spectrum()

sloanR = sp.spectrum(name='r',filename='data/corr_r7601SA.dat')
lambdaR, passbandR = sloanR.get_spectrum()

sloanI = sp.spectrum(name='i',filename='data/corr_i7604B.dat')
lambdaI, passbandI = sloanI.get_spectrum()

sloanZ = sp.spectrum(name='z',filename='data/corr_z7603B.dat')
lambdaZ, passbandZ = sloanZ.get_spectrum()


print("Convolving with D65 illuminant...")
sloanG.set_spectrum(lambdaG,passbandG*white)
sloanR.set_spectrum(lambdaR,passbandR*white)
sloanI.set_spectrum(lambdaI,passbandI*white)
sloanZ.set_spectrum(lambdaZ,passbandZ*white)

sloanG_XYZ = sloanG.get_XYZ()
sloanR_XYZ = sloanR.get_XYZ()
sloanI_XYZ = sloanI.get_XYZ()
sloanZ_XYZ = sloanZ.get_XYZ()

print("Sloan g' XYZ= ",sloanG_XYZ)
print("Sloan r' XYZ= ",sloanG_XYZ)
print("Sloan i' XYZ= ",sloanG_XYZ)
print("Sloan z' XYZ= ",sloanG_XYZ)

print()

sloanG.set_RGB2XYZ_transforms(sp.sRGBchromaD65,Xw,Yw,Zw)
sloanR.set_RGB2XYZ_transforms(sp.sRGBchromaD65,Xw,Yw,Zw)
sloanI.set_RGB2XYZ_transforms(sp.sRGBchromaD65,Xw,Yw,Zw)
sloanZ.set_RGB2XYZ_transforms(sp.sRGBchromaD65,Xw,Yw,Zw)

#should be all the same
#print("D65_XYZ2RGB =  ",D65.get_XYZ2RGB())
#print("sloanG_XYZ2RGB= ",sloanG.get_XYZ2RGB())
#print("sloanR_XYZ2RGB= ",sloanR.get_XYZ2RGB())
#print("sloanI_XYZ2RGB= ",sloanI.get_XYZ2RGB())
#print("sloanZ_XYZ2RGB= ",sloanZ.get_XYZ2RGB())

print("sloanG_RGB= ",sloanG.get_RGB())
print("sloanR_RGB= ",sloanR.get_RGB())
print("sloanI_RGB= ",sloanI.get_RGB())
print("sloanZ_RGB= ",sloanZ.get_RGB())
print()
print("Transformation matrix griz2RGB= ")
print(np.array([sloanG.get_RGB(),sloanR.get_RGB(),sloanI.get_RGB(),sloanZ.get_RGB()]).transpose())
print()

print("Check by direct computations: ")
sloan2XYZ = np.array([sloanG_XYZ,sloanR_XYZ,sloanI_XYZ,sloanZ_XYZ]).transpose()
print("griz2XYZ= ",sloan2XYZ)
print("griz2RGB= ")
print(np.matmul(XYZ2RGB,sloan2XYZ))


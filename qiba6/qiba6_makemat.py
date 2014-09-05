from pylab import *
from scipy.io import loadmat, savemat
import time
import dicom


Rel = 4.5   # assumed Relaxivity of Gd-DTPA at 3 T [s^-1 [mmol Gd-DTPA]^{-1}]
flip_angle = 30 * pi / 180.0 # rad
TR = 5e-3   # sec
nx = 80
ny = 50
nt = 1321

data_dir = 'DICOM/'
file_ext = 'QIBA_v06_Tofts_beta1'
outfile = 'qiba6.mat'

data_dicom = zeros((nt, nx, ny))

t = 0.5*arange(nt)  # ms
print 'reading DICOMs from', data_dir
for k in range(nt):
    file_name = '%s/%s_%04d.dcm' % (data_dir, file_ext, k+1)
    dcm = dicom.read_file(file_name)
    data_dicom[k,:,:] = dcm.pixel_array.astype('float')

data_dce = data_dicom[:,10:70,:]
nt, nx, ny = data_dce.shape
T1map = ones((nx, ny)) # s
R1map = 1 / T1map
S0map = ones((nx, ny)) * 50000.0 #
data_aif = mean(mean(data_dicom[:,70:,:], axis=2), axis=1)



# ## 2. Derive the AIF ##
# turn Sb into Cp
print 'converting plasma ROI to AIF'

def dce_to_r1eff(S, S0, R1, TR, flip):
  S = S.T
  S0 = S0.T
  A = S.copy() / S0  # normalize by pre-contrast signal
  E0 = exp(-R1 * TR)
  E = (1.0 - A + A*E0 - E0*cos(flip)) /\
  (1.0 - A*cos(flip) + A*E0*cos(flip) - E0*cos(flip))
  R = (-1.0 / TR) * log(E)
  return R.T

def r1eff_to_conc(R1eff, R1map, relaxivity):
    return (R1eff - R1map) / relaxivity

T1p = 1.440
R1p = 1 / T1p
Hct = 0.45
S0 = data_aif[:4].mean()
R1_eff_aif = dce_to_r1eff(data_aif, S0, R1p, TR, flip_angle)
Cb = r1eff_to_conc(R1_eff_aif.flatten(), R1p, Rel)
Cp = Cb.flatten() / (1.0 - Hct)


print 'writing MAT file', outfile
mat = {}
mat["R"] = 4.5
mat["TR"] = 5e-3
mat["dcedata"] = data_dce
mat["dceflip"] = 30.0
mat["R1map"] = R1map
mat["S0map"] = S0map
mat["t"] = t
mat["aif"] = Cp
savemat(outfile, mat)

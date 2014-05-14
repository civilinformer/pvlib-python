from nose.tools import *
import numpy as np
import pandas as pd 
from .. import pvl_tools
from .. import pvl_readtmy3 as tmy3
from .. import pvl_ephemeris as eph
from .. import pvl_extraradiation as ext
from .. import pvl_relativeairmass as AM
from .. import pvl_reindl1990 as rd
import os
def test():
	
	TMY, meta=tmy3.pvl_readtmy3(FileName=os.path.abspath('')+'/723650TY.csv')
	meta.SurfTilt=30

	meta.SurfAz=0
	meta.Albedo=0.2 

	TMY['SunAz'], TMY['SunEl'], TMY['ApparentSunEl'], TMY['SolarTime'], TMY['SunZen']=eph.pvl_ephemeris(Time=TMY.index,Location=meta)

	TMY['HExtra']=ext.pvl_extraradiation(doy=TMY.index.dayofyear)

	TMY['AM']=AM.pvl_relativeairmass(z=TMY.SunZen)

	TMY['In_Plane_SkyDiffuse']=rd.pvl_reindl1990(SurfTilt=meta.SurfTilt,
	                                        SurfAz=meta.SurfAz,
	                                        DHI=TMY.DHI,
	                                        DNI=TMY.DNI,
	                                        GHI=TMY.GHI,
	                                        HExtra=TMY.HExtra,
	                                        SunZen=TMY.SunZen,
	                                        SunAz=TMY.SunAz)

	assert(np.size(TMY['In_Plane_SkyDiffuse'])==np.size(TMY['SunZen']))

def test_scalar():
	
	assert(False)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
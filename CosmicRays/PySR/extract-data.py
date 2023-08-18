# imports and definitions

import numpy as np
import matplotlib.pyplot as plt
import h5py
import pandas as pd
from datetime import datetime, timedelta

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "text.latex.preamble" : r'\boldmath'
})

# constants
pc   = 3.0856775814913674e+18
kpc  = 3.0856775814913673e+21
Msol = 1.988409870698051e+33
Myr  = 31557600000000.0

# definitions for the units
def _read_units(fname, verbose=False):
    if verbose:
        print("reading file: ", fname)
    f = h5py.File(fname, "r")
    # get momentum boundaries from file
    try:
        UnitMass = f[u'Parameters'].attrs.get("UnitMass_in_g")
        UnitLen  = f[u'Parameters'].attrs.get("UnitLength_in_cm")
        UnitVelo = f[u'Parameters'].attrs.get("UnitVelocity_in_cm_per_s")
        BoxSize  = f[u'Parameters'].attrs.get("BoxSize")
    except:
        print("Unit parameters not found!!!")
    f.close()
    return UnitMass, UnitLen, UnitVelo, BoxSize


def _compute_arepo_units(UnitMass, UnitLength, UnitVelocity, print_units=False):
    UnitTime = UnitLength/UnitVelocity
    d = { "UnitLength"   : UnitLength,
          "UnitMass"     : UnitMass,
          "UnitVelocity" : UnitVelocity,
          "UnitTime"     : UnitLength/UnitVelocity,
          "UnitDensity"  : UnitMass/(UnitLength**3),
          "UnitColdens"  : UnitMass/(UnitLength**2),
          "UnitEnergy"   : UnitMass*UnitVelocity*UnitVelocity,
          "UnitEspecific": UnitVelocity*UnitVelocity,
          "UnitEdensity" : UnitMass / UnitLength / UnitTime**2,
          "UnitPressure" : UnitMass / UnitLength / UnitTime**2,
          "UnitBfield"   : np.sqrt(UnitMass) / np.sqrt(UnitLength) / UnitTime,
          "UnitGrav"     : UnitLength**3 / (UnitMass * UnitTime**2),
          "UnitPotential": UnitLength**2 / (UnitTime**2),
          # non cgs
          "UnitColdens_Msol_pc2" : UnitMass/(UnitLength**2) / Msol * pc*pc

    }
    if print_units:
        print()
        print("Arepo units")
        # find longest key name
        maxlen = len(max(d, key=len))
        for key in d:
            print(key.ljust(maxlen), ":", d[key])
        print()
    return d


def _read_momentum_bins(fname):
    print("reading file: ", fname)
    f = h5py.File(fname, "r")
    Nspec = f[u'PartType0/CRspecEnergy'].shape[1]
    # get momentum boundaries from file
    try:
        pmin = f[u'Parameters'].attrs.get("CRspec_pmin")
        p0   = f[u'Parameters'].attrs.get("CRspec_p0")
        p1   = f[u'Parameters'].attrs.get("CRspec_p1")
        pmax = f[u'Parameters'].attrs.get("CRspec_pmax")

        pf = np.zeros(Nspec+1)
        pf[0]  = pmin
        pf[-1] = pmax
        pf[1:-1] = np.logspace(np.log10(p0), np.log10(p1), Nspec-1, endpoint=True)

        pi   = np.sqrt(pf[:-1]*pf[1:])
    except:
        print("momentum parameters not found!!!")
    return pf, pi


# read data from one snapshot
def _read_snapshot_data(filename, ax_spec = None, ax_slope = None, print_fields = False, print_info = False):
    # open file
    f = h5py.File(filename)
    if print_fields:
        if filename == files[0]:
            for k in f["PartType0"].keys():
                print(k)
    
    # read units from file
    UnitM, UnitL, UnitV, BoxSize = _read_units(filename)
    U = _compute_arepo_units(UnitM, UnitL, UnitV, False)
    
    # read momenta
    pf, pi = _read_momentum_bins(filename)
    #print(pi)
    
    BoxCtr = BoxSize*U["UnitLength"]/2.

    # get full data and convert it to cgs
    
    # positions
    pos  = np.array(f[u'PartType0/Coordinates']).astype(np.float64)*U["UnitLength"]-BoxCtr
    rad  = np.sqrt(np.sum(pos**2,axis=1))

    # velocities
    vel  = np.array(f[u'PartType0/Velocities']).astype(np.float64)*U["UnitVelocity"]
    velo = np.sqrt(np.sum(vel**2,axis=1))
    
    # density, mass and volume
    dens = np.array(f[u'PartType0/Density']).astype(np.float64)*U["UnitDensity"]
    mass = np.array(f[u'PartType0/Masses'])*U["UnitMass"]
    volu = mass/dens

    # gravitational potential
    gpot = np.array(f[u'PartType0/Potential']).astype(np.float64)*U["UnitPotential"]

    # thermal pressure
    pres = np.array(f[u'PartType0/Pressure']).astype(np.float64)*U["UnitPressure"]

    # magnetic field vector
    mag  = np.array(f[u'PartType0/MagneticField']).astype(np.float64)*U["UnitBfield"]
    Babs = np.sqrt(np.sum(mag**2,axis=1))
    
    # total CR energy density
    cren = np.array(f[u'PartType0/CosmicRaySpecificEnergy']).astype(np.float64)*U["UnitEspecific"]
    encr = cren*dens
    
    # CR spectrum amplitude
    crspec = np.array(f[u'PartType0/CRspecEnergy']).astype(np.float64)
    slope  = np.log(crspec[:,-1]/crspec[:,-2]) / np.log(pi[-1]/pi[-2])
    
    if not ax_slope is None:
        ax_slope.hist(slope)
    
    # print some checks
    # select cell closest to the centre of the galaxy
    if print_info:
        ichk = np.argsort(rad)[0]
        print("properties of the central cells")
        print("  position", pos[ichk])
        print("  density ", dens[ichk])
        print("  slope   ", slope[ichk])
    
    if not ax_spec is None:
        ax_spec.loglog(pi, crspec[ichk])
    
    #idx = np.where((dens > 1e-25) & (rad < 2*kpc))
    idx = np.where(dens > 1e-29)
    print("selected number of cells: ", dens[idx].shape)
    
    return {"density": dens[idx], \
            "radius": rad[idx], \
            "slope" : slope[idx], \
            "Babs"  : Babs[idx], \
            "encr"  : encr[idx]} 

# list of files directly or from command line
if False:
    import argparse
    parser = argparse.ArgumentParser(description='cmd line args')
    parser.add_argument('files', nargs='+', help='files')
    args = parser.parse_args()
    files = args.files
else:
    # files by hand
    files = [ "snapshot_100.hdf5" ]




plot_chk_spectra = False

def conv(data):
    return np.log10(data)

if plot_chk_spectra:
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

# collect all data from all snapshots
all_dens   = np.array([])
all_radius = np.array([])
all_slope  = np.array([])
all_encr   = np.array([])
all_Babs   = np.array([])

# loop over files
for filename in files:
    loc_data = _read_snapshot_data(filename)
    
    # add local data to global arrays
    all_dens   = np.append(all_dens,   loc_data["density"])
    all_slope  = np.append(all_slope,  loc_data["slope"])
    all_radius = np.append(all_radius, loc_data["radius"])
    all_encr   = np.append(all_encr,   loc_data["encr"])
    all_Babs   = np.append(all_Babs,   loc_data["Babs"])

if plot_chk_spectra:
    ax1.set_xlabel("momentum (GeV/c)")
    ax1.set_ylabel("energy")
    fig1.savefig("spectra-of-central-cell.pdf", bbox_inches="tight")
    
data = pd.DataFrame({'density': conv(all_dens),\
                     'radius': all_radius,\
                     'slope': all_slope,\
                     'encr': conv(all_encr),\
                     'Babs': conv(all_Babs)})
                     #'mass': mass[idx],\
                     #'gpot': gpot[idx],\
                     #'pres': conv(pres[idx]),\
                     #'velo': velo[idx]})

                     
# normalise data to range between 0 and 1
def _norm(x):
    vmin = np.min(x)
    vmax = np.max(x)
    return vmin, vmax, (x-vmin)/(vmax-vmin)

def _unnorm(x, vmin, vmax):
    return x*(vmax-vmin) + vmin

ndens   = _norm(data["density"])
nradius = _norm(data["radius"])
nencr   = _norm(data["encr"])
nBabs   = _norm(data["Babs"])
nslope  = _norm(data["slope"])

for f, n in zip([ndens[2], nradius[2], nencr[2], nBabs[2], nslope[2]], ["dens", "radius", "encr", "Babs", "slope"]):
    np.save("sum-data-"+n, f)
    

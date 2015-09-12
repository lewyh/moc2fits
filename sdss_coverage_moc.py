from __future__ import print_function, division
import numpy as np
import healpy
from astropy.io import fits
import urllib

def calc_order(value):
    return (np.log2(value / 4) / 2).astype(int)

urllib.urlretrieve('http://wsa.roe.ac.uk/coverage-maps/OtherSurveys/sdssDR9-hires.fits', 'sdssDR9-hires.fits')
fn = 'sdssDR9-hires.fits'

h = fits.getheader(fn, 1)
d = fits.getdata(fn, 1)

MOCORDER = 10

values = np.array(d).astype(int)
orders = calc_order(values)
cells = values - 4 * np.power(4, orders)

moc = np.zeros(12 * np.power(4, MOCORDER))

dt = {}

for o in set(orders):
    mask = np.where(orders == o)
    dt[o] = cells[mask]

moc = np.zeros(12 * np.power(4, MOCORDER))

allcells = set(dt[MOCORDER])

for order in range(np.min(dt.keys()), MOCORDER):
    shift = 2 * (MOCORDER - order)
    for cell in dt[order]:
        allcells.update(range(cell << shift, (cell+1) << shift ))

for cell in allcells:
    moc[cell] += 1

xsize = 6400
ysize = 3200

mocmap = healpy.visufunc.cartview(moc, sub=111, nest=True, notext=True, coord=['C', 'G'], rot=(0,0,0), xsize=xsize, ysize=ysize, return_projected_map=True)

header = fits.Header()
header['CRPIX1'] = xsize/2.0
header['CRPIX2'] = ysize/2.0
header['CRVAL1'] = 0
header['CRVAL2'] = 0
header['CTYPE1'] = 'GLON-CAR'
header['CTYPE2'] = 'GLAT-CAR'
header['CDELT1'] = 360.0/xsize
header['CDELT2'] = 180.0/ysize
header['EQUINOX'] = 2000.0
header['OBJECT'] = 'SDSS DR9 coverage'

hdu = fits.PrimaryHDU(np.fliplr(np.array((mocmap))), header=header)
hdu.writeto('sdss_dr9_coverage.fits', clobber=True)

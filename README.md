# moc2fits
Convert multi-order coverage file to fits image for easier visualization

---

Downloads SDSS DR9 MOC file hosted on WFCAM Science Archive, converts the HEALPIX coverage information into a numpy array and writes out to a FITS image.

Requires numpy, astropy & healpix.

Max resolution of ~3.5 arcmin limited by MOC file order.

The script currently generates an image in Galactic coordinates. 
Details can be found at http://healpy.readthedocs.org/ on how to generate alternative projections.

If the script eats up too much memory, reduce the xsize/ysize of the generated FITS file. If this doesn't solve the problem try reducing the MOCORDER (though this will result in a lower resolution image).

import os
import urllib.request 


def download_NCLIMGRID(year, month):
    """ Download an NCLIMGRID data file for a particular year-month """
    
    month = str(month).zfill(2)
    year = str(year)
    root = 'https://www.ncei.noaa.gov/data/nclimgrid-daily/access/grids'
    filename = 'ncdd-' + year + month + '-grd-scaled.nc'

    url = '/'.join([root, str(year), filename])

    urllib.request.urlretrieve(url, filename)
    return None


years = range(1991, 1992)
months = range(1, 13)

for year in years:
    print('Downloading ' + str(year) + '...')
    for month in months:
        download_NCLIMGRID(year, month)
    
    print('Done!')

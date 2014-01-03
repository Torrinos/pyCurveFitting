from lmfit import minimize, Parameters, Parameter, report_fit
import numpy as np
from uncertainties import ufloat

infile = open('../data/temperatures.dat','r')
t=np.genfromtxt(infile,names=True,skip_header=17,skip_footer=2)
tx=t['YEAR']
ty=t['JUN']

# create data to be fitted
x = np.linspace(0, 15, 301)
data = (5. * np.sin(2 * x - 0.1) * np.exp(-x*x*0.025) +
        np.random.normal(size=len(x), scale=0.2) )

# define objective function: returns the array to be minimized
def fcn2min(params, x, data):
    """ model decaying sine wave, subtract data"""
    A1 = params['A1'].value
    A2 = params['A2'].value
    A3 = params['A3'].value
    A4 = params['A4'].value

    model = A1 + A2*np.exp(A3*x)
    return model - data

# create a set of Parameters
params = Parameters()
params.add('A1', value= 1,  min=0)
params.add('A2', value= 1)
params.add('A3', value= 0.1)
params.add('A4', value= 0.2)

# do fit, here with leastsq model
result = minimize(fcn2min, params, args=(tx, ty))

# calculate final result
final = ty + result.residual

# write error report
report_fit(params)

# try to plot results
try:
    import pylab
    pylab.plot(tx, ty, 'k+')
    pylab.plot(tx, final, 'r')
    pylab.show()
except:
    pass
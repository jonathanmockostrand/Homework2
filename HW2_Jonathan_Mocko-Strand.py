#############################################################################
##                                                                         ##
## Jonathan Mocko-Strand                                                   ##
## Dept. of Geology & Geophysics, TAMU. 2013-10-15                         ##
## Python for Geoscientists                                                ##
## Homework Assignment 2                                                   ##
##                                                                         ##
#############################################################################

# import packages
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import urllib as ulb

def USGS_River_Discharge (start_date, end_date, site_number):
    '''
    USGS_River_Discharge is a function that will retrieve river discharge data 
    from the USGS database. This function will read the station numner, 
    discharge amount, and calculated the mean as well ass the standard deviation 
    of the discharge.

    Input:
        USGS URL for discharge data containing:
            start_date = initialization data
            end_date = ending data
            site_number = number associated to site location
    Output:
        Selected USGS discharge data output to plot_USGS_River_Discharge 
        function to be plotted.        
    '''
    
    # Data selection
    start  = str( date(1900,1,1) )
    end    = str( date.today() )
    site   = '01100000'
    
    # Retrieval of USGS river discharge data
    USGS_URL = ulb.urlopen\
             ('http://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb'+\
              '&begin_date='+start+'&end_date='+end+'&site_no='+site)
              
    # Define lists
    dates         = []
    datesplit     = []
    discharge     = []
    avg_discharge = []
    std_discharge = []
    
    # Read discharge data
    # Split date data into year, month, day, then append
    for line in USGS_URL.readlines()[28:]:
        data = line.split ()
        datesplit = data[2]
        year  = int(datesplit.split('-')[0])
        month = int(datesplit.split('-')[1])
        day   = int(datesplit.split('-')[2])
        dates.append(date(year, month, day))
        discharge.append(int(data[3]))
    
    USGS_URL.close()
    
    # Convert defined lists into array format
    dates     = np.array (dates)
    discharge = np.array (discharge)
    
    # Calculations
    # Conversion of discharge units from cfs to cms
    discharge = discharge / 35.315
    
    months = np.array( [d.month for d in dates] )
    days   = np.array( [d.day for d in dates] )
    
    for idx in dates:
    # Calculate the annual mean discharge
        cal_discharge = discharge [(months==idx.month) & (days==idx.day)]
        avg_discharge.append (np.mean (cal_discharge))
    
    # Calculate the std. dev. of mean discharge
        std_discharge.append (np.std (cal_discharge))

####################################################
                
    # Convert Calculated lists into arrays
    avg_discharge  = np.array(avg_discharge)
    std_discharge = np.array(std_discharge)

    # Select the time span for plotting
    plt_year    = np.array ([d.year for d in dates])
    idx         = np.where (plt_year >= 2011)
    plt_dates   = dates [idx]
    plt_discharge    = discharge [idx]
    plt_avg_discharge = avg_discharge [idx]
    plt_upstdv  = avg_discharge [idx] + std_discharge [idx]
    plt_lowstdv = avg_discharge [idx] - std_discharge [idx]

    USGS_River_Discharge_Plot(plt_year,idx,plt_dates,plt_discharge,plt_avg_discharge,plt_upstdv,plt_lowstdv,site)


####################################################


def USGS_River_Discharge_Plot(plt_year,idx,plt_dates,plt_flow,plt_avgflow,plt_upstdv,plt_lowstdv,site):
    '''    
    USGS_River_Discharge_Plot is a function that will retrieve river 
    discharge data from the USGS USGS_River_Discharge fuction and then 
    plot the data in a PDF file format.

    Input:
        USGS_River_Discharge data output.
    Output:
        A PDF file at 300dpi that contains the plotted Daily Discharge, 
        Annual Mean Discharge, and Annual Standard Deciation for the Annual 
        Mean Discharge.
    '''

    # Plot the results of USGS_River_Discharge
    Discharge_Figure=plt.figure()
    Discharge_Figure.autofmt_xdate()

    axis=Discharge_Figure.add_axes([0.1,0.1,0.8,0.8])
    axis.plot(plt_dates, plt_flow, color = '#000000', label = "Daily Discharge",  lw = 1)
    axis.plot(plt_dates, plt_avgflow, color = '#ff6600', label = "Annual Mean Discharge", lw = 1)
    axis.plot(plt_dates, plt_upstdv, ':', color = '#003300', label = 'Upper Std. Dev.')
    axis.plot(plt_dates, plt_lowstdv, ':', color = '#003300', label = 'Lower Std. Dev.')
    axis.fill_between(plt_dates, plt_upstdv, plt_lowstdv, facecolor='#ccff99',alpha=0.3)

    # Plot title and axis labels
    plt.title('Timeseries of Discharge from 2010\n'
                'For Site No. '+site+'\n'
                'MERRIMACK RIVER BL CONCORD RIVER AT LOWELL, MA', size=16)
    plt.xlabel('\nDates', size= 14)
    plt.ylabel(r'Discharge (m$^{3}$ s$^{-1}$)', size= 14)

    # Add legend and maximize figure window
    axis.legend()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()

    plt.show()

    # Save the output figure as a .pdf file with a dpi of 300
    plt.savefig('HW2_Jonathan_Mocko-Strand.pdf', dpi=300)

    plt.close()

# Initiate the function
USGS_River_Discharge (2010, 2013, '01100000')

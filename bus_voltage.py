
# ----------------------------------------------------------------------------------------------------
import os

# ----------------------------------------------------------------------------------------------------
def array2dict(dict_keys, dict_values):
    '''Convert array to dictionary of arrays.
    Returns dictionary as {dict_keys:dict_values}
    '''
    tmpdict = {}
    for i in range(len(dict_keys)):
        tmpdict[dict_keys[i].lower()] = dict_values[i]
    return tmpdict

# ----------------------------------------------------------------------------------------------------
def brnflows_csv(savfile,csvfile):
    '''Generates power flow result report.
    When 'savfile' is provided, FNSL with default options is used to solve the case.
    When 'savfile' is not provided, it uses solved Case from PSS(R)E memory.
    When 'csvfile' is provided, report is saved in ASCII text file 'csvfile'.
    When 'csvfile' is not provided, it produces report in PSS(R)E report window.
    '''

    import psspy
    psspy.psseinit()

    # Set Save and CSV files according to input file names
    if savfile:
        ierr = psspy.case(savfile)
        if ierr != 0: return
        fpath, fext = os.path.splitext(savfile)
        if not fext: savfile = fpath + '.sav'
    else:   # saved case file not provided, check if working case is in memory
        ierr, nbuses = psspy.abuscount(-1,2)
        if ierr != 0:
            print('\n No working case in memory.')
            print(' Either provide a Saved case file name or open Saved case in PSSE.')
            return
        savfile, snapfile = psspy.sfiles()

    csvfile_h = open(csvfile,'w')
    report = csvfile_h.write

    # ------------------------------------------------------------------------------------------------
    # Bus Data
    # Bus Data - Integer

    istrings = ['number', 'type', 'area']
    ierr, idata = psspy.abusint(sid=-1,flag=2,string=istrings)
    if ierr != 0: return
    iflow = array2dict(istrings, idata)
    # Bus Data - Real
    rstrings = ['base', 'pu', 'kv','angle','angled','nvlmhi','nvlmlo','evlmhi','evlmlo']
    ierr, rdata = psspy.abusreal(sid=-1,flag=2,string=rstrings)

    if ierr != 0: return
    rflow = array2dict(rstrings, rdata)
    # Bus Data - Character
    cstrings = ['name','exname']
    ierr, cdata = psspy.abuschar(sid=-1,flag=2,string=cstrings)
    if ierr != 0: return
    cflow = array2dict(cstrings, cdata)
    report("Bus Data from Saved case: %s\n" %savfile)
    clnttls = "%10s,%10s,%10s,%10s,%10s,%10s\n" %('Bus Number','Bus Name','Area','Base Voltage', 'Bus Voltage(PU)', 'Bus Voltage(kV)') 
  
    report(clnttls)
    for i in range(len(rflow['base'])):
        number     = iflow['number'][i]
        area       = iflow['area'][i]
        name       = cflow['name'][i]
        base       = rflow['base'][i]
        pu         = round(rflow['pu'][i],3)
        kv         = round(rflow['kv'][i],3)
        report("%(number)6d,%(name)6s,%(area)18s,%(base)6.8f,%(pu)6.8f,%(kv)6.8f\n" %vars())
    csvfile_h.close()
    print('\n Done .... Bus results Report saved to file %s' % csvfile)
# =====================================================================================================

def run_brnflows_csv():
    # psspy.case(r"""savnw_solar.sav""")
    # list_gens = [5,50,100] # for solar

    # for gen in list_gens:
    #     for load in list_loads:
    #         load = 
    #         sav = 'savnw_solar_' + str(gen)
    #         file_sav_out = sav + '.sav'
    #         file_csv_out = 'loading_' + sav + '.csv'
    brnflows_csv('savnw.sav', 'savnw_volt.csv')

# ====================================================================================================
if __name__ == '__main__':

    import psse35
    run_brnflows_csv()

# ====================================================================================================

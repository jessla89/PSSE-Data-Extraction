
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
    report    = csvfile_h.write

    istring= ['number']
    ierr, iarray = psspy.aareaint(sid=-1, flag=2, string=istring)
    if ierr != 0: return
    iareanumb = array2dict(istring, iarray)
    cstring = ['areaname']
    ierr, carray = psspy.aareachar(sid=-1, flag=2, string=cstring)
    if ierr != 0: return
    iareaname = array2dict(cstring, carray)
    astring = ['pdes','ptol','pload','qload','ploadld','qloadld','pgen','qgen','ploss','qloss',
               'pxfrmag','qxfrmag','pint','qint','o_pdes','o_ptol','o_pload','o_qload','o_ploadld',
                'o_qloadld','o_pgen','o_qgen','o_ploss','o_qloss','o_pxfrmag','o_qxfrmag','o_pint','o_qint']
    ierr, rarray = psspy.aareareal(sid=-1,flag=2,string=astring)
    if ierr != 0: return
    iareadata = array2dict(astring, rarray)
    clnttls_1 = "%10s,%10s,%10s,%10s,%10s,%10s\n" %('Area','Number','From Generation','To Load','To(+)/From(-) Ties','To Losses')
    report(clnttls_1)
    
    for i in range(len(iareaname['areaname'])):
        area   = iareaname['areaname'][i]
        number = iareanumb['number'][i]
        pgen   = iareadata['pgen'][i]
        pload  = iareadata['pload'][i]
        pint   = iareadata['pint'][i]
        ploss  = iareadata['ploss'][i]
        report("%(area)6s,%(number)6d,%(pgen)6d,%(pload)6d,%(pint)6d,%(ploss)6d\n" %vars())
    
    csvfile_h.close()
    print('\n Done .... Power Flow Results Report saved to file %s' % csvfile)
# =====================================================================================================

def run_brnflows_csv():
    list_savs = ['savnw']
    for sav in list_savs:
        file_sav_out = sav + '.sav'
        file_csv_out = sav + '_tot.csv'
        brnflows_csv(file_sav_out, file_csv_out)

# ====================================================================================================
# ====================================================================================================
if __name__ == '__main__':

    import psse35
    run_brnflows_csv()

# ====================================================================================================

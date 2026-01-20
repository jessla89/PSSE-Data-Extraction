"""
This program gives 
Active power output of in-service machines at this plant, in MW and 
spinning reserve available from machines at this plant. 
Power flow is conducted with automatic adjustment option for the system to meet area net interchange schedules.
"""
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

    # ------------------------------------------------------------------------------------------------
    # Generator Data
    # Generator Data - Integer
    istrings = ['number','area',]
    ierr, idata = psspy.agenbusint(sid = -1, flag = 4,string=istrings)
    if ierr != 0: return
    iflow = array2dict(istrings, idata)
    # Branch Flow Data - Real
    rstrings = ['base','pu','kv','pgen','pmax']
    ierr, rdata = psspy.agenbusreal(sid = -1, flag = 4,string=rstrings)
    if ierr != 0: return
    rflow = array2dict(rstrings, rdata)

    # Branch Flow Data - Character
    cstrings = ['name','exname']
    ierr, cdata = psspy.agenbuschar(sid = -1, flag = 4,string=cstrings)
    if ierr != 0: return
    cflow = array2dict(cstrings, cdata)
    report("Branch flows from Saved case: %s\n" %savfile)
    clnttls= "%6s,%4s,%4s,%4s,%4s,%7s\n" %('Number','Name','Area','Pgen','Pmax','Reserve')
    report(clnttls)

    for i in range(len(iflow['number'])):
        fromnum    = iflow['number'][i]
        fromexname = cflow['name'][i]
        tonum      = iflow['area'][i]
        pgen       = rflow['pgen'][i]
        pmax       = rflow['pmax'][i]
        reserve    = rflow['pmax'][i] - rflow['pgen'][i]
        report("%(fromnum)6d,%(fromexname)18s,%(tonum)6d,%(pgen)9.2F,%(pmax)9.2F,%(reserve)9.2F\n" %vars())
    
    csvfile_h.close()
    print('\n Done .... Power Flow Results Report saved to file %s' % csvfile)
# =====================================================================================================

def run_brnflows_csv():
    file_sav_out = 'savnw.sav'
    file_csv_out = 'gen_sav.csv'
    brnflows_csv(file_sav_out, file_csv_out)

# ====================================================================================================
if __name__ == '__main__':

    import psse35
    run_brnflows_csv()

# ====================================================================================================

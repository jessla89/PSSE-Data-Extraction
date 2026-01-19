
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

    sid = -1
    flag_brflow  = 1    # in-service
    owner_brflow = 1    # use bus ownership, ignored if sid is -ve
    ties_brflow  = 5    # ignored if sid is -ve

    # ------------------------------------------------------------------------------------------------
    # Branch Flow Data
    # Branch Flow Data - Integer
    istrings = ['fromnumber','tonumber','status','nmeternumber','owners','own1','own2','own3','own4']
    ierr, idata = psspy.aflowint(sid, owner_brflow, ties_brflow, flag_brflow, istrings)
    if ierr != 0: return
    iflow = array2dict(istrings, idata)
    # Branch Flow Data - Real
    rstrings = ['amps','pucur','pctrate','pctratea','pctrateb','pctratec','pctmvarate',
                'pctmvaratea','pctmvarateb','pctmvaratec','fract1','fract2','fract3',
                'fract4','rate','ratea','rateb','ratec',
                'p','q','mva','ploss','qloss',
                'o_p','o_q','o_mva','o_ploss','o_qloss'
                ]
    ierr, rdata = psspy.aflowreal(sid, owner_brflow, ties_brflow, flag_brflow, rstrings)
    if ierr != 0: return
    rflow = array2dict(rstrings, rdata)
    # Branch Flow Data - Complex
    xstrings = ['pq','pqloss','o_pq','o_pqloss']
    ierr, xdata = psspy.aflowcplx(sid, owner_brflow, ties_brflow, flag_brflow, xstrings)
    if ierr != 0: return
    xflow = array2dict(xstrings, xdata)
    # Branch Flow Data - Character
    cstrings = ['id','fromname','fromexname','toname','toexname','nmetername','nmeterexname']
    ierr, cdata = psspy.aflowchar(sid, owner_brflow, ties_brflow, flag_brflow, cstrings)
    if ierr != 0: return
    cflow = array2dict(cstrings, cdata)
    report("Branch flows from Saved case: %s\n" %savfile)

    clnttls = "%6s,%18s,%6s,%18s,%3s,%3s,%9s,%9s,%9s,%6s,%8s,%8s,%8s\n" %('FRMBUS',
             'FROMBUSVOLT','TOBUS','TOBUSVOLT','CKT','STS','MW','MVAR','MVA','%I','MWLOSS','MVARLOSS','%MVA')
    report(clnttls)
    for i in range(len(iflow['fromnumber'])):
        fromnum    = iflow['fromnumber'][i]
        fromexname = cflow['fromexname'][i]
        tonum      = iflow['tonumber'][i]
        toexname   = cflow['toexname'][i]
        ckt        = cflow['id'][i]
        status     = iflow['status'][i]
        p          = rflow['p'][i]
        q          = rflow['q'][i]
        mva        = rflow['mva'][i]
        ploss      = rflow['ploss'][i]
        qloss      = rflow['qloss'][i]
        pcti       = rflow['pctrate'][i]
        pctr       = rflow['pctmvarate'][i]
        report("%(fromnum)6d,%(fromexname)18s,%(tonum)6d,%(toexname)18s,%(ckt)3s,%(status)3d,\
                %(p)9.2F,%(q)9.2F,%(mva)9.2F,%(ploss)8.2F,%(qloss)8.2F,%(pcti)6.2F,%(pctr)8.2F\n" %vars())
    
    csvfile_h.close()
    print('\n Done .... Power Flow Results Report saved to file %s' % csvfile)
# =====================================================================================================

def run_brnflows_csv():
    sav = 'savnw' 
    file_sav_out = sav + '.sav'
    file_csv_out = 'loading_' + sav + '.csv'
    brnflows_csv(file_sav_out, file_csv_out)

# ====================================================================================================
if __name__ == '__main__':

    import psse35
    run_brnflows_csv()

# ====================================================================================================

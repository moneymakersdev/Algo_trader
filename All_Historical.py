import subprocess
import threading

## Define a list of Python scripts to run
#scripts_to_run = ['Historical/Zerodha_TVS.py', 'Historical/Zerodha_M_M.py',
#                'Historical/Zerodha_HDFCBANK.py', 'Historical/Zerodha_INDUSINDBK.py', 'Historical/Zerodha_INFY.py', 'Historical/Zerodha_HAVELLS.py', 'Historical/Zerodha_SBILIFE.py',
#                'Historical/Zerodha_ICICIGI.py', 'Historical/Zerodha_CHOLAFIN.py', 'Historical/Zerodha_HCLTECH.py', 'Historical/Zerodha_MUTHOOTCAP.py',
#                'Historical/Zerodha_TECHM.py', 'Historical/Zerodha_CIPLA.py', 'Historical/Zerodha_SUNPHARMA.py', 'Historical/Zerodha_MCDOWELL-N.py', 'Historical/Zerodha_GODREJCP.py',
#                'Historical/Zerodha_ICICIBANK.py', 'Historical/Zerodha_ADANIGREEN.py', 'Historical/Zerodha_VBL.py', 'Historical/Zerodha_SBICARD.py', 'Historical/Zerodha_JSWSTEEL.py',
#                'Historical/Zerodha_IRFC.py', 'Historical/Zerodha_JINDALSTEL.py', 'Historical/Zerodha_LICI.py', 'Historical/Zerodha_TATAMOTORS.py', 'Historical/Zerodha_HDFCLIFE.py',
#                'Historical/Zerodha_ATGL.py', 'Historical/Zerodha_ZYDUSLIFE.py', 'Historical/Zerodha_SBIN.py', 'Historical/Zerodha_DLF.py', 'Historical/Zerodha_BERGEPAINT.py',
#                'Historical/Zerodha_MARICO.py', 'Historical/Zerodha_DABUR.py', 'Historical/Zerodha_ICICIPRULI.py', 'Historical/Zerodha_HINDALCO.py', 'Historical/Zerodha_ITC.py',
#                'Historical/Zerodha_TATAMTRDVR.py', 'Historical/Zerodha_AMBUJACEM.py', 'Historical/Zerodha_WIPRO.py', 'Historical/Zerodha_COALINDIA.py', 'Historical/Zerodha_TATAPOWER.py',
#                'Historical/Zerodha_NTPC.py', 'Historical/Zerodha_BPCL.py', 'Historical/Zerodha_AWL.py', 'Historical/Zerodha_MUTHOOTFIN.py', 'Historical/Zerodha_AXISBANK.py',
#                'Historical/Zerodha_ADANIPORTS.py', 'Historical/Zerodha_BHARTIARTL.py', 'Historical/Zerodha_KOTAKBANK.py', 'Historical/Zerodha_ONGC.py', 'Historical/Zerodha_POWERGRID.py',
#                'Historical/Zerodha_TATASTEEL.py', 'Historical/Zerodha_TATACONSUM.py', 'Historical/Zerodha_UPL.py']



scripts_to_run = ['Historical/zerodha_bnf_5M.py', 'Historical/zerodha_bnf_15M.py', 'Historical/zerodha_bnf_fut_15m.py', 
                'Historical/zerodha_bnf_fut_5m.py', 'Historical/zerodha_bnf_fut_1H.py', 'Historical/zerodha_nifty_Fut_5M.py', 
                'Historical/zerodha_nifty_Fut_15m.py', 'Historical/zerodha_nifty_Fut_1H.py', 'Historical/zerodha_bnf_fut_1m.py', 
                'Historical/zerodha_bnf_1m.py']



def run_script(script):
    try:
        subprocess.run(["python", script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}: {e}")

# Create and start a thread for each script
threads = []
for script in scripts_to_run:
    thread = threading.Thread(target=run_script, args=(script,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("All scripts have finished.")
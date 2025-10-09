# save as plot_sp500_jolts.py and run with: python plot_sp500_jolts.py
import io
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# FRED series IDs used:
# S&P 500: SP500  (monthly, index)
# Job Openings (level, thousands, not seasonally adjusted): JTUJOL
# (JOLTS series begin Dec 2000). See FRED pages:
# Job Openings: https://fred.stlouisfed.org/series/JTUJOL
# S&P 500:      https://fred.stlouisfed.org/series/SP500

FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={id}"

def fetch_fred_series(series_id):
    url = FRED_CSV.format(id=series_id)
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    # fred csv has DATE,VALUE header
    df = pd.read_csv(io.StringIO(r.text), parse_dates=['DATE'])
    df = df.rename(columns={'DATE':'date', 'VALUE': series_id})
    df.set_index('date', inplace=True)
    return df

def main():
    # fetch series
    print("Downloading S&P 500 (SP500) ...")
    sp = fetch_fred_series("SP500")            # daily or monthly; FRED SP500 series is monthly (monthly close)
    print("Downloading Job Openings (JTUJOL) ...")
    jolts = fetch_fred_series("JTUJOL")        # monthly, level in thousands

    # Ensure monthly frequency and align
    # Convert SP500 to month-end monthly if daily exists (SP500 on FRED is monthly already)
    sp_monthly = sp.resample('M').last()
    jolts_monthly = jolts.resample('M').last()

    # Restrict to overlap period where JOLTS available (JOLTS starts Dec 2000)
    start = max(sp_monthly.index.min(), jolts_monthly.index.min(), pd.to_datetime("2000-12-01"))
    end = min(sp_monthly.index.max(), jolts_monthly.index.max())
    sp_trim = sp_monthly.loc[start:end].copy()
    jolts_trim = jolts_monthly.loc[start:end].copy()

    # Merge
    df = sp_trim.join(jolts_trim, how='inner')

    # Convert JTUJOL to numeric (it may contain '.')
    df['JTUJOL'] = pd.to_numeric(df['JTUJOL'], errors='coerce')
    df['SP500']  = pd.to_numeric(df['SP500'], errors='coerce')

    # Drop missing if any
    df = df.dropna()

    # Normalize both series to 100 at start date for visual comparison
    base_sp = df['SP500'].iloc[0]
    base_jolts = df['JTUJOL'].iloc[0]
    df['SP500_index'] = df['SP500'] / base_sp * 100.0
    df['JOLTS_index']  = df['JTUJOL'] / base_jolts * 100.0

    # Plot
    plt.figure(figsize=(12,6))
    plt.plot(df.index, df['SP500_index'], label='S&P 500 (indexed, base=100 at {})'.format(df.index[0].strftime('%Y-%m')))
    plt.plot(df.index, df['JOLTS_index'], label='Job Openings (JOLTS, indexed, base=100 at {})'.format(df.index[0].strftime('%Y-%m')))
    plt.title('S&P 500 vs Job Openings (JOLTS) — {} to {}'.format(df.index[0].strftime('%Y-%m'), df.index[-1].strftime('%Y-%m')))
    plt.xlabel('Date')
    plt.ylabel('Index (base=100)')
    plt.legend()
    plt.grid(axis='y', alpha=0.4)
    plt.tight_layout()
    outfile = f"sp500_vs_jolts_{df.index[0].strftime('%Y%m')}_{df.index[-1].strftime('%Y%m')}.png"
    plt.savefig(outfile, dpi=150)
    print(f"Saved chart to {outfile}")

if __name__ == "__main__":
    main()

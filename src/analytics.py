import pandas as pd

def load_data(filepath='data/call_logs.csv'):
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def calculate_kpis(df):
    if df.empty:
        return {
            "aht": 0,
            "sla_percent": 0,
            "abandon_rate": 0,
            "total_calls": 0
        }

    # Total Calls
    total_calls = len(df)
    
    # Abandon Rate
    abandoned_calls = df[df['abandoned'] == 'Yes']
    abandon_rate = (len(abandoned_calls) / total_calls) * 100 if total_calls > 0 else 0
    
    # AHT (Average Handling Time) - only for answered calls implies duration > 0 usually
    # Assuming 'duration' lists the handle time.
    answered_calls = df[df['answered'] == 'Yes']
    aht = answered_calls['duration'].mean() if not answered_calls.empty else 0
    
    # SLA (Service Level Agreement)
    # Let's define SLA as answered within 20 seconds.
    # We generated 'wait_time' in the data generator.
    if 'wait_time' in df.columns:
        sla_met_calls = df[(df['answered'] == 'Yes') & (df['wait_time'] <= 20)]
        sla_percent = (len(sla_met_calls) / total_calls) * 100 if total_calls > 0 else 0
    else:
        sla_percent = 0

    return {
        "aht": round(aht, 2),
        "sla_percent": round(sla_percent, 2),
        "abandon_rate": round(abandon_rate, 2),
        "total_calls": total_calls
    }

def get_hourly_metrics(df):
    if df.empty:
        return pd.DataFrame()
        
    # Ensure time column is datetime? The csv has '10:05' etc. 
    # Since we didn't put Year/Month/Day, it might infer today
    # But for simple grouping by hour:
    
    # We accept the time string format
    # Let's extract hour
    df['hour'] = df['time'].apply(lambda x: int(x.split(':')[0]))
    
    hourly = df.groupby('hour').agg(
        calls=('call_id', 'count'),
        abandons=('abandoned', lambda x: (x == 'Yes').sum())
    ).reset_index()
    
    return hourly

# Example PASR implementation 
import pandas as pd

def calculate_psar(df, af_start=0.02, af_step=0.02, af_max=0.2):
    # Initialize columns
    df['PSAR'] = df['Low']  # Initial PSAR is set to Low
    df['Trend'] = 'Up'      # Initial trend is upward
    df['EP'] = df['High']   # Initial Extreme Price is the first High
    df['AF'] = af_start     # Acceleration Factor starts at af_start

    # Start iterating over rows to calculate PSAR
    for i in range(1, len(df)):
        prev_psar = df.at[i - 1, 'PSAR']
        prev_trend = df.at[i - 1, 'Trend']
        prev_ep = df.at[i - 1, 'EP']
        prev_af = df.at[i - 1, 'AF']

        if prev_trend == 'Up':
            # Calculate PSAR for Uptrend
            current_psar = prev_psar + prev_af * (prev_ep - prev_psar)
            # PSAR cannot exceed the current or previous lows
            current_psar = min(current_psar, df.at[i - 1, 'Low'], df.at[i, 'Low'])

            # Update trend based on High
            if df.at[i, 'High'] > prev_ep:
                current_ep = df.at[i, 'High']
                current_af = min(prev_af + af_step, af_max)
            else:
                current_ep = prev_ep
                current_af = prev_af

            # Check for trend reversal
            if df.at[i, 'Low'] < current_psar:
                df.at[i, 'Trend'] = 'Down'
                current_psar = prev_ep  # Reverse PSAR
                current_ep = df.at[i, 'Low']
                current_af = af_start
            else:
                df.at[i, 'Trend'] = 'Up'

        elif prev_trend == 'Down':
            # Calculate PSAR for Downtrend
            current_psar = prev_psar - prev_af * (prev_psar - prev_ep)
            # PSAR cannot exceed the current or previous highs
            current_psar = max(current_psar, df.at[i - 1, 'High'], df.at[i, 'High'])

            # Update trend based on Low
            if df.at[i, 'Low'] < prev_ep:
                current_ep = df.at[i, 'Low']
                current_af = min(prev_af + af_step, af_max)
            else:
                current_ep = prev_ep
                current_af = prev_af

            # Check for trend reversal
            if df.at[i, 'High'] > current_psar:
                df.at[i, 'Trend'] = 'Up'
                current_psar = prev_ep  # Reverse PSAR
                current_ep = df.at[i, 'High']
                current_af = af_start
            else:
                df.at[i, 'Trend'] = 'Down'

        # Update current row with calculated values
        df.at[i, 'PSAR'] = current_psar
        df.at[i, 'EP'] = current_ep
        df.at[i, 'AF'] = current_af

    return df

df = pd.DataFrame(data)
df = calculate_psar(df)
print(df)

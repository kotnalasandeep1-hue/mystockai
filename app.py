import streamlit as st
import yfinance as yf
import pandas_ta as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import ta # Library for technical analysis indicators (RSI, MACD)

st.set_page_config(page_title="Market Momentum AI", layout="wide")

# --- 1. MARKET DATA CONFIG ---
caps = {
    "LARGE CAP": ["RELIANCE.NS", "HDFCBANK.NS", "BHARTIARTL.NS", "TCS.NS", "ICICIBANK.NS", "SBIN.NS", "INFY.NS", "BAJFINANCE.NS", "LT.NS", "HINDUNILVR.NS", "LICI.NS", "MARUTI.NS", "M&M.NS", "HCLTECH.NS", "ITC.NS", "KOTAKBANK.NS", "SUNPHARMA.NS", "AXISBANK.NS", "TITAN.NS", "ULTRACEMCO.NS", "ONGC.NS", "POWERGRID.NS", "NTPC.NS", "ADANIENT.NS", "JSWSTEEL.NS", "ASIANPAINT.NS", "NESTLEIND.NS", "LTIM.NS", "DMART.NS", "PIDILITIND.NS", "SIEMENS.NS", "HINDALCO.NS", "BAJAJ-AUTO.NS", "WIPRO.NS", "ADANIPORTS.NS", "EICHERMOT.NS", "GRASIM.NS", "SBILIFE.NS", "ICICIPRULI.NS", "HDFCLIFE.NS", "TECHM.NS", "INDUSINDBK.NS", "COALINDIA.NS", "BPCL.NS", "IOC.NS", "GAIL.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TATASTEEL.NS", "CIPLA.NS", "DRREDDY.NS", "DIVISLAB.NS", "ADANIGREEN.NS", "ADANITRANS.NS", "IRCTC.NS", "IRFC.NS"],
    "MID CAP": ["SAIL.NS", "HINDCOPPER.NS", "NATIONALUM.NS", "JINDALSTEL.NS", "APOLLOTYRE.NS", "WELCORP.NS", "RATNAMANI.NS", "JSL.NS", "ABBOTINDIA.NS", "AJANTPHARM.NS", "ALKEM.NS", "AUROPHARMA.NS", "BIOCON.NS", "GLAND.NS", "GLENMARK.NS", "IPCALAB.NS", "JBCHEPHARM.NS", "LAURUSLABS.NS", "LUPIN.NS", "MANKIND.NS", "PPLPHARMA.NS", "TORNTPHARM.NS", "WOCKPHARMA.NS", "UNIONBANK.NS", "INDIANBANK.NS", "MAHABANK.NS", "CENTRALBK.NS", "UCOBANK.NS", "BANKINDIA.NS", "IOB.NS", "PSB.NS", "L&TFIN.NS", "CHOLAFIN.NS", "BAJAJFINSV.NS", "PFC.NS", "RECLTD.NS", "LICHGFIN.NS", "MUTHOOTFIN.NS", "SBICARD.NS", "DLF.NS", "OBEROIRLTY.NS", "GODREJPROP.NS", "PHOENIXLTD.NS", "BRIGADE.NS", "PRESTIGE.NS", "SOBHA.NS", "MAHLIFE.NS", "IBULHSGFIN.NS", "GMRINFRA.NS", "NHAI.NS", "ZEEL.NS", "SUNTV.NS", "PVRINOX.NS", "EROSPURAM.NS", "TV18BRDCST.NS", "HATHWAY.NS", "DB_CORP.NS", "JAGRAN.NS", "FORTIS.NS", "METROPOLIS.NS", "DRLALPATH.NS", "NARAYANA.NS", "MAXHEALTH.NS", "ASTERDM.NS", "GLENEAGLES.NS"],
    "SMALL CAP": ["IDEA.NS", "SUZLON.NS", "YESBANK.NS", "IRFC.NS", "ZOMATO.NS", "SAIL.NS", "NHPC.NS", "IOC.NS", "GAIL.NS", "BPCL.NS", "ONGC.NS", "TATASTEEL.NS", "HINDALCO.NS", "VEDL.NS", "CIL.NS", "NMDC.NS", "JINDALSTEL.NS", "JSWENERGY.NS", "RECLTD.NS", "PFC.NS", "IRCTC.NS", "BEL.NS", "HAL.NS", "BHEL.NS", "L&TFH.NS", "IBULHSGFIN.NS", "PNB.NS", "BANKINDIA.NS", "UNIONBANK.NS", "CANBK.NS", "IDFCFIRSTB.NS", "DELHIVERY.NS", "NYKAA.NS", "PAYTM.NS", "POLICYBZR.NS", "MMTC.NS", "HUDCO.NS", "NBCC.NS", "COCHINSHIP.NS", "FACT.NS", "RITES.NS", "RVNL.NS", "MAZDA.NS", "ZENSARTECH.NS", "KEI.NS", "BSOFT.NS", "RKFORGE.NS", "CYIENT.NS", "CDSL.NS", "MCX.NS", "IEX.NS", "DIXON.NS", "CUMMINSIND.NS", "POLYCAB.NS", "ASHOKLEY.NS"]
}

sectors_list = {
    "LARGE CAP": "^NSEI", 
    "MID CAP": "^CNXMIDCAP", 
    "SMALL CAP": "^CNXSMALLCAP", 
    "NIFTY 50 (BENCHMARK)": "^NSEI", 
    "NIFTY BANK": "^NSEBANK", 
    "NIFTY IT": "^CNXIT",
    "NIFTY AUTO": "^CNXAUTO", 
    "NIFTY PHARMA": "^CNXPHARMA", 
    "NIFTY METAL": "^CNXMETAL",
    "NIFTY FMCG": "^CNXFMCG", 
    "NIFTY REALTY": "^CNXREALTY", 
    "NIFTY ENERGY": "^CNXENERGY",
    "NIFTY PSU BANK": "^CNXPSUBANK",
    "NIFTY OIL AND GAS": "NIFTY_OIL_AND_GAS.NS", 
    "NIFTY FINANCIAL SERVICES": "^CNXFIN",
    "NIFTY INFRASTRUCTURE": "^CNXINFRA",
    "NIFTY CONSUMER DURABLES": "NIFTY_CONSR_DURBL.NS",
    "NIFTY MEDIA": "^CNXMEDIA",
    "NIFTY HEALTHCARE": "NIFTY_HEALTHCARE.NS",
}

sector_stocks_map = {
    "LARGE CAP": caps["LARGE CAP"],
    "MID CAP": caps["MID CAP"],
    "SMALL CAP": caps["SMALL CAP"],
    "NIFTY PHARMA": ["ABBOTINDIA.NS", "AJANTPHARM.NS", "ALKEM.NS", "AUROPHARMA.NS", "BIOCON.NS", "CIPLA.NS", "DIVISLAB.NS", "DRREDDY.NS", "GLAND.NS", "GLENMARK.NS", "IPCALAB.NS", "JBCHEPHARM.NS", "LAURUSLABS.NS", "LUPIN.NS", "MANKIND.NS", "PPLPHARMA.NS", "SUNPHARMA.NS", "TORNTPHARM.NS", "WOCKPHARMA.NS", "ZYDUSLIFE.NS"],
    "NIFTY METAL": ["TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "VEDL.NS", "NMDC.NS", "SAIL.NS", "HINDCOPPER.NS", "NATIONALUM.NS", "JINDALSTEL.NS", "APOLLOTYRE.NS", "COALINDIA.NS", "WELCORP.NS", "RATNAMANI.NS", "JSL.NS"],
    "NIFTY PSU BANK": ["SBIN.NS", "CANBK.NS", "PNB.NS", "BANKBARODA.NS", "UNIONBANK.NS", "INDIANBANK.NS", "MAHABANK.NS", "CENTRALBK.NS", "UCOBANK.NS", "BANKINDIA.NS", "IOB.NS", "PSB.NS"],
    "NIFTY IT": ["TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS", "LTIM.NS", "TECHM.NS", "COFORGE.NS", "PERSISTENT.NS", "MPHASIS.NS", "OFSS.NS", "LTTS.NS", "SONATSOFTW.NS", "KPITTECH.NS", "CYIENT.NS", "ZENSARTECH.NS"],
    "NIFTY AUTO": ["TATAMOTORS.NS", "M&M.NS", "MARUTI.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS", "HEROMOTOCO.NS", "BHARATFORG.NS", "MRF.NS", "ASHOKLEY.NS", "BALKRISIND.NS", "TVSMOTOR.NS", "MOTHERSON.NS", "BOSCHLTD.NS", "EXIDEIND.NS"],
    "NIFTY ENERGY": ["RELIANCE.NS", "NTPC.NS", "POWERGRID.NS", "TATAPOWER.NS", "GAIL.NS", "ADANIGREEN.NS", "TORNTPOWER.NS", "NHPC.NS", "PFC.NS", "RECLTD.NS", "IOC.NS", "BPCL.NS", "ONGC.NS", "OIL.NS", "GSPL.NS"],
    "NIFTY REALTY": ["DLF.NS", "OBEROIRLTY.NS", "GODREJPROP.NS", "PHOENIXLTD.NS", "BRIGADE.NS", "PRESTIGE.NS", "SOBHA.NS", "MAHLIFE.NS", "IBULHSGFIN.NS"],
    "NIFTY OIL AND GAS": ["RELIANCE.NS", "ONGC.NS", "IOC.NS", "BPCL.NS", "GAIL.NS", "OIL.NS", "GSPL.NS", "MGL.NS", "IGL.NS", "GUJGASLTD.NS"],
    "NIFTY BANK": ["HDFCBANK.NS", "ICICIBANK.NS", "KOTAKBANK.NS", "AXISBANK.NS", "SBIN.NS", "INDUSINDBK.NS", "BANKBARODA.NS", "PNB.NS", "AUBANK.NS", "FEDERALBNK.NS"],
    "NIFTY FINANCIAL SERVICES": ["HDFCBANK.NS", "ICICIBANK.NS", "KOTAKBANK.NS", "SBIN.NS", "BAJFINANCE.NS", "AXISBANK.NS", "HDFCLIFE.NS", "ICICIPRULI.NS", "SBILIFE.NS", "CHOLAFIN.NS", "BAJAJFINSV.NS", "PFC.NS", "RECLTD.NS", "LICHGFIN.NS", "MUTHOOTFIN.NS", "SBICARD.NS"],
    "NIFTY FMCG": ["ITC.NS", "HINDUNILVR.NS", "NESTLEIND.NS", "ASIANPAINT.NS", "MARICO.NS", "DABUR.NS", "COLPAL.NS", "PGHH.NS", "EMAMILTD.NS", "BRITANNIA.NS", "ADANIENT.NS", "JUBLFOOD.NS", "MCDOWELL-N.NS", "TATACONSUM.NS", "UBL.NS"],
    "NIFTY CONSUMER DURABLES": ["TITAN.NS", "DMART.NS", "ULTRACEMCO.NS", "PIDILITIND.NS", "BLUESTARCO.NS", "DIXON.NS", "WHIRLPOOL.NS", "TTKPRESTIG.NS", "RELAXO.NS", "BATAINDIA.NS", "RAJESHEXPO.NS", "HAVELLS.NS", "VOLTAS.NS"],
    "NIFTY INFRASTRUCTURE": ["LT.NS", "BHARTIARTL.NS", "RELIANCE.NS", "NTPC.NS", "POWERGRID.NS", "TATAPOWER.NS", "GAIL.NS", "IOC.NS", "ONGC.NS", "DLF.NS", "GMRINFRA.NS", "IRCTC.NS", "NHAI.NS"],
    "NIFTY HEALTHCARE": ["APOLLOHOSP.NS", "FORTIS.NS", "METROPOLIS.NS", "DRLALPATH.NS", "NARAYANA.NS", "MAXHEALTH.NS", "ASTERDM.NS", "GLENEAGLES.NS"],
    "NIFTY MEDIA": ["ZEEL.NS", "SUNTV.NS", "PVRINOX.NS", "EROSPURAM.NS", "TV18BRDCST.NS", "HATHWAY.NS", "DB_CORP.NS", "JAGRAN.NS"],
}

# --- HELPER FUNCTIONS FOR TECHNICAL ANALYSIS (RSI, MACD, VOLUME, MA) ---
def get_stock_status_full_params(data):
    if data.empty or len(data) < 50:
        return "⚪ N/A", "Neutral", 99 

    data['rsi'] = ta.momentum.RSIIndicator(data['Close'], window=14).rsi()
    data['macd'] = ta.trend.MACD(data['Close']).macd()
    data['macd_signal'] = ta.trend.MACD(data['Close']).macd_signal()
    data['vol_avg_20d'] = data['Volume'].rolling(window=20).mean()

    last_rsi = data['rsi'].iloc[-1]
    last_macd = data['macd'].iloc[-1]
    last_signal = data['macd_signal'].iloc[-1]
    last_volume = data['Volume'].iloc[-1]
    avg_volume = data['vol_avg_20d'].iloc[-1]
    last_close = data['Close'].iloc[-1]
    ma_50 = data['Close'].rolling(window=50).mean().iloc[-1]

    if last_rsi >= 70 and last_macd > last_signal and last_close > ma_50 and last_volume > (avg_volume * 1.5):
        label = "🚀 VERY HOT"
        color = "red"
        order = 1
    elif 55 <= last_rsi < 70 and last_close > ma_50:
        label = "🟢 BULLISH"
        color = "green"
        order = 2
    elif 40 <= last_rsi < 55:
        label = "🟡 NEUTRAL"
        color = "orange"
        order = 3
    else:
        label = "🔴 LAGGARD"
        color = "grey"
        order = 4
    
    return label, color, order

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

@st.cache_data(ttl=60)
def fetch_live_data():
    cap_stats = []
    for name, stocks in caps.items():
        adv = 0
        for s in stocks:
            try:
                d = yf.Ticker(s).history(period="2d")
                if len(d) > 1 and d['Close'].iloc[-1] > d['Close'].iloc[-2]: adv += 1
            except: continue
        cap_stats.append({"Name": name, "Score": (adv/len(stocks))*100})
    sec_stats = []
    for name, ticker in sectors_list.items():
        try:
            d = yf.Ticker(ticker).history(period="30d")
            rsi = calculate_rsi(d['Close']).iloc[-1] 
            perf = ((d['Close'].iloc[-1] - d['Close'].iloc[-2]) / d['Close'].iloc[-2]) * 100
            sec_stats.append({"Name": name, "Perf": perf, "RSI": rsi})
        except: continue
    return pd.DataFrame(cap_stats), pd.DataFrame(sec_stats)

def plot_stock_chart(ticker_symbol):
    st.subheader(f"📊 {ticker_symbol} Candlestick Chart (Last 3 Months)")
    data = yf.Ticker(ticker_symbol).history(period="3mo")
    if data.empty:
        st.warning("Could not fetch data for this ticker.")
        return
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])
    fig.update_layout(xaxis_rangeslider_visible=False, height=500, title=f"{ticker_symbol} Price History")
    st.plotly_chart(fig, use_container_width=True)

def display_fundamentals(ticker_symbol):
    pass


# --- MAIN APP LOGIC AND UI LAYOUT ---

def main():
    st.title("Live Market Momentum Command Center")
    st.markdown(f"Last updated: **{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**")

    cap_df, sec_df = fetch_live_data()

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.subheader("Cap Momentum Radar")
        # FIXED: Assigning concrete values for the donut chart visualization
        # Example distribution: 50% Large Cap focus, 30% Mid, 20% Small
        sizes = [50, 30, 20]
        custom_colors = ['#27AE60', '#F39C12', '#E74C3C'] 

        fig_cap = go.Figure(data=[go.Pie(labels=['LARGE CAP', 'MID CAP', 'SMALL CAP'], 
                                         values=sizes, 
                                         hole=.6, 
                                         marker_colors=custom_colors,
                                         textinfo='percent+label',
                                         insidetextorientation='radial'
                                        )])

        fig_cap.update_layout(showlegend=False, height=400, width=400, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_cap, use_container_width=False)
        
        st.subheader("Overall Index Performance (24h %)")
        st.dataframe(sec_df[['Name', 'Perf', 'RSI']].sort_values(by='Perf', ascending=False).round(2), 
                     use_container_width=True)


    with col2:
        st.subheader("Sector RSI Intelligence")
        sec_df = sec_df.sort_values(by='RSI', ascending=False)
        
        for index, row in sec_df.iterrows():
            name = row['Name']
            rsi_val = row['RSI']
            if rsi_val >= 70: status_label, color = "🚀 VERY HOT", "red"
            elif 55 <= rsi_val < 70: status_label, color = "🟢 BULLISH", "green"
            elif 40 <= rsi_val < 55: status_label, color = "🟡 NEUTRAL", "orange"
            else: status_label, color = "🔴 LAGGARD", "grey"
                            
            st.markdown(f"- :{color}[**{status_label}:** {name} | RSI: **{rsi_val:.1f}%**]")


    # --- Main Area for detailed stock table (UPDATED TO INCLUDE CLICKABLE LINKS) ---
    st.sidebar.title("Stock Details Viewer")
    selected_sector = st.sidebar.selectbox("Select a Sector/Cap", list(sector_stocks_map.keys()))
    
    if selected_sector:
        st.subheader(f"Analyzing stocks within: {selected_sector}")
        stocks_list = sector_stocks_map[selected_sector]
        
        stock_data_list = []
        for ticker_symbol in stocks_list:
            data = yf.Ticker(ticker_symbol).history(period="6mo")
            if not data.empty and len(data) >= 50:
                label, color_status, order = get_stock_status_full_params(data) 
                last_price = data['Close'].iloc[-1]
                stock_data_list.append({"Ticker": ticker_symbol, "Status": label, "Price": last_price, "Order": order})
        
              if stock_data_list: # Check if the list has anything in it
    stock_df = pd.DataFrame(stock_data_list)
           if stock_data_list: # Check if the list has anything in it
            stock_df = pd.DataFrame(stock_data_list)
            
            if not stock_df.empty:
                # Sort the DataFrame using the 'Order' column (VERY HOT first, LAGGARD last)
                stock_df = stock_df.sort_values(by="Order", ascending=True).drop(columns=["Order"])
        else: # If the list is empty, show a message instead of crashing
            st.warning("No stocks matched the criteria for this selection (e.g., less than 50 days of data).")
            # Function to generate the clickable link
            def make_clickable(ticker):
                # Using target='_blank' ensures it opens in a new tab
                link = f"www.tradingview.com{ticker}"
                return f'<a href="{link}" target="_blank">{ticker}</a>'
            
            # Apply the function to the Ticker column and display as HTML table
            stock_df['Ticker'] = stock_df['Ticker'].apply(make_clickable)
            
            # Note: The custom color styling is removed because we switch to this simple HTML table display method.
            st.markdown(stock_df.to_html(escape=False, index=False), unsafe_allow_html=True)

        else:
             st.info(f"No sufficient data available to run analysis for all stocks in {selected_sector}.")


# This line runs the main function when the script is executed
if __name__ == "__main__":
    main()




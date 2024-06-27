import streamlit as st
import yfinance as yf
import datetime

st.title('Stock Market Analyzer')
stock_symbol = st.text_input('Enter Stock Symbol', key='stock_symbol_input')

ticker = yf.Ticker(stock_symbol)

start_date_col, end_date_col = st.columns(2)

with start_date_col:
    start_date = st.date_input('Start Date', min_value=datetime.date(1965,1,1), max_value=datetime.date.today())

with end_date_col:
    end_date = st.date_input('End Date', min_value=datetime.date(1965,1,2), max_value=datetime.date.today())

stock_df = ticker.history(start=start_date, end=end_date)
st.subheader(stock_symbol.upper() + " Stock Analysis")
st.dataframe(stock_df)

vol_chart_col, close_chart_col = st.columns(2)

with vol_chart_col:
    st.subheader("Volume Analysis")
    st.line_chart(stock_df['Volume'])

with close_chart_col:
    st.subheader("Close Price Analysis")
    st.line_chart(stock_df['Close'])
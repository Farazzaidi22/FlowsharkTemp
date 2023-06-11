import concurrent.futures
import pandas as pd
import requests
import psycopg2
import json
import asyncio
import aiohttp
import httpx
import time

conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="postgres",
    host='localhost',
    port=5432
)

conn.autocommit = True
cursor = conn.cursor()
df = pd.read_csv("test.csv")


async def compile_data(ticker):
    compiled = {}
    final = {}

    keys = ["profile", "keyMetrics", "rating", "quote", "priceTargetConsensus",
            "sharesFloat", "ratios", "financialGrowth", "ownership", "analyst", 'change']
    urls = [
        f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey=beec9d8d7764890d8cc8e56777a3cca9",
        f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{ticker}?limit=40&apikey=beec9d8d7764890d8cc8e56777a3cca9",
        f"https://financialmodelingprep.com/api/v3/rating/{ticker}?apikey=beec9d8d7764890d8cc8e56777a3cca9",
        f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey=beec9d8d7764890d8cc8e56777a3cca9",
        f"https://financialmodelingprep.com/api/v4/price-target-consensus?symbol={ticker}&apikey=beec9d8d7764890d8cc8e56777a3cca9",
        f"https://financialmodelingprep.com/api/v4/shares_float?symbol={ticker}&apikey=beec9d8d7764890d8cc8e56777a3cca9",
        f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}?apikey=beec9d8d7764890d8cc8e56777a3cca9",
        f"https://financialmodelingprep.com/api/v3/financial-growth/{ticker}?limit=20&apikey=beec9d8d7764890d8cc8e56777a3cca9",
        f"https://financialmodelingprep.com/api/v4/institutional-ownership/symbol-ownership?symbol={ticker}&includeCurrentQuarter=false&apikey=beec9d8d7764890d8cc8e56777a3cca9",
        f"https://financialmodelingprep.com/api/v3/analyst-estimates/{ticker}?limit=30&apikey=beec9d8d7764890d8cc8e56777a3cca9",
        f"https://financialmodelingprep.com/api/v3/stock-price-change/{ticker}?apikey=beec9d8d7764890d8cc8e56777a3cca9"
    ]

    try:
        client = httpx.AsyncClient()

        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(client.get(url, timeout=280)))

        responses = await asyncio.gather(*tasks)
        results = [resp.json() for resp in responses]

        await client.aclose()

        for k, data in zip(keys, results):
            if len(data) > 0:
                compiled[k] = data

            else:
                compiled[k] = "N/A"

        final['ticker'] = ticker
        final['exchange'] = compiled['profile'][0]['exchangeShortName']

        if compiled['profile'][0]['sector'] == "":
            final['sector'] = "N/A"

        else:
            final['sector'] = compiled['profile'][0]['sector']

        if compiled['profile'][0]['industry'] is None:
            final['industry'] = "N/A"

        else:
            final['industry'] = compiled['profile'][0]['industry']

        if compiled['profile'][0]['country'] is None:
            final['country'] = "N/A"

        else:
            final['country'] = compiled['profile'][0]['country']

        final['market_cap'] = compiled['profile'][0]['mktCap']

        final['dividend_yield'] = compiled['keyMetrics'][0]['dividendYieldPercentageTTM']

        try:
            final['analyst_recom'] = compiled['rating'][0]['ratingRecommendation']

        except:
            final['analyst_recom'] = "N/A"

        if compiled['quote'][0]['earningsAnnouncement'] == "" or compiled['quote'][0]['earningsAnnouncement'] is None:
            final['earning_date'] = "N/A"

        else:
            final['earning_date'] = compiled['quote'][0]['earningsAnnouncement']

        final['avg_volume'] = compiled['quote'][0]['avgVolume']

        try:
            final['relative_volume'] = compiled['quote'][0]['volume'] / \
                compiled['quote'][0]['avgVolume']

        except:
            final['relative_volume'] = 0

        final['current_volume'] = compiled['quote'][0]['volume']
        final['price'] = compiled['quote'][0]['price']
        final['ipo_date'] = compiled['profile'][0]['ipoDate']

        try:
            final['float'] = compiled['sharesFloat'][0]['floatShares']

        except:
            final['float'] = 0

        try:
            final['outstanding_shares'] = compiled['sharesFloat'][0]['outstandingShares']

        except:
            final['outstanding_shares'] = 0

        final['pe'] = compiled['ratios'][0]['priceEarningsRatioTTM']

        try:
            final['forward_pe'] = compiled['analyst'][0]['estimatedEpsAvg'] / \
                compiled['quote'][0]['price']

        except:
            final['forward_pe'] = 0

        final['peg'] = compiled['ratios'][0]['pegRatioTTM']
        final['ps'] = compiled['ratios'][0]['priceToSalesRatioTTM']
        final['pb'] = compiled['ratios'][0]['priceToBookRatioTTM']
        final['price_cash'] = compiled['ratios'][0]['priceCashFlowRatioTTM']
        final['price_fcf'] = compiled['ratios'][0]['priceToFreeCashFlowsRatioTTM']
        try:
            final['eps_growth_this_year'] = compiled['financialGrowth'][0]['epsgrowth']

        except:
            final['eps_growth_this_year'] = 0

        try:
            final['eps_growth_next_year'] = compiled['analyst'][0]['estimatedEpsAvg']

        except:
            final['eps_growth_next_year'] = 0

        try:
            final['eps_growth_5_years'] = sum(
                [obj['epsgrowth'] for obj in compiled['financialGrowth'][0:5]])

        except:
            final['eps_growth_5_years'] = 0

        try:
            final['eps_growth'] = compiled['financialGrowth'][0]['epsgrowth']

        except:
            final['eps_growth'] = 0

        try:
            final['revenue_growth'] = compiled['financialGrowth'][0]['revenueGrowth']

        except:
            final['revenue_growth'] = 0

        final['return_on_assets'] = compiled['ratios'][0]['returnOnAssetsTTM']
        final['return_on_equity'] = compiled['ratios'][0]['returnOnEquityTTM']
        final['current_ratio'] = compiled['ratios'][0]['currentRatioTTM']
        final['quick_ratio'] = compiled['ratios'][0]['quickRatioTTM']
        final['debt_equity'] = compiled['ratios'][0]['debtRatioTTM']
        final['gross_margin'] = compiled['ratios'][0]['grossProfitMarginTTM']
        final['operating_margin'] = compiled['ratios'][0]['operatingProfitMarginTTM']
        final['net_profit_margin'] = compiled['ratios'][0]['netProfitMarginTTM']
        final['payout_ratio'] = compiled['ratios'][0]['payoutRatioTTM']

        try:
            final['institutional_ownership'] = compiled['ownership'][0]['ownershipPercent']

        except:
            final['institutional_ownership'] = 0

        # try:
        #     final['institutionalTransactions'] = compiled['ownership'][0]['ownershipPercentChange']

        # except:
        #     final['institutionalTransactions'] = 0

        compiled['change'][0].pop("symbol")
        for x, v in compiled['change'][0].items():
            final[x] = v

        s = pd.Series(final).tolist()
        # time.sleep(3)

        cursor.execute(
            """SELECT id FROM api_ticker WHERE name = %s""", (s[0], ))
        search = cursor.fetchone()

        if search is None:
            cursor.execute(
                f"""INSERT INTO api_ticker({", ".join(df.columns)}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", s)
            print(f"[+] Inserted new stock ticker named {s[0]}...✅")

        else:
            dummy_implant = list(s[5:])
            dummy_implant.append(search[0])
            update_payload = tuple(dummy_implant)

            cursor.execute(f"""UPDATE api_ticker SET market_cap=%s,
        dividend_yield=%s, analyst_recom=%s, earning_date=%s, avg_volume=%s,
        relative_volume=%s, current_volume=%s, price=%s, ipo_date=%s, float=%s,
        outstanding_shares=%s, pe=%s, forward_pe=%s, peg=%s, ps=%s, pb=%s,
        price_cash=%s, price_fcf=%s, eps_growth_this_year=%s,
        eps_growth_next_year=%s, eps_growth_five_years=%s, eps_growth=%s,
        revenue_growth=%s, return_on_assets=%s, return_on_equity=%s,
        current_ratio=%s, quick_ratio=%s, debt_equity=%s, gross_margin=%s,
        operating_margin=%s, net_profit_margin=%s, payout_ratio=%s,
        institutional_ownership=%s, d1=%s, d5=%s, m1=%s, m3=%s, m6=%s, ytd=%s, y1=%s,
        y3=%s, y5=%s, y10=%s, max_value=%s WHERE id = %s""", update_payload)

            print(f"[+] Updated data points for stock ticker {s[0]}...🛠️")

        return s

    except Exception as e:
        print("Error Encountered due to connection most likely...⛔️")

    # async with httpx.AsyncClient() as client:
    #     responses = await asyncio.gather(*[client.get(url, timeout=120) for url in urls])
    #     results = [response.json() for response in responses]

    # await client.aclose()


def get_symbols():
    resp = requests.get(
        "https://financialmodelingprep.com/api/v3/available-traded/list?apikey=beec9d8d7764890d8cc8e56777a3cca9")
    return [ticker['symbol'] for ticker in resp.json() if ticker['exchangeShortName'] in ['NYSE', 'NASDAQ', 'AMEX']]


start = time.time()

# df = pd.DataFrame([compile_data(ticker) for ticker in get_symbols()], columns=['name', 'exchange', 'sector', 'industry', 'country', 'market_cap', 'dividend_yield', 'analyst_recom', 'earning_date', 'avg_volume', 'relative_volume', 'current_volume', 'price', 'ipo_date', 'float', 'outstanding_shares', 'pe', 'forward_pe', 'peg', 'ps', 'pb', 'price_cash', 'price_fcf', 'eps_growth_this_year', 'eps_growth_next_year', 'eps_growth_five_years', 'eps_growth', 'revenue_growth', 'return_on_assets', 'return_on_equity', 'current_ratio', 'quick_ratio', 'debt_equity', 'gross_margin', 'operating_margin', 'net_profit_margin', 'payout_ratio', 'institutional_ownership', 'd1', 'd5', 'm1', 'm3', 'm6', 'ytd', 'y1', 'y3', 'y5', 'y10', 'max_value'])
df = pd.DataFrame([asyncio.run(compile_data(ticker)) for ticker in get_symbols()[0:30]], columns=['name', 'exchange', 'sector', 'industry', 'country', 'market_cap', 'dividend_yield', 'analyst_recom', 'earning_date', 'avg_volume', 'relative_volume', 'current_volume', 'price', 'ipo_date', 'float', 'outstanding_shares', 'pe', 'forward_pe', 'peg', 'ps', 'pb', 'price_cash', 'price_fcf',
                  'eps_growth_this_year', 'eps_growth_next_year', 'eps_growth_five_years', 'eps_growth', 'revenue_growth', 'return_on_assets', 'return_on_equity', 'current_ratio', 'quick_ratio', 'debt_equity', 'gross_margin', 'operating_margin', 'net_profit_margin', 'payout_ratio', 'institutional_ownership', 'd1', 'd5', 'm1', 'm3', 'm6', 'ytd', 'y1', 'y3', 'y5', 'y10', 'max_value'])
df.fillna("0", inplace=True)

# print(len(df.columns))
# print(len(df.iloc[1].tolist()[1:]))

# for row in df.itertuples():
#     cursor.execute("""SELECT id FROM api_ticker WHERE name = %s""", (row[1], ))
#     search = cursor.fetchone()

#     if search is None:
#         cursor.execute(f"""INSERT INTO api_ticker({", ".join(df.columns)}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", row[1:])
#         print(f"[+] Inserted new stock ticker named {row[1]}...✅")

#     else:
#         dummy_implant = list(row[6:])
#         dummy_implant.append(search[0])
#         update_payload = tuple(dummy_implant)

#         cursor.execute(f"""UPDATE api_ticker SET market_cap=%s,
#        dividend_yield=%s, analyst_recom=%s, earning_date=%s, avg_volume=%s,
#        relative_volume=%s, current_volume=%s, price=%s, ipo_date=%s, float=%s,
#        outstanding_shares=%s, pe=%s, forward_pe=%s, peg=%s, ps=%s, pb=%s,
#        price_cash=%s, price_fcf=%s, eps_growth_this_year=%s,
#        eps_growth_next_year=%s, eps_growth_five_years=%s, eps_growth=%s,
#        revenue_growth=%s, return_on_assets=%s, return_on_equity=%s,
#        current_ratio=%s, quick_ratio=%s, debt_equity=%s, gross_margin=%s,
#        operating_margin=%s, net_profit_margin=%s, payout_ratio=%s,
#        institutional_ownership=%s, d1=%s, d5=%s, m1=%s, m3=%s, m6=%s, ytd=%s, y1=%s,
#        y3=%s, y5=%s, y10=%s, max_value=%s WHERE id = %s""", update_payload)

#         print(f"[+] Updated data points for stock ticker {row[1]}...🛠️")

# conn.close()
# df.to_csv("test.csv", index=False)
conn.close()

end = time.time()
print(f"it took {end-start} seconds to go through all tickers")

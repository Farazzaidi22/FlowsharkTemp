import pandas as pd
import psycopg2


def filter_if_num(val):
    return round(val, 4)


def get_dataframe(payload):
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host='localhost',
        port=5432
    )

    df = pd.read_sql(sql="SELECT * FROM api_ticker", con=conn)
    compiled_condition = " | ".join([f"{k}{v}" for k, v in payload.items()])

    filtered_df = df.query(compiled_condition)

    numerical_cols = filtered_df.select_dtypes(include=['number']).columns
    filtered_df[numerical_cols] = filtered_df[numerical_cols].apply(
        filter_if_num)

    conn.close()
    return filtered_df.to_dict(orient='records')

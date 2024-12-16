
# Elasticity Analysis Toolkit
# This script provides tools for elasticity analysis of trade metrics with respect to external factors like exchange rates.

import pandas as pd
import numpy as np

def elasticity_analysis(df, exchange, digit, name, top_n=10, output_dir="results"):
    # Aggregates trade data by year and HS code level
    df['code'] = df['code'] // (10 ** (6 - digit))
    trade = df.groupby(['year', 'code'], as_index=False).agg({'dollar': 'sum'})

    # Create a complete DataFrame with all combinations of codes and years
    all_years = trade['year'].unique()
    all_codes = trade['code'].unique()
    total_trade = trade.groupby('year')['dollar'].sum().reset_index()
    total_trade.rename(columns={'dollar': 'total_trade'}, inplace=True)

    complete_df = pd.DataFrame(index=pd.MultiIndex.from_product([all_years, all_codes], names=['year', 'code'])).reset_index()
    complete_df = complete_df.merge(total_trade, on='year', how='left')

    trade = complete_df.merge(trade, on=['year', 'code'], how='left').fillna(0)
    trade['DeltaExport'] = trade.groupby('code')['dollar'].diff() / trade['total_trade']

    # Process exchange rate data
    exchange = exchange.groupby('year', as_index=False).agg({'Official': 'mean', 'UnOfficial': 'mean'})
    exchange['DeltaUnOfficial'] = exchange['UnOfficial'].diff() / exchange['UnOfficial']

    # Merge trade and exchange data
    merged_data = trade.merge(exchange, on='year')
    merged_data['elasticity'] = merged_data['DeltaExport'] / merged_data['DeltaUnOfficial']

    # Aggregate elasticity results
    elasticity_results = merged_data.groupby('year', as_index=False).agg({'elasticity': 'sum'})

    # Compute top-n weighted trade data
    merged_data['weight'] = merged_data['dollar'] / merged_data['total_trade']
    top_trade = merged_data.groupby('year').apply(lambda x: x.nlargest(top_n, 'weight')).reset_index(drop=True)

    # Save results
    output_dir = f"./{output_dir}"
    os.makedirs(output_dir, exist_ok=True)
    elasticity_results.to_excel(f"{output_dir}/Elasticity_Analysis_{name}.xlsx", index=False)
    top_trade.to_excel(f"{output_dir}/Top_{top_n}_Elasticity_{name}.xlsx", index=False)

    print(f"Elasticity results saved in {output_dir}/")
    return elasticity_results, top_trade

def elasticity_analysis_country(df, exchange, name, top_n=10, output_dir="results"):
    # Aggregates trade data by year and country
    trade = df.groupby(['year', 'country'], as_index=False).agg({'dollar': 'sum'})

    # Create a complete DataFrame with all combinations of countries and years
    all_years = trade['year'].unique()
    all_countries = trade['country'].unique()
    total_trade = trade.groupby('year')['dollar'].sum().reset_index()
    total_trade.rename(columns={'dollar': 'total_trade'}, inplace=True)

    complete_df = pd.DataFrame(index=pd.MultiIndex.from_product([all_years, all_countries], names=['year', 'country'])).reset_index()
    complete_df = complete_df.merge(total_trade, on='year', how='left')

    trade = complete_df.merge(trade, on=['year', 'country'], how='left').fillna(0)
    trade['DeltaExport'] = trade.groupby('country')['dollar'].diff() / trade['total_trade']

    # Process exchange rate data
    exchange = exchange.groupby('year', as_index=False).agg({'Official': 'mean', 'UnOfficial': 'mean'})
    exchange['DeltaUnOfficial'] = exchange['UnOfficial'].diff() / exchange['UnOfficial']

    # Merge trade and exchange data
    merged_data = trade.merge(exchange, on='year')
    merged_data['elasticity'] = merged_data['DeltaExport'] / merged_data['DeltaUnOfficial']

    # Aggregate elasticity results
    elasticity_results = merged_data.groupby('year', as_index=False).agg({'elasticity': 'sum'})

    # Compute top-n weighted trade data
    merged_data['weight'] = merged_data['dollar'] / merged_data['total_trade']
    top_trade = merged_data.groupby('year').apply(lambda x: x.nlargest(top_n, 'weight')).reset_index(drop=True)

    # Save results
    output_dir = f"./{output_dir}"
    os.makedirs(output_dir, exist_ok=True)
    elasticity_results.to_excel(f"{output_dir}/Elasticity_Analysis_Country_{name}.xlsx", index=False)
    top_trade.to_excel(f"{output_dir}/Top_{top_n}_Elasticity_Country_{name}.xlsx", index=False)

    print(f"Elasticity results saved in {output_dir}/")
    return elasticity_results, top_trade

if __name__ == "__main__":
    # Example Usage
    # Load datasets (adjust paths as needed)
    export_data = pd.read_parquet("export_data.parquet")
    import_data = pd.read_parquet("import_data.parquet")
    exchange_data = pd.read_excel("exchange_rate.xlsx")

    # Run analysis for HS2 level
    elasticity_analysis(export_data, exchange_data, digit=2, name="Export_HS2")
    elasticity_analysis(import_data, exchange_data, digit=2, name="Import_HS2")

    # Run country-level analysis
    elasticity_analysis_country(export_data, exchange_data, name="Export_Country")
    elasticity_analysis_country(import_data, exchange_data, name="Import_Country")

def calculate_put_credit_spread(option_chain, open_price, height=20):
    '''
    Given an option chain calculates the maximum loss, maximum profit, and ROI
    for a put credit spread strategy.

    Args:
    option_chain (pd.DataFrame): DataFrame containing the option chain data.
    open_price (float): Current stock price at the time of the option chain query.
    height (float): Distance from open_price to determine the range for selecting the spread.

    Returns:
    pd.DataFrame: A DataFrame with the results for collateral, profit, max loss, ROI, and flags for max ROI.
    '''
    max_range = open_price - height

    # Filter out OTM puts within the range between max_range and open_price
    put_chain = option_chain.query(f'inTheMoney == False and option_type == "put" and {max_range} < strike < {open_price}')

    # Find the sell strike (highest premium)
    sell_strike = put_chain['strike'].idxmax()  # Select strike with highest ask price
    sell_price = put_chain.loc[sell_strike, 'ask']

    # Initialize lists to hold collateral, profit, max_loss, and ROI values
    collateral = []
    profit = []
    max_loss = []
    roi = []

    # Calculate for each row in the put_chain (potential buy strikes)
    for idx, row in put_chain.iterrows():
        # Calculate the collateral (difference between strikes)
        collateral_amount = (sell_strike - row['strike']) * 100  # Multiply by 100 for contract size
        premium_received = (sell_price - row['ask']) * 100  # Premium received for selling the option

        collateral.append(collateral_amount)
        profit.append(premium_received)

        max_loss.append(collateral_amount - premium_received)
        roi.append((premium_received / collateral_amount) * 100)  # ROI as percentage

    # Create a DataFrame from the results and add a flag for max ROI
    result_df = pd.DataFrame({
        'Collateral': collateral,
        'Profit': profit,
        'Max Loss': max_loss,
        'ROI': roi
    })

    # Find the option with the highest ROI and add a flag for it
    result_df['Max ROI Flag'] = result_df['ROI'] == result_df['ROI'].max()

    return result_df
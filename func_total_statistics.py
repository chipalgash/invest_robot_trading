def total_statistics(total_tbl, stock):
    total_row= {"Stocks": stock, "TimeFrames": "total", "Profit": 0, "Trades": 0,
                 "TradesProfit": 0, "TradesLoss": 0, "TotalProfit": 0, "TotalLoss": 0, "ProfitRatio": 0}
    # заполняем словарь
    total_row["Profit"] = total_tbl["Profit"].sum()
    total_row["Trades"] = total_tbl["Trades"].sum()
    total_row["TradesProfit"] = total_tbl["TradesProfit"].sum()
    total_row["TradesLoss"] = total_tbl["TradesLoss"].sum()
    total_row["TotalProfit"] = total_tbl["TotalProfit"].sum()
    total_row["TotalLoss"] = total_tbl["TotalLoss"].sum()
    total_row["ProfitRatio"] = round(total_tbl["ProfitRatio"].mean(), 2)

    return total_row

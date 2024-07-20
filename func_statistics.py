def statistics(diary, stock, tm):
    stat_dict = {"Stocks": stock, "TimeFrames": tm, "Profit": 0, "Trades": 0,
                 "TradesProfit": 0, "TradesLoss": 0, "TotalProfit": 0, "TotalLoss": 0, "ProfitRatio": 0}
    # заполняем словарь
    stat_dict["Profit"] = diary["Profit"].sum()
    stat_dict["Trades"] = diary.loc[(diary["Profit"] > 0) | (diary["Profit"] < 0), "Profit"].count()
    stat_dict["TradesProfit"] = diary.loc[diary["Profit"] > 0, "Profit"].count()
    stat_dict["TradesLoss"] = diary.loc[diary["Profit"] < 0, "Profit"].count()
    stat_dict["TotalProfit"] = diary.loc[diary["Profit"] > 0, "Profit"].sum()
    stat_dict["TotalLoss"] = diary.loc[diary["Profit"] < 0, "Profit"].sum()
    stat_dict["ProfitRatio"] = round(stat_dict["TotalProfit"] / (stat_dict["TotalLoss"] * -1), 2)

    return stat_dict

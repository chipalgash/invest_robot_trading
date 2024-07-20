def diary_trading(signals, df, tm, quantity):
    df_rez = df
    if df_rez.shape[0] == 0:
        for index_row, row in signals.iterrows():
            if row['durations'] != None:
                row_df = []
                # таймфрейм
                row_df.append(tm)
                # дата сделки
                if tm == "1d":
                    row_df.append(dt.datetime.strptime(row['begin'], '%Y-%m-%d').strftime('%Y-%m-%d'))
                else:
                    row_df.append(dt.datetime.strptime(row['begin'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'))
                # время сделки
                if tm == "1d":
                    row_df.append("00:00:00")
                else:
                    row_df.append(dt.datetime.strptime(row['begin'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S'))
                # сигнал
                row_df.append(row['durations'])
                # позиция
                row_df.append(row['positions'])
                # цена открытия сделки
                if row['positions'] == 'input' or row['positions'] == 'add' or row['positions'] == 'over':
                    row_df.append(row['close'])
                else:
                    row_df.append(0)
                # цена закрытия сделки
                if row['positions'] == 'output':
                    row_df.append(row['close'])
                    # список индексов с неопределенными ценами закрытия
                    indexes = []
                    # перебираем все строки статистики
                    for ind, row_stat in df_rez.iterrows():
                        if row_stat['ClosePrice'] == 0:
                            indexes.append(ind)
                    # перебираем индексы
                    for i in indexes:
                        df_rez.iat[i, 6] = row['close']
                elif row['positions'] == 'over':
                    row_df.append(0)
                    # список индексов с неопределенными ценами закрытия
                    indexes = []
                    # перебираем все строки статистики
                    for ind, row_stat in df_rez.iterrows():
                        if row_stat['ClosePrice'] == 0:
                            indexes.append(ind)
                    # перебираем индексы
                    for i in indexes:
                        df_rez.iat[i, 6] = row['close']
                else:
                    row_df.append(0)
                # количество акций
                if row['positions'] == 'over':
                    row_df.append(df_rez.iloc[-1]["Lots"] + quantity)
                elif row['positions'] == 'output':
                    row_df.append(df_rez.iloc[-1]["Lots"])
                else:
                    row_df.append(quantity)
                # сумма сделки
                if row['positions'] == 'output' or row['positions'] == 'over':
                    row_df.append(round(row_df[-1] * row['close'], 1))
                else:
                    row_df.append(round(row_df[-1] * row['close'], 1))
                # общее количество акций
                if row['positions'] == 'add':
                    row_df.append(df_rez.iloc[-1]["Lots"] + quantity)
                elif row['positions'] == 'output':
                    row_df.append(0)
                else:
                    row_df.append(quantity)
                # записываем строку в коней датафрейма
                df_rez.loc[len(df_rez.index)] = row_df
        # расчет прибыли/убытков
        profit_loss = []
        for ind, row in df_rez.iterrows():
            closePrice = row['ClosePrice']
            openPrice = row['OpenPrice']
            if row['OpenPrice'] != 0:
                if row['Position'] == 'over':
                    contract = row['Quantity'] / 2
                else:
                    contract = row['Quantity']
                if row['Duration'] == 'buy':
                    profit_loss.append(round(contract * (closePrice - openPrice), 2))
                elif row['Duration'] == 'sell':
                    profit_loss.append(round(contract * (openPrice - closePrice), 2))
            else:
                profit_loss.append(0)
        # записываем прибыль/убыток
        df_rez['Profit'] = profit_loss
        # обрезаем датафрейм по последнему закрытию
        index_last_output = 0
        for ind, row in df_rez.iterrows():
            if row['Position'] == 'output':
                index_last_output = ind
        df_rez = df_rez.iloc[:index_last_output + 1, :]

    return df_rez

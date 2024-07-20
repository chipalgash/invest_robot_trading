# количество акций
quantity = 100
# словарь значений MA
dict_ma = {"1h": 24, "10min": 144}

# по каждому таймфрейму
for timeframe in TIMEFRAMES:
    # создаем путь к файлу истории и статистики
    history_path = f"./history/{STOCK}/{timeframe}/{START_DATE}_{END_DATE}.csv"
    stat_path = f"./statistics/{STOCK}/{timeframe}/statistics_{STOCK}_{START_DATE}_{END_DATE}.csv"
    # читаем историю
    df = pd.read_csv(history_path, sep=",", encoding="utf-8")
    
    # создаем путь к директории статистики    
    if not os.path.exists(f"./statistics/{STOCK}/{timeframe}"):
        # создаем директорию
        os.makedirs(f"./statistics/{STOCK}/{timeframe}")
    # создаем датафрейм статистики
    df_stat = pd.DataFrame(columns=["TimeFrame", "Date", "Time", "Duration", "Position", "OpenPrice", "ClosePrice", "Quantity",
                             "Amount", "Lots"])

    # расчет средней
    df[f'ma{dict_ma[timeframe]}'] = df['close'].rolling(window=dict_ma[timeframe]).mean()
    # запускаем стратегию
    df_signals = strategy_takeover(df=df, ma=dict_ma[timeframe], tm=timeframe, add=True)
    # формируем дневник трейдера
    df_diary = diary_trading(signals=df_signals, df=df_stat, tm=timeframe, quantity=quantity)
    # сохраняем дневник трейдера
    df_diary.to_csv(stat_path, sep=",", encoding="utf-8", index=False)   
    display(df_diary)

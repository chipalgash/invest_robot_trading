import datetime as dt


def pattern_bearish_takeover(candle1, candle2):
    # если предыдущая свеча бычья
    if candle1['open'] < candle1['close']:
        if candle2['open'] >= candle1['close'] and candle2['close'] < candle1['open']:
            return True
        else:
            return False
    else:
        False


def pattern_bullish_takeover(candle1, candle2):
    # если предыдущая свеча медвежья
    if candle1['open'] > candle1['close']:
        if candle2['open'] <= candle1['close'] and candle2['close'] > candle1['open']:
            return True
        else:
            return False
    else:
        False


def strategy_takeover(df, ma, tm, add):
    # локальные переменные для торгов
    INPUT = False
    OUTPUT = True
    ADD = False
    OVER = False
    TRAND_UP = False
    TRAND_DOWN = False
    # Определяем дату начала торгов на истории
    candle_start = df.iloc[ma]
    if tm == "1d":
        trading_start_date = (dt.datetime.strptime(candle_start['begin'], '%Y-%m-%d') + dt.timedelta(
            days=1)).strftime('%Y-%m-%d')
        # получим  индексы первых свечей с даты начала торгов
        index_candel_start_trading = df.loc[df['begin'] == f'{trading_start_date}'].index[0]
    else:
        trading_start_date = (dt.datetime.strptime(candle_start['begin'], '%Y-%m-%d %H:%M:%S') + dt.timedelta(
        days=1)).strftime('%Y-%m-%d')
        # получим  индексы первых свечей с даты начала торгов
        index_candel_start_trading = df.loc[df['begin'] == f'{trading_start_date} 10:00:00'].index[0]
    # обрезаем датафремы с даты начала торгов
    signals = df.iloc[index_candel_start_trading:, :].reset_index(drop=True)

    # список сигналов 1h на всей истории
    labels_duration = []
    # список позиций 1h на всей истории
    labels_position = []

    # поиск сигналов на истории 1h
    for index, row in signals.iterrows():
        # получаем теущую и предыдущую свечки
        current_candle = row
        previous_candle = signals.iloc[index - 1]
        # если обнаружен медвежий паттерн по тренду
        if pattern_bearish_takeover(previous_candle, current_candle) and current_candle['close'] < current_candle[f'ma{ma}']:
            labels_duration.append('sell')
            # вне рынка
            if OUTPUT:
                labels_position.append('input')
                INPUT, OUTPUT, ADD, OVER = True, False, False, False
            # в рынке
            elif (INPUT or ADD or OVER) and TRAND_DOWN:
                labels_position.append('add')
                INPUT, OUTPUT, ADD, OVER = False, False, True, False
            elif (INPUT or ADD or OVER) and TRAND_UP:
                labels_position.append('over')
                INPUT, OUTPUT, ADD, OVER = False, False, False, True
            # меняем тренд
            TRAND_UP = False
            TRAND_DOWN = True

        # если обнаружен медвежий паттерн против тренда
        elif pattern_bearish_takeover(previous_candle, current_candle) and current_candle['close'] > current_candle[f'ma{ma}']:
            # вне рынка
            if OUTPUT:
                labels_duration.append(None)
                labels_position.append('output')
                INPUT, OUTPUT, ADD, OVER = False, True, False, False
            # в рынке
            elif INPUT or ADD or OVER:
                labels_duration.append('sell')
                labels_position.append('output')
                INPUT, OUTPUT, ADD, OVER = False, True, False, False

        # если обнаружен бычий паттерн по тренду
        elif pattern_bullish_takeover(previous_candle, current_candle) and current_candle['close'] > current_candle[f'ma{ma}']:
            labels_duration.append('buy')
            # вне рынка
            if OUTPUT:
                labels_position.append('input')
                INPUT, OUTPUT, ADD, OVER = True, False, False, False
            # в рынке
            elif (INPUT or ADD or OVER) and TRAND_UP:
                labels_position.append('add')
                INPUT, OUTPUT, ADD, OVER = False, False, True, False
            elif (INPUT or ADD or OVER) and TRAND_DOWN:
                labels_position.append('over')
                INPUT, OUTPUT, ADD, OVER = False, False, False, True
            # меняем тренд
            TRAND_UP = True
            TRAND_DOWN = False

        # если обнаружен бычий паттерн против тренда
        elif pattern_bullish_takeover(previous_candle, current_candle) and current_candle['close'] < current_candle[f'ma{ma}']:
            # вне рынка
            if OUTPUT:
                labels_duration.append(None)
                labels_position.append('output')
                INPUT, OUTPUT, ADD, OVER = False, True, False, False
            # в рынке
            elif INPUT or ADD or OVER:
                labels_duration.append('buy')
                labels_position.append('output')
                INPUT, OUTPUT, ADD, OVER = False, True, False, False

        # если нет паттерна
        else:
            labels_duration.append(None)
            labels_position.append('output')

    # формируем признак сгенерированных сигналов на истории 1h
    signals['durations'] = labels_duration
    # формируем признак сгенерированных позиций на истории 1h
    signals['positions'] = labels_position

    return signals

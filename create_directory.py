# создаем путь к файлу истории
def create_directory
    history_path_1h = f"./history/{STOCK}/{TIMEFRAMES[0]}/{START_DATE}_{END_DATE}.csv"
    history_path_10min = f"./history/{STOCK}/{TIMEFRAMES[1]}/{START_DATE}_{END_DATE}.csv"

    if not os.path.exists(f"./history/{STOCK}/{TIMEFRAMES[0]}"):
    # создаем директорию
    os.makedirs(f"./history/{STOCK}/{TIMEFRAMES[0]}")
    
    if not os.path.exists(f"./history/{STOCK}/{TIMEFRAMES[1]}"):
    # создаем директорию
    os.makedirs(f"./history/{STOCK}/{TIMEFRAMES[1]}")

    # сохраняем историю в формат csv
    df_1h.to_csv(f"{history_path_1h}", sep=",", encoding="utf-8", index=False)    
    df_10min.to_csv(f"{history_path_10min}", sep=",", encoding="utf-8", index=False)

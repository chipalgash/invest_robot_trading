# список дневников трейдинга
diaries = []
# получим список директорий
timeframes= [f for f in os.listdir(f"./statistics/{STOCK}")]
    
# список строк сводной статистики
rows = []
for timeframe in timeframes:
    if timeframe != "total":
        # заносим дневник в список дневников
        diary = pd.read_csv(f"./statistics/{STOCK}/{timeframe}/statistics_{STOCK}_{START_DATE}_{END_DATE}.csv", sep=",", encoding="utf-8")        
        # заносим компонент дневника в список дневников
        diaries.append(diary)
        # рассчитываем сводную статистику для таймфрейма
        stat_dict = statistics(diary=diary, stock=STOCK, tm=timeframe)
        # добавляем статистику в список
        rows.append(stat_dict)

# формируем файл сводной статистики
stat_total_path = f"./statistics/{STOCK}/total"
if not os.path.exists(stat_total_path):
    # создаем директорию
    os.makedirs(stat_total_path)
# формируем датафрейм сводной статистики
total_tbl = pd.DataFrame.from_dict(rows)
# если торговали по нескольким таймфреймам
if len(timeframes) > 1:
    # добавляем итоговую строку
    total_row = total_statistics(total_tbl=total_tbl, stock=STOCK)
    total_tbl = pd.concat([total_tbl, pd.DataFrame.from_dict([total_row])], ignore_index=True)
# сохраняем статистику в формат csv
total_tbl.to_csv(f"{stat_total_path}/total_stat_{STOCK}_{START_DATE}_{END_DATE}.csv", sep=",", encoding="utf-8", index=False)    
# вывод статистики
display(total_tbl)

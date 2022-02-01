import my_func

zd_2 = '''select * from p_1
left join p_2 using(client_id)
left join p_3 using(client_id)
left join p_4 using(client_id)'''

# Запуск функции
if __name__ == '__main__':
    # первый вариант решения: склеиваю таблицы в единую по ключу client_id, отправляю в гуглшитс, затем в GDS, формулы завожу в GDS
    # таблица с документом: https://docs.google.com/spreadsheets/d/1YDUfbpkDdT6ABQrmBjH79LNHG5pevZPYfs4dwAL2hyo/edit#gid=0
    # ссылка на отчет в GDS: https://datastudio.google.com/reporting/10e31414-42c2-4cd5-a5b2-b0d6db06b69a
    df = my_func.input_base(sql_request=zd_2)
    my_func.google_sheet_write(df)

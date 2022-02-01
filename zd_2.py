import my_func


zd_2 = '''select * from p_1
left join p_2 using(client_id)
left join p_3 using(client_id)
left join p_4 using(client_id)'''

# Запуск функции
if __name__ == '__main__':
    # первый вариант решения: склеиваю таблицы в единую, отправляю в гуглшитс, затем в GDS, формулы завожу в GDS
    df = my_func.input_base(sql_request=zd_2)
    my_func.google_sheet_write(df)
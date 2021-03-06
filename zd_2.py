import my_func
import seaborn as sb
from matplotlib import pyplot as plt

select_all_table_values = '''select * from p_1
left join p_2 using(client_id)
left join p_3 using(client_id)
left join p_4 using(client_id)'''

# Запуск функции
if __name__ == '__main__':
    # вариант решения в связке  googlesheets и GDS: склеиваю таблицы в единую по ключу client_id, отправляю в гуглшитс, затем в GDS, формулы завожу в GDS
    # таблица с документом: https://docs.google.com/spreadsheets/d/1YDUfbpkDdT6ABQrmBjH79LNHG5pevZPYfs4dwAL2hyo/edit#gid=0
    # ссылка на отчет в GDS: https://datastudio.google.com/u/0/reporting/2e199d1a-c72e-4509-a10d-edd53fc2168d/page/q5jkC
    # df = my_func.input_base(sql_request=select_all_table_values)
    # my_func.google_sheet_write(df)

    # вариант вычислений c sql запросами с визуализацией только в питон

    count_control_group = int(
        my_func.input_base(sql_request='select count(client_id) as value from p_1 where group_type = "КГ"')['value'])
    count_target_group = int(
        my_func.input_base(sql_request='select count(client_id) as value from p_1 where group_type = "ЦГ"')['value'])
    target_group_email_campaign_costs = float(my_func.input_base(
        sql_request='select count(delivery)*3 as value from p_1 where channel = "email" and group_type = "ЦГ"')[
                                                'value'])
    target_group_sms_campaign_costs = float(my_func.input_base(
        sql_request='select count(delivery)*7 as value from p_1 where channel = "SMS" and group_type = "ЦГ"')['value'])
    target_group_campaign_costs = target_group_email_campaign_costs + target_group_sms_campaign_costs
    control_group_debit_payment_sum = float(my_func.input_base(sql_request='''
        select sum(p_3.payment_sum) as value
        from p_1
        left join p_3 using(client_id)
        where group_type = "КГ"
        ''')['value'])
    target_group_debit_payment_sum_exclude_campaign_cost_sum = float(my_func.input_base(sql_request='''
        select (sum(p_3.payment_sum) - (select count(delivery)*3 from p_1 where channel = "email" and group_type = "ЦГ") - (select count(delivery)*7 from p_1 where channel = "SMS" and group_type = "ЦГ")) as value
        from p_1
        left join p_3 using(client_id)
        where group_type = "ЦГ"
        ''')['value'])

    arpu_control_group = float(my_func.input_base(sql_request='''
        select sum(p_3.payment_sum)/count(p_1.client_id) as value
        from p_1
        left join p_3 using(client_id)
        where group_type = "КГ"
        ''')['value'])
    arpu_target_group = round(float(my_func.input_base(sql_request='''
        select (sum(p_3.payment_sum) - (select count(delivery)*3 from p_1 where channel = "email" and group_type = "ЦГ") - (select count(delivery)*7 from p_1 where channel = "SMS" and group_type = "ЦГ"))/count(p_1.client_id) as value
        from p_1
        left join p_3 using(client_id)
        where group_type = "ЦГ"
        ''')['value']), 2)
    percent_difference_arpu_from_target_group_to_control_group = round(
        (arpu_target_group / arpu_control_group * 100 - 100), 2)

    dict_metrix = {'число клиентов КГ:': count_control_group,
                   'число клиентов ЦГ:': count_target_group,
                   'затраты на е-mail рассылку для ЦГ:': target_group_email_campaign_costs,
                   'затраты на sms рассылку для ЦГ:': target_group_sms_campaign_costs,
                   'затраты на обе кампании для ЦГ:': target_group_campaign_costs,
                   'сумма оплаченной задолженности КГ:': control_group_debit_payment_sum,
                   'сумма оплаченной задолженности ЦГ за исключением затрат на кампании:': target_group_debit_payment_sum_exclude_campaign_cost_sum,
                   'arpu КГ:': arpu_control_group,
                   'arpu ЦГ:': arpu_target_group,
                   'разница в процентах arpu ЦГ / КГ:': percent_difference_arpu_from_target_group_to_control_group
                   }
    print(f'сводка в разрезе групп клиентов:')
    for key, value in dict_metrix.items():
        print(key, value)

    # визуализация разницы arpu ЦГ / КГ (скорректировал)
    difference_arpu_target_group_control_group_df = my_func.input_base(sql_request='''select group_type, (sum(p_3.payment_sum) - (select count(delivery)*3 from p_1 where group_type="ЦГ" and channel="email")-(select count(delivery)*7 from p_1 where group_type="ЦГ" and channel="SMS"))/count(p_1.client_id) as value
    from p_1
    left join p_3 using(client_id)
    group by group_type''')
    sb.barplot(x="group_type", y="value", data=difference_arpu_target_group_control_group_df)
    plt.show()

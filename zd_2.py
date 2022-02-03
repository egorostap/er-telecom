import my_func
import seaborn as sb
from matplotlib import pyplot as plt



zd_2 = '''select * from p_1
left join p_2 using(client_id)
left join p_3 using(client_id)
left join p_4 using(client_id)'''

sum_channels = '''select channel, sum(payment_sum) payment_sum from p_1
left join p_2 using(client_id)
left join p_3 using(client_id)
left join p_4 using(client_id)
group by channel'''

# Запуск функции
if __name__ == '__main__':
    # вариант решения в связке  googlesheets и GDS: склеиваю таблицы в единую по ключу client_id, отправляю в гуглшитс, затем в GDS, формулы завожу в GDS
    # таблица с документом: https://docs.google.com/spreadsheets/d/1YDUfbpkDdT6ABQrmBjH79LNHG5pevZPYfs4dwAL2hyo/edit#gid=0
    # ссылка на отчет в GDS: https://datastudio.google.com/reporting/10e31414-42c2-4cd5-a5b2-b0d6db06b69a
    df = my_func.input_base(sql_request=zd_2)
    # my_func.google_sheet_write(df)

    # варианты отдельных запросов в коде
    payment_for_sms = len(df[df.channel == 'SMS'].channel) * 7
    viruchka_after_sms = sum(df[(df.channel == 'SMS')&(df.payment_sum > 0)].payment_sum)
    profit = viruchka_after_sms - payment_for_sms
    roi = (viruchka_after_sms - payment_for_sms) / payment_for_sms * 100
    dict_metrix = {'затраты на смс рассылку': payment_for_sms, 'выручка после отправки смс': viruchka_after_sms, 'профит': profit, 'roi': f'{roi}%'}
    print(f'sms stats: {dict_metrix}')

    # визуализация суммы оплат клиентами задолженности в разрезе источников трафика
    sum_channels_df = my_func.input_base(sql_request=sum_channels)
    sb.barplot(x="channel", y="payment_sum", data=sum_channels_df)
    plt.show()

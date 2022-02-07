# эксель таблицы загружены в бд sqlite, данная база данных также находится в репозитории проекта отрывать можно через db browser
# готовые запросы по домашнему заданию находятся в переменных: "zd_1_1 - zd_1_3"
import my_func

# переменные с решениями
sql_requests_zd_1 = [
    # решение 1.1
    '''
    select distinct s_1.cl_id,
    (select sum(revenue_summ)/count(cl_id) as arpu
    from s_1 join s_2 using(cl_id)
    where s_1.calc_period IN (202106, 202107, 202108)
    and campaign_theme = "Продажа" 
    and group_pos_1 = 1
    and s_2.calc_period IN (202106, 202107, 202108)
    and cl_activ = 1) as arpu,
    (case when (rev_last.revenue_summ - rev_first.revenue_summ) > 0 then "True" else "False" end) as revenue_up
    
    from s_1 
    join s_2 using(cl_id)
    join (select s_1.cl_id, min(s_2.calc_period), revenue_summ
    from s_1 join s_2 using(cl_id)
    where s_1.calc_period IN (202106, 202107, 202108)
    and campaign_theme = "Продажа" 
    and group_pos_1 = 1
    and s_2.calc_period IN (202106, 202107, 202108)
    and cl_activ = 1
    group by s_1.cl_id) rev_first using(cl_id)
    join (select s_1.cl_id, max(s_2.calc_period), revenue_summ
    from s_1 join s_2 using(cl_id)
    where s_1.calc_period IN (202106, 202107, 202108)
    and campaign_theme = "Продажа" 
    and group_pos_1 = 1
    and s_2.calc_period IN (202106, 202107, 202108)
    and cl_activ = 1
    group by s_1.cl_id) rev_last using(cl_id)
    
    where  s_1.calc_period IN (202106, 202107, 202108)
    and campaign_theme = "Продажа" 
    and group_pos_1 = 1
    and s_2.calc_period IN (202106, 202107, 202108)
    and cl_activ = 1
    ''',

    # решение 1.2
    '''
    ''',

    # решение 1.3
    '''
    WITH A AS
    (
    select cl_id, product_name, product_probability,
    ROW_NUMBER() over (PARTITION by cl_id order by product_probability desc) as rownum
    from s_3
    )
    SELECT cl_id, A2.product_name, sum(product_probability)/count(product_probability) as average_top_3_prod
    FROM A 
    left join (select cl_id, product_name from A where rownum = 3) A2 using(cl_id) 
    WHERE rownum <= 3
    group by cl_id
    '''
]

# Запуск функции
if __name__ == '__main__':
    for req in sql_requests_zd_1:
        my_func.input_base(sql_request=req)

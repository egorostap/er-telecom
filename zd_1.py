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
    WITH t_0 AS
    (
    SELECT campaign_theme, count(distinct(cl_id)) as ch_0 from s_1 where channel_id = 0 and group_pos_1 = 1 group by campaign_theme
    ),
    t_1 AS
    (
    SELECT campaign_theme, count(distinct(cl_id)) as ch_1 from s_1 where channel_id = 1 and group_pos_1 = 1 group by campaign_theme
    ),
    t_2 AS 
    (
    SELECT campaign_theme, count(distinct(cl_id)) as ch_2 from s_1 where channel_id = 2 and group_pos_1 = 1 group by campaign_theme
    ),
    t_3 AS 
    (
    SELECT campaign_theme, count(distinct(cl_id)) as ch_3 from s_1 where channel_id = 3 and group_pos_1 = 1 group by campaign_theme
    ),
    t_4 AS 
    (
    SELECT campaign_theme, count(distinct(cl_id)) as ch_4 from s_1 where channel_id = 4 and group_pos_1 = 1 group by campaign_theme
    ),
    t_5 AS 
    (
    SELECT campaign_theme, count(distinct(cl_id)) as ch_5 from s_1 where channel_id = 5 and group_pos_1 = 1 group by campaign_theme
    ),
    t_6 AS 
    (
    SELECT campaign_theme, count(distinct(cl_id)) as ch_6 from s_1 where channel_id = 6 and group_pos_1 = 1 group by campaign_theme
    )
    SELECT t_0.campaign_theme, ch_0, ch_1, ch_2, ch_3, ch_4, ch_5, ch_6
    FROM t_0
    left join t_1 using (campaign_theme)
    left join t_2 using (campaign_theme)
    left join t_3 using (campaign_theme)
    left join t_4 using (campaign_theme)
    left join t_5 using (campaign_theme)
    left join t_6 using (campaign_theme)
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

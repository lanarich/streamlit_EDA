import streamlit as st
import pandas as pd
from PIL import Image
import plotly
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np


@st.cache_data
def load_data():
    DATA = 'data.csv'
    data = pd.read_csv(DATA)
    m_1 = {1: 'Отклик был', 0 : 'Отклика не было'}
    m_2 = {1: 'Работает', 0 : 'Не работает'}
    m_3 = {1: 'Пенсионер', 0 : 'Не пенсионер'}
    m_4 = {1: 'Мужчина', 0: 'Женщина'}
    m_5 = {1: 'Квартира есть', 0: 'Квартиры нет'}

    data['target'] = data['target'].astype(object).replace(m_1)
    data['socstatus_work_fl'] = data['socstatus_work_fl'].astype(object).replace(m_2)
    data['socstatus_pens_fl'] = data['socstatus_pens_fl'].astype(object).replace(m_3)
    data['gender'] = data['gender'].astype(object).replace(m_4)
    data['fl_presence_fl'] = data['fl_presence_fl'].astype(object).replace(m_5)

    return data



def main():
    image = Image.open('pic1.jpg')

    st.set_page_config(
        layout="wide",
        page_title="Demo EDA",
        page_icon=image,

        )

    st.write(
            """
            # Что такое эффективное взаимодействие с клиентом?
            Определяем по EDA к каким клиентам лучше обратиться с предложением для положительного отклика
            """
        )

    st.image(image, width = 1100)

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Распределение", "🔍 Корреляция", "🥊 Target vs Var", "📐 Статистики"])

    with tab1:
        render_tab1()

    with tab2:
        render_tab2()

    with tab3:
        render_tab3()

    with tab4:
        render_tab4()

def render_tab1():

    st.write(
        """
        ### Выберете переменную
        """
    )


    var = st.selectbox("Переменная", ("Отклик на маркетинговую кампанию", "Возраст",  "Наличие работы", "Пребывание на пенсии",
                                              "Пол", "Количество детей", "Количество иждивенцев", "Личный доход (в рублях)",
                                              "Наличие в собственности квартиры", "Количество автомобилей в собственности", "Образование", "Общее количество кредитов",
                                             "Количество закрытых кредитов"), label_visibility  = "hidden")

    graph(var)

    st.write(
        """
        #### Вывод:  
        Исходя из графиков распределений можно сделать вывод, что интервальные переменные: **Возраст**, **Количество детей**, **Количество иждивенцев**,
        **Личный доход (в рублях)**, **Количество автомобилей в собственности**, **Общее количество кредитов** и **Количество закрытых кредитов** имеют ненормлаьное распределение.
        Для построения хорошей модели скорее всего нужно будет логарифмировать шкалы, чтобы достичь наибольшей точности.  
        Также можно сказать, что большую часть выборки составляю работающие мужчины, которые получили среднеспециальное образование и не имеют в собственности квартиры.  
        Из 15К респондентов откликнулись на предложение банка только ~12% клиентов.
        """
    )

def graph(var):

    translatetion = {
        "Отклик на маркетинговую кампанию": "target",
        "Возраст": "age",
        "Наличие работы": "socstatus_work_fl",
        "Пребывание на пенсии": "socstatus_pens_fl",
        "Пол": "gender",
        "Количество детей": "child_total",
        "Количество иждивенцев": "dependants",
        "Личный доход (в рублях)": "personal_income",
        "Наличие в собственности квартиры":"fl_presence_fl",
        "Количество автомобилей в собственности":"own_auto",
        "Образование":"education",
        "Общее количество кредитов": "loan_num_total",
        "Количество закрытых кредитов":"loan_num_closed"
    }

    df = load_data()

    int_list = ['age', 'child_total', 'dependants', 'personal_income', 'loan_num_total', 'loan_num_closed', 'own_auto']
    str_list = ['target', 'socstatus_work_fl', 'socstatus_pens_fl', 'gender', 'fl_presence_fl', 'education']

    if translatetion[var] in int_list:
        if translatetion[var] in ['personal_income']:
            fig = px.histogram(df, x=translatetion[var], title=f'Гистограмма по переменной: {var}', range_x=(0, 100000))
        else:
            fig = px.histogram(df, x=translatetion[var], title=f'Гистограмма по переменной: {var}')
        fig.update_traces(marker_color='skyblue', marker_line_color='black', marker_line_width=1, showlegend=False)
        fig.update_xaxes(title=None)
        fig.update_yaxes(title=None)
        st.plotly_chart(fig, use_container_width=True)
    elif translatetion[var] in str_list:
        fig = px.pie(df, names = translatetion[var],  title=f'Круговая диаграмма по переменной: {var}',
                     color_discrete_sequence=['#A4969B', 'skyblue', 'gray', 'skyblue'])
        fig.update_traces(textinfo='percent+label', pull=[0.05, 0.05, 0.05, 0.05], showlegend=False)
        fig.update_layout(
            height=600,  # Увеличиваем высоту графика
            width=700
            # Увеличиваем ширину графика
        )
        st.plotly_chart(fig, use_container_width=True)

def render_tab2():

    st.write(
        """
        ### Корреляция переменных
        """
    )

    df = load_data()


    df_corr = df.loc[:, ~df.columns.isin(['agreement_rk', 'education', 'target', 'socstatus_work_fl', 'socstatus_pens_fl',
                                          'gender', 'fl_presence_fl', 'work_time'])].corr()
    x = list(df_corr.columns)
    y = list(df_corr.index)
    z = np.array(df_corr)

    new_column_names = ["Возраст", "Количество<br>детей", "Количество<br>иждивенцев",
                        "Личный доход<br>(в рублях)", "Количество автомобилей<br>в собственности",
                        "Общее количество<br> кредитов", "Количество<br> закрытых кредитов"]

    fig = ff.create_annotated_heatmap(
        z,
        x=new_column_names,
        y=new_column_names,
        annotation_text=np.around(z, decimals=2),
        hoverinfo='z',
        colorscale='Viridis'
    )
    fig.update_layout(
        height=600,  # Увеличиваем высоту графика
        width=700)



    st.plotly_chart(fig, use_container_width=True)

    st.write(
        """
        #### Вывод:  
        Как и ожидалось корреляция между изучаемыми переменными очень низкая, так как ее сложно предположить на теоретическом уровне.
        Наиболее скоррелированными переменными (и по смыслу тоже) оказались пары: **Количество детей** и **Количество иждивенцев** = 0.51, а также
        **Общее количество кредитов** и **Количество закрытых кредитов** = 0.86. Между ними присутсвует тесная линейная связь.
        """
    )

def render_tab3():

    st.write(
        """
        ### Выберете переменную для изучения связи с целевым признаком
        """
    )

    var = st.selectbox("Переменная",
                       ("Возраст", "Наличие работы", "Пребывание на пенсии",
                        "Пол", "Количество детей", "Количество иждивенцев", "Личный доход (в рублях)",
                        "Наличие в собственности квартиры", "Количество автомобилей в собственности", "Образование",
                        "Общее количество кредитов",
                        "Количество закрытых кредитов"), label_visibility="hidden")


    translatetion = {
        "Отклик на маркетинговую кампанию": "target",
        "Возраст": "age",
        "Наличие работы": "socstatus_work_fl",
        "Пребывание на пенсии": "socstatus_pens_fl",
        "Пол": "gender",
        "Количество детей": "child_total",
        "Количество иждивенцев": "dependants",
        "Личный доход (в рублях)": "personal_income",
        "Наличие в собственности квартиры": "fl_presence_fl",
        "Количество автомобилей в собственности": "own_auto",
        "Образование": "education",
        "Общее количество кредитов": "loan_num_total",
        "Количество закрытых кредитов": "loan_num_closed"
    }

    df = load_data()

    int_list = ['age', 'child_total', 'dependants', 'personal_income', 'loan_num_total', 'loan_num_closed']
    str_list = ['target', 'socstatus_work_fl', 'socstatus_pens_fl', 'gender', 'fl_presence_fl', 'education', 'own_auto']

    if translatetion[var] in int_list:
        if translatetion[var] in ['personal_income']:
            fig = px.box(df, x='target', y=translatetion[var], points='all', color='target', title=f'Отклик vs {var}', range_y=(0, 100000))
        else:
            fig = px.box(df, x='target', y=translatetion[var], points='all', color='target', title=f'Отклик vs {var}')
    elif translatetion[var] in str_list:
         fig = px.histogram(df, x=translatetion[var], color='target', title=f'Отклик vs {var}')

    fig.update_layout(
        height=600,  # Увеличиваем высоту графика
        width=700)
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)

    st.plotly_chart(fig, use_container_width=True)


    st.write(
        """
        #### Вывод:  
        По графикам видно, что целевая переменная связана с некоторыми переменными.  
        * Отклик совершают более молодые клиенты, а также
        те, кто имеют работу.  
        * Пенсионеры не склоны совершать отклик.  
        * Мужчины чуть чаще совершаю отклик, однако примерно такое же значение имеют женщины.  
        * Количество детей и иждевенцов не влияет на отклик, а личный доход скорее влияет.  
        * Отклик сорвешают клиенты с более высоким личным доходом.  
        * У кого нет квартиры и машины, чаще откликаются на предложение, чем те, у кого они есть.  
        * Высокий отклик у тех респондентов, которые получили среднеспециальное, среднее и высшее образование.  
        * Количество кредитов не влияет на отклик.
        """
    )

def render_tab4():
    translatetion = {
        "target": "Отклик на маркетинговую кампанию",
        "socstatus_work_fl": "Наличие работы",
        "socstatus_pens_fl": "Пребывание на пенсии",
        "gender":"Пол",
        "child_total":"Количество детей",
        "dependants":"Количество иждивенцев",
        "personal_income":"Личный доход (в рублях)",
        "fl_presence_fl":"Наличие в собственности квартиры",
        "own_auto":"Количество автомобилей в собственности",
        "education":"Образование",
        "loan_num_total":"Общее количество кредитов",
        "loan_num_closed":"Количество закрытых кредитов",
        "Возраст": "age"
    }

    df = load_data()
    df_desc_int = df.loc[:, ~df.columns.isin(['work_time', 'agreement_rk'])].describe()
    df_desc_int = df_desc_int.rename(columns=translatetion).style.format("{:.2f}")

    df_desc_str = df.describe(include=[object])
    df_desc_str = df_desc_str.rename(columns=translatetion)

    st.write(
        """
        #### Описательные статистики для интервальных переменных
        """
    )

    st.table(df_desc_int)

    st.write(
        """
        #### Описательные статистики для категориальных переменных
        """
    )

    st.table(df_desc_str)


if __name__ == "__main__":
    main()
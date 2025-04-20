import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType

# 读取CSV文件
df = pd.read_csv('ScoreData.csv')

majors = df['专业名'].tolist()
years = df['年份'].tolist()
rankings = df['排名'].tolist()
# print(majors, years, rankings)
n = m = l = 0
for i in years:
    if i == 2023:
        n += 1
    elif i == 2022:
        m += 1
    else:
        l += 1
# print(n, m, l)
data23 = rankings[0:n]
data22 = rankings[n + 1:n + m]
data21 = rankings[n + m + 1:n + m + l]

majornamr23 = majors[0:n]
majornamr22 = majors[n + 1:n + m]
majornamr21 = majors[n + m + 1:n + m + l]

all_specialties = majornamr23 + majornamr22 + majornamr21

specialty_counts = {}
for specialty in all_specialties:
    if specialty in specialty_counts:
        specialty_counts[specialty] += 1
    else:
        specialty_counts[specialty] = 1
# 找出只出现了一次或两次的专业
unique_or_twice_specialties = [specialty for specialty, count in specialty_counts.items() if count <= 2]

ditct23 = dict(zip(majornamr23, data23))
ditct22 = dict(zip(majornamr22, data22))
ditct21 = dict(zip(majornamr21, data21))
for specialty in unique_or_twice_specialties:
    if specialty in ditct23:
        del ditct23[specialty]
    if specialty in ditct22:
        del ditct22[specialty]
    if specialty in ditct21:
        del ditct21[specialty]

sortrd_dict23 = {k: v for k, v in sorted(ditct23.items(), key=lambda item: item[0])}
sortrd_dict22 = {k: v for k, v in sorted(ditct22.items(), key=lambda item: item[0])}
sortrd_dict21 = {k: v for k, v in sorted(ditct21.items(), key=lambda item: item[0])}
key_majorname = list(sortrd_dict23.keys())
# print(key_majorname)
sorted_list_ranking23 = list(sortrd_dict23.values())
sorted_list_ranking22 = list(sortrd_dict22.values())
sorted_list_ranking21 = list(sortrd_dict21.values())

bar = (
    Bar(init_opts=opts.InitOpts(width="1500px", height="750px", theme=ThemeType.DARK))
    .add_xaxis(key_majorname)
    .add_yaxis("2023", sorted_list_ranking23)
    .add_yaxis("2022", sorted_list_ranking22)
    .add_yaxis("2021", sorted_list_ranking21)
    .set_global_opts(title_opts=opts.TitleOpts(title="山东理工大学各专业录取分排名对比"
                                               , title_link='https://www.dxsbb.com/news/33038.html')
                     , toolbox_opts=opts.ToolboxOpts(is_show=True)
                     , xaxis_opts=opts.AxisOpts(axislabel_opts={"interval": "0.1", "rotate": 45})
                     ,datazoom_opts=[opts.DataZoomOpts(is_show=True, type_="inside", range_start=10, range_end=25)],
                     )

    .set_series_opts(label_opts=opts.LabelOpts(is_show=False)
                     ,markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min")]))

    .render("山东理工大学各专业录取分排名对比.html")
)

print("可视化图表生成成功，请查看山东理工大学各专业录取分排名对比.html")

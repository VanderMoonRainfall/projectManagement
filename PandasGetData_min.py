import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
from pyecharts.charts import Pie
from pyecharts.globals import SymbolType

# 读取CSV文件
df = pd.read_csv('ScoreData.csv')

majors = df['专业名'].tolist()
years = df['年份'].tolist()
minScoer = df['最低录取分'].tolist()
# print(majors, years, minScoer)
n = m = l = 0
for i in years:
    if i == 2023:
        n += 1
    elif i == 2022:
        m += 1
    else:
        l += 1
# print(n, m, l)
data23 = minScoer[0:n]
data22 = minScoer[n + 1:n + m]
data21 = minScoer[n + m + 1:n + m + l]

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

dict23 = dict(zip(majornamr23, data23))
dict22 = dict(zip(majornamr22, data22))
dict21 = dict(zip(majornamr21, data21))
for specialty in unique_or_twice_specialties:
    if specialty in dict23:
        del dict23[specialty]
    if specialty in dict22:
        del dict22[specialty]
    if specialty in dict21:
        del dict21[specialty]

sortrd_dict23 = {k: v for k, v in sorted(dict23.items(), key=lambda item: item[0])}
sortrd_dict22 = {k: v for k, v in sorted(dict22.items(), key=lambda item: item[0])}
sortrd_dict21 = {k: v for k, v in sorted(dict21.items(), key=lambda item: item[0])}
key_majorname = list(sortrd_dict23.keys())

sorted_list_min23 = list(sortrd_dict23.values())
sorted_list_min22 = list(sortrd_dict22.values())
sorted_list_min21 = list(sortrd_dict21.values())

bar = (
    Bar(init_opts=opts.InitOpts(width="1500px", height="750px", theme=ThemeType.LIGHT))
    .add_xaxis(key_majorname)
    .add_yaxis("2023", sorted_list_min23)
    .add_yaxis("2022", sorted_list_min22)
    .add_yaxis("2021", sorted_list_min21)
    .set_global_opts(title_opts=opts.TitleOpts(title="山东理工大学各专业录取最低分对比"
                                               , title_link='https://www.dxsbb.com/news/33038.html')
                     , toolbox_opts=opts.ToolboxOpts(  is_show=True)
                     , xaxis_opts=opts.AxisOpts(axislabel_opts={"interval": "0.1", "rotate": 45})
                     ,datazoom_opts=[opts.DataZoomOpts(is_show=True, type_="inside", range_start=10, range_end=25)]
                     )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False)
                     , markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="最高分")])
                     , markline_opts= opts.MarkLineOpts(data = [opts.MarkLineItem(type_="max", name="最高分")]))

    .render("山东理工大学各专业录取最低分对比.html")
)


up_list22_23 = []
down_list22_23 = []
unchange_list22_23 = []
for i in range(len(sorted_list_min23)):
    if sorted_list_min23[i] > sorted_list_min22[i]:
        up_list22_23.append(sorted_list_min23[i])
    elif sorted_list_min23[i] < sorted_list_min22[i]:
        down_list22_23.append(sorted_list_min23[i])
    else:
        unchange_list22_23.append(sorted_list_min23[i])
# print(len(up_list22_23), len(down_list22_23), len(unchange_list22_23))

up_list21_22 = []
down_list21_22 = []
unchange_list21_22 = []
for i in range(len(sorted_list_min23)):
    if sorted_list_min22[i] > sorted_list_min21[i]:
        up_list21_22.append(sorted_list_min22[i])
    elif sorted_list_min22[i] < sorted_list_min21[i]:
        down_list21_22.append(sorted_list_min22[i])
    else:
        unchange_list21_22.append(sorted_list_min22[i])

datafin1_ = (len(up_list22_23), len(down_list22_23), len(unchange_list22_23))
datafin2_ = (len(up_list21_22), len(down_list21_22), len(unchange_list21_22))
# print(datafin1_, datafin2_)


# 数据准备
data_2022_2023 = [("录取分数上升", datafin1_[0]), ("录取分数下降", datafin1_[1]), ("录取分数不变", datafin1_[2])]
data_2021_2022 = [("录取分数上升", datafin2_[0]), ("录取分数下降", datafin2_[1]), ("录取分数不变", datafin2_[2])]

# 创建第一个环图
rose_2022_2023 = (
    Pie(init_opts=opts.InitOpts(width='800px', height='400px'))
    .add(
        series_name="2022-2023年专业录取分数变化",
        data_pair=data_2022_2023,
        radius=[40, 100],
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="2022-2023年专业录取分数变化", pos_left="center"),
        legend_opts=opts.LegendOpts(pos_left="left", orient="vertical")
    )
)

# 创建第二个环图
rose_2021_2022 = (
    Pie(init_opts=opts.InitOpts(width='800px', height='400px'))
    .add(
        series_name="2021-2022年专业录取分数变化",
        data_pair=data_2021_2022,
        radius=[40, 100],
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="2021-2022年专业录取分数变化", pos_left="center"),
        legend_opts=opts.LegendOpts(pos_left="left", orient="vertical")
    )
)

# 导入Page类
from pyecharts.charts import Page

# 将两个饼图添加到页面中
page = Page(layout=Page.DraggablePageLayout)
page.add(rose_2022_2023, rose_2021_2022)

# 渲染页面
page.render("专业录取分数变化.html")


print("可视化图表生成成功，请查看 山东理工大学各专业录取最低分对比.html  和专业录取分数变化.html ")
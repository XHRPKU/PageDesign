'''
用第三方库pyecharts绘制关系图（Graph）
使用前面练习题生成的人物关系数据
'''
from pyecharts import options as opts
from pyecharts.charts import Graph

node_file_name='./output/红楼梦-人物节点图.csv'
link_file_name='./output/红楼梦-人物连接图尝试.csv'

out_file_name='./output/关系图-红楼梦1.html'

node_file=open(node_file_name,'r')
node_file_list=node_file.readlines()
node_file.close()
del node_file_list[0]
print(node_file_list)

link_file=open(link_file_name,'r')
link_file_list=link_file.readlines()
link_file.close()
del link_file_list[0]


node_in_graph=[]
for i in node_file_list:
    i=i.strip('\n')
    i=i.split(',')
    print(i)
    if i[0] in ['薛姨妈','李纨','刘姥姥','贾珍','邢夫人','尤氏','香菱','薛蟠']:
        continue
    node_in_graph.append(opts.GraphNode(
        name=i[0],
        value=int(i[1]),
        symbol_size=int(i[1])/50))

link_in_graph=[]
for i in link_file_list:
    i=i.strip('\n')
    i=i.split(',')
    link_in_graph.append(opts.GraphLink(
        source=i[0],
        target=i[1],
        value=int(i[2])))

c=Graph(init_opts=opts.InitOpts(theme="",
                                width='1200px',
                                height='800px',
                                page_title='红楼梦'))
c.add('',node_in_graph,
      link_in_graph,
      edge_length=[10,50],
      repulsion=1000,
      layout='circular',
      )
c.set_global_opts(title_opts=opts.TitleOpts(title='')
                  )
c.render(out_file_name)
##--- 第3步：画图


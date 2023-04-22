'''
练习题
选择一部中文小说或者剧本，10万字以上为宜
按照程序示例的功能要求，统计人名“共现”情况
'''
'''
选择案例：红楼梦
'''
import jieba
import jieba.posseg as pseg

txt_file_name='./data/红楼梦.txt'

node_file_name='./output/红楼梦-人物节点图.csv'
link_file_name='./output/红楼梦-人物连接图尝试.csv'

txt_file=open(txt_file_name,'r',encoding='utf-8')
line_list=txt_file.readlines()
txt_file.close()


#相当于在已有的pseg.cut分词词典中增加我们想要的特点的词典
jieba.load_userdict('./data/红楼梦词典.txt')

line_name_list=[]
name_cnt_dict={}

progress=0
for line in line_list:
    word_gen=pseg.cut(line)
    line_name_list.append([])
 #每一自然段的分词
#对每一段分词后的结果进行筛选，只有两个以上的，且在字典库的单词才会进入到筛选中。   
    for one in word_gen:
        word=one.word
        flag=one.flag
        
        if len(word) ==1:
            continue
        if word =='宝玉':
            word='贾宝玉'
        elif word=='黛玉':
            word='林黛玉'
        elif word=='老太太':
            word="贾母"
        elif word in['凤姐','凤姐儿']:
            word='王熙凤'
        elif word=='小丫头':
            word="林红玉"
        elif word=='宝钗':
            word="薛宝钗"
        elif word=="二人":
            continue

        
        if 'nr' in flag:
          line_name_list [-1].append(word)#本步的用意是统计出每一自然段中出现的人物，便于后续的节点共线分析
          #本步的用意是统计出在本段中，总结全部出现的人名，并用字典的方式去统计出每个名字出现的次数
          if word in name_cnt_dict.keys():
              name_cnt_dict[word] += 1
          else:
              name_cnt_dict[word] = 1
              
        progress = progress+1
        progress_que=int(progress/1000)
        if progress%1000 == 0:
            print('\r'+'-'*progress_que+'>'\
                  +str(progress_que)+'千',end='')
        #\r在python中r的意思是raw，即忠实地打印出\r之后的东西
        
print('\n基础分析已经完成')
##--- 第2步：用字典统计人名“共现”数量（relation_dict）
relation_dict = {}

# 只统计出现次数达到限制数的人名
name_cnt_limit = 200  
for line in line_name_list:
    for name1 in line:
        if name1 in relation_dict.keys():
            pass
        #pass和continue的区别在于，continue表示终止后面的程序，重新开始新的循环，而pass则表示站位，即站着位置使得for循环不会出错
        #意味着后续的程序依旧会执行
        
        elif name_cnt_dict[name1] >= name_cnt_limit:
            relation_dict[name1]={}
        else:
            continue
        
        for name2 in line:
            if name2 == name1 or name_cnt_dict[name2] < name_cnt_limit:
                continue
         
            
            if name2 in relation_dict[name1].keys():
                relation_dict[name1][name2] += 1
            else:
                relation_dict[name1][name2] =1      
    
print('共线统计完成，已完成'+str(name_cnt_limit)+'以上的成员名单')

#第三部分
item_list=list(name_cnt_dict.items())
item_list.sort(key=lambda x:x[1], reverse=True)

node_file=open(node_file_name,'w')
node_file.write('名字,次数\n')
node_cnt=0
for name, cnt in item_list:
    if cnt >= name_cnt_limit:
        node_file.write(name+','+str(cnt)+'\n')
        node_cnt += 1
node_file.close()

print('人物数量'+str(node_cnt))
print('已写入文件'+node_file_name)  

link_cnt_limit=800
print('只输出'+str(link_cnt_limit)+'以上的连接')  
link_file=open(link_file_name,'w')
link_file.write('传者,受者,连接点\n')
link_cnt=0
for name1, link_dic in relation_dict.items():
    for name2, link_time in link_dic.items():
        if link_time >=link_cnt_limit:
            link_file.write(name1+','+name2+','+str(link_time)+'\n')
            link_cnt +=1
print('已写入连接数量'+str(link_cnt))
print('已写入文件'+link_file_name)

              
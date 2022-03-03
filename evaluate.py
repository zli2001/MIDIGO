import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib
''' 由于原本生成文本为字符音名，需要先转换成数据列表'''
def txt_to_list(filename,mod): # 注：此处文件名为相对路径 需要在根目录下
    # 先读取txt文件内容为字符串
    f = open(filename,"r",encoding='gbk')#设置文件对象  加了一个encoding=’gbk'
    line = f.readline()
    # print(line)

    # 将字符串转换为列表
    line_list=line.strip('\t').split('\t')
    # print(line_list)

    # 构建两个字典，一个里面是正常的加#的l，另一个是-的
    yinming=['A0','A#0','B0',
             'C1','C#1','D1','D#1','E1','F1','F#1','G1','G#1','A1','A#1','B1',
             'C2','C#2','D2','D#2','E2','F2','F#2','G2','G#2','A2','A#2','B2',
             'C3','C#3','D3','D#3','E3','F3','F#3','G3','G#3','A3','A#3','B3',
             'C4','C#4','D4','D#4','E4','F4','F#4','G4','G#4','A4','A#4','B4',
             'C5','C#5','D5','D#5','E5','F5','F#5','G5','G#5','A5','A#5','B5',
             'C6','C#6','D6','D#6','E6','F6','F#6','G6','G#6','A6','A#6','B6',
             'C7','C#7','D7','D#7','E7','F7','F#7','G7','G#7','A7','A#7','B7',
             'C8']
    yinming2={'B-0':2,
              'D-1':5,'E-1':7,'G-1':10,'A-1':12,'B-1':14,
              'D-2':17,'E-2':19,'G-2':22,'A-2':24,'B-2':26,
              'D-3':29,'E-3':31,'G-3':34,'A-3':36,'B-3':38,
              'D-4':41,'E-4':43,'G-4':46,'A-4':48,'B-4':50,
              'D-5':53,'E-5':55,'G-5':58,'A-5':60,'B-5':62,
              'D-6':65,'E-6':67,'G-6':70,'A-6':72,'B-6':74,
              'D-7':77,'E-7':79,'G-7':82,'A-7':84,'B-7':86}

    finallist=[] # 最后返回的数值列表
    key=0 #用于存贮当前最后一个加入数值列表的数，以备出现‘-’延迟符号时替换
    # 将列表中音名用对应权位替换
    if mod == 'sl':
        for a in line_list:
            if a!='-' and a!='^':
                if (a in yinming):
                    b=yinming.index(a)+1
                    finallist.append(b)
                    key=b
                elif (a in yinming2):
                    finallist.append(yinming2[a])
                    key=yinming2[a]
            elif a=='-':
                finallist.append(key)
                key=key
            elif a=='^':
                finallist.append(0)
                key=0
            elif a=='\n': # 遇到回车符则退出
                break
    elif mod == 'yl':
        for a in line_list:
            if a!='-' and a!='^':
                if (a in yinming):
                    b=yinming.index(a)+1
                    finallist.append(b)
                    key=b
                elif (a in yinming2):
                    finallist.append(yinming2[a])
                    key=yinming2[a]
            elif a=='-':
                continue
            elif a=='^':
                continue
            elif a=='\n': # 遇到回车符则退出
                break

    #print(finallist)
    f.close()
    return finallist

def L_JTDB(music_list):
    '''
    :param misic_list: 输入为音乐转换后的序列
    :return: 返回级进-跳进对比值q
    '''
    woc = music_list
    diff = [woc[i] - woc[i + 1] for i in range(len(woc) - 1)]
    abss= [abs(i) for i in diff]
    T = 0
    J = 0
    for i in abss:
        if i >= 4:
            J = J + 1
        elif i < 4:
            T = T + 1
    print('级进个数 = ',J)
    print('跳进个数 = ',T)
    q = J/T
    print('级进-跳进比q = ',q)
    return q


def L_BL(music_list):
    '''
    波浪检验，即对音乐的波浪形进行检验
    :param music_list:  music_list：输入音乐转换后的序列
    :return:
    '''
    woc = music_list
    diff = [woc[i] - woc[i + 1] for i in range(len(woc) - 1)]
    k = 0
    for i in range(len(diff)-5):
        if diff[i]*diff[i+1] >= 0:
            if diff[i+1]*diff[i+2] <= 0:
                if diff[i+2]*diff[i+3] >= 0:
                    if abs(diff[i])+abs(diff[i+1])+abs(diff[i+2])+abs(diff[i+3]) != 0:
                        k += 1
                    else:
                        continue
                else:
                    continue
            else:
                continue
        else:
            continue
    return k

def L_DXJY(music_List):
    l = music_List
    C = [1,3,
         4,6,8,9,11,13,15,
         16,18,20,21,23,25,27,
         28,30,32,33,35,37,39,
         40,42,44,45,47,49,51,
         52,54,56,57,59,61,63,
         64,66,68,69,71,73,75,
         76,78,80,81,83,85,87,
         88]
    k = 0
    for i in range(len(l)):
        if l[i] in C:
            k+=1
        else:
            continue
    Dxjy = k/len(l)
    return Dxjy


def main_evaluate(filename_gen):
    '''
    音乐评价数理统计部分

    使用Wilcoxon符号检验
    Kruskal-Wallis H 检验
    Mann-Whitney U 检验
    '''
    '''
    曼惠特尼u检验是非参数检验：
    它假设两个样本分别来自除了总体均值以外完全相同的两个总体，目的是检验这两个总体的均值是否有显著的差别
    简单来说就是AB小样本（样本数不一定相等）分别来自于不同的总体，且AB二者的均值不相等
    我们目的是要通过AB去检验一下两个总体的均值是否有显著的差异
    '''

    real_music_sl=txt_to_list('data/real_music.txt',mod = 'sl') # 现有音乐txt,用于数理统计

    real_music_yl = txt_to_list('data/real_music.txt',mod = 'yl')

    real_abs = [real_music_sl[i] - real_music_sl[i + 1] for i in range(len(real_music_sl) - 1)]

    g_music_sl=txt_to_list(filename_gen,mod = 'sl') # 生成音乐txt，用于数理统计

    g_music_yl = txt_to_list(filename_gen, mod='yl')

    g_abs = [g_music_sl[i] - g_music_sl[i + 1] for i in range(len(g_music_sl) - 1)]

    mini_len = min(len(real_music_sl), len(g_music_sl))
    mini_len_abs = min(len(real_abs),len(g_abs))

    w1 = real_music_sl[0:mini_len]
    w2 = g_music_sl[0:mini_len]
    w1_abs = real_abs[0:mini_len_abs]
    w2_abs = g_abs[0:mini_len_abs],


    U = stats.mannwhitneyu(w1, w2, alternative='two-sided').pvalue
    U2 = stats.mannwhitneyu(w1_abs,w2_abs, alternative='two-sided').pvalue

    print('U检验',U) # pvalue>0.5则认为两组数据具有相似性
    print('U检验其差分的序列',U2)

    '''
    Wilcoxon符号检验
    scipy.stats.wilcoxon( x, y, correction = Flase, alternative = ‘two-sided’ )
    x：第一组测量值（在这种情况下，y是第二组测量值），或者在两组测量值之间的差（在这种情况下，不指定y）。必须是一维的。
    y：第二组测量值（如果x是第一组测量值），或者未指定（如果x是两组测量值之间的差）。必须是一维的。
    correction：如果为True，则是在小样本情况下，在计算Z统计量时用0.5来连续性校正。默认值为False。
    alternative：等于 “two-sided” 或 “greater” 或 “less”。“two-sided” 为双边检验，“greater” 为备择假设是大于的单边检验，“less” 为备择假设是小于的单边检验。
    '''

    # 双边检验，大于0.25就认为i其有显著意义，和真实的音乐生成分布相同
    W = stats.wilcoxon(w1,w2,alternative='two-sided').pvalue
    W2= stats.wilcoxon(w1_abs, w2_abs, alternative='two-sided').pvalue
    print('W检验',W)
    print('W_abs',W2)

    K = stats.kruskal(w1,w2).pvalue
    K2 = stats.kruskal(w1_abs, w2_abs).pvalue
    print('K检验',K)
    print('K_abs',K2)
    '''
    音乐评价乐理评价方面
    L_JTDB 级进-跳进对比检验
    L_BL 波浪检验
    L_DXJY 调性检验
    '''
    q1 = L_JTDB(real_music_yl)
    # q1 = L_JTDB(w1_abs)
    q2 = L_JTDB(g_music_yl)
    # q2 = L_JTDB(w2_abs)
    q2=q2/0.35

    k1 = L_BL(real_music_yl)#现有音乐
    print('real music的波浪数', k1)
    k2 = L_BL(g_music_yl)#generation
    print('generated music的波浪数', k2)
    #GKX
    k2=k2/150

    Dxjy1 = L_DXJY(real_music_yl)
    print('真实音乐其中音符处于C大调的比率为', Dxjy1)
    Dxjy2 = L_DXJY(g_music_yl)
    print('生成音乐其中音符处于C大调的比率为', Dxjy2)

    #gkx
    print(q2)
    data=np.array([U2,W2,K2,q2,k2,Dxjy2])
    return data


if __name__ == '__main__':

    path = r'D:\midi-gan\midi-process\adv_txt'
    filelist = os.listdir(path)
    savepath = r'D:\midi-gan\midi-process\img'
    for file in filelist:
        filepath = path + '/' + file
        #ori_data = main_evaluate(r'D:\midi-gan\midi-process\dataset\eval.txt')
        ori_data = main_evaluate(filepath)
        nAttr = 6
        labels = np.array(["Wilcoxon Test", 'Mann-Whitney U test', 'Kruskal-Wallis H test', 'SSP Comparison', 'Wave Test', 'Note-level Mode Test'])
        '''
        angles = np.linspace(0, 2 * np.pi, nAttr, endpoint=False)
        data = np.concatenate((ori_data, [ori_data[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        labels = np.concatenate((labels, [labels[0]]))  # 对labels进行封闭
        
        plt.plot(angles, data, linewidth=2)
        plt.show()
        plt.fill(angles, data, facecolor="g", alpha=0.25)
        plt.show()
        plt.thetagrids(angles * 180 / np.pi, labels)
        plt.figtext(0.5, 0.9, "综合评价图", ha="center")
        plt.grid(True)
        '''
        radar_labels = np.array(labels)
        nAttr = 6
        data = np.array(ori_data)
        angles = np.linspace(0, 2 * np.pi, nAttr, endpoint=False)
        fig = plt.figure(facecolor="white")
        plt.subplot(111, polar=True)
        plt.plot(angles, data, 'bo', color='gray', linewidth=1, alpha=0.2)
        plt.plot(angles, data, 'o-', linewidth=1.5, alpha=0.2)
        plt.fill(angles, data, alpha=0.25)
        plt.thetagrids(angles * 180 / np.pi, radar_labels)
        plt.figtext(0.52, 0.95, 'Comprehensive evaluation chart', ha='center', size=20)
        #legend = plt.legend(loc=(0.94, 0.80), labelspacing=0.1)
        plt.grid(True)
        name_1=file.split('.')[0]
        save_file=savepath+'\\'+name_1+'_eval.JPG'
        with open(save_file,'w') as obj:
            plt.savefig(save_file)
        #plt.show()



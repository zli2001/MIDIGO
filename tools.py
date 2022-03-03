from music21 import *
import pretty_midi
import os
import traceback
import glob

def transpose_to_c(midipath,transposepath,to_key,to_name):#把歌曲的调式转换为想要的调式
    midi_path = glob.glob(midipath)#MIDI数据集的存放路径
    transpose_root_dir = transposepath#转换后的保存路径
    for midi in midi_path:#使用一个参数midi在这个路径中循环，得到每个文件的路径
        name_1 = midi.split('\\')[-1]
        name_2 = name_1.split('.')[0]
        #设置保存的文件名
        # transposed_path = os.path.join(transpose_root_dir + '/' + name_2 + '_to_A.mid')

        transposed_path = os.path.join(transpose_root_dir + '/' + name_2 + to_name)

        stream = converter.parse(midi)#把midi数据通过music21中的converter函数转换为stream格式

        midi_key = stream.analyze('key')#分析调式
        # print(estimate_key)
        midi_tone, midi_mode = (midi_key.tonic, midi_key.mode)#midi_key中有两个值，分别传到前面两个参数中

        # c_key = key.Key('A', 'major')#定义需要转换到的调式

        c_key = key.Key(to_key, 'major')

        c_tone, c_mode = (c_key.tonic, c_key.mode)

        margin = interval.Interval(midi_tone, c_tone)#计算调式之间的距离

        semitones = margin.semitones

        mid = pretty_midi.PrettyMIDI(midi)
        for instr in mid.instruments:#对每个轨道进行循环
            if not instr.is_drum:#如果不是鼓，就进行转换
                for note in instr.notes:#对这一轨里面的每一个音符进行转换
                    if note.pitch + semitones < 128 and note.pitch + semitones > 0:
                        note.pitch += semitones

        mid.write(transposed_path)
        # new_stream = converter.parse(transposed_path)
        # new_key = new_stream.analyze('key')
        # print(new_key)
    print('转换完成')

def get_tempo(path):#获取midi数据的速度
    pm = pretty_midi.PrettyMIDI(path)
    _, tempo = pm.get_tempo_changes()#第一个参数没用，只要第二个参数
    return tempo.tolist()

def tempo_transpose(midipath,transposepath,speed):#把midi的速度转换到想要的速度上
    """midi_path = glob.glob(midipath)
    transpose_root_dir = transposepath

    i = 1
    for midi in midi_path:#对每个midi文件进行处理
        name_1 = midi.split('\\')[-1]
        name_2 = name_1.split('.')[0]
        # 设置保存的文件名
        transposed_path = os.path.join(transpose_root_dir + '/' + name_2 +'转换速度：'+ str(speed) + '.mid')
        i=i+1
        original_tempo = get_tempo(midi)[0]#得到所选的midi数据的速度
        print("%s的原始速度为：%s"%(midi,original_tempo))
        changed_rate = original_tempo / speed #得到和想要的速度的比例

        pm = pretty_midi.PrettyMIDI(midi)
        for instr in pm.instruments:
            for note in instr.notes:#对每个音符进行放缩
                note.start *= changed_rate
                note.end *= changed_rate

        pm.write(transposed_path)
        # print("tempo transpose fallished")"""
    #lzh改
    midi=midipath
    i = 1
    name_1 = midi.split('\\')[-1]
    name_2 = name_1.split('.')[0]
    # 设置保存的文件名
    i = i + 1
    original_tempo = get_tempo(midi)[0]  # 得到所选的midi数据的速度
    print("%s的原始速度为：%s" % (midi, original_tempo))
    changed_rate = original_tempo / speed  # 得到和想要的速度的比例

    pm = pretty_midi.PrettyMIDI(midi)
    for instr in pm.instruments:
        for note in instr.notes:  # 对每个音符进行放缩
            note.start *= changed_rate
            note.end *= changed_rate
    savepath = transposepath + '/' + midipath.split('/')[-1].split('.')[0] + 'to_speed' + str(speed) + '.mid'
    pm.write(savepath)
    print("tempo transpose finished")

def midi_to_txt(midipath,transposepath,track = 1):
    """midi_path = glob.glob(midipath)  # MIDI数据集的存放路径
    transpose_root_dir = transposepath  # 转换后的保存路径
    ifs = []
    for midi1 in midi_path:  # 使用一个参数midi在这个路径中循环，得到每个文件的路径
        name_1 = midi1.split('\\')[-1]
        name_2 = name_1.split('.')[0]
        # 设置保存的文件名
        # transposed_path = os.path.join(transpose_root_dir + '/' + name_2 + '_to_txt.txt')
        # print(transposed_path)
        mf = midi.MidiFile()
        mf.open(midi1)
        mf.read()
        mf.close()
        # stream = converter.parse(midi)
        notes = []
        mt = mf.tracks[track]
        stream2 = midi.translate.midiTrackToStream(mt)
        # chords = []
        parts = instrument.partitionByInstrument(stream2)

        for part in parts.parts:
            if 'Piano' in str(part):
                notes_to_parse = part.recurse()  # 递归
            elif parts:
                notes_to_parse = parts.parts[0].recurse()  # 纯音符组成
            else:
                notes_to_parse = stream.flat.notes

            list_time = []
            for element in notes_to_parse:
                time = element.duration.quarterLength
                if time != 0:
                    list_time.append(time)
            # min_time = min(list_time)
            min_time = 0.25
            for element in notes_to_parse:  # notes本身不是字符串类型
                # 如果是note类型，取它的音高(pitch)
                if isinstance(element, note.Note):
                    # 格式例如：E6
                    notes.append(str(element.pitch))
                    # ifs.append(str(element.pitch))
                    f = int(element.duration.quarterLength/min_time)
                    for i in range(f):
                        notes.append(str("-"))
                        # ifs.append(str(element.pitch))
                elif isinstance(element, note.Rest):#休止符转换
                    f = int(element.duration.quarterLength / min_time)
                    if f >= 50:
                        continue
                    for i in range(f):
                        notes.append(str("^"))
        # text_save(transposed_path,notes)
        text_save(transpose_root_dir, notes)
        print("%s SAVE2TXT"%midi1)
    # return ifs
        # print(notes)
        # print(chords)"""
    #lzh改
    midi1 = midipath  # MIDI数据集的存放路径
    transpose_root_dir = transposepath  # 转换后的保存路径
    ifs = []
    name_1 = midi1.split('\\')[-1]
    name_2 = name_1.split('.')[0]
    # 设置保存的文件名
    # transposed_path = os.path.join(transpose_root_dir + '/' + name_2 + '_to_txt.txt')
    # print(transposed_path)
    mf = midi.MidiFile()
    mf.open(midi1)
    mf.read()
    mf.close()
    # stream = converter.parse(midi)
    notes = []
    mt = mf.tracks[track]
    stream2 = midi.translate.midiTrackToStream(mt)
    # chords = []
    parts = instrument.partitionByInstrument(stream2)

    for part in parts.parts:
        if 'Piano' in str(part):
            notes_to_parse = part.recurse()  # 递归
        elif parts:
            notes_to_parse = parts.parts[0].recurse()  # 纯音符组成
        else:
            notes_to_parse = stream.flat.notes

        list_time = []
        for element in notes_to_parse:
            time = element.duration.quarterLength
            if time != 0:
                list_time.append(time)
        min_time = min(list_time)

        for element in notes_to_parse:  # notes本身不是字符串类型
            # 如果是note类型，取它的音高(pitch)
            if isinstance(element, note.Note):
                # 格式例如：E6
                notes.append(str(element.pitch))
                # ifs.append(str(element.pitch))
                f = int(element.duration.quarterLength / min_time)
                for i in range(f):
                    notes.append(str("-"))
                    # ifs.append(str(element.pitch))
            elif isinstance(element, note.Rest):  # 休止符转换
                f = int(element.duration.quarterLength / min_time)
                if f >= 20:
                    continue
                for i in range(f):
                    notes.append(str("^"))
    # text_save(transposed_path,notes)
    savepath=transposepath+'/'+midipath.split('/')[-1].split('.')[0]+'to_txt.txt'
    text_save(savepath, notes)
    print("%s SAVE2TXT" % midi1)

def text_save(filename,data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'a')
    # file.write('<s>')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','')   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
        file.write('\t')
        #16个音符分为一小节
        # if((i+1) % 16 == 0):
        #     file.write('\n')
    # file.write('<e>')
    file.write('\n')

    file.close()

#读取文件数据保存为列表
def loadDatadet(infile):
    with open(infile,'r') as f:
        sourceInLine=f.readlines()
        dataset=[]
        for line in sourceInLine:
            curLine=line.strip().split(" ")
            dataset.extend(curLine)
    # print(dataset)
    return dataset

#把txt文件转化为midi
def text2midi(txt_path,save_path):
    #txt_path为txt文件的路径
    #save_path为保存路径，格式为 r'路径地址'

    #先使用loadDatadet函数读取文件保存为note1
    note1 = loadDatadet(txt_path)
    #定义一个空的stream
    note1 = note1[0].strip().split('\t')
    while '[UNK]' in note1:
        note1.remove('[UNK]')
    while '[SEP]' in note1:
        note1.remove('[SEP]')
    while '' in note1:
        note1.remove('')
    stream1 = stream.Stream()

    #使用enumerate函数在note1中循环提取每个value和其下标key
    for key, value in enumerate(note1):
        # print(key, value)
        #如果为'-'（延音符），跳过本次循环
        if value == '-':
            continue
        elif value == '^':
            if key + 1 < len(note1):
                if note1[key + 1] != '^':
                    f = note.Rest()
                    f.duration.quarterLength = 0.25
                    stream1.append(f)
                else:
                    f = note.Rest()
                    time = 0
                    for i in range(key + 1, len(note1), 1):
                        time += 0.25
                        if note1[i] != '^':
                            f.duration.quarterLength = time
                            stream1.append(f)
                            time = 0
                            break
                        else:
                            continue
        else:
            #这里是让键值不能大于序列长度
            if key + 1 < len(note1):
                #如果下一个符号的值不是为'-',说明不需要延音
                if note1[key + 1] != '-':
                    f = note.Note(value)
                    f.duration.quarterLength = 0.25
                    stream1.append(f)
                else:
                    # 如果下一个符号的值为'-',说明需要延音
                    f = note.Note(value)
                    time = 0
                    #计算需要延音的时长
                    for i in range(key + 1, len(note1), 1):
                        time += 0.25
                        if note1[i] != '-':
                            f.duration.quarterLength = time
                            stream1.append(f)
                            time = 0
                            break
                        else:
                            continue
    #生成一个乐谱对象
    score = stream.Score()
    #添加声部，给声部命名
    part = stream.Part()
    part.partName = 'generation Part'
    #加入stream
    part.append(stream1)
    #声部加入乐谱中
    score.insert(0, part)
    # 添加题目、作者等元数据
    score.insert(0, metadata.Metadata())
    score.metadata.title = 'lyc_generation'
    score.metadata.composer = 'genertion composer'
    #写入文件
    #score.write('midi', fp=save_path)
    #lzh改
    savepath = save_path + '/' + txt_path.split('/')[-1].split('.')[0] + 'to_mid.mid'
    #savepath = txt_path.split('/')[-1].split('.')[0] + 'to_mid.mid'
    score.write('midi', fp=savepath)
    print('转换成功')

#把midi文件转换为序列
def midi_2_number(generate_midi_path,):
    midi_path = glob.glob(generate_midi_path)  # MIDI生成后的的存放路径
    for midi1 in midi_path:

        pass

def remove_note(notes):
    note_r = notes.strip('\t').split('\t')
    while '[UNK] ' in note_r:
        note_r.remove('[UNK] ')
    while '[SEP] ' in note_r:
        note_r.remove('[SEP] ')
    print(note_r)
    return note_r



if __name__ == '__main__':
    #remove_note('[UNK] 	[UNK] 	- 	^ 	[UNK] 	- 	[UNK] 	- 	[UNK] 	[UNK] 	- 	[UNK] 	[UNK] 	- 	F4 	- 	F4 	- 	- 	- 	- 	- 	^ 	^ 	^ 	G4 	- 	^ 	G4 	- 	G4 	- 	G4 	- 	G4 	- 	F4 	- 	F4 	- 	- 	- 	- 	^ 	G4 	- 	^ 	C4 	- 	G4 	- 	F4 	- 	- 	F4 	- 	G4 	- 	C4 	- 	D4 	- 	E4 	- 	E4 	- 	- 	F4 	- 	G4 	- 	C4 	- 	- 	D4 	- 	D4 	- 	D4 	- 	C4 	- 	B3 	- 	C4 	- 	- 	- 	- 	^ 	^ 	F4 	- 	F4 	- 	G4 	- 	C4 	- 	G4 	- 	C5 	- 	- 	- 	B4 	- 	C5 	- 	- 	^ 	G4 	- 	A4 	- 	A4 	- 	G4 	- 	G4 	- 	C5 	- 	C4 	- 	C4 	- 	E4 	- 	G4 	- 	G4 	- 	D4 	- 	D4 	- 	D4 	- 	C4 	- 	B3 	- 	C4 	- 	- 	- 	- 	^ 	F4 	- 	F4 	- 	G4 	- 	C4 	- 	G4 	- 	C5 	- 	- 	- 	B4 	- 	C5 	- 	- 	^ 	G4 	- 	A4 	- 	A4 	- 	G4 	- 	G4 	- 	C5 	- 	C4 	- 	C4 	- 	E4 	- 	G4 	- 	G4 	- 	D4 	- 	D4 	- 	D4 	- 	C4 	- 	B3 	- 	C4 	- 	- 	- 	- 	- 	^ 	F4 	- 	F4 	- 	G4 	- 	C5 	- 	C5 	- 	D5 	- 	C5 	- 	D5 	- 	^ 	C5 	- 	D5 	- 	E5 	- 	- 	D5 	- 	D5 	- 	C5 	- 	G4 	- 	- 	^ 	^ 	^ 	^ 	^ 	F4 	- 	F4 	- 	G4 	- 	D5 	- 	D5 	- 	G4 	- 	G4 	- 	F4 	- 	F4 	- 	- 	- 	^ 	G4 	- 	D5 	- 	D5 	- 	D5 	- 	D5 	- 	G4 	- 	G4 	- 	- 	- 	- 	G4 	- 	G4 	- 	G4 	- 	F4 	- 	F4 	- 	- 	- 	- 	^ 	^ 	^ 	G4 	- 	G4 	- 	G4 	- 	F4 	- 	- 	^ 	C4 	- 	G4 	- 	F4 	- 	- 	F4 	- 	G4 	- 	C4 	- 	D4 	- 	E4 	- 	E4 	- 	- 	F4 	- 	G4 	- 	C4 	- 	- 	D4 	- 	D4 	- 	D4 	- 	C4 	- 	B3 	- 	C4 	- 	- 	- 	- 	^ 	^ 	F4 	- 	F4 	- 	G4 	- 	C4 	- 	C5 	- 	G4 	- 	- 	- 	B4 	- 	C5 	- 	- 	G4 	- 	A4 	- 	A4 	- 	G4 	- 	G4 	- 	C5 	- 	C4 	- 	C4 	- 	E4 	- 	G4 	- 	G4 	- 	D4 	- 	D4 	- 	D4 	- 	C4 	- 	B3 	- 	C4 	- 	- 	- 	- 	- 	^ 	^ 	F4 	- 	F4 	- 	G4 	- 	C5 	- 	C5 	- 	D5 	- 	C5 	- 	D5 	- 	C5 	- 	D5 	- 	E5 	- 	- 	D5 	- 	D5 	- 	C5 	- 	G4 	- 	- 	^ 	^ 	^ 	^ 	^ 	F4 	- 	F4 	- 	G4 	- 	D5 	- 	D5 	- 	G4 	- 	G4 	- 	F4 	- 	F4 	- 	- 	- 	- 	- 	^ 	^ 	^ 	G4 	- 	G4 	- 	G4 	- 	F4 	- 	F4 	- 	- 	- 	- 	^ 	^ 	G4 	- 	G4 	- 	G4 	- 	A4 	- 	G4 	- 	A4 	- 	D5 	- 	D5 	- 	D5 	- 	D5 	- 	^ 	D5 	- 	D5 	- 	G4 	- 	G4 	- 	- 	- 	- 	^ 	^ 	G4 	- 	G4 	- 	G4 	- 	G4 	- 	G4 	- 	F4 	- 	F4 	- 	- 	- 	- 	^ 	^ 	^ 	G4 	- 	G4 	- 	G4 	- 	A4 	- 	G4 	- 	A4 	- 	^ 	D5 	- 	D5 	- 	D5 	- 	D5 	- 	G4 	- 	G4 	- 	- 	- 	- 	- 	^ 	G4 	- 	G4 	- 	G4 	- 	G4 	- 	F4 	- 	F4 	- 	- 	- 	- 	^ 	^ 	^ 	^ 	^ 	G4 	- 	C5 	- 	C5 	- 	- 	- 	B4 	- 	C5 	- 	- 	^ 	G4 	- 	A4 	- 	A4 	- 	G4 	- 	G4 	- 	G4 	- 	C5 	- 	C4 	- 	C4 	- 	E4 	- 	G4 	- 	G4 	- 	D4 	- 	D4 	- 	D4 	- 	C4 	- 	B3 	- 	C4 	- 	- 	- 	- 	- 	[SEP] 	E4 	- 	E4 	- 	E4 	- 	D4 	- 	E4 	- 	- 	^ 	E4 	- 	D4 	- 	E4 	- 	F4 	- 	E4 	- 	F4 	- 	G4 	- 	^ 	A4 	- 	F4 	- 	E4 	- 	D4 	- 	E4 	- 	F4 	- 	G4 	- 	A4 	- 	^ 	A4 	- 	D4 	- 	A4 	- 	G4 	- 	D4 	- 	- 	- 	^ 	^ 	^ 	^ 	E4 	- 	E4 	- 	E4 	- 	D4 	- 	E4 	- 	^ 	E4 	- 	D4 	- 	E4 	- 	F4 	- 	E4 	- 	F4 	- 	G4 	- 	^ 	A4 	- 	F4 	- 	E4 	- 	D4 	- 	E4 	- 	F4 	- 	G4 	- 	A4 	- 	^ 	A4 	- 	D4 	- 	A4 	- 	G4 	- 	D4 	- 	- 	^ 	^ 	^ 	^ 	E4 	- 	E4 	- 	E4 	- 	D4 	- 	E4 	- 	F4 	- 	E4 	- 	F4 	- 	G4 	- 	A4 	- 	F4 	- 	E4 	- 	D4 	- 	E4 	- 	F4 	- 	G4 	- 	A4 	- 	A4 	- 	D4 	- 	A4 	- 	G4 	- 	D4 	- 	- 	^ 	D4 	- 	E4 	- 	E4 	- 	E4 	- 	E4 	- 	E4 	- 	D4 	- 	E4 	- 	F4 	- 	E4 	- 	F4 	- 	G4 	- 	A4 	- 	F4 	- 	E4 	- 	D4 	- 	E4 	- 	F4 	- 	G4 	- 	A4 	- 	^ 	A4 	- 	D4 	- 	A4 	- 	G4 	- 	D4 	- 	- 	^ 	^ 	^ 	^ 	E4 	- 	E4 	- 	E4 	- 	D4 	- 	E4 	- 	E4 	- 	F4 	- 	E4 	- 	F4 	- 	G4 	- 	A4 	- 	F4 	- 	E4 	- 	D4 	- 	E4 	- 	F4 	- 	G4 	- 	A4 	- 	^ 	A4 	- 	D4 	- 	A4 	- 	G4 	- 	D4 	- 	- 	^ 	^ 	^ 	^ 	E4 	- 	E4 	- 	E4 	- 	D4 	- 	E4 	- 	F4 	- 	E4 	- 	F4 	- 	G4 	- 	A4 	- 	F4 	- 	E4 	- 	D4 	- 	E4 	- 	F4 	- 	G4 	- 	A4 	- 	^ 	A4 	- 	D4 	- 	A4 	- 	G4 	- 	D4 	- 	- 	- 	^ 	^ 	^ 	^ 	^ 	^ 	^ 	A4 	- 	A4 	- 	A4 	- 	A4 	- 	C5 	- 	C5 	- 	D5 	- 	E5 	- 	E5 	- 	B4 	- 	B4 	- 	G4 	- 	A4 	- 	- 	- 	F4 	- 	F4 	- 	- 	G4 	- 	A4 	- 	D5 	- 	C5 	- 	- 	- 	- 	- 	^ 	^ 	^ 	^ 	^ 	^ 	^ 	^ 	^ 	^ 	^ 	^ 	^ 	^ 	^ 	^ 	^')
    text2midi(r'C:\Users\15623\Desktop\test.txt',r'C:\Users\15623\Desktop')

#text2midi(r'C:\Users\15623\Desktop\test.txt',r'C:\Users\15623\Desktop')
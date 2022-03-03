import glob
import json

names =glob.glob("./data/wiki_zh/*/*")
for i, name in enumerate(names):
    musics=[]
    if i>10:
        break
    print(name)
    f=open(name,'r',encoding='utf-8')
    for line in f.readlines():
        dic=json.loads(line)
        musics.append(dic)
    print(musics)

    texts=[]
    for article in articles:
        text=article['text']
        texts.append(text)

print(texts)
fout=open('clean_out.txt',"w+",encoding="utf-8")
json.dump(texts,fout, ensure_ascii=False)
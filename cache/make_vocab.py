import argparse
import thulac
import json

from tqdm import tqdm
from tensorflow.keras.preprocessing.text import Tokenizer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_data_path', default='../data/train.json',type=str,required=False,help='原始训练语料')
    parser.add_argument('--vocab_file',default='vocab_50.txt',type=str, required=False, help='生成vocab链接')
    parser.add_argument('--vocab_size',default=295,type=int,required=False,help='词表大小')
    args = parser.parse_args()

    lac = thulac.thulac(seg_only=True)
    tokenizer = Tokenizer(num_words=args.vocab_size,
                          lower=False, split=" ",
                          char_level=False,
                          filters='!"$%&()*+,./:;=?@[\\]_`{|}~\t\n')
    print('args:\n' + args.__repr__())
    print('This script is extremely slow especially for large corpus. Take a break.')

    lines = []
    all_lines = []
    for line in open('data_50.txt'):
        line = line.rstrip()
        if not line:
            continue
        # 所有行的数据
        lines = ' ' + line
        all_lines.append(lines)
    #
    # f = open(args.raw_data_path, 'r')
    # # lines = json.load(f)
    # lines = f.readlines()
    # for i, line in enumerate(tqdm(lines)):
    #     lines[i] = lac.cut(line, text=True)
    print(all_lines)
    tokenizer.fit_on_texts(all_lines)
    vocab = list(tokenizer.index_word.values())
    pre = ['[SEP]', '[CLS]', '[MASK]', '[PAD]', '[UNK]']
    vocab = pre + vocab
    with open(args.vocab_file, 'w') as f:
        for word in vocab[:args.vocab_size + 5]:
            f.write(word + '\n')


if __name__ == "__main__":
    main()

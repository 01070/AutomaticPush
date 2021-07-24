import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,\
    QLineEdit, QLabel, QTextBrowser
from spider import *
import torch
from models.bert import Model, Config
import time

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
PAD, CLS = '[PAD]', '[CLS]'
label_dict = {0: '财经',
              1: '房产',
              2: '股票',
              3: '教育',
              4: '科技',
              5: '社会',
              6: '时政',
              7: '体育',
              8: '游戏',
              9: '娱乐'
}

def predict_run4push(sentence):
    config = Config()
    our_model = Model(config)
    save_dir = 'saved_dict/bert.ckpt'
    our_model.load_state_dict(torch.load(save_dir))
    sentences = load_sentence(config, sentence)
    outputs = our_model(sentences)
    predicts = torch.max(outputs.data, 1)[1].cpu().numpy().tolist()
    predict_labels = []
    predict_list = []
    for predict in predicts:
        predict_labels.append(label_dict[predict])
    for sent, lab in zip(sentence, predict_labels):
        predict_list.append(sent + ': ' + lab)
    return predict_list



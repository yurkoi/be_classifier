import re
import pandas as pd

pA, pNotA =0 ,0

SPAM = True
NOT_SPAM = False

spam_words = {}
non_spam_words = {}
pattern = re.compile('[a-zа-я0-9]+')

train_data = [  
    ['Купите новое чистящее средство', SPAM],   
    ['Купи мою новую книгу', SPAM],  
    ['Подари себе новый телефон', SPAM],
    ['Добро пожаловать и купите новый телевизор', SPAM],
    ['Привет давно не виделись', NOT_SPAM], 
    ['Довезем до аэропорта из пригорода всего за 399 рублей', SPAM], 
    ['Добро пожаловать в Мой Круг', NOT_SPAM],  
    ['Я все еще жду документы', NOT_SPAM],  
    ['Приглашаем на конференцию Data Science', NOT_SPAM],
    ['Потерял твой телефон напомни', NOT_SPAM],
    ['Порадуй своего питомца новым костюмом', SPAM]
]



def prepeare_text(value):
    return list(set(pattern.findall(value.lower())))

def return_dict(label):
    if label == SPAM:
        return spam_words
    else : 
        return non_spam_words

def calculate_word_frequencies(body,label):
    text = prepeare_text(body)
    dct = return_dict(label)
    for word in text:
        if len(word) < 3:
                continue
        if word in dct:
            dct[word] += 1
        else:
            dct[word] = 1

def train(data = train_data):
    global pA
    global pNotA
    
    for k in range(len(data)):
        calculate_word_frequencies(data[k][0],data[k][1])
    
    pA = sum(spam_words.values())/(sum(spam_words.values()) + sum(non_spam_words.values()))
    pNotA = sum(non_spam_words.values())/(sum(spam_words.values()) + sum(non_spam_words.values()))
    return

def calculate_P_Bi_A(word, label):
    dct = return_dict(label)
    p =1
    if word in dct:
        p = dct[word]/sum(dct.values())
    return p

def calculate_P_B_A(textt, label):
    #if type(textt) == str:
    text = prepeare_text(textt)
    
    #text = text.lower()
    if label == SPAM:
        sumW_probability = 1
        for word in text:
            sumW_probability*=calculate_P_Bi_A(word,label)
        return (pA*sumW_probability)
    else:
        sumW_probability = 1
        for word in text:
            sumW_probability*=calculate_P_Bi_A(word,label)
        return (pNotA*sumW_probability)

def classify(email):
    #text = email.lower()
    P_AB = calculate_P_B_A(email,SPAM)
    P_NAB =calculate_P_B_A(email,NOT_SPAM)
    if P_AB == P_NAB:
        return NOT_SPAM
    else:
        return (P_AB < P_NAB)
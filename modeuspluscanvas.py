from __future__ import unicode_literals
from datetime import datetime, timedelta

import json
import logging

from flask import Flask, request
application = Flask(__name__)

path = 'data.json'

with open(path, 'r', encoding="utf8") as f:
    data = json.loads(f.read())
    
today_string = data['ACCESS_INFO']['DATE']
today_day, today_month, today_year = map(int, today_string.split('.'))
today = datetime(today_year,today_month,today_day)
tomorrow_datetime = today + timedelta(days=1)
tomorrow_string = tomorrow_datetime.strftime("%d.%m.%Y")

days_dict = {}
for day in data['MODEUS_DAYS']:
    days_dict[day['DAY_NAME']] = day['DATE']

logging.basicConfig(level=logging.DEBUG)

@application.route("/post", methods=['POST'])

def main():
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

def handle_dialog(req, res):
    
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in [
                "Какие занятия сегодня?",
                "Что делать на завтра?",
                "Новые письма?",
            ] ]

    if req['session']['new']:
        
        res['response']['text'] = 'Добро пожаловать! Задавайте Ваш вопрос.'
        res['response']['buttons'] = suggests
        return

    # Analyzing words in the request:
    original_utterance_words = req['request']['nlu']['tokens']
    chosen_string = 'none'
    
    if (any(e in original_utterance_words for e in ('занятия','пары'))) or (all(d in original_utterance_words for d in ('что', 'у', 'меня'))):
        if 'сегодня' in original_utterance_words:
            chosen_string = today_string
        elif 'завтра' in original_utterance_words:
            chosen_string = tomorrow_string
        elif 'понедельник' in original_utterance_words:
            if 'следующий' in original_utterance_words:
                chosen_string = days_dict['NEXT_MONDAY']
            else:
                chosen_string = days_dict['MONDAY']
        elif 'вторник' in original_utterance_words:
            if 'следующий' in original_utterance_words:
                chosen_string = days_dict['NEXT_TUESDAY']
            else:
                chosen_string = days_dict['TUESDAY']
        elif 'среда' in original_utterance_words or 'среду' in original_utterance_words:
            if 'следующая' in original_utterance_words or 'следующую' in original_utterance_words:
                chosen_string = days_dict['NEXT_WEDNESDAY']
            else:
                chosen_string = days_dict['WEDNESDAY']
        elif 'четверг' in original_utterance_words:
            if 'следующий' in original_utterance_words:
                chosen_string = days_dict['NEXT_THURSDAY']
            else:
                chosen_string = days_dict['THURSDAY']
        elif 'пятница' in original_utterance_words or 'пятницу' in original_utterance_words:
            if 'следующая' in original_utterance_words or 'следующую' in original_utterance_words:
                chosen_string = days_dict['NEXT_FRIDAY']
            else:
                chosen_string = days_dict['FRIDAY']
        elif 'суббота' in original_utterance_words or 'субботу' in original_utterance_words:
            if 'следующая' in original_utterance_words or 'следующую' in original_utterance_words:
                chosen_string = days_dict['NEXT_SATURDAY']
            else:
                chosen_string = days_dict['SATURDAY']
        elif 'воскресенье' in original_utterance_words:
            if 'следующее' in original_utterance_words:
                chosen_string = days_dict['NEXT_SUNDAY']
            else:
                chosen_string = days_dict['SUNDAY']
                
        res['response']['text'] = prepare_line_modeus(chosen_string)
        return
    
    if any(e in original_utterance_words for e in ('делать', 'сделать', 'задания', 'задание', 'задали', 'домашка')):
        if 'сегодня' in original_utterance_words:
            chosen_string = 'TODAY'
        elif 'завтра' in original_utterance_words:
            chosen_string = 'TOMORROW'
        
        res['response']['text'] = prepare_line_canvas_assignments(chosen_string)
        return

    if any(e in original_utterance_words for e in ('письмо', 'письма', 'почта', 'почту', 'входящие', 'сообщения', 'написали')):
        res['response']['text'] = prepare_line_canvas_inbox()
        return
    
    # Error! Can't find that question!
    res['response']['text'] = 'Не поняла Ваш запрос.' 
    res['response']['buttons'] = suggests

def prepare_line_modeus(date_string):
    if date_string == 'none':
        return 'Пожалуйста, уточните день недели'
    line = ''
    for element in data['MODEUS_DAYS']:
            if element['DATE'] == date_string:
                if element['CLASSES'] != "none":
                    for a_class in element['CLASSES']:
                        line = line + 'В '+a_class['TIME']+' '+a_class['COURSE']+' у профессора '+a_class['PROFESSOR']+' в кабинете '+a_class['ROOM']+'\n\n'
                else:
                    line = 'В этот день пар нет.'
    return line

def prepare_line_canvas_assignments(day):
    if day == 'none':
        return 'Повторите запрос, уточнив, на сегодня или на завтра'
    line = ''
    for element in data['CANVAS_DASHBOARD_DAYS']:
        if element['DAY'] == day:
           if element['ASSIGNMENTS'] != "none":
               for assignment in element['ASSIGNMENTS']:
                   line = line + 'По ' + assignment['COURSE'] + ' задали ' + assignment['TITLE'] + '. Дэдлайн до ' + assignment['TIME'] + '\n\n'
           else:
               line = 'На этот день ничего не задано.'
    return line

def prepare_line_canvas_inbox():
    line = ''
    if data['CANVAS_INBOX_LETTERS'] != "none":
        for letter in data['CANVAS_INBOX_LETTERS']:
                        line = line + 'Письмо в диалоге ' + letter['AUTHOR'] + ' под названием ' + letter['TITLE'] + '. \nПисьмо начинается со слов ' + letter['SUMMARY'] + '\n\n'
    else:
        line = 'Новых писем нет.'
    return line

if __name__ == '__main__':
    application.run()
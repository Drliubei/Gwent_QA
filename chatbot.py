#!/usr/bin/env python3
# coding: utf-8


from classifier import *
from parse import *
from answer import *


class Chatbot:
    def __init__(self):
        self.classifier = Classifier()
        self.parser = Parser()
        self.answerer = Answerer()

    def chat_main(self, question):
        answer = '这是一条提示语句'
        classified = self.classifier.classify(question)
        if not classified:
            return answer
        request_cypher = self.parser.parser_main(classified)
        final_answer = self.answerer.search_main(request_cypher)
        if not final_answer:
            return answer
        else:
            return '\n'.join(final_answer)

if __name__ == '__main__':
    t = Chatbot()
    while 1:
        question = input('输入(quit退出)：')
        if(question == 'quit'):
            break;
        answer = t.chat_main(question)
        print(answer)
#!/usr/bin/env python3
# coding: utf-8

import re
import ahocorasick


class Classifier:
    def __init__(self):
        #字典
        self.card_words = [i.strip() for i in open('card.txt', encoding='UTF-8') if i.strip()]
        self.provision_words = ['费用', '花费', '消耗', '人口']
        self.power_words = ['战力', '点数', '血量']
        self.armor_words = ['护甲']
        self.faction_words = ['阵营']
        self.color_words = ['颜色']
            #['金色', '铜色', '金卡', '铜卡', '领袖']
        self.type_words = ['类型', '类别', '种类']
            #['单位', '法术', '神器', '能力']
        self.rarity_words = ['稀有度']
        self.availability_words = ['扩展包', '来源', '获取途径']
        self.ability_words = ['特效', '能力', '描述']
        self.flavor_words = ['背景', '风味', '故事']
        self.category_words = ['种类', '标签']
        self.keyword_words = ['关键词', '关键字']

        self.faction_SK_words = ['群岛', '史凯利杰']
        self.faction_NR_words = ['北方', '北方领域']
        self.faction_NG_words = ['帝国', '尼弗迦德']
        self.faction_ST_words = ['非人', '松鼠党']
        self.faction_MO_words = ['怪物', '怪兽']
        self.faction_SY_words = ['辛迪加']
        self.faction_NE_words = ['中立']
        self.region_words = set(self.card_words + self.provision_words + self.power_words + self.armor_words +
                                self.faction_words + self.color_words + self.type_words + self.availability_words +
                                self.ability_words + self.flavor_words + self.category_words + self.keyword_words +
                                self.faction_SK_words + self.faction_NR_words + self.faction_NG_words +
                                self.faction_ST_words + self.faction_SY_words + self.faction_NE_words)
        self.region_tree = self.build_actree(list(self.region_words))
        self.wdtype_dict = self.build_wdtype_dict()

    def test(self):
        return self.card_words

    def classify(self, question):
        data = {}
        card_dicts = self.check_card(question)
        if not card_dicts:
            return {}
        data['dicts'] = card_dicts
        types = []
        for type_ in card_dicts.values():
            types += type_
        question_type = 'others'
        question_types = []
        if self.check_words(self.card_words, question):
            if self.check_words(self.provision_words, question):
                question_type = 'card_provision_type'
                question_types.append(question_type)
            if self.check_words(self.armor_words, question):
                question_type = 'card_armor_type'
                question_types.append(question_type)
            if self.check_words(self.power_words, question):
                question_type = 'card_power_type'
                question_types.append(question_type)
            if self.check_words(self.faction_words, question):
                question_type = 'card_faction_type'
                question_types.append(question_type)
            if self.check_words(self.color_words, question):
                question_type = 'card_color_type'
                question_types.append(question_type)
            if self.check_words(self.rarity_words, question):
                question_type = 'card_rarity_type'
                question_types.append(question_type)
            if self.check_words(self.type_words, question):
                question_type = 'card_type_type'
                question_types.append(question_type)
            if self.check_words(self.availability_words, question):
                question_type = 'card_availability_type'
                question_types.append(question_type)
            if self.check_words(self.ability_words, question):
                question_type = 'card_ability_type'
                question_types.append(question_type)
            if self.check_words(self.flavor_words, question):
                question_type = 'card_flavor_type'
                question_types.append(question_type)
            if self.check_words(self.category_words, question):
                question_type = 'card_category_type'
                question_types.append(question_type)
            if self.check_words(self.keyword_words, question):
                question_type = 'card_keyword_type'
                question_types.append(question_type)

        elif self.check_words(self.provision_words, question):
            question_type = 'provision_type'
            question_types.append(question_type)
            number = re.sub("\D", '', question)
            if number != '':
                data['number'] = number

        elif self.check_words(self.armor_words, question):
            question_type = 'armor_type'
            question_types.append(question_type)
            number = re.sub("\D", '', question)
            if number != '':
                data['number'] = number

        elif self.check_words(self.power_words, question):
            question_type = 'power_type'
            question_types.append(question_type)
            number = re.sub("\D", '', question)
            if number != '':
                data['number'] = number

        elif self.check_words(self.faction_ST_words, question):
            question_type = 'faction_ST_type'
            question_types.append(question_type)

        elif self.check_words(self.faction_SK_words, question):
            question_type = 'faction_SK_type'
            question_types.append(question_type)

        elif self.check_words(self.faction_SY_words, question):
            question_type = 'faction_SY_type'
            question_types.append(question_type)

        elif self.check_words(self.faction_MO_words, question):
            question_type = 'faction_MO_type'
            question_types.append(question_type)

        elif self.check_words(self.faction_NR_words, question):
            question_type = 'faction_NR_type'
            question_types.append(question_type)

        elif self.check_words(self.faction_NG_words, question):
            question_type = 'faction_NG_type'
            question_types.append(question_type)

        elif self.check_words(self.faction_NE_words, question):
            question_type = 'faction_NE_type'
            question_types.append(question_type)

        data['question_types'] = question_types
        return data

    def check_words(self, words, sent):
        for word in words:
            if word in sent:
                return True
        return False

    def check_card(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.card_words:
                wd_dict[wd].append('card')
            if wd in self.provision_words:
                wd_dict[wd].append('provision')
            if wd in self.armor_words:
                wd_dict[wd].append('armor')
            if wd in self.power_words:
                wd_dict[wd].append('power')
            if wd in self.color_words:
                wd_dict[wd].append('color')
            if wd in self.rarity_words:
                wd_dict[wd].append('rarity')
            if wd in self.availability_words:
                wd_dict[wd].append('availability')
            if wd in self.type_words:
                wd_dict[wd].append('type')
            if wd in self.faction_words:
                wd_dict[wd].append('faction')
            if wd in self.faction_SK_words:
                wd_dict[wd].append('faction_SK')
            if wd in self.faction_ST_words:
                wd_dict[wd].append('faction_ST')
            if wd in self.faction_MO_words:
                wd_dict[wd].append('faction_MO')
            if wd in self.faction_SY_words:
                wd_dict[wd].append('faction_SY')
            if wd in self.faction_NR_words:
                wd_dict[wd].append('faction_NR')
            if wd in self.faction_NE_words:
                wd_dict[wd].append('faction_NE')
            if wd in self.faction_NG_words:
                wd_dict[wd].append('faction_NG')
        return wd_dict


if __name__ == '__main__':
    a = Classifier()
    while 1:
        q = input('input a question')
        print(a.classify(q))

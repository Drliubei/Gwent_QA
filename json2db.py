#!/usr/bin/env python3
# coding: utf-8

import os
import json
from py2neo import Graph, Node, Relationship


class GwentJson:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # self.data_path = os.path.join(cur_dir, 'data/gwent_api_en.json')
        # 英文文件
        self.data_path = os.path.join(cur_dir, 'data/gwent_api_cn.json')
        # 中文文件
        self.g = Graph(
            "http://localhost:7474",
            user="neo4j",
            password="zykbei")

    '''读取文件'''
    def read_nodes(self):
        Cards = []  # 卡牌 存储卡牌名字

        card_info = []  # 卡牌信息 存储解析完的json dict

        count = 0
        for data in open(self.data_path, encoding='UTF-8'):
            card_dict = {}
            count += 1
            print('read:', count)
            data_json = json.loads(data)
            card = data_json['name']
            card_dict['name'] = card
            Cards.append(card)

            card_dict['id'] = data_json['id']
            card_dict['category'] = data_json['category']
            card_dict['category_id'] = data_json['categoryId']
            card_dict['faction'] = data_json['faction']
            card_dict['faction_secondary'] = data_json['factionSecondary']
            card_dict['keyword'] = data_json['keyword']
            card_dict['related'] = data_json['related']
            card_dict['power'] = data_json['power']
            card_dict['armor'] = data_json['armor']
            card_dict['provision'] = data_json['provision']
            card_dict['color'] = data_json['color']
            card_dict['type'] = data_json['type']
            card_dict['availability'] = data_json['availability']
            card_dict['rarity'] = data_json['rarity']
            card_dict['art_id'] = data_json['artid']
            card_dict['ability'] = data_json['ability']
            card_dict['ability_html'] = data_json['abilityHMTL']
            card_dict['flavor'] = data_json['flavor']

            card_info.append(card_dict)

        return Cards, card_info

    '''创建卡牌节点'''
    def create_cards_nodes(self, cards_info):
        count = 0
        for card_dict in cards_info:
            node = Node("Cards", name=card_dict['name'], id=card_dict['id'],
                        category=card_dict['category'], categoryID=card_dict['category_id'],
                        faction=card_dict['faction'], factionSecondary=card_dict['faction_secondary'],
                        keyword=card_dict['keyword'], related=card_dict['related'],
                        power=card_dict['power'], armor=card_dict['armor'],
                        provision=card_dict['provision'], color=card_dict['color'],
                        type=card_dict['type'], availability=card_dict['availability'],
                        rarity=card_dict['rarity'], artid=card_dict['art_id'],
                        ability=card_dict['ability'], abilityHTML=card_dict['ability_html'],
                        flavor=card_dict['flavor']
                        )
            self.g.create(node)
            count += 1
            print('create:', count)
        return

    def create_relationship(self):
        minV = 112101
        maxV = 202577
        # No of first card and last card
        i = minV
        related = ''
        while i <= maxV:
            print(i)
            if self.g.run("MATCH (m:Cards) where m.id = '{0}' return m".format(i)).data():
                if self.g.run("MATCH (m:Cards) where m.id = '{0}' return m.related".format(i)).data()[0]['m.related']:
                    related = self.g.run("MATCH (m:Cards) where m.id = '{0}' return m.related".format(i)).data()
                    relatedList = related[0]['m.related'].split(', ')
                    for n in relatedList:
                        self.g.run("MATCH (n:Cards),(m:Cards)  where n.id = '{0}' and m.id = '{1}'\
                                   CREATE  (n)-[r:related]->(m)".format(i, n))

            i += 1

    '''导出数据'''
    def export_data(self):
        Cards, card_info = self.read_nodes()
        f_card = open('card.txt', 'w', encoding='UTF-8')
        f_card.write('\n'.join(list(Cards)))
        f_card.close()
        return


if __name__ == '__main__':
    handler = GwentJson()
    cards, card_info = handler.read_nodes()
    handler.export_data()
    handler.create_cards_nodes(card_info)
    handler.create_relationship()

#!/usr/bin/env python3
# coding: utf-8


from classifier import *


class Parser:
    # 将输入转化为查询语句
    def __init__(self):
        return

    def build_entity_dict(self, dicts):
        entity_dict = {}
        for dict, types in dicts.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [dict]
                else:
                    entity_dict[type].append(dict)

        return entity_dict

    # ???

    def parser_main(self, data):
        dicts = data['dicts']
        entity_dict = self.build_entity_dict(dicts)
        question_types = data['question_types']
        cyphers = []
        for question_type in question_types:
            cypher_ = {'question_type': question_type}
            cypher = []
            if question_type in {'card_provision_type', 'card_armor_type', 'card_power_type', 'card_faction_type',
                                 'card_color_type', 'card_type_type', 'card_rarity_type', 'card_availability_type',
                                 'card_ability_type', 'card_flavor_type', 'card_category_type'}:
                cypher = self.cypher_transfer(question_type, entity_dict.get('card'))

            elif question_type in {'provision_type', 'armor_type', 'power_type'}:
                cypher = self.cypher_transfer(question_type, data['number'])

            elif question_type == 'faction_type':
                cypher = self.cypher_transfer(question_type, entity_dict.get('faction'))

            elif question_type in {'faction_ST_type', 'faction_NR_type', 'faction_NG_type', 'faction_MO_type',
                                   'faction_SY_type', 'faction_NE_type', 'faction_SK_type'}:
                cypher = self.cypher_transfer(question_type, 25)

            elif question_type == 'ability_type':
                cypher = self.cypher_transfer(question_type, '1')

            if cypher:
                cypher_['cypher'] = cypher

            cyphers.append(cypher_)

        return cyphers

    def cypher_transfer(self, question_type, entities):
        if not entities:
            return []

        cypher = []

        if question_type == 'card_provision_type':
            cypher = ["MATCH (m:Cards) where m.name = '{0}' return m.name, m.provision".format(i) for i in entities]

        elif question_type == 'card_armor_type':
            cypher = ["MATCH (m:Cards) where m.name = '{0}' return m.name, m.armor".format(i) for i in entities]

        elif question_type == 'card_power_type':
            cypher = ["MATCH (m:Cards) where m.name = '{0}' return m.name, m.power".format(i) for i in entities]

        elif question_type == 'card_faction_type':
            cypher = ["MATCH (m:Cards) where m.name = '{0}' return m.name, m.faction".format(i) for i in entities]

        elif question_type == 'card_color_type':
            cypher = ["MATCH (m:Cards) where m.name = '{0}' return m.name, m.color".format(i) for i in entities]

        elif question_type == 'card_type_type':
            cypher = ["MATCH (m:Cards) where m.name = '{0}' return m.name, m.type".format(i) for i in entities]

        elif question_type == 'card_rarity_type':
            cypher = ["MATCH (m:Cards) where m.name = '{0}' return m.name, m.rarity".format(i) for i in entities]

        elif question_type == 'card_availability_type':
            cypher = ["MATCH (m:Cards) where m.name = '{0}' return m.name, m.availability".format(i) for i in entities]

        elif question_type == 'card_ability_type':
            cypher = ["MATCH (m:Cards) where m.name = '{0}' return m.name, m.ability".format(i) for i in entities]

        elif question_type == 'card_flavor_type':
            cypher = ["MATCH (m:Cards) where m.name = '{0}' return m.name, m.flavor".format(i) for i in entities]

        elif question_type == 'card_category_type':
            cypher = ["MATCH (m:Cards) where m.name = '{0}' return m.name, m.category".format(i) for i in entities]

        elif question_type == 'provision_type':
            cypher = ["MATCH (m:Cards) where m.provision = '{0}' return m.name".format(i) for i in entities]

        elif question_type == 'armor_type':
            cypher = ["MATCH (m:Cards) where m.armor = '{0}' return m.name".format(i) for i in entities]

        elif question_type == 'power_type':
            cypher = ["MATCH (m:Cards) where m.power = '{0}' return m.name".format(i) for i in entities]

        elif question_type == 'faction_SY_type':
            cypher = ["MATCH (m:Cards) where m.faction = 'Syndicate' return m.name LIMIT 25"]

        elif question_type == 'faction_SK_type':
            cypher = ["MATCH (m:Cards) where m.faction = 'Skellige' return m.name LIMIT 25"]

        elif question_type == 'faction_ST_type':
            cypher = ["MATCH (m:Cards) where m.faction = 'Scoiatael' return m.name LIMIT 25"]

        elif question_type == 'faction_MO_type':
            cypher = ["MATCH (m:Cards) where m.faction = 'Monster' return m.name LIMIT 25"]

        elif question_type == 'faction_NR_type':
            cypher = ["MATCH (m:Cards) where m.faction = 'Northern Realms' return m.name LIMIT 25"]

        elif question_type == 'faction_NG_type':
            cypher = ["MATCH (m:Cards) where m.faction = 'Nilfgaard' return m.name LIMIT 25"]

        elif question_type == 'faction_NE_type':
            cypher = ["MATCH (m:Cards) where m.faction = 'Neutral' return m.name LIMIT 25"]

        return cypher


if __name__ == '__main__':
    p = Parser()
    a = Classifier()
    while 1:
        q = input('input a question')
        b = a.classify(q)
        print(b)
        print(p.parser_main(b))

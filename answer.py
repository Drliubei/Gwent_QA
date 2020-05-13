from py2neo import *


class Answerer:
    def __init__(self):
        self.g = Graph(
            "http://localhost:7474",
            user='neo4j',
            password='zykbei'
        )
        self.num_limit = 25

    def search_main(self, cyphers):
        final_answers = []
        for cypher_ in cyphers:
            question_type = cypher_['question_type']
            queries = cypher_['cypher']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''

        if question_type == 'card_provision_type':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.provision']
            final_answer = '{0}的人口为{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        if question_type == 'card_power_type':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.power']
            final_answer = '{0}的战力为{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        if question_type == 'card_armor_type':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.armor']
            final_answer = '{0}的护甲为{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        if question_type == 'card_faction_type':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.faction']
            faction = ''
            if subject == 'Skellige':
                faction = '史凯利杰'
            elif subject == 'Monster':
                faction = '怪兽'
            elif subject == 'Scoiatael':
                faction = '松鼠党'
            elif subject == 'Northern Realms':
                faction = '北方领域'
            elif subject == 'Nilfgaard':
                faction = '尼弗迦德'
            elif subject == 'Neutral':
                faction = '中立'
            final_answer = '{0}的阵营为{1}'.format('；'.join(list(set(desc))[:self.num_limit]), faction)

        if question_type == 'card_color_type':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.color']
            color = ''
            if subject == 'Gold':
                color = '金色'
            elif subject == 'Bronze':
                color = '铜色'
            elif subject == 'Leader':
                color = '领袖'
            final_answer = '{0}的颜色为{1}'.format('；'.join(list(set(desc))[:self.num_limit]), color)

        if question_type == 'card_type_type':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.type']
            type = ''
            if subject == 'Unit':
                type = '单位'
            elif subject == 'Special':
                type = '特殊'
            elif subject == 'Artifact':
                type = '神器'
            elif subject == 'Ability':
                type = '领袖'
            elif subject == 'Stratagem':
                type = '战术'
            final_answer = '{0}的类型为{1}'.format('；'.join(list(set(desc))[:self.num_limit]), type)

        if question_type == 'card_rarity_type':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.rarity']
            rarity = ''
            if subject == 'Legendary':
                rarity = '传奇'
            if subject == 'Epic':
                rarity = '史诗'
            if subject == 'Rare':
                rarity = '稀有'
            if subject == 'Common':
                rarity = '普通'
            final_answer = '{0}的稀有度为{1}'.format('；'.join(list(set(desc))[:self.num_limit]), rarity)

        if question_type == 'card_availability_type':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.availability']
            availability = ''
            if subject == 'BaseSet':
                availability = '基础'
            elif subject == 'Unmillable':
                availability = '不可分解'
            elif subject == 'Iron Judgement':
                availability = '钢铁审判'
            elif subject == 'CrimsonCurse':
                availability = '猩红诅咒'
            elif subject == 'Merchants of Ofir':
                availability = '异域游商'
            elif subject == 'NonOwnable':
                availability = '衍生物'
            final_answer = '{0}的扩展包为{1}'.format('；'.join(list(set(desc))[:self.num_limit]), availability)

        if question_type == 'card_ability_type':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.ability']
            final_answer = '{0}的能力为：{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        if question_type == 'card_flavor_type':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.flavor']
            final_answer = '{0}的背景为：{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        if question_type == 'faction_ST_type':
            desc = [i['m.name'] for i in answers]
            final_answer = '松鼠党阵营的卡牌名称为：{0}（只显示25个）'.format('；'.join(list(set(desc))[:self.num_limit]))

        if question_type == 'faction_SK_type':
            desc = [i['m.name'] for i in answers]
            final_answer = '史凯利杰阵营的卡牌名称为：{0}（只显示25个）'.format('；'.join(list(set(desc))[:self.num_limit]))

        if question_type == 'faction_SY_type':
            desc = [i['m.name'] for i in answers]
            final_answer = '辛迪加阵营的卡牌名称为：{0}（只显示25个）'.format('；'.join(list(set(desc))[:self.num_limit]))

        if question_type == 'faction_NR_type':
            desc = [i['m.name'] for i in answers]
            final_answer = '北方领域阵营的卡牌名称为：{0}（只显示25个）'.format('；'.join(list(set(desc))[:self.num_limit]))

        if question_type == 'faction_MO_type':
            desc = [i['m.name'] for i in answers]
            final_answer = '怪兽阵营的卡牌名称为：{0}（只显示25个）'.format('；'.join(list(set(desc))[:self.num_limit]))

        if question_type == 'faction_NG_type':
            desc = [i['m.name'] for i in answers]
            final_answer = '尼弗迦德阵营的卡牌名称为：{0}（只显示25个）'.format('；'.join(list(set(desc))[:self.num_limit]))

        if question_type == 'faction_NE_type':
            desc = [i['m.name'] for i in answers]
            final_answer = '中立的卡牌名称为：{0}（只显示25个）'.format('；'.join(list(set(desc))[:self.num_limit]))


        return final_answer

if __name__ == '__main__':
    searcher = Answerer()
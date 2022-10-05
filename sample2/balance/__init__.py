from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'balance'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField()

    pass


# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['age']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            random_number=1001,
        )

    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            age=player.age
        )
    pass


page_sequence = [MyPage , Results]

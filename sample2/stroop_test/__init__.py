from otree.api import *
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'stroop_test'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    MAX_OBJECT_PER_BLOCK = {1: "max_number_of_objects_in_block_1",
                            2: "max_number_of_objects_in_block_2",
                            3: "max_number_of_objects_in_block_3"}

    NUMBER_OF_TRIALS = {1: "number_of_trials_in_block_1",
                        2: "number_of_trials_in_block_2",
                        3: "number_of_trials_in_block_3"}


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    trial_block = models.IntegerField(initial=0)
    trial_max_number_of_objects = models.IntegerField()
    pass


class TrialInfo(ExtraModel):
    trial_block = models.IntegerField()
    trial_character = models.StringField()
    trial_length = models.IntegerField()
    trial_response = models.StringField()
    trial_correct = models.BooleanField()
    trial_reaction_time = models.IntegerField()
    player = models.Link(Player)


# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['trial_max_number_of_objects']

    @staticmethod
    def generate_trial_list(player):
        trial_list = []
        number_of_trials = player.session.config[C.NUMBER_OF_TRIALS[player.participant.stroop_test_block_number]]
        if player.participant.stroop_test_block_number == 1:

            for i in range(number_of_trials):
                # randomly select player.trial_character from 'O' and 'X'
                trial_character = random.choice(['O', 'X'])
                # randomly select length from 1 to max_number_of_objects_in_block_1
                trial_length = random.randint(1, player.trial_max_number_of_objects)
                while len(trial_list) > 0 and (trial_character, trial_length) == tuple(trial_list[-1].values()):
                    trial_character = random.choice(['O', 'X'])
                    trial_length = random.randint(1, player.trial_max_number_of_objects)
                # generate player.trial_sequence
                trial_list.append({'character': trial_character, 'length': trial_length})

        elif player.participant.stroop_test_block_number == 2:
            # randomly select length from 1 to max_number_of_objects_in_block_1
            for i in range(number_of_trials):
                trial_length = random.randint(1, player.trial_max_number_of_objects)
                # set the character to the string of length
                trial_character = str(trial_length)

                while len(trial_list) > 0 and(trial_character, trial_length) == tuple(trial_list[-1].values()):
                    trial_length = random.randint(1, player.trial_max_number_of_objects)
                    trial_character = str(trial_length)

                trial_list.append({'character': trial_character, 'length': trial_length})

        elif player.participant.stroop_test_block_number == 3:
            # randomly select length from 1 to max_number_of_objects_in_block_1
            for i in range(number_of_trials):
                trial_length = random.randint(1, player.trial_max_number_of_objects)

                # randomly select player.trial_character from 1 to max_number_of_objects_in_block_1
                # and convert to string
                # if matches length, select again until different
                trial_character = str(
                    random.randint(1, player.trial_max_number_of_objects))
                while trial_character == str(trial_length):
                    trial_character = str(
                        random.randint(1, player.trial_max_number_of_objects))
                trial_list.append({'character': trial_character, 'length': trial_length})

        return dict(type='sequence', sequence=trial_list)

    @staticmethod
    def is_displayed(player: Player):
        # set block

        if "stroop_test_block_number" not in player.participant.vars:
            player.participant.stroop_test_block_number = 1
        # set maximum number of objects
        if player.participant.stroop_test_block_number > 3:
            return False

        player.trial_max_number_of_objects = player.session.config[C.MAX_OBJECT_PER_BLOCK[player.participant.stroop_test_block_number]]

        return True

    @staticmethod
    def save_results(player: Player, results):

        block = player.participant.stroop_test_block_number

        for trial in results:
            character = None
            length = None
            response = None
            correct = None
            reaction_time = None

            if "character" in trial:
                character = trial["character"]

            if "length" in trial:
                length = trial["length"]

            if "response" in trial:
                response = trial["response"]

            if "correct" in trial:
                correct = trial["correct"]
                if correct:
                    player.payoff += 1

            if "reaction_time" in trial:
                reaction_time = trial["reaction_time"]

            TrialInfo.create(trial_block=block,
                             trial_character=character,
                             trial_length=length,
                             trial_response=response,
                             trial_correct=correct,
                             trial_reaction_time=reaction_time,
                             player=player)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pass

    @staticmethod
    def live_method(player: Player, data):
        sending_data = None
        if data['type'] == 'next':
            sending_data = MyPage.generate_trial_list(player)
            pass

        if data['type'] == 'result':
            if 'results' in data:
                MyPage.save_results(player, data['results'])

                # Next block
                player.participant.stroop_test_block_number += 1

        return {player.id_in_group: sending_data}
        pass


class TimeoutPage(Page):
    timeout_seconds = 3


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [TimeoutPage, MyPage, TimeoutPage, MyPage, TimeoutPage, MyPage, ResultsWaitPage, Results]


def custom_export(players):
    # header row
    yield ['session_code',
           'participant_code',
           'id_in_group',
           'payoff',
           'block',
           'character',
           'length',
           'response',
           'correct',
           'reaction_time']

    for trial in TrialInfo.filter():
        yield [trial.player.session.code,
               trial.player.participant.code,
               trial.player.id_in_group,
               trial.player.payoff,
               trial.trial_block,
               trial.trial_character,
               trial.trial_length,
               trial.trial_response,
               trial.trial_correct,
               trial.trial_reaction_time]

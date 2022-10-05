from otree.api import *
from otree.session import *
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'hearts_and_flowers'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    STAGE_MAPPING = {1: "number_of_hearts_in_block_1_round_1",
                     2: "number_of_hearts_in_block_1_round_2",
                     3: "number_of_hearts_in_block_1_round_3",
                     4: "number_of_hearts_in_block_2_round_1",
                     5: "number_of_hearts_in_block_2_round_2",
                     6: "number_of_hearts_in_block_2_round_3",
                     7: "number_of_hearts_in_block_3_round_1",
                     8: "number_of_hearts_in_block_3_round_2",
                     9: "number_of_hearts_in_block_3_round_3"}

    STAGE_PASSING_MAPPING = {1: "number_of_hearts_in_block_1_round_1_passing",
                             2: "number_of_hearts_in_block_1_round_2_passing",
                             3: "number_of_hearts_in_block_1_round_3_passing",
                             4: "number_of_hearts_in_block_2_round_1_passing",
                             5: "number_of_hearts_in_block_2_round_2_passing",
                             6: "number_of_hearts_in_block_2_round_3_passing",
                             7: "number_of_hearts_in_block_3_round_1_passing",
                             8: "number_of_hearts_in_block_3_round_2_passing",
                             9: "number_of_hearts_in_block_3_round_3_passing"}

    STAGE_APPEARANCE_INTERVAL_MAPPING = {1: "number_of_hearts_in_block_1_round_1_appearance_interval",
                                         2: "number_of_hearts_in_block_1_round_2_appearance_interval",
                                         3: "number_of_hearts_in_block_1_round_3_appearance_interval",
                                         4: "number_of_hearts_in_block_2_round_1_appearance_interval",
                                         5: "number_of_hearts_in_block_2_round_2_appearance_interval",
                                         6: "number_of_hearts_in_block_2_round_3_appearance_interval",
                                         7: "number_of_hearts_in_block_3_round_1_appearance_interval",
                                         8: "number_of_hearts_in_block_3_round_2_appearance_interval",
                                         9: "number_of_hearts_in_block_3_round_3_appearance_interval"}


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class SystemInfo(ExtraModel):
    # System
    player = models.Link(Player)
    target = models.StringField()
    side = models.StringField()
    inter_stimuli_interval = models.IntegerField()

    # def custom_export(players):
    #     return ['target', 'side', 'inter_stimuli_interval']

    pass


class UserInfo(ExtraModel):
    # User
    player = models.Link(Player)
    reaction_time = models.IntegerField()
    keypress = models.StringField()
    correct = models.BooleanField()
    pass


# PAGES
class MyPage(Page):

    # create a static method that accept  a number n and a boolean value repeat_h and a boolean value repeat_f
    # and generate a list of h with n elements if repeat_h is True
    # and generate a list of f with n elements if repeat_f is True
    # and generate a list of h and f randomly with n elements if repeat_h and repeat_f are False
    @staticmethod
    def generate_image_list(n, repeat_h=False, repeat_f=False, half_half=False):
        if repeat_h:
            return ['heart'] * n
        elif repeat_f:
            return ['flower'] * n
        elif half_half:
            if n % 2 != 0:
                raise Exception("n must be even if you want a half half")
            n = int(n / 2)
            unsorted_list = ['heart'] * n + ['flower'] * n
            random.shuffle(unsorted_list)
            return unsorted_list
        else:
            # sample a random list of h and f with n elements
            return random.choices(['heart', 'flower'], k=n)

    @staticmethod
    def generate_side_list(n):
        return random.choices(['left', 'right'], k=n)

    pass

    @staticmethod
    def show_instruction():
        return dict(status='ok', type='instruction')

    @staticmethod
    def generate(player: Player):
        # For temporary storage of the list of images
        # and the sides in case subject accidentally refresh the page
        stage_name = C.STAGE_MAPPING[player.participant.hf_current_stage]
        if 0 < player.participant.hf_current_stage < 4:
            player.participant.hf_candidates = MyPage.generate_image_list(
                player.session.config[stage_name],
                repeat_h=True)
        elif 3 < player.participant.hf_current_stage < 7:
            player.participant.hf_candidates = MyPage.generate_image_list(
                player.session.config[stage_name],
                repeat_f=True)
        elif player.participant.hf_current_stage == 7:
            player.participant.hf_candidates = MyPage.generate_image_list(
                player.session.config[stage_name], half_half=True)
        else:
            player.participant.hf_candidates = MyPage.generate_image_list(
                player.session.config[stage_name])

        # print candidates
        print(player.participant.hf_candidates)

        # Generate the list of sides
        player.participant.hf_sides = MyPage.generate_side_list(
            player.session.config[stage_name])

        # print sides
        print(player.participant.hf_sides)

        # Get the passing threshold
        player.participant.hf_passing = player.session.config[
            C.STAGE_PASSING_MAPPING[player.participant.hf_current_stage]]
        player.participant.hf_number_passed = 1

        return MyPage.give_next_target(player)

    @staticmethod
    def save(player: Player, data):
        # print participant number passed
        # print("Passed", player.participant.number_passed)

        # data.target is the target image
        keypress = None
        reaction_time = None
        correct = None

        if not data['timeout']:
            keypress = data['keypress']
            reaction_time = data['reaction_time']
            correct = data['correct']

            if reaction_time < 0.001 * player.session.config['minimum_keypress_interval']:
                correct = False

            if correct:
                player.participant.hf_number_passed += 1

        print("Now Passed:", player.participant.hf_number_passed)

        # Record the user input, correctness, reaction time, timeout status in the database
        UserInfo.create(player=player, keypress=keypress, correct=correct, reaction_time=reaction_time)

    @staticmethod
    def give_next_target(player: Player):
        # if not player.participant.candidates or not player.participant.sides:
        #     sending_data = dict(status="ok")
        #     return {player.id_in_group: sending_data}

        # let target and side to be the first element in the list and remove it from the list
        target = player.participant.hf_candidates.pop(0)
        side = player.participant.hf_sides.pop(0)

        # Get inter-stimuli interval
        inter_stimuli_interval = player.session.config['inter_stimuli_interval']

        # Get appearance time
        appearance_interval = player.session.config[
            C.STAGE_APPEARANCE_INTERVAL_MAPPING[player.participant.hf_current_stage]]

        # Record the target and side in the database
        SystemInfo.create(player=player, target=target, side=side, inter_stimuli_interval=inter_stimuli_interval)
        return dict(status="ok",
                    type="target",
                    target=target,
                    side=side,
                    inter_stimuli_interval=inter_stimuli_interval,
                    appearance_interval=appearance_interval)

    @staticmethod
    def is_displayed(player: Player):

        # Initialize participant current stage to 1
        player.participant.hf_current_stage = 1
        print(player.participant.vars)
        return True

    @staticmethod
    def vars_for_template(player: Player):
        return {
        }

    @staticmethod
    def live_method(player: Player, data):
        print(data)
        # First time access
        if data['type'] == 'init':
            return MyPage.show_instruction()

        if data['type'] == 'generate':
            sending_data = MyPage.generate(player)
            return {player.id_in_group: sending_data}

        if data['type'] == 'next':
            # Save the user input
            MyPage.save(player, data)

            # If the image list is empty, check if the subject has passed the passing threshold
            # If the subject has passed the passing threshold, go to the next stage
            # If the subject has not passed the passing threshold, generate
            # In either case, reset the counter
            if not player.participant.hf_candidates:
                if player.participant.hf_number_passed >= player.participant.hf_passing:
                    player.participant.hf_current_stage += 1
                    # print("Next stage", player.participant.hf_current_stage)
                    if player.participant.hf_current_stage > 9:
                        return {player.id_in_group: dict(status="ok", type="submit")}

                sending_data = MyPage.show_instruction()
                return {player.id_in_group: sending_data}

            # Record and generate the next target and side
            sending_data = MyPage.give_next_target(player)
            return {player.id_in_group: sending_data}

    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]


def custom_export(players):
    # header row
    yield ['session_code', 'participant_code', 'round_number', 'id_in_group', 'payoff', 'target', 'position', 'isi', 'keypress', 'correct', 'reaction_time']
    for system, user in zip(SystemInfo.filter(), UserInfo.filter()):
        yield [system.player.session.code, system.player.participant.code, system.player.round_number,
               system.player.id_in_group, system.player.payoff, system.target, system.side,
               system.inter_stimuli_interval, user.keypress, user.correct, user.reaction_time]

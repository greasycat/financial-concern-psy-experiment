from os import environ

SESSION_CONFIGS = [
    dict(
        name='hearts_and_flowers',
        app_sequence=['hearts_and_flowers'],
        num_demo_participants=3,

        inter_stimuli_interval=600,
        appearance_interval=700,
        timeout_interval=150,
        minimum_keypress_interval=150,
        point_per_success=1,

        number_of_hearts_in_block_1_round_1=4,
        number_of_hearts_in_block_1_round_2=10,
        number_of_hearts_in_block_1_round_3=20,
        number_of_hearts_in_block_2_round_1=4,
        number_of_hearts_in_block_2_round_2=10,
        number_of_hearts_in_block_2_round_3=20,
        number_of_hearts_in_block_3_round_1=6,
        number_of_hearts_in_block_3_round_2=20,
        number_of_hearts_in_block_3_round_3=40,

        number_of_hearts_in_block_1_round_1_passing=4,
        number_of_hearts_in_block_1_round_2_passing=5,
        number_of_hearts_in_block_1_round_3_passing=0,
        number_of_hearts_in_block_2_round_1_passing=4,
        number_of_hearts_in_block_2_round_2_passing=5,
        number_of_hearts_in_block_2_round_3_passing=0,
        number_of_hearts_in_block_3_round_1_passing=6,
        number_of_hearts_in_block_3_round_2_passing=10,
        number_of_hearts_in_block_3_round_3_passing=0,

        number_of_hearts_in_block_1_round_1_appearance_interval=60000,
        number_of_hearts_in_block_1_round_2_appearance_interval=750,
        number_of_hearts_in_block_1_round_3_appearance_interval=750,
        number_of_hearts_in_block_2_round_1_appearance_interval=60000,
        number_of_hearts_in_block_2_round_2_appearance_interval=750,
        number_of_hearts_in_block_2_round_3_appearance_interval=750,
        number_of_hearts_in_block_3_round_1_appearance_interval=60000,
        number_of_hearts_in_block_3_round_2_appearance_interval=750,
        number_of_hearts_in_block_3_round_3_appearance_interval=750,
    ),

    dict(
        name='stroop_test',
        app_sequence=['stroop_test'],
        num_demo_participants=1,

        max_number_of_objects_in_block_1=5,
        max_number_of_objects_in_block_2=5,
        max_number_of_objects_in_block_3=5,

        number_of_trials_in_block_1=10,
        number_of_trials_in_block_2=10,
        number_of_trials_in_block_3=10,

    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ["hf_current_stage",
                      "hf_candidates",
                      "hf_sides",
                      "hf_passing",
                      "hf_number_passed",
                      "stroop_test_block_number"]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5523967279597'

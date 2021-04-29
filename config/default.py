import os
from configModule import Config

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TASK_CONFIG = Config().from_yaml(os.path.dirname('task.yml'))
RESOURCE_PATH = 'app/resources'

# TASK Setting
TASKS = TASK_CONFIG.TASKS
TASK_MODELS = TASK_CONFIG.MODELS
MODEL_SUBMIT_POSSIBLE = True

for key in TASK_MODELS.keys():
    TASK_MODELS[key].file_list = sorted(os.listdir(TASK_MODELS[key].label_path))

REGISTRATION_EMAIL_DOMAIN = '@gachon.ac.kr'
#REGISTRATION_EMAIL_DOMAIN = '@gmail.

# LEADERBOARD TABLE
LEADERBOARD_TABLE = ['Rank', 'Team', 'Submitter','Method', 'Code', 'LOSSES', 'Total', 'blank']

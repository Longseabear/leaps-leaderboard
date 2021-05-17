from flask import jsonify, session
from flask_table import Table, Col
from app import db
from app.models import SubmitModel, Losses, User
import config.default as config
import math
import pandas as pd
import json

### temp dictionary
# example,

example = [dict(Team='가천대',Submitter='장해웅',Method='SSFMNet',Code='github_link', MSE=2.77, L1=1.0, SSIM=0.7755),
           dict(Team='가천대2팀', Submitter='웅장해', Method='SQLIte', Code='github_link', MSE=900.0, L1=900.0, SSIM=0.6655),
           dict(Team='가천대3팀', Submitter='해웅장', Method='SQLIte', Code='github_link', MSE=3.0, L1=300.0, SSIM=0.7755)]

class LeaderBoardTable():
    def __init__(self, task=None):
        # example = db 처리
        self.examples = None
        self.losses = [{'name':name, 'w':weight} for name, weight in zip(config.TASK_MODELS[task].losses, config.TASK_MODELS[task].losses_weight)]
        self.eps = 0.000001
        self.task = task

    # id task L1Metric MSEMetric PSNRMEtric
    # 1  color  0.074    0.008     20.51875
    def fetch_all(self):
        try:
            query = db.session.query(Losses).filter(SubmitModel.id==Losses.model_id, SubmitModel.task == self.task,
                                                    Losses.name.in_([dic['name'] for dic in self.losses]))
            df = pd.read_sql(query.statement, query.session.bind)
            query_submit_model = db.session.query(SubmitModel.id,
                                                  SubmitModel.teamname,
                                                  SubmitModel.task,
                                                  User.nickname,
                                                  SubmitModel.method,
                                                  SubmitModel.code,
                                                  SubmitModel.submitted_on).filter(SubmitModel.task == self.task).join(User)
            df_submit_model = pd.read_sql(query_submit_model.statement, query_submit_model.session.bind)

            pivoted_losses = df.pivot_table(index='model_id', columns='name',values='val')

            self.examples = pd.merge(left=df_submit_model, right=pivoted_losses, how='inner', left_on='id', right_on='model_id')
        except Exception as e:
            self.examples = None


    def calculate_rank(self):
        try:
            self.examples['total'] = 0
            for loss_container in self.losses:
                loss = loss_container['name']
                self.examples['total'] += (self.examples[loss] - self.examples[loss].mean()) / (
                            self.examples[loss].std(ddof=0) + self.eps) * loss_container['w']
            self.examples['total'] /= len(self.losses)
            self.examples = self.examples.sort_values(by=['total'], ascending=False)
            self.examples = self.examples.reset_index()

            if session.get('admin_mode') is None:
                del self.examples['id']
            del self.examples['task'], self.examples['index']

        except Exception as e:
            self.examples = None

    def make_table_template(self):
        if self.examples is None:
            return 'Empty'
        html = self.examples.to_html(classes=['table','table-striped', 'table-bordered', 'table-condensed'], justify='center')
        return html


if __name__ == '__main__':
    a = LeaderBoardTable('colorization')
    a.fetch_all()
    a.calculate_rank()
    print(a.examples)

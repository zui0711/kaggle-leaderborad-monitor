import os
import time

from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import json
from datetime import datetime, timezone
import sys
import warnings
import zipfile
warnings.filterwarnings('ignore')

if __name__ == '__main__':
    # 参数1 比赛名
    # 参数2 最近提交时间
    competition_name = sys.argv[1]
    sub_time = float(sys.argv[2])
    api = KaggleApi()
    api.authenticate()
    # 获取排行榜
    last_team = None
    while(True):
        now = datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"))  # 2023-06-30 14:25:36
        api.competition_leaderboard_download(competition_name, path='.', quiet=False)
        with zipfile.ZipFile(f'{competition_name}.zip', 'r') as z:
            with z.open(z.namelist()[0]) as f:
                ld_df = pd.read_csv(f)[:50]  # 可以添加其他参数如 encoding='utf-8'

        ld_df['LastSubmissionDate'] = pd.to_datetime(ld_df['LastSubmissionDate']).dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')
        ld_df['time_diff'] = ((pd.Timestamp.now(tz='Asia/Shanghai')-ld_df['LastSubmissionDate']).dt.total_seconds() / 60).round(2)
        print('最近提交...')
        print(ld_df[ld_df['time_diff']<sub_time][['Rank', 'TeamName', 'LastSubmissionDate', 'Score', 'SubmissionCount', 'time_diff']])
        print('------')
        if last_team is not None:
            print('新进入排行榜...')
            print(ld_df[~ld_df['TeamName'].isin(last_team)][['Rank', 'TeamName', 'LastSubmissionDate', 'Score', 'SubmissionCount', 'time_diff']])
        last_team = ld_df['TeamName'].unique()

        print('===============================\n')
        time.sleep(300)

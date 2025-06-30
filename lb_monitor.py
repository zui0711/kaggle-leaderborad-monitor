import os
import time

from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import json
from datetime import datetime, timezone
import sys
import warnings
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

        leaderboard = api.competition_leaderboard_view(competition_name)

        leaderboard_data = []
        for i, entry in enumerate(leaderboard[:50]):
            leaderboard_data.append({
                'Rank': i + 1,
                'teamName': entry.team_name,
                'score': entry.score,
                'submissionDate': entry.submission_date,
            })

        ld_df = pd.DataFrame(leaderboard_data)

        ld_df['submissionDate'] = ld_df['submissionDate'].dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')
        ld_df['time_diff'] = ((pd.Timestamp.now(tz='Asia/Shanghai')-ld_df['submissionDate']).dt.total_seconds() / 60).round(2)
        print('最近提交...')
        print(ld_df[ld_df['time_diff']<sub_time])
        print('------')
        if last_team is not None:
            print('新进入排行榜...')
            print(ld_df[~ld_df['teamName'].isin(last_team)])
        last_team = ld_df['teamName'].unique()

        print('===============================\n')
        time.sleep(300)

import glob
import os
import sys

import pandas as pd


class Books:
    def __init__(self):
        if getattr(sys, "frozen", False):
            script_dir = os.path.dirname(sys.executable)
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))

        excel_folder = os.path.join(script_dir, "src/excel")
        soldout_folder = os.path.join(script_dir, "src/soldout")

        os.makedirs(excel_folder, exist_ok=True)
        os.makedirs(soldout_folder, exist_ok=True)

        # 품절 목록
        soldout_files = [f for f in os.listdir(soldout_folder) if f.endswith(".txt")]
        soldout_list = [os.path.splitext(f)[0] for f in soldout_files]
        self.soldout_list = soldout_list

        # 엑셀 파일 로드
        excel_files = glob.glob(os.path.join(excel_folder, "*.xlsx"))
        if not excel_files:
            raise ValueError("엑셀 파일을 엑셀 폴더에 넣어야 합니다.")

        latest_file = max(excel_files, key=os.path.getmtime)
        self.latest_file = latest_file

        # 엑셀 파일 전처리
        dataframe = pd.DataFrame()
        df = pd.read_excel(latest_file)
        df["주문"] = pd.to_datetime(df["주문"], errors="coerce")
        df.loc[df["도서명(저자)"].isin(soldout_list), "위치"] = -1  # -1 은 품절
        df["도서명(저자)"] = df["도서명(저자)"].str.replace(" ", "", regex=False)
        today = pd.to_datetime("today").normalize()
        df["D-일수"] = (today - df["주문"]).dt.days.apply(
            lambda x: f"D-{int(x)}" if pd.notna(x) else ""
        )

        dataframe["도서명"] = df["도서명(저자)"]
        dataframe["출판사"] = df["출판사"]
        dataframe["위치"] = df["위치"]
        dataframe["주문월일"] = df["주문"]
        dataframe["주문경과일"] = df["D-일수"]
        self.dataframe = dataframe

    def get_soldout_list(self):
        return self.soldout_list

    def get_dataframe(self):
        return self.dataframe

    def get_excel_file_name(self):
        return self.latest_file

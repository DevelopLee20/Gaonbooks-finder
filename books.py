import os
import glob
from tabulate import tabulate
import pandas as pd
import tkinter as tk
from tkinter import ttk
import sys

# PATH 지정
if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))

excel_folder = os.path.join(script_dir, 'excel')
soldout_folder = os.path.join(script_dir, 'soldout')

# 폴더 없으면 새로 생성
os.makedirs(excel_folder, exist_ok=True)
os.makedirs(soldout_folder, exist_ok=True)

# 품절 목록 불러오기
soldout_files = [f for f in os.listdir(soldout_folder) if f.endswith('.txt')]
soldout_list = [os.path.splitext(f)[0] for f in soldout_files]

# 엑셀 파일 로드
excel_files = glob.glob(os.path.join(excel_folder, '*.xlsx'))

if not excel_files:
    print('엑셀 파일이 없습니다. "excel" 폴더에 파일을 추가하세요.')
    sys.exit()

latest_file = max(excel_files, key=os.path.getmtime)
file_name = [[f'적용된 엑셀 파일: {latest_file}']]
# print(tabulate(file_name, tablefmt="fancy_grid"))

# 엑셀 파일 전처리
df = pd.read_excel(latest_file)
df['주문'] = pd.to_datetime(df['주문'], errors='coerce')
df.loc[df['도서명(저자)'].isin(soldout_list), '위치'] = '품절'
df['도서명(저자)'] = df['도서명(저자)'].str.replace(" ", "", regex=False)
today = pd.to_datetime('today').normalize()

# 전역 변수 설정 및 초기 설정
last_filtered_df = pd.DataFrame()

# 인터페이스 제공
root = tk.Tk()
root.title("도서 검색 및 품절 관리 프로그램")
root.geometry("800x600")
root.configure(bg="#F0F0F0")  # 배경색 설정

# 화면 최대화로 실행
try:
    root.state('zoomed')  # Windows에서는 잘 작동
except:
    root.attributes('-zoomed', True)

# 스타일 적용
style = ttk.Style()
style.theme_use("clam")  # 세련된 테마 사용
style.configure("Treeview", 
                background="#F5F5F5",
                foreground="black",
                rowheight=40,
                fieldbackground="#F5F5F5",
                font=("Arial", 18))
style.configure("Treeview.Heading", font=("Arial", 18, "bold"))  # 헤더 폰트
style.map('Treeview', background=[('selected', '#A9A9A9')])

# 입력창 라벨
# StringVar 생성
text_var = tk.StringVar()
text_var.set(f'''적용된 파일: {file_name}
             도서명 입력''')  # 초기 값 설정
# 라벨에 StringVar 바인딩
label = tk.Label(root, textvariable=text_var, bg="#F0F0F0", font=("Arial", 24))
label.pack(pady=10)

# 입력창 (Treeview와 넓이 동일하게 설정)
entry = tk.Entry(root, font=("Arial", 18), relief="solid", bd=1)
entry.pack(pady=5, padx=10, fill="x")
entry.focus_set()  # 프로그램 시작 시 입력창에 포커스 강제 적용

# 백엔드 함수
# 검색 함수
def search(event=None):
    global last_filtered_df
    user_input = entry.get().strip()

    # 입력이 빈 문자열일 경우 건너뜀
    if user_input == "":
        return

    # "₩ {인덱스 번호}" 형식으로 입력한 경우
    if user_input.startswith("₩"):
        try:
            index_number = int(user_input[2:].strip()) - 1  # 1부터 시작하는 인덱스를 0부터 시작하도록 조정
            if last_filtered_df is not None and 0 <= index_number < len(last_filtered_df):
                # 원본 DataFrame의 인덱스 가져오기
                original_index = last_filtered_df.iloc[index_number].name
                book_title = df.at[original_index, '도서명(저자)']
                df.at[original_index, '위치'] = '품절'

                soldout_file_path = os.path.join(soldout_folder, f"{book_title}.txt")
                if not os.path.exists(soldout_file_path):
                    with open(soldout_file_path, 'w', encoding='utf-8') as file:
                        file.write(f"{book_title}")
                
                text_var.set(f"'{book_title}' 도서 품절처리가 완료되었습니다.")
            else:
                text_var.set("유효하지 않은 연번입니다.")
            
            entry.delete(0, tk.END)
        except ValueError:
            return
            # print(tabulate([[title] for title in soldout_list], headers=['품절 도서 목록'], tablefmt='grid'))
        return

    # 도서명 컬럼에서 검색어를 포함하는 행 필터링
    filtered_df = df[df['도서명(저자)'].str.contains(user_input, case=False, na=False)].copy()
    
    # 최근 필터링된 DataFrame을 저장
    last_filtered_df = filtered_df

    # 결과 출력
    if not filtered_df.empty:
            filtered_df = filtered_df.reset_index(drop=True)
            filtered_df.insert(0, '연번', filtered_df.index + 1)
            filtered_df['주문_MM-DD'] = filtered_df['주문'].dt.strftime('%m-%d')
            filtered_df['D-일수'] = (today - filtered_df['주문']).dt.days.apply(lambda x: f"D-{int(x)}" if pd.notna(x) else "")
            filtered_df = filtered_df[['연번', '도서명(저자)', '출판사', '위치', '주문_MM-DD', 'D-일수']]

            text_var.set(f"검색 결과: {len(filtered_df)}건")
    else:
        text_var.set(f'"{user_input}" 검색어를 포함하는 도서명을 찾을 수 없습니다.')

    update_treeview(filtered_df)
    entry.delete(0, tk.END)

# DataFrame을 Treeview에 출력
def update_treeview(dataframe):
    for item in tree.get_children():
        tree.delete(item)
    for _, row in dataframe.iterrows():
        tree.insert("", tk.END, values=list(row))

# Treeview (DataFrame 출력)
tree_frame = tk.Frame(root, bg="#F0F0F0")
tree_frame.pack(pady=20, padx=10, fill="both", expand=True)

columns = ['연번', '도서명(저자)', '출판사', '위치', '주문일', 'D-일수']
col_size = [100, 400, 250, 250, 250, 250]
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)

# 컬럼 설정 (넓이 자동 설정)
for col, size in zip(columns, col_size):
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=size)  # 입력창과 넓이 통일

# 스크롤바 추가
scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# 처음 실행 시 전체 데이터 출력
# update_treeview(df)

# Enter 키로 검색 가능
entry.bind("<Return>", lambda event: search())

root.mainloop()
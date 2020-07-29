import os
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.messagebox as msgbox
from PIL import Image, ImageTk
import time


#################
## 파일 추가
def add_file():
    files = filedialog.askopenfilenames(title="이미지 파일을 선택하세요", \
                                        filetypes=(("PNG 파일", "*.png"), ("모든 파일", "*.*")), \
                                        initialdir=r"C:\my_develop\image_merge\images")  # 소문자 r을 찍음으로서 탈출문자 등 무시하고 그냥 생으로 사용
    ## 사용자가 선택한 파일 목록에 삽입
    for file in files:
        list_file.insert(END, file)

## 선택 파일 삭제
def del_file():
    # print(list_file.curselection())
    for index in reversed(list_file.curselection()):  # reversed를 쓰면 순서가 뒤집힌 새로운 리스트 생성
        list_file.delete(index)

## 저장 경로 (폴더를 선택)
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected =="":
        return

    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, folder_selected)

## 이미지 통합 함수
def merge_image():

    ## 각 옵션들 값을 확인
    # print("가로넓이: ", comb_width.get())   # 시범 출력
    # print("간격: ", comb_space.get())     # 시범 출력
    # print("포맷: ", comb_format.get())    # 시범 출력
    try:
        ## 가로 넓이 먼저
        img_width = comb_width.get()
        if img_width == "원본유지":
            img_width = -1   # -1은 원본 기준으로 의미
        else:
            img_width = int(img_width)

        # 간격
        img_space = comb_space.get()
        if img_space == "좁게":
            img_space = 30
        elif img_space == "보통":
            img_space = 60
        elif img_space == "넓게":
            img_space = 90
        else:
            img_space = 0

        # 포맷
        img_format = comb_format.get().lower()

        # print(list_file.get(0, END))   # 대상 이미지 잡기
        images = [Image.open(x) for x in list_file.get(0, END)]   # 한줄 for 문
        # 이미지 사이즈를 리스트에 넣어서 하나씩 처리
        image_sizes = []   #(width1, height1), (width2, height2)...
        if img_width > -1:    # width 값을 변경해야 할 때
            image_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]
        else:
            image_sizes = [(x.size[0], x.size[1]) for x in images]


        # 이미지는 사이즈 값을 갖고 있다. size[0] : width, size[1]: height
        # widths = [x.size[0] for x in images]
        # heights = [x.size[1] for x in images]

        widths, heights = zip(*(image_sizes))

        # print("width : ", widths)   # 시범 출력
        # print("height : ", heights)  # 시범 출력
        ## 통합 이미지는 width가 가장 큰 사이즈 기준으로 정리되어야 하고, 높이는 heights의 합이다.
        max_width, total_height = max(widths), sum(heights)
        # print("max_width : ", max_width)   # 시범 출력
        # print("total_height : ", total_height)   # 시범 출력

        ## 통합 이미지를 담을 스케치북을 준비
        if img_space > 0:    # 이미지 간격 옵션 적용
            total_height += (img_space * (len(images) -1))
        result_img = Image.new("RGB", (max_width, total_height), (255, 255, 255))
        y_offset = 0  # 이미지를 이어 붙일 때.. y 위치 오프셋 영으로...

        for idx, img in enumerate(images):
            ## width가 원본유지가 아닐 때에는 이미지 크기 조정
            if img_width > -1:
                img = img.resize(image_sizes[idx])

            result_img.paste(img, (0, y_offset))
            y_offset += (img.size[1] + img_space)   # 두번째 그림 붙일 때는 첫번째 그림의 높이 만큼 오프셋 y값 더해줌

            ## 프로그레스 바 연동시키기
            progress = (idx + 1) / len(images) * 100   # 실제 %정보 계산하기
            p_var.set(progress)
            progress_bar.update()

        ## 포맷 옵션 처리
        curr_time = time.strftime("%Y%m%d_%H%M%S")
        file_name = "image_merge_{0}.".format(curr_time) + img_format

        dest_path = os.path.join(txt_dest_path.get(), file_name)
        result_img.save(dest_path)
        msgbox.showinfo("알림", "작업이 완료되었습니다.")
    except Exception as err:
        msgbox.showerror("에러", err)

## 시작 버튼 함수
def start():
    ## 각 옵션들 값을 확인
    # print("가로넓이: ", comb_width.get())   # 시범 출력
    # print("간격: ", comb_space.get())     # 시범 출력
    # print("포맷: ", comb_format.get())    # 시범 출력

    ## 파일 목록 유무 확인
    if list_file.size() == 0:
        msgbox.showwarning("경고", "이미지 파일을 추가하세요")
        return

    ## 저장 경로 설정 여부 확인
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("경고", "저장 경로를 설정해 주세요.")
        return

    ## 이미지 합치기 (시작버튼이 눌러졌을 때)
    merge_image()    # 별도 정의


################### 레이아웃 깔기 #################

root = Tk()
root.title("Image Merge")

# 백그라운드 배경 그림 넣기
IMAGE_PATH = "bg.png"
C = Canvas(root, bg="blue", height=10, width=100)
filename1 = ImageTk.PhotoImage(Image.open(IMAGE_PATH))
background_label = Label(root, image=filename1)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
C.pack()

root.wm_attributes("-transparentcolor", 'grey')


# 파일 프레임 (파일 추가, 선택 삭제)

file_frame = Frame(root)
file_frame.pack(fill="x", padx=5, pady=5)

btn_add_file = Button(file_frame, text="add file", padx=5, pady=5, width=12, command=add_file, bg="yellow")
btn_add_file.pack(side = "left")
btn_del_file = Button(file_frame, text="remove file", padx=5, pady=5, width=12, command=del_file, bg="yellow")
btn_del_file.pack(side = "right")



# 리스트 프레임 만들기 + 스크롤바 연동
list_frame = Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
list_file.pack(side="right", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

# 저장경로 프레임
path_frame = LabelFrame(root, text="저장경로")
path_frame.pack(fill="x", padx=5, pady=5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left", fill="x", expand=True, ipady=5, padx=5, pady=5)  # inner pad y = 4

btn_dest_path = Button(path_frame, text="찾아보기", width=10, command=browse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)

# 옵션 프레임
frame_option = LabelFrame(root, text="옵션")
frame_option.pack(fill="both", padx=5, pady=5)

## 1. 가로 넓이 옵션
## 가로 넓이 레이블
label_width = Label(frame_option, text="가로넓이", width=8)
label_width.pack(side="left")
## 가로 넓이 콤보
opt_width = ["원본유지", "1024", "800", "640"]
comb_width = ttk.Combobox(frame_option, state="readonly", values=opt_width, width=10)
comb_width.current(0)  # 기본 값 잡기
comb_width.pack(side="left")

## 2. 이미지 간격 옵션
## 간격 옵션 레이블
label_space = Label(frame_option, text="간격", width=8)
label_space.pack(side="left", padx=5, pady=5, ipady=5)
## 간격 옵션 콤보
opt_space = ["없음", "좁게", "보통", "넓게"]
comb_space = ttk.Combobox(frame_option, state="readonly", values=opt_space, width=10)
comb_space.current(0)  # 기본 값 잡기
comb_space.pack(side="left", padx=5, pady=5)

## 3. 파일 포맷 옵션
## 파일 포맷 옵션 레이블
label_format = Label(frame_option, text="포맷", width=8)
label_format.pack(side="left", padx=5, pady=5, ipady=5)
## 파일 포맷 옵션 콤보
opt_format = ["PNG", "JPG", "BMP"]
comb_format = ttk.Combobox(frame_option, state="readonly", values=opt_format, width=10)
comb_format.current(0)  # 기본 값 잡기
comb_format.pack(side="left", padx=5, pady=5)

# 진행 상황 프로그레스 바
frame_progress = LabelFrame(root, text="진행상황")
frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, max=100, variable=p_var)
progress_bar.pack(fill="x", padx=5, pady=5, ipady=5)

# 실행 프레임 (시작, 종료)

frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5, ipady=5)

btn_end = Button(frame_run, text="닫기", padx=5, pady=5, width=12, command=root.quit)
btn_end.pack(side="right", padx=5, pady=5)
btn_std = Button(frame_run, text="시작", padx=5, pady=5, width=12, command=start)
btn_std.pack(side="right", padx=5, pady=5)


root.resizable(False, False)
root.mainloop()
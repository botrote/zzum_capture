from  tkinter import *

from tkinter import filedialog

import cv2

import tkinter as tk2

import tkinter as tk3

import tkinter as tw



count = 0

j = 0

x1 = 0

y1 = 0

x2 = 0

y2 = 0



source = tk3.Tk()

source.withdraw()

#source_path = filedialog.askdirectory(initialdir="/",title='감지용 이미지가 저장된 폴더를 선택하세요.')

#print(source_path)



root = Tk()

root.filename = filedialog.askopenfilename(initialdir = "/", title = "녹화 파일을 선택하세요.")

print(root.filename)

root.withdraw()



path = tk2.Tk()

path.withdraw()

dir_path = filedialog.askdirectory(initialdir="/",title='캡쳐 이미지를 저장할 폴더를 선택하세요.')

print(dir_path)



#templ1 = cv2.imread("%s/7_off.jpg" % source_path, cv2.IMREAD_COLOR)  # 다운받아야 할 사진 1

#templ2 = cv2.imread("%s/7_on.jpg" % source_path, cv2.IMREAD_COLOR)  # 다운받아야 할 사진 2

#templ3 = cv2.imread("%s/xp_off.jpg" % source_path, cv2.IMREAD_COLOR)  # 다운받아야 할 사진 3

#templ4 = cv2.imread("%s/xp_on.jpg" % source_path, cv2.IMREAD_COLOR)  # 다운받아야 할 사진 4

templ1 = cv2.imread("images/7_off.jpg", cv2.IMREAD_COLOR)  # 다운받아야 할 사진 1

templ2 = cv2.imread("images/7_on.jpg", cv2.IMREAD_COLOR)  # 다운받아야 할 사진 2

templ3 = cv2.imread("images/xp_off.jpg", cv2.IMREAD_COLOR)  # 다운받아야 할 사진 3

templ4 = cv2.imread("images/xp_on.jpg", cv2.IMREAD_COLOR)  # 다운받아야 할 사진 4


window = tw.Tk()

window.title("자르기 범위 설정")



def done():

    global x1, x2, y1, y2

    x1 = int(e1.get())

    x2 = int(e2.get())

    y1 = int(e3.get())

    y2 = int(e4.get())

    window.destroy()



l1 = tw.Label(window, text="좌측 끝 좌표")  # Label:텍스트 표시

l2 = tw.Label(window, text="우측 끝 좌표")

l3 = tw.Label(window, text="상단 끝 좌표")

l4 = tw.Label(window, text="하단 끝 좌표")

l1.grid(row=0, column=0)

l2.grid(row=1, column=0)

l3.grid(row=2, column=0)

l4.grid(row=3, column=0)



e1 = tw.Entry(window)

e2 = tw.Entry(window)

e3 = tw.Entry(window)

e4 = tw.Entry(window)

e1.grid(row=0, column=1)

e2.grid(row=1, column=1)

e3.grid(row=2, column=1)

e4.grid(row=3, column=1)



b1 = tw.Button(window, text="완료", command=done)

b1.grid(row=4, column=1)



window.wait_window()



cap = cv2.VideoCapture(root.filename)  # 동영상 위치



def paint_check(img):

    result1, _, ax1, _ = cv2.minMaxLoc(cv2.matchTemplate(img, templ1, 1), None)

    result2, _, ax2, _ = cv2.minMaxLoc(cv2.matchTemplate(img, templ2, 1), None)

    result3, _, ax3, _ = cv2.minMaxLoc(cv2.matchTemplate(img, templ3, 1), None)

    result4, _, ax4, _ = cv2.minMaxLoc(cv2.matchTemplate(img, templ4, 1), None)



    raw = [result1, result2, result3, result4]

    ax = [ax1, ax2, ax3, ax4]

    norm = [float(i) / sum(raw) for i in raw]



    print("checking")



    if min(norm) < 0.1:

        return norm.index(min(norm)), ax[norm.index(min(norm))]



    else:

        return -1, (0, 0)


imgCount = 0
while cap.isOpened(): # cap 정상동작 확인

    _, image = cap.read()



    if j % 300 == 0:

        check = paint_check(image)



    i = image[check[1][1], check[1][0], :]



    if check[0] == 0 or check[0] == 1:



        if i[0] > 100 and i[0] < 140 and i[1] > 170 and i[1] < 210 and i[2] > 180 and i[2] < 230 and count == 0:

             k = cap.get(1)

             cap.set(1, k - 3)

             _, image = cap.read()

             crop = image[y1:y1+y2, x1:x1+x2]

             imgCount += 1
             cv2.imwrite("%s/%d.jpg" % (dir_path, imgCount), crop)   # 사진 저장 위치

             k = cap.get(1)

             cap.set(1, k + 3)

             count = 1

             print("save")



        if i[0] > 240 and i[0] < 256 and i[1] > 240 and i[1] < 256 and i[2] > 230 and i[2] < 256:

            count = 0



    elif check[0] == 2 or check[0] == 3:



        if i[0] > 100 and i[0] < 190 and i[1] > 100 and i[1] < 190 and i[2] > 100 and i[2] < 190 and count == 0:

             k = cap.get(1)

             cap.set(1, k - 3)

             _, image = cap.read()

             crop = image[y1:y1+y2, x1:x1+x2]
             imgCount += 1
             cv2.imwrite("%s/%d.jpg" % (dir_path, imgCount), crop)  # 사진 저장 위치 (위랑 똑같음)

             k = cap.get(1)

             cap.set(1, k + 3)

             count = 1

             print("save")



        if i[0] > 230 and i[0] < 250 and i[1] > 230 and i[1] < 250 and i[2] > 230 and i[2] < 250:

             count = 0



    else:

        pass

    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imshow("ing...", image)

    print(i)

    j += 1



    if cv2.waitKey(42) == ord('q'):

        break



# 작업 완료 후 해제

cap.release()

cv2.waitKey(0)

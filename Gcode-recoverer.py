#Author: PencilCore

import os
import glob
import re
import decimal

print("这是Gcode断点续打恢复工具 This is Gcode Recoverer in case you failed a print and want to resume.")
print("请在当前目录放置你需要恢复的Gcode文件 Place your Gcode file in this folder.")
print("选择你要恢复的文件 Choose the file you want to recover :")
file_list = os.listdir('.')

gcode_file_list = []
path = os.getcwd() + "/*.gcode"
for name in glob.glob(path):
    name = os.path.basename(name)
    gcode_file_list.append(name)
    print(str(len(gcode_file_list)) + ": " + name)
    
num = -1
while(num <= 0 or num > len(gcode_file_list)):
    # 用户输入
    try:
        num = int(input())
        if num <= 0 or num > len(gcode_file_list):
            num = int("haha")
        else:
            break
    except ValueError:
        print("请输入有效数字 Please enter a vaild number.")
        num = -1

path = str(os.getcwd() + "/" + gcode_file_list[num - 1])
gcode_file = open(path, mode = "r+")

layer_height = ""


lines = gcode_file.readlines()
for line in lines:
    if "Layer height" in line:
        layer_height = float((line.split(":")[1])[:-1])

# gcode_content = gcode_file.read()

print("将你的打印机返回原点，使用运动功能测量已打印的高度")
print("Set Home, then use Motion function to measure the height that have printed.")
print("层高 Layer Height:")
print(layer_height)
print("你所测量的值应当是它的倍数 The value you measured should be its multiple.")
print("输入已打印层高(>=1mm) Enter height printed(>=1mm):")

while(True):
    try:
        num = float(input())
        if num >= 1 and int(num * 10) % int(layer_height * 10) == 0 :
            if  num >= 1 and int(num * 10) % int(10) == 0:
                num = "{:.0f}".format(num)
        else:
            print("请输入有效数字 Please enter a vaild number.")
            gcode_file.close()
            exit()
        start_line_num = 0
        end_line_num = 0
        line_num = 1
        for line in lines:
            if("Reset Flowrate") in line:
                start_line_num = line_num + 1

            if (("Z" + str(num)) in line):
                if ((line.split("Z")[1])[:-1] == str(num)):
                    end_line_num = line_num - 1
                    
            line_num = line_num + 1
        break
    except ValueError:
        print("请输入有效数字 Please enter a vaild number.")
    
gcode_file.seek(0)
gcode_file.truncate()
gcode_file.writelines(lines[0:start_line_num])
gcode_file.writelines(lines[end_line_num:len(lines)])

gcode_file.close()
print("Done.")
input("Any key to close.")

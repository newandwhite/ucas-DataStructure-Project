# ucas-DataStructure-Project
ucas数据结构大作业-池塘夜降彩色雨

这是通过python的**pygame**模块实现的代码

## code
code文件夹下是正式提交的代码，已实现基础和进阶的所有功能

主界面由main.py实现
* 通过PgUp与PgDn键控制雨点数目
* 通过w和s键控制起风（给雨点施加水平速度）和风停
* 通过空格键控制打雷闪电

## code-advanced
code-advance文件夹下是尝试整活的代码，由于当前实现了雨点落到不同荷叶上的音调不同，因此希望可以通过控制雨点落下的位置进行打谱，从而实现一段音乐演奏。由于时间有限，只实现了一段简单的单音，暂时没有实现和声部分。因此最终没有提交这个版本

main.py被替换为musicpool1.py，增加利用数组打谱的文件opern.py

## graphics
graphics文件夹下是所有贴图。每一个对象的贴图都是一个文件夹，文件夹里有多张图片，可以通过循环播放实现动画。

## node
node文件夹下是所有音效

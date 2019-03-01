#!/usr/bin/python
# -*-coding:utf8 -*-
__author__="wanglongfei"

import re
import os
import sys

# 前面几行固定代码
indir=sys.argv[1]
outfile=sys.argv[2]
# sys.argv[0] 为程序名本身

# 获取路径下的所有表达量文件
expfiles=os.listdir(indir)

total_counts={}
exp_info={}
# 声明一个字典存放所有文件的表达量信息
for expfile_name in expfiles:
    if(re.search(r'expr\.xls$',expfile_name)):
        # 匹配文件名
        infile=indir+"/"+expfile_name
        # 拼接文件路径

        samplename=re.sub(r'\.expr\.xls$','',expfile_name)
        # 获取文件名

        fin=open(infile,"r")
        # 打开文件读写
        line=fin.readline()
        line=line.strip()
        arr=re.split(r'\t+',line)
        total_counts[samplename]=arr[1]
        # 读取一行，第一行忽略掉
        for line in fin:
            line=line.strip()          # 去掉行首行尾的空白
            arr=re.split(r'\t+',line)
            if(arr[0] in exp_info):
                exp_info[arr[0]][samplename]=arr
            else:
                exp_info[arr[0]]={samplename:arr}
        fin.close()

        print("read file:"+infile)

fout=open(outfile,"w")
# 写入文件
fout.write("sRNA id\taverage_tpm\tType\tDescription")
for sample in  sorted(total_counts.keys()):
    count_str=sample+"_"+total_counts[sample]
    fout.write("\t"+count_str)

for sample in  sorted(total_counts.keys()):
    fout.write("\t"+sample+"_TPM")
fout.write("\n")
# 处理表头

average_tpm=[]
sorted_average_tpm=[]
for miRNA in sorted(exp_info.keys()):
    sum_tpm=0
    for sample in  sorted(exp_info[miRNA].keys()):
        sum_tpm=sum_tpm+float(exp_info[miRNA][sample][4])
    average_tpm.append([miRNA,sum_tpm/len(list(total_counts.keys()))])

# 数组排序
# sorted_average_tpm=sorted(average_tpm,key=lambda u:u[1])
sorted_average_tpm=sorted(average_tpm,key=lambda u:u[1],reverse=True) # 降序
    # 对每个miRNA的内容循环写入
for record in sorted_average_tpm:
    miRNA=record[0]
    fout.write(miRNA+"\t")
    fout.write(str(record[1]))
    
    sample_0=list(exp_info[miRNA].keys())[0]
    des=exp_info[miRNA][sample_0][3]
    miRNA_type=exp_info[miRNA][sample_0][2]
    # 每个miRNA至少有一个样品记录,获取第一个样品记录的描述信息
    fout.write("\t"+miRNA_type)
    fout.write("\t"+des)

    for sample in  sorted(total_counts.keys()):
        if(sample in exp_info[miRNA]):
            fout.write("\t"+exp_info[miRNA][sample][1])
        else:
            fout.write("\tNA")
        # 写入每个样品的reads个数
    for sample in  sorted(total_counts.keys()):
        if(sample in exp_info[miRNA]):
            fout.write("\t"+exp_info[miRNA][sample][4])
        else:
            fout.write("\tNA")
        # 写入每个样品的TPM
    fout.write("\n")

fout.close()

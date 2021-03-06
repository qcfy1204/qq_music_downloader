#!usr/bin/env python
# -*- coding: UTF-8 -*-
import traceback

import requests, re, os, time
import sys

api_url = 'https://api.bzqll.com/music/tencent/songList?key=579621905&id='
song_url = 'https://api.itooi.cn/music/tencent/song?key=579621905&id='
m_id = '6940396907'  # 歌单的id
path = os.getcwd() + '\\download\\' + m_id + '\\'  # 保存的路径


# 保存歌曲
def save_song(url, singer, name, lrc):
    global path
    path = os.getcwd() + '\\download\\' + m_id + '\\'  # 保存的路径
    if not os.path.exists(path):
        os.makedirs(path)
    mp3_path = path + name + '-' + singer + ".mp3"
    flac_path = path + name + '-' + singer + ".flac"
    if os.path.exists(mp3_path):
        if os.path.getsize(mp3_path) > 0:
            print('exist skip  ' + mp3_path)
            return
    if os.path.exists(flac_path):
        if os.path.getsize(flac_path) > 0:
            print('exist skip  ' + flac_path)
            return
    resource = get_url(url + '&br=flac', True)
    if resource.status_code != 200:
        r = get_url(url + '&br=320', True)
        if r.status_code == 200:
            with open(mp3_path, mode="wb") as fh:
                print('dl ' + mp3_path)
                dl_lrc(singer, name, lrc)
                fh.write(r.content)
        return
    # 下载歌曲并保存
    with open(flac_path, mode="wb") as fh:
        fh.write(resource.content)
        dl_lrc(singer, name, lrc)
        print('dl ' + flac_path)


def dl_lrc(singer, name, lrc):
    global path
    lrc_path = path + name + '-' + singer + ".lrc"
    resource = get_url(lrc, False)
    with open(lrc_path, mode="w", encoding='utf-8') as fh:
        fh.write(resource.text)


def get_url(url, stream):
    num = 5
    while num > 0:
        try:
            r = requests.get(url, stream=stream, timeout=3)
            return r
        except:
            print('timeout retry')
            num = num - 1
    return


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "", title)  #
    return new_title.strip()


if __name__ == '__main__':
    input2 = input(" 输入数字，1歌单、2单曲：")
    if int(input2) == 1:
        s = input("输入qq音乐歌单id例如 6940396907 :")
        if len(str(s).strip()) != 10:
            print('请输入正确的10位id号')
            time.sleep(1)
            sys.exit()
        m_id = str(s).strip()
        r = requests.get(api_url + m_id)
        response_dict = r.json()
        res = response_dict['data']['songs']
        lenght = response_dict['data']['songnum']
        left = int(lenght)
        print('total ' + str(lenght))
        for i in range(int(lenght)):
            name = res[i]['name']
            name = validateTitle(name)
            url = res[i]['url']
            lrc = res[i]['lrc']
            singer = res[i]['singer'].replace('/', '&')
            try:
                save_song(url, singer, name, lrc)
                left = left - 1
                print('left  ' + str(left))
            except Exception as e:
                print('error ' + name)
                traceback.print_exc()
    elif int(input2) == 2:
        s = input("输入qq歌曲id例如 002u0fTY2HoJJp :")
        if len(str(s).strip()) != 14:
            print('请输入正确的10位id号')
            time.sleep(1)
            sys.exit()
        m_id = str(s).strip()
        r = requests.get(song_url + m_id)
        response_dict = r.json()
        res = response_dict['data']
        name = res['name']
        name = validateTitle(name)
        url = res['url']
        lrc = res['lrc']
        singer = res['singer'].replace('/', '&')
        try:
            save_song(url, singer, name, lrc)
        except Exception as e:
            print('error ' + name)
            traceback.print_exc()

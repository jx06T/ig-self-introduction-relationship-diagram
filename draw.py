import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
import os
import json
import time
from PIL import Image
class PeopleGraph:
    def __init__(self, people):
        self.people = people
        self.G = nx.DiGraph()
        self.SIZE = len(self.people) // 3.5 if len(self.people) // 3.5> 12 else 12
        self.create_graph()
        
    
    def generate_hex_color(self, position):
        position = 400- min(400, max(0, position))
        red = (255 if position < 255 else 510 - position )
        green = (position if position < 255 else 255)
        red_hex = format(red, '02x')
        green_hex = format(green, '02x')
        hex_color = f'#{red_hex}{green_hex}63'

        return hex_color
        
    def create_graph(self):
        plt.figure(figsize=(self.SIZE, self.SIZE))
        self.TempPeople = self.people.copy()
        MaxLevel = 0
        for key, value in self.TempPeople.items():
            self.people[key]["state"] = {}
            if value["level"]+1 >MaxLevel:
                MaxLevel = value["level"]+1
            

        for key, value in self.TempPeople.items():
            self.G.add_node(key)
            self.people[key]["color"] = self.generate_hex_color((len(value["at"]) + 1) * random.randint(37, 53))
            self.people[key]["size"] = (MaxLevel - value["level"]) * 600 + 500
            if  value["level"] == 0:
                self.people[key]["size"] = MaxLevel*600+2000
            if  value["level"] == MaxLevel -1 :
                self.people[key]["color"] =  "#C4CF9E"
    
            for aAt in value["at"]:
                # print(key,aAt)
                if  aAt in self.people[key]["state"]:
                    if self.people[key]["state"][aAt] == '<|-|>':
                        continue

                self.G.add_edge(key, aAt , weight=100)
                self.people[key]["state"][aAt] = '-|>'
                if aAt not in self.people :
                    self.people[aAt] = {}
                    self.people[aAt]["size"] = 300
                    self.people[aAt]["color"] = "#C4CF9E"
                    self.people[aAt]["state"] = {}
                    self.people[aAt]["at"] = []
                    continue

                if key in self.people[aAt]["at"]:
                    self.people[key]["state"][aAt] = '<|-|>'
                    self.people[aAt]["state"][key] = "<|-|>"
                    
        # pos = nx.spring_layout(self.G)
        pos = nx.spring_layout(self.G,k=10,iterations=100,weight='weight')  # 增加迭代次數
        # pos = nx.spring_layout(self.G, pos=nx.kamada_kawai_layout(self.G))
        # pos = nx.spring_layout(self.G, pos=nx.fruchterman_reingold_layout(self.G))

        for node in self.G.nodes:
            nx.draw_networkx_nodes(self.G, pos, nodelist=[node], alpha=0.9 , node_color=self.people[node]["color"], node_size=self.people[node]["size"])
        
        for edge in self.G.edges:
            source_node, target_node = edge
            
            x1, y1 = pos[source_node]
            x2, y2 = pos[target_node]
            
            dx = x2 - x1
            dy = y2 - y1

            # t2 = 100000
            # t2 = self.SIZE * 4000
            t2 = self.SIZE * 7000

            t = self.people[source_node]["size"] / t2
            arrow_position1 = (x1 + t * ((dx > 0) * 2 - 1), y1 + t * ((dy > 0) * 2 - 1))  
            
            t = self.people[target_node]["size"] / t2
            arrow_position2 = (x2 - t * ((dx > 0) * 2 - 1), y2 - t * ((dy > 0) * 2 - 1)) 
            
            NewPos = {source_node: arrow_position1, target_node: arrow_position2}
            
            nx.draw_networkx_edges(self.G, NewPos, edgelist=[edge], width=1.4, arrows=True, arrowstyle=patches.ArrowStyle(self.people[source_node]["state"][target_node], head_length=0.5, head_width=0.1), connectionstyle="arc3, rad=0.2", arrowsize=20)
            # nx.draw_networkx_edges(self.G, pos, edgelist=[edge], width=1.4, arrows=True, arrowstyle=patches.ArrowStyle(self.people[source_node]["state"][target_node], head_length=0.5, head_width=0.1), connectionstyle="arc3, rad=0.2", arrowsize=20)
        
        nx.draw_networkx_labels(self.G, pos)
    
    def show_graph(self,filename,driver):
        plt.subplots_adjust(left=0.005, right=0.995, top=0.995 ,bottom=0.005)
        filename = filename+".png"
        plt.savefig(filename, format="png",dpi=100)
            
        current_directory = os.getcwd()
        local_file_path = 'file:///' + os.path.join(current_directory, filename)
        try:
            driver.execute_script("window.open('', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(local_file_path)
        except:
            # plt.show()
            # time.sleep(1)
            # os.startfile(local_file_path)
            img = Image.open(os.path.join(current_directory, filename))
            img.show()  # 使用預設圖片查看器顯示圖片

            pass
        
        print("開啟圖片",os.path.join(current_directory, filename))



if __name__ == '__main__':
    people = {
    "Alice": {"level":0,"at": ["Bob", "Charlie"]},
    "Bob": {"level":1,"at": ["Alice", "David", "Eve"]},
    "Charlie": {"level":1,"at": ["David"]},
    "David": {"level":2,"at": ["Alice", "Eve"]},
    "Eve": {"level":2,"at": []},
    "Frank": {"level":2,"at": ["Bob", "David"]},
    "Grace": {"level":2,"at": ["Alice", "Frank", "Eve"]},
    }
    # people = {'xy__0823': {'level': 0, 'at': ['chia_yun24', 'citra._.08', 'millie.sun26', '_823yee']}, 'chia_yun24': {'level': 1, 'at': ['kali_.0117']}, 'citra._.08': {'level': 1, 'at': []}, 'millie.sun26': {'level': 1, 'at': ['m.wildlife_', 'liyliy_0911', 'agnes101229']}, '_823yee': {'level': 1, 'at': ['ting_yuuu0710', '___yue.h', 'joytseng_76', 'bella._.wee', 'lei._10.28', 'ly._09_11', 'ninibaba0223', 'li7nniuy.__']}, 'm.wildlife_': {'level': 2, 'at': []}, 'liyliy_0911': {'level': 2, 'at': []}, 'agnes101229': {'level': 2, 'at': ['su_athena', '101229_luna']}, 'kali_.0117': {'level': 2, 'at': ['yun_tseng7', 'i42kip']}, 'ting_yuuu0710': {'level': 2, 'at': []}, '___yue.h': {'level': 2, 'at': ['39saku_chan']}, 'joytseng_76': {'level': 2, 'at': []}, 'bella._.wee': {'level': 2, 'at': []}, 'lei._10.28': {'level': 2, 'at': []}, 'ly._09_11': {'level': 2, 'at': ['yu.0218_qq', 'riky.820', '7zqx__', '_cl.920']}, 'ninibaba0223': {'level': 2, 'at': ['smile0223__', 'ccc.___.0812', 'zyutong1208', 'zoey_.0919']}, 'li7nniuy.__': {'level': 2, 'at': ['panyunlin7_amis', 'lin._.3.22']}, 'su_athena': {'level': 3, 'at': []}, '101229_luna': {'level': 3, 'at': []}, 'yun_tseng7': {'level': 3, 'at': ['ck_yu_2534', 'wzh_.shiyu_u']}, 'i42kip': {'level': 3, 'at': []}, '39saku_chan': {'level': 3, 'at': []}, 'yu.0218_qq': {'level': 3, 'at': []}, 'riky.820': {'level': 3, 'at': []}, '7zqx__': {'level': 3, 'at': ['cshs102__']}, '_cl.920': {'level': 3, 'at': ['roses_are_rosie', '_zjlx.10', 'cnm._.0121', 'yuu._1110', 'esa.0726']}, 'panyunlin7_amis': {'level': 3, 'at': []}, 'lin._.3.22': {'level': 3, 'at': ['tongu._', 'hcy.0821_']}, 'smile0223__': {'level': 3, 'at': []}, 'ccc.___.0812': {'level': 3, 'at': []}, 'zyutong1208': {'level': 3, 'at': []}, 'zoey_.0919': {'level': 3, 'at': ['zoey.0919', 'jdy.__0811']}, 'ck_yu_2534': {'level': 4, 'at': []}, 'wzh_.shiyu_u': {'level': 4, 'at': ['saythename_17', 'wayvofficial', 'zb1official', 'le_vtime']}, 'cshs102__': {'level': 4, 'at': ['68_wlsh_102']}, 'roses_are_rosie': {'level': 4, 'at': []}, '_zjlx.10': {'level': 4, 'at': ['lu.981105', 'czh._10', '_cty.__.0210', 'tammy._.1218', 'qiaoshi._.1222']}, 'cnm._.0121': {'level': 4, 'at': ['mina1003691', 'zhu.xianzhen', 'che._.0415']}, 'yuu._1110': {'level': 4, 'at': ['lily._.ann1017', 'dora._0306']}, 'esa.0726': {'level': 4, 'at': ['7_y5kl', 'phoe.be410', 'shylie._.1022', 'c.c._y10']}, 'tongu._': {'level': 4, 'at': ['xrx_.10', '09._jing', 'tseng._.0203', 'cy_9926']}, 'hcy.0821_': {'level': 4, 'at': ['lzu_09_802', 'yr__.09___0902.__', 'wwwnmybb', 'j._.gone', 'vanessa_hsu.0108']}, 'zoey.0919': {'level': 4, 'at': []}, 'jdy.__0811': {'level': 4, 'at': []}, 'saythename_17': {'level': 5, 'at': []}, 'wayvofficial': {'level': 5, 'at': []}, 'zb1official': {'level': 5, 'at': []}, 'le_vtime': {'level': 5, 'at': []}, '68_wlsh_102': {'level': 5, 'at': []}, '7_y5kl': {'level': 5, 'at': []}, 'phoe.be410': {'level': 5, 'at': []}, 'shylie._.1022': {'level': 5, 'at': []}, 'c.c._y10': {'level': 5, 'at': []}, 'lzu_09_802': {'level': 5, 'at': []}, 'yr__.09___0902.__': {'level': 5, 'at': []}, 'wwwnmybb': {'level': 5, 'at': []}, 'j._.gone': {'level': 5, 'at': []}, 'vanessa_hsu.0108': {'level': 5, 'at': []}, 'xrx_.10': {'level': 5, 'at': []}, '09._jing': {'level': 5, 'at': []}, 'tseng._.0203': {'level': 5, 'at': []}, 'cy_9926': {'level': 5, 'at': []}, 'lily._.ann1017': {'level': 5, 'at': []}, 'dora._0306': {'level': 5, 'at': []}, 'mina1003691': {'level': 5, 'at': []}, 'zhu.xianzhen': {'level': 5, 'at': []}, 'che._.0415': {'level': 5, 'at': []}, 'lu.981105': {'level': 5, 'at': []}, 'czh._10': {'level': 5, 'at': []}, '_cty.__.0210': {'level': 5, 'at': []}, 'tammy._.1218': {'level': 5, 'at': []}, 'qiaoshi._.1222': {'level': 5, 'at': []}}
    # people = {'elsie__12__': {'level': 0, 'at': ['jx06_t'], 'url': 'https://www.instagram.com/elsie__12__/?next=%2F'}, 'jx06_t': {'level': 1, 'at': ['elsie__12__', 'lsie__12__在追蹤'], 'url': 'https://www.instagram.com/jx06_t/?next=%2F'}}
    # people = {'yuann0722': {'level': 0, 'at': ['rii.1oo', 'nuo971225', 'lsie__12__在追蹤'], 'url': 'https://www.instagram.com/yuann0722/'}, 'rii.1oo': {'level': 1, 'at': ['yuann0722', '1'], 'url': 'https://www.instagram.com/rii.1oo/'}, 'nuo971225': {'level': 1, 'at': ['uo971225', 'iyruins', 'yuann0722', 'i_am_ann123', '97.12.02ww', 'gl.link/nuo971225'], 'url': 'https://www.instagram.com/nuo971225/'}, 'iyruins': {'level': 2, 'at': ['yruins', 'hesiiiimi'], 'url': 'https://www.instagram.com/iyruins/'}, 'i_am_ann123': {'level': 2, 'at': ['nuo971225', 'cuteicebaby2020', 'nn._.731', 'paulweng_.09'], 'url': 'https://www.instagram.com/i_am_ann123/'}, '97.12.02ww': {'level': 2, 'at': ['7.12.02ww', 'nuo971225', 'gl.link/97.12.02ww1'], 'url': 'https://www.instagram.com/97.12.02ww/'}, 'cuteicebaby2020': {'level': 3, 'at': ['kiko990825', 'lin._.980115', 'i_am_ann123'], 'url': 'https://www.instagram.com/cuteicebaby2020/'}, 'nn._.731': {'level': 3, 'at': ['n._.731', 'i_am_ann123', 'citra._.08', 'paulweng_.09', 'nxy_.0925'], 'url': 'https://www.instagram.com/nn._.731/'}, 'paulweng_.09': {'level': 3, 'at': [], 'url': 'https://www.instagram.com/paulweng_.09/'}, 'hesiiiimi': {'level': 3, 'at': ['esiiiimi', 'iyruins'], 'url': 'https://www.instagram.com/hesiiiimi/'}, 'citra._.08': {'level': 4, 'at': ['xy__0823', 'gl.link/citra._.08'], 'url': 'https://www.instagram.com/citra._.08/'}, 'nxy_.0925': {'level': 4, 'at': ['xy_.0925', '08', '新北', '非單', 'anninmirudayo', 'hoshi._.970217', 'nn._.731', 'tangyuxuan201', '9czxin._', 'di._.308', 'gl.link/nxy_.0925'], 'url': 'https://www.instagram.com/nxy_.0925/'}, 'kiko990825': {'level': 4, 'at': ['cuteicebaby2020', 'kiko._.aurora'], 'url': 'https://www.instagram.com/kiko990825/'}, 'lin._.980115': {'level': 4, 'at': ['xinn._.14', 'ling._.980522', 'yun.love.justin', 'cuteicebaby2020', 'li._.jiexin'], 'url': 'https://www.instagram.com/lin._.980115/'}, 'anninmirudayo': {'level': 5, 'at': ['nninmirudayo', 'ww.youtube.com/c/AnninMiruChannel'], 'url': 'https://www.instagram.com/anninmirudayo/'}, 'hoshi._.970217': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/hoshi._.970217/'}, 'tangyuxuan201': {'level': 5, 'at': ['angyuxuan201', 'nicolecuic', 'janic_e0522', 'cy__.29', 'emo._.2735', 'mr.__.0522', 'nxy_.0925', 'lmx._.210', 'huangbrotherss'], 'url': 'https://www.instagram.com/tangyuxuan201/'}, '9czxin._': {'level': 5, 'at': ['czxin._', 'bibi_1223_', 'nxy_.0925', 'yuu._.pq', 'jing._.822_'], 'url': 'https://www.instagram.com/9czxin._/'}, 'di._.308': {'level': 5, 'at': ['0123_.xin', 'nxy_.0925', 'luo.__15', 'zuiyyy_21'], 'url': 'https://www.instagram.com/di._.308/'}, 'xy__0823': {'level': 5, 'at': ['y__0823', 'chia_yun24', 'citra._.08', 'millie.sun26', '_823yee', 'gl.link/xyee2'], 'url': 'https://www.instagram.com/xy__0823/'}, 'xinn._.14': {'level': 5, 'at': ['ccccc__.13', 'lin._.980115', 'chian_.ning', 'nina.liu__'], 'url': 'https://www.instagram.com/xinn._.14/'}, 'ling._.980522': {'level': 5, 'at': ['ing._.980522', 'yu_hsin204', 'an._.1023', 'lin._.980115', 'huayu_0608'], 'url': 'https://www.instagram.com/ling._.980522/'}, 'yun.love.justin': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/yun.love.justin/'}, 'li._.jiexin': {'level': 5, 'at': ['l.jun_217', 'w.y.c0227_', 'yxc.c_xc', 'hsin_______970913', 'lin._.980115', 'linpeiyi79', 'lin._.chiying', 'pinky._.0526', 'ellonym.me/li._.jiexin'], 'url': 'https://www.instagram.com/li._.jiexin/'}, 'kiko._.aurora': {'level': 5, 'at': ['kiko990825'], 'url': 'https://www.instagram.com/kiko._.aurora/'}, '0123_.xin': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/0123_.xin/'}, 'luo.__15': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/luo.__15/'}, 'zuiyyy_21': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/zuiyyy_21/'}, 'bibi_1223_': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/bibi_1223_/'}, 'yuu._.pq': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/yuu._.pq/'}, 'jing._.822_': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/jing._.822_/'}, 'nicolecuic': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/nicolecuic/'}, 'janic_e0522': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/janic_e0522/'}, 'cy__.29': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/cy__.29/'}, 'emo._.2735': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/emo._.2735/'}, 'mr.__.0522': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/mr.__.0522/'}, 'lmx._.210': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/lmx._.210/'}, 'huangbrotherss': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/huangbrotherss/'}, 'chia_yun24': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/chia_yun24/'}, 'millie.sun26': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/millie.sun26/'}, '_823yee': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/_823yee/'}, 'ccccc__.13': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/ccccc__.13/'}, 'chian_.ning': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/chian_.ning/'}, 'nina.liu__': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/nina.liu__/'}, 'yu_hsin204': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/yu_hsin204/'}, 'an._.1023': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/an._.1023/'}, 'huayu_0608': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/huayu_0608/'}, 'l.jun_217': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/l.jun_217/'}, 'w.y.c0227_': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/w.y.c0227_/'}, 'yxc.c_xc': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/yxc.c_xc/'}, 'hsin_______970913': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/hsin_______970913/'}, 'linpeiyi79': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/linpeiyi79/'}, 'lin._.chiying': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/lin._.chiying/'}, 'pinky._.0526': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/pinky._.0526/'}}
    # people = {'shawn_.00': {'level': 0, 'at': ['h__h0813', 'yuan_moche'], 'url': 'https://www.instagram.com/shawn_.00/'}, 'h__h0813': {'level': 1, 'at': ['lzh__215', 'lun_court', 'yuan_moche', 'shawn_.00'], 'url': 'https://www.instagram.com/h__h0813/'}, 'yuan_moche': {'level': 1, 'at': ['h__h0813', 'lzh__215', 'lun_court', '0124_wow'], 'url': 'https://www.instagram.com/yuan_moche/'}, 'lzh__215': {'level': 2, 'at': [], 'url': 'https://www.instagram.com/lzh__215/'}, 'lun_court': {'level': 2, 'at': [], 'url': 'https://www.instagram.com/lun_court/'}, '0124_wow': {'level': 2, 'at': [], 'url': 'https://www.instagram.com/0124_wow/'}}
    people = {'xy__0823': {'level': 0, 'at': ['chia_yun24', 'citra._.08', 'millie.sun26', '_823yee'], 'url': 'https://www.instagram.com/xy__0823/?next=%2F'}, 'chia_yun24': {'level': 1, 'at': ['xy__0823', 'qo_op01.18', 'kali_.0117'], 'url': 'https://www.instagram.com/chia_yun24/?next=%2F'}, 'citra._.08': {'level': 1, 'at': ['xy__0823', 'nn._.731', 'paulweng_.09'], 'url': 'https://www.instagram.com/citra._.08/?next=%2F'}, 'millie.sun26': {'level': 1, 'at': ['m.wildlife_', 'xy__0823', 'shizuku_16045'], 'url': 'https://www.instagram.com/millie.sun26/?next=%2F'}, '_823yee': {'level': 1, 'at': ['xy__0823', 'chia_yun24', 'ting_yuuu0710', '___yue.h', 'joytseng_76', 'lei._10.28', 'ly._09_11'], 'url': 'https://www.instagram.com/_823yee/?next=%2F'}, 'ting_yuuu0710': {'level': 2, 'at': [], 'url': 'https://www.instagram.com/ting_yuuu0710/?next=%2F'}, '___yue.h': {'level': 2, 'at': [], 'url': 'https://www.instagram.com/___yue.h/?next=%2F'}, 'joytseng_76': {'level': 2, 'at': [], 'url': 'https://www.instagram.com/joytseng_76/?next=%2F'}, 'lei._10.28': {'level': 2, 'at': ['lei.__10.28', '_gaxn._'], 'url': 'https://www.instagram.com/lei._10.28/?next=%2F'}, 'ly._09_11': {'level': 2, 'at': ['yeh.shaa_', 'imwinter', 'boynextdoor_official', 'yu.0218_qq', 'xy__0823', '0.cyee', 'yx__98_9_'], 'url': 'https://www.instagram.com/ly._09_11/?next=%2F'}, 'm.wildlife_': {'level': 2, 'at': [], 'url': 'https://www.instagram.com/m.wildlife_/?next=%2F'}, 'shizuku_16045': {'level': 2, 'at': [], 'url': 'https://www.instagram.com/shizuku_16045/?next=%2F'}, 'nn._.731': {'level': 2, 'at': ['dk_is_dokyeom', 'citra._.08', 'paulweng_.09'], 'url': 'https://www.instagram.com/nn._.731/?next=%2F'}, 'paulweng_.09': {'level': 2, 'at': ['nn._.731', 'citra._.08', 'nnzz10._03'], 'url': 'https://www.instagram.com/paulweng_.09/?next=%2F'}, 'qo_op01.18': {'level': 2, 'at': ['qo_op__18', 'tianty_.0328', 'jddk._.0727', 'chia_yun24', 'xin_11_.16', 'y._0857', 'sns_jsks_'], 'url': 'https://www.instagram.com/qo_op01.18/?next=%2F'}, 'kali_.0117': {'level': 2, 'at': ['chia_yun24', 'real_fanchengcheng'], 'url': 'https://www.instagram.com/kali_.0117/?next=%2F'}, 'lei.__10.28': {'level': 3, 'at': ['lei._10.28', '0.cyee', 'zzz._1105'], 'url': 'https://www.instagram.com/lei.__10.28/?next=%2F'}, '_gaxn._': {'level': 3, 'at': ['en._.sansui.6.09', 'lei._10.28', 'rn._0411', 'lty._.0406', 'caifei.l', '__10_zzz'], 'url': 'https://www.instagram.com/_gaxn._/?next=%2F'}, 'yeh.shaa_': {'level': 3, 'at': [], 'url': 'https://www.instagram.com/yeh.shaa_/?next=%2F'}, 'imwinter': {'level': 3, 'at': [], 'url': 'https://www.instagram.com/imwinter/?next=%2F'}, 'boynextdoor_official': {'level': 3, 'at': [], 'url': 'https://www.instagram.com/boynextdoor_official/?next=%2F'}, 'yu.0218_qq': {'level': 3, 'at': ['0724rebecca', 'ly._09_11', 'yuuuuu.y218'], 'url': 'https://www.instagram.com/yu.0218_qq/?next=%2F'}, '0.cyee': {'level': 3, 'at': ['e.cye9_', 'lei.__10.28', '7u.mono', 'ynn._0830', 'rui_xin.427', 'cnyuu.__', 'yicheng._.822', 'ly._09_11'], 'url': 'https://www.instagram.com/0.cyee/?next=%2F'}, 'yx__98_9_': {'level': 3, 'at': ['ly._09_11'], 'url': 'https://www.instagram.com/yx__98_9_/?next=%2F'}, 'dk_is_dokyeom': {'level': 3, 'at': [], 'url': 'https://www.instagram.com/dk_is_dokyeom/?next=%2F'}, 'nnzz10._03': {'level': 3, 'at': ['_chaechae_1', 'faker', 'newjeans_official', 't1__zeus', 'hao_yuan_09_24_', 'kaili185', 'potaa_.07', 'penny_tsai1208', 'paulweng_.09'], 'url': 'https://www.instagram.com/nnzz10._03/?next=%2F'}, 'real_fanchengcheng': {'level': 3, 'at': [], 'url': 'https://www.instagram.com/real_fanchengcheng/?next=%2F'}, 'qo_op__18': {'level': 3, 'at': ['qo_op01.18'], 'url': 'https://www.instagram.com/qo_op__18/?next=%2F'}, 'tianty_.0328': {'level': 3, 'at': ['qo_op01.18'], 'url': 'https://www.instagram.com/tianty_.0328/?next=%2F'}, 'jddk._.0727': {'level': 3, 'at': ['wuuk_0512', 'li_8.23', 'qo_op01.18', 'jbbk._.0512'], 'url': 'https://www.instagram.com/jddk._.0727/?next=%2F'}, 'xin_11_.16': {'level': 3, 'at': ['2011_8_30', 'qo_op01.18', 'xi_az_121', 'min._614'], 'url': 'https://www.instagram.com/xin_11_.16/?next=%2F'}, 'y._0857': {'level': 3, 'at': ['101._.021', 'min._614', 'nana._0323', 'qo_op01.18'], 'url': 'https://www.instagram.com/y._0857/?next=%2F'}, 'sns_jsks_': {'level': 3, 'at': ['qo_op01.18'], 'url': 'https://www.instagram.com/sns_jsks_/?next=%2F'}, 'en._.sansui.6.09': {'level': 4, 'at': ['_gaxn._', 's.u._.i.10'], 'url': 'https://www.instagram.com/en._.sansui.6.09/?next=%2F'}, 'rn._0411': {'level': 4, 'at': ['tcon._.0503'], 'url': 'https://www.instagram.com/rn._0411/?next=%2F'}, 'lty._.0406': {'level': 4, 'at': ['cy.__46', 'linpeiyi._10.6', 'oqe._.0809', '_gaxn._', 'caifei.l', 'yin_09_04', '_xnn.2111', 'amanda_.0701', 'honey_10_14'], 'url': 'https://www.instagram.com/lty._.0406/?next=%2F'}, 'caifei.l': {'level': 4, 'at': ['lty._.0406', '_gaxn._'], 'url': 'https://www.instagram.com/caifei.l/?next=%2F'}, '__10_zzz': {'level': 4, 'at': ['_gaxn._'], 'url': 'https://www.instagram.com/__10_zzz/?next=%2F'}, 'zzz._1105': {'level': 4, 'at': ['zhen.981105', 'ant._.1129', 'xhzzzzzz__', 'lei.__10.28'], 'url': 'https://www.instagram.com/zzz._1105/?next=%2F'}, 'e.cye9_': {'level': 4, 'at': [], 'url': 'https://www.instagram.com/e.cye9_/?next=%2F'}, '7u.mono': {'level': 4, 'at': ['7u.qmj', 'l.0121_.jx', '0.cyee', 'chenxinle0209', '1004.jess', 'cindy_.130', 'xinni_1_4'], 'url': 'https://www.instagram.com/7u.mono/?next=%2F'}, 'ynn._0830': {'level': 4, 'at': ['1109._6', '0125._y', 'e.cye9_', '8cunx_', 'zss._09', 'shylie._.1022'], 'url': 'https://www.instagram.com/ynn._0830/?next=%2F'}, 'rui_xin.427': {'level': 4, 'at': ['gracesung127', '1gy._.an01', 'esa.0726', '0.cyee', 'r_.xin_.427'], 'url': 'https://www.instagram.com/rui_xin.427/?next=%2F'}, 'cnyuu.__': {'level': 4, 'at': ['0.cyee'], 'url': 'https://www.instagram.com/cnyuu.__/?next=%2F'}, 'yicheng._.822': {'level': 4, 'at': ['tang._.827382', 'rui_xin.427', 'zhanggeyu4', 'esa.0726', 'e.cye9_', 'en._.107', 'janey_0127'], 'url': 'https://www.instagram.com/yicheng._.822/?next=%2F'}, '0724rebecca': {'level': 4, 'at': ['z.1__c'], 'url': 'https://www.instagram.com/0724rebecca/?next=%2F'}, 'yuuuuu.y218': {'level': 4, 'at': ['yu.0218_qq'], 'url': 'https://www.instagram.com/yuuuuu.y218/?next=%2F'}, '_chaechae_1': {'level': 4, 'at': [], 'url': 'https://www.instagram.com/_chaechae_1/?next=%2F'}, 'faker': {'level': 4, 'at': ['t1lol'], 'url': 'https://www.instagram.com/faker/?next=%2F'}, 'newjeans_official': {'level': 4, 'at': [], 'url': 'https://www.instagram.com/newjeans_official/?next=%2F'}, 't1__zeus': {'level': 4, 'at': [], 'url': 'https://www.instagram.com/t1__zeus/?next=%2F'}, 'hao_yuan_09_24_': {'level': 4, 'at': ['nnzz10._03', 't.w_c_'], 'url': 'https://www.instagram.com/hao_yuan_09_24_/?next=%2F'}, 'kaili185': {'level': 4, 'at': [], 'url': 'https://www.instagram.com/kaili185/?next=%2F'}, 'potaa_.07': {'level': 4, 'at': [], 'url': 'https://www.instagram.com/potaa_.07/?next=%2F'}, 'penny_tsai1208': {'level': 4, 'at': ['nnzz10._03'], 'url': 'https://www.instagram.com/penny_tsai1208/?next=%2F'}, 'zhen.981105': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/zhen.981105/?next=%2F'}, 'ant._.1129': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/ant._.1129/?next=%2F'}, 'xhzzzzzz__': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/xhzzzzzz__/?next=%2F'}, 'cy.__46': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/cy.__46/?next=%2F'}, 'linpeiyi._10.6': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/linpeiyi._10.6/?next=%2F'}, 'oqe._.0809': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/oqe._.0809/?next=%2F'}, 'yin_09_04': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/yin_09_04/?next=%2F'}, '_xnn.2111': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/_xnn.2111/?next=%2F'}, 'amanda_.0701': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/amanda_.0701/?next=%2F'}, 'honey_10_14': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/honey_10_14/?next=%2F'}, 'tang._.827382': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/tang._.827382/?next=%2F'}, 'zhanggeyu4': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/zhanggeyu4/?next=%2F'}, 'esa.0726': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/esa.0726/?next=%2F'}, 'en._.107': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/en._.107/?next=%2F'}, 'janey_0127': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/janey_0127/?next=%2F'}, 'z.1__c': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/z.1__c/?next=%2F'}, 't.w_c_': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/t.w_c_/?next=%2F'}, 't1lol': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/t1lol/?next=%2F'}, 'gracesung127': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/gracesung127/?next=%2F'}, '1gy._.an01': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/1gy._.an01/?next=%2F'}, 'r_.xin_.427': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/r_.xin_.427/?next=%2F'}, '1109._6': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/1109._6/?next=%2F'}, '0125._y': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/0125._y/?next=%2F'}, '8cunx_': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/8cunx_/?next=%2F'}, 'zss._09': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/zss._09/?next=%2F'}, 'shylie._.1022': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/shylie._.1022/?next=%2F'}, '7u.qmj': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/7u.qmj/?next=%2F'}, 'l.0121_.jx': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/l.0121_.jx/?next=%2F'}, 'chenxinle0209': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/chenxinle0209/?next=%2F'}, '1004.jess': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/1004.jess/?next=%2F'}, 'cindy_.130': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/cindy_.130/?next=%2F'}, 'xinni_1_4': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/xinni_1_4/?next=%2F'}, 'tcon._.0503': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/tcon._.0503/?next=%2F'}, 's.u._.i.10': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/s.u._.i.10/?next=%2F'}, '101._.021': {'level': 4, 'at': [], 'url': 'https://www.instagram.com/101._.021/?next=%2F'}, 'min._614': {'level': 4, 'at': ['nana._0323', 'xin_11_.16', 'yix._6.14', '101._.021', 'y._0857', 'wei_.1203'], 'url': 'https://www.instagram.com/min._614/?next=%2F'}, 'nana._0323': {'level': 4, 'at': ['y._0857', 'guo.clear.12', 'min._614'], 'url': 'https://www.instagram.com/nana._0323/?next=%2F'}, '2011_8_30': {'level': 4, 'at': ['xin_11_.16', '2010_9_05', '2011_1_15'], 'url': 'https://www.instagram.com/2011_8_30/?next=%2F'}, 'xi_az_121': {'level': 4, 'at': ['_1aniy', 'xin_11_.16', 'yuki_1121_014'], 'url': 'https://www.instagram.com/xi_az_121/?next=%2F'}, 'wuuk_0512': {'level': 4, 'at': ['jddk._.0727'], 'url': 'https://www.instagram.com/wuuk_0512/?next=%2F'}, 'li_8.23': {'level': 4, 'at': ['hui._.0708'], 'url': 'https://www.instagram.com/li_8.23/?next=%2F'}, 'jbbk._.0512': {'level': 4, 'at': ['jbbk._.0423'], 'url': 'https://www.instagram.com/jbbk._.0512/?next=%2F'}, 'guo.clear.12': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/guo.clear.12/?next=%2F'}, 'yix._6.14': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/yix._6.14/?next=%2F'}, 'wei_.1203': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/wei_.1203/?next=%2F'}, '2010_9_05': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/2010_9_05/?next=%2F'}, '2011_1_15': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/2011_1_15/?next=%2F'}, '_1aniy': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/_1aniy/?next=%2F'}, 'yuki_1121_014': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/yuki_1121_014/?next=%2F'}, 'jbbk._.0423': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/jbbk._.0423/?next=%2F'}, 'hui._.0708': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/hui._.0708/?next=%2F'}}
    with open(r'output\ckcos16th_241015_21_18.json','r')as f:
        ppp = f.read()
        people = json.loads(ppp)

    graph = PeopleGraph(people)
    graph.show_graph("Sample3",None)

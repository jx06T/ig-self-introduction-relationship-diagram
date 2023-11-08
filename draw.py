import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
import os


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

                self.G.add_edge(key, aAt)
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
        pos = nx.spring_layout(self.G)
        # pos = nx.spring_layout(self.G, pos=nx.kamada_kawai_layout(self.G))
        # pos = nx.spring_layout(self.G, pos=nx.fruchterman_reingold_layout(self.G))
        for node in self.G.nodes:
            nx.draw_networkx_nodes(self.G, pos, nodelist=[node], node_color=self.people[node]["color"], node_size=self.people[node]["size"])
        
        for edge in self.G.edges:
            source_node, target_node = edge
            x1, y1 = pos[source_node]
            x2, y2 = pos[target_node]
            dx = x2 - x1
            dy = y2 - y1
            # t2 = 100000
            t2 = self.SIZE * 4000
            t = self.people[source_node]["size"] / t2
            arrow_position1 = (x1 + t * ((dx > 0) * 2 - 1), y1 + t * ((dy > 0) * 2 - 1))  
            t = self.people[target_node]["size"] / t2
            arrow_position2 = (x2 - t * ((dx > 0) * 2 - 1), y2 - t * ((dy > 0) * 2 - 1)) 
            NewPos = {source_node: arrow_position1, target_node: arrow_position2}
            nx.draw_networkx_edges(self.G, NewPos, edgelist=[edge], width=1.4, arrows=True, arrowstyle=patches.ArrowStyle(self.people[source_node]["state"][target_node], head_length=0.5, head_width=0.1), connectionstyle="arc3, rad=0.2", arrowsize=20)
        
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
            plt.show()
        print("開啟圖片",local_file_path)



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
    people = {
    "4._.4_89": {
        "level": 0,
        "at": [
            "3._.3_u",
            "904_.cookie",
            "wni_fufu",
            "yo__.chen11"
        ],
        "url": "https://www.instagram.com/4._.4_89/",
        "state": {
            "3._.3_u": "<|-|>",
            "904_.cookie": "-|>",
            "wni_fufu": "<|-|>",
            "yo__.chen11": "<|-|>"
        },
        "color": "#ff9663",
        "size": 6200
    },
    "3._.3_u": {
        "level": 1,
        "at": [
            "904_.cookie",
            "wni_fufu",
            "jus._0719",
            "4._.4_89",
            "yo__.chen11",
            "mm._.yypp"
        ],
        "url": "https://www.instagram.com/3._.3_u/",
        "state": {
            "4._.4_89": "<|-|>",
            "904_.cookie": "<|-|>",
            "wni_fufu": "<|-|>",
            "jus._0719": "<|-|>",
            "yo__.chen11": "-|>",
            "mm._.yypp": "<|-|>"
        },
        "color": "#ff3963",
        "size": 4100
    },
    "904_.cookie": {
        "level": 1,
        "at": [
            "cook_.0930",
            "wni_fufu",
            "kathy_07_15",
            "yuann0722",
            "3._.3_u"
        ],
        "url": "https://www.instagram.com/904_.cookie/",
        "state": {
            "3._.3_u": "<|-|>",
            "cook_.0930": "-|>",
            "wni_fufu": "<|-|>",
            "kathy_07_15": "-|>",
            "yuann0722": "-|>"
        },
        "color": "#ffa063",
        "size": 4100
    },
    "wni_fufu": {
        "level": 1,
        "at": [
            "904_.cookie",
            "3._.3_u",
            "4._.4_89",
            "hongjuan319",
            "allen._.91957",
            "rosser_13y"
        ],
        "url": "https://www.instagram.com/wni_fufu/",
        "state": {
            "4._.4_89": "<|-|>",
            "3._.3_u": "<|-|>",
            "904_.cookie": "<|-|>",
            "hongjuan319": "-|>",
            "allen._.91957": "-|>",
            "rosser_13y": "<|-|>"
        },
        "color": "#ff3963",
        "size": 4100
    },
    "yo__.chen11": {
        "level": 1,
        "at": [
            "4._.4_89"
        ],
        "url": "https://www.instagram.com/yo__.chen11/",
        "state": {
            "4._.4_89": "<|-|>"
        },
        "color": "#d4ff63",
        "size": 4100
    },
    "hongjuan319": {
        "level": 2,
        "at": [],
        "url": "https://www.instagram.com/hongjuan319/",
        "state": {},
        "color": "#9aff63",
        "size": 3500
    },
    "allen._.91957": {
        "level": 2,
        "at": [
            "allen._.98518",
            "hyl._.1030"
        ],
        "url": "https://www.instagram.com/allen._.91957/",
        "state": {
            "allen._.98518": "<|-|>",
            "hyl._.1030": "<|-|>"
        },
        "color": "#e6ff63",
        "size": 3500
    },
    "rosser_13y": {
        "level": 2,
        "at": [
            "mw_19rx",
            "yb_minnie",
            "wni_fufu"
        ],
        "url": "https://www.instagram.com/rosser_13y/",
        "state": {
            "wni_fufu": "<|-|>",
            "mw_19rx": "<|-|>",
            "yb_minnie": "<|-|>"
        },
        "color": "#ffe063",
        "size": 3500
    },
    "jus._0719": {
        "level": 2,
        "at": [
            "ynn._.20",
            "3._.3_u",
            "904_.cookie",
            "wni_fufu"
        ],
        "url": "https://www.instagram.com/jus._0719/",
        "state": {
            "3._.3_u": "<|-|>",
            "ynn._.20": "-|>",
            "904_.cookie": "-|>",
            "wni_fufu": "-|>"
        },
        "color": "#ff9b63",
        "size": 3500
    },
    "mm._.yypp": {
        "level": 2,
        "at": [
            "mm._.ppyy",
            "3._.3_u"
        ],
        "url": "https://www.instagram.com/mm._.yypp/",
        "state": {
            "3._.3_u": "<|-|>",
            "mm._.ppyy": "<|-|>"
        },
        "color": "#fff763",
        "size": 3500
    },
    "cook_.0930": {
        "level": 2,
        "at": [],
        "url": "https://www.instagram.com/cook_.0930/",
        "state": {},
        "color": "#9fff63",
        "size": 3500
    },
    "kathy_07_15": {
        "level": 2,
        "at": [
            "penny980303",
            "jkz_0919",
            "hc180_"
        ],
        "url": "https://www.instagram.com/kathy_07_15/",
        "state": {
            "penny980303": "<|-|>",
            "jkz_0919": "-|>",
            "hc180_": "-|>"
        },
        "color": "#ffd063",
        "size": 3500
    },
    "yuann0722": {
        "level": 2,
        "at": [
            "rii.1oo",
            "nuo971225"
        ],
        "url": "https://www.instagram.com/yuann0722/",
        "state": {
            "rii.1oo": "<|-|>",
            "nuo971225": "<|-|>"
        },
        "color": "#ddff63",
        "size": 3500
    },
    "mw_19rx": {
        "level": 3,
        "at": [
            "rosser_13y",
            "yen122._7",
            "dorcas.610"
        ],
        "url": "https://www.instagram.com/mw_19rx/",
        "state": {
            "rosser_13y": "<|-|>",
            "yen122._7": "<|-|>",
            "dorcas.610": "<|-|>"
        },
        "color": "#fff463",
        "size": 2900
    },
    "yb_minnie": {
        "level": 3,
        "at": [
            "tina._.0429",
            "qian._.724",
            "rosser_13y"
        ],
        "url": "https://www.instagram.com/yb_minnie/",
        "state": {
            "rosser_13y": "<|-|>",
            "tina._.0429": "-|>",
            "qian._.724": "<|-|>"
        },
        "color": "#ffe063",
        "size": 2900
    },
    "allen._.98518": {
        "level": 3,
        "at": [
            "hyl._.lin",
            "nick11543",
            "shawn_.00",
            "jsn244.__.safe",
            "allen._.91957"
        ],
        "url": "https://www.instagram.com/allen._.98518/",
        "state": {
            "allen._.91957": "<|-|>",
            "hyl._.lin": "<|-|>",
            "nick11543": "<|-|>",
            "shawn_.00": "-|>",
            "jsn244.__.safe": "<|-|>"
        },
        "color": "#ff7063",
        "size": 2900
    },
    "hyl._.1030": {
        "level": 3,
        "at": [
            "hyl._.lin",
            "allen._.91957"
        ],
        "url": "https://www.instagram.com/hyl._.1030/",
        "state": {
            "allen._.91957": "<|-|>",
            "hyl._.lin": "-|>"
        },
        "color": "#fff463",
        "size": 2900
    },
    "mm._.ppyy": {
        "level": 3,
        "at": [
            "mm._.yypp"
        ],
        "url": "https://www.instagram.com/mm._.ppyy/",
        "state": {
            "mm._.yypp": "<|-|>"
        },
        "color": "#d2ff63",
        "size": 2900
    },
    "ynn._.20": {
        "level": 3,
        "at": [],
        "url": "https://www.instagram.com/ynn._.20/",
        "state": {},
        "color": "#a1ff63",
        "size": 2900
    },
    "penny980303": {
        "level": 3,
        "at": [
            "kathy_07_15",
            "zounixuan",
            "love_2020_12_23"
        ],
        "url": "https://www.instagram.com/penny980303/",
        "state": {
            "kathy_07_15": "<|-|>",
            "zounixuan": "<|-|>",
            "love_2020_12_23": "<|-|>"
        },
        "color": "#ffec63",
        "size": 2900
    },
    "jkz_0919": {
        "level": 3,
        "at": [],
        "url": "https://www.instagram.com/jkz_0919/",
        "state": {},
        "color": "#9fff63",
        "size": 2900
    },
    "hc180_": {
        "level": 3,
        "at": [
            "immmina._"
        ],
        "url": "https://www.instagram.com/hc180_/",
        "state": {
            "immmina._": "<|-|>"
        },
        "color": "#d6ff63",
        "size": 2900
    },
    "rii.1oo": {
        "level": 3,
        "at": [
            "yuann0722"
        ],
        "url": "https://www.instagram.com/rii.1oo/",
        "state": {
            "yuann0722": "<|-|>"
        },
        "color": "#caff63",
        "size": 2900
    },
    "nuo971225": {
        "level": 3,
        "at": [
            "iyruins",
            "yuann0722",
            "i_am_ann123",
            "97.12.02ww"
        ],
        "url": "https://www.instagram.com/nuo971225/",
        "state": {
            "yuann0722": "<|-|>",
            "iyruins": "-|>",
            "i_am_ann123": "<|-|>",
            "97.12.02ww": "<|-|>"
        },
        "color": "#ff9b63",
        "size": 2900
    },
    "yen122._7": {
        "level": 4,
        "at": [
            "mw_19rx",
            "lunayu593"
        ],
        "url": "https://www.instagram.com/yen122._7/",
        "state": {
            "mw_19rx": "<|-|>",
            "lunayu593": "-|>"
        },
        "color": "#efff63",
        "size": 2300
    },
    "dorcas.610": {
        "level": 4,
        "at": [
            "mw_19rx",
            "ty6._.15"
        ],
        "url": "https://www.instagram.com/dorcas.610/",
        "state": {
            "mw_19rx": "<|-|>",
            "ty6._.15": "-|>"
        },
        "color": "#fff163",
        "size": 2300
    },
    "tina._.0429": {
        "level": 4,
        "at": [
            "oliver_1_31",
            "tammy._.1218"
        ],
        "url": "https://www.instagram.com/tina._.0429/",
        "state": {
            "oliver_1_31": "<|-|>",
            "tammy._.1218": "<|-|>"
        },
        "color": "#e3ff63",
        "size": 2300
    },
    "qian._.724": {
        "level": 4,
        "at": [
            "yu._.qian0724",
            "yun.jie_1107",
            "yb_minnie",
            "zzx_.0806"
        ],
        "url": "https://www.instagram.com/qian._.724/",
        "state": {
            "yb_minnie": "<|-|>",
            "yu._.qian0724": "<|-|>",
            "yun.jie_1107": "-|>",
            "zzx_.0806": "<|-|>"
        },
        "color": "#ff9663",
        "size": 2300
    },
    "hyl._.lin": {
        "level": 4,
        "at": [
            "allen._.98518",
            "wyjjj_903",
            "cook_.0930",
            "yucc.__.922",
            "mizi._l_o_v_e",
            "mia_t000",
            "grs_5568",
            "jsn244.__.safe"
        ],
        "url": "https://www.instagram.com/hyl._.lin/",
        "state": {
            "allen._.98518": "<|-|>",
            "wyjjj_903": "<|-|>",
            "cook_.0930": "-|>",
            "yucc.__.922": "<|-|>",
            "mizi._l_o_v_e": "<|-|>",
            "mia_t000": "<|-|>",
            "grs_5568": "<|-|>",
            "jsn244.__.safe": "<|-|>"
        },
        "color": "#ff1f63",
        "size": 2300
    },
    "nick11543": {
        "level": 4,
        "at": [
            "allen._.98518",
            "904_.cookie",
            "ley._0106",
            "4._.4_89",
            "linyouchen988"
        ],
        "url": "https://www.instagram.com/nick11543/",
        "state": {
            "allen._.98518": "<|-|>",
            "904_.cookie": "-|>",
            "ley._0106": "-|>",
            "4._.4_89": "-|>",
            "linyouchen988": "-|>"
        },
        "color": "#ff5863",
        "size": 2300
    },
    "shawn_.00": {
        "level": 4,
        "at": [
            "h__h0813",
            "yuan_moche"
        ],
        "url": "https://www.instagram.com/shawn_.00/",
        "state": {
            "h__h0813": "<|-|>",
            "yuan_moche": "-|>"
        },
        "color": "#feff63",
        "size": 2300
    },
    "jsn244.__.safe": {
        "level": 4,
        "at": [
            "junn._.725",
            "h__h0813",
            "4._.4_89",
            "yuan_moche",
            "rora.03.02",
            "mizi._l_o_v_e",
            "allen._.98518",
            "hyl._.lin",
            "3._.3_u",
            "sillek_uahaqnsfaui"
        ],
        "url": "https://www.instagram.com/jsn244.__.safe/",
        "state": {
            "allen._.98518": "<|-|>",
            "hyl._.lin": "<|-|>",
            "junn._.725": "-|>",
            "h__h0813": "-|>",
            "4._.4_89": "-|>",
            "yuan_moche": "-|>",
            "rora.03.02": "-|>",
            "mizi._l_o_v_e": "-|>",
            "3._.3_u": "-|>",
            "sillek_uahaqnsfaui": "<|-|>"
        },
        "color": "#ff0063",
        "size": 2300
    },
    "zounixuan": {
        "level": 4,
        "at": [
            "emma971005",
            "yuting._.0930",
            "zys.1123",
            "penny980303",
            "_yulia__1008",
            "junjunwang26"
        ],
        "url": "https://www.instagram.com/zounixuan/",
        "state": {
            "penny980303": "<|-|>",
            "emma971005": "<|-|>",
            "yuting._.0930": "-|>",
            "zys.1123": "<|-|>",
            "_yulia__1008": "-|>",
            "junjunwang26": "<|-|>"
        },
        "color": "#ff7f63",
        "size": 2300
    },
    "love_2020_12_23": {
        "level": 4,
        "at": [
            "penny980303"
        ],
        "url": "https://www.instagram.com/love_2020_12_23/",
        "state": {
            "penny980303": "<|-|>"
        },
        "color": "#d4ff63",
        "size": 2300
    },
    "immmina._": {
        "level": 4,
        "at": [
            "hc180_"
        ],
        "url": "https://www.instagram.com/immmina._/",
        "state": {
            "hc180_": "<|-|>"
        },
        "color": "#c8ff63",
        "size": 2300
    },
    "iyruins": {
        "level": 4,
        "at": [
            "hesiiiimi"
        ],
        "url": "https://www.instagram.com/iyruins/",
        "state": {
            "hesiiiimi": "<|-|>"
        },
        "color": "#b8ff63",
        "size": 2300
    },
    "i_am_ann123": {
        "level": 4,
        "at": [
            "nuo971225",
            "cuteicebaby2020",
            "nn._.731",
            "paulweng_.09"
        ],
        "url": "https://www.instagram.com/i_am_ann123/",
        "state": {
            "nuo971225": "<|-|>",
            "cuteicebaby2020": "<|-|>",
            "nn._.731": "<|-|>",
            "paulweng_.09": "-|>"
        },
        "color": "#ff9163",
        "size": 2300
    },
    "97.12.02ww": {
        "level": 4,
        "at": [
            "nuo971225"
        ],
        "url": "https://www.instagram.com/97.12.02ww/",
        "state": {
            "nuo971225": "<|-|>"
        },
        "color": "#beff63",
        "size": 2300
    },
    "ty6._.15": {
        "level": 5,
        "at": [
            "yue._.lxmi"
        ],
        "url": "https://www.instagram.com/ty6._.15/",
        "state": {
            "yue._.lxmi": "-|>"
        },
        "color": "#b8ff63",
        "size": 1700
    },
    "yu._.qian0724": {
        "level": 5,
        "at": [
            "qian._.724",
            "yujie.10"
        ],
        "url": "https://www.instagram.com/yu._.qian0724/",
        "state": {
            "qian._.724": "<|-|>",
            "yujie.10": "-|>"
        },
        "color": "#ddff63",
        "size": 1700
    },
    "yun.jie_1107": {
        "level": 5,
        "at": [
            "lzyh_0527",
            "zzx_.0806",
            "zy_6.24"
        ],
        "url": "https://www.instagram.com/yun.jie_1107/",
        "state": {
            "lzyh_0527": "-|>",
            "zzx_.0806": "-|>",
            "zy_6.24": "-|>"
        },
        "color": "#ffe063",
        "size": 1700
    },
    "zzx_.0806": {
        "level": 5,
        "at": [
            "_cn._102",
            "zy_6.24",
            "yunn._1107",
            "qian._.724",
            "sunnyy_1015"
        ],
        "url": "https://www.instagram.com/zzx_.0806/",
        "state": {
            "qian._.724": "<|-|>",
            "_cn._102": "-|>",
            "zy_6.24": "-|>",
            "yunn._1107": "-|>",
            "sunnyy_1015": "-|>"
        },
        "color": "#ffb263",
        "size": 1700
    },
    "wyjjj_903": {
        "level": 5,
        "at": [
            "_1yunny",
            "hyl._.lin",
            "yccc8_",
            "yn._.9.24_"
        ],
        "url": "https://www.instagram.com/wyjjj_903/",
        "state": {
            "hyl._.lin": "<|-|>",
            "_1yunny": "-|>",
            "yccc8_": "-|>",
            "yn._.9.24_": "-|>"
        },
        "color": "#ffd263",
        "size": 1700
    },
    "yucc.__.922": {
        "level": 5,
        "at": [
            "hyl._.lin",
            "mia_t000",
            "mizi._l_o_v_e",
            "cheng941027"
        ],
        "url": "https://www.instagram.com/yucc.__.922/",
        "state": {
            "hyl._.lin": "<|-|>",
            "mia_t000": "<|-|>",
            "mizi._l_o_v_e": "-|>",
            "cheng941027": "-|>"
        },
        "color": "#ffbe63",
        "size": 1700
    },
    "mizi._l_o_v_e": {
        "level": 5,
        "at": [
            "mia_t000",
            "hyl._.lin"
        ],
        "url": "https://www.instagram.com/mizi._l_o_v_e/",
        "state": {
            "hyl._.lin": "<|-|>",
            "mia_t000": "<|-|>"
        },
        "color": "#fbff63",
        "size": 1700
    },
    "mia_t000": {
        "level": 5,
        "at": [
            "yb_minnie",
            "b_doy0000",
            "s_m_i_l_e_9_9",
            "mizi._l_o_v_e",
            "wyjjj_903",
            "hyl._.lin",
            "yucc.__.922",
            "jus._0719"
        ],
        "url": "https://www.instagram.com/mia_t000/",
        "state": {
            "hyl._.lin": "<|-|>",
            "yucc.__.922": "<|-|>",
            "mizi._l_o_v_e": "<|-|>",
            "yb_minnie": "-|>",
            "b_doy0000": "-|>",
            "s_m_i_l_e_9_9": "-|>",
            "wyjjj_903": "-|>",
            "jus._0719": "-|>"
        },
        "color": "#ff0063",
        "size": 1700
    },
    "grs_5568": {
        "level": 5,
        "at": [
            "cook_.0930",
            "hyl._.lin",
            "leo98_0324",
            "yo__.chen11",
            "4._.4_89"
        ],
        "url": "https://www.instagram.com/grs_5568/",
        "state": {
            "hyl._.lin": "<|-|>",
            "cook_.0930": "-|>",
            "leo98_0324": "-|>",
            "yo__.chen11": "-|>",
            "4._.4_89": "-|>"
        },
        "color": "#ff6a63",
        "size": 1700
    },
    "junn._.725": {
        "level": 5,
        "at": [],
        "url": "https://www.instagram.com/junn._.725/",
        "state": {},
        "color": "#9cff63",
        "size": 1700
    },
    "h__h0813": {
        "level": 5,
        "at": [
            "lzh__215",
            "lun_court",
            "yuan_moche",
            "shawn_.00"
        ],
        "url": "https://www.instagram.com/h__h0813/",
        "state": {
            "shawn_.00": "<|-|>",
            "lzh__215": "-|>",
            "lun_court": "-|>",
            "yuan_moche": "<|-|>"
        },
        "color": "#ffc863",
        "size": 1700
    },
    "yuan_moche": {
        "level": 5,
        "at": [
            "h__h0813",
            "lzh__215",
            "lun_court",
            "0124_wow"
        ],
        "url": "https://www.instagram.com/yuan_moche/",
        "state": {
            "h__h0813": "<|-|>",
            "lzh__215": "-|>",
            "lun_court": "-|>",
            "0124_wow": "-|>"
        },
        "color": "#ffc863",
        "size": 1700
    },
    "rora.03.02": {
        "level": 5,
        "at": [
            "pn.07.06"
        ],
        "url": "https://www.instagram.com/rora.03.02/",
        "state": {
            "pn.07.06": "-|>"
        },
        "color": "#b8ff63",
        "size": 1700
    },
    "sillek_uahaqnsfaui": {
        "level": 5,
        "at": [
            "jsn244.__.safe"
        ],
        "url": "https://www.instagram.com/sillek_uahaqnsfaui/",
        "state": {
            "jsn244.__.safe": "<|-|>"
        },
        "color": "#c8ff63",
        "size": 1700
    },
    "ley._0106": {
        "level": 5,
        "at": [],
        "url": "https://www.instagram.com/ley._0106/",
        "state": {},
        "color": "#9eff63",
        "size": 1700
    },
    "linyouchen988": {
        "level": 5,
        "at": [],
        "url": "https://www.instagram.com/linyouchen988/",
        "state": {},
        "color": "#a0ff63",
        "size": 1700
    },
    "oliver_1_31": {
        "level": 5,
        "at": [
            "tina._.0429"
        ],
        "url": "https://www.instagram.com/oliver_1_31/",
        "state": {
            "tina._.0429": "<|-|>"
        },
        "color": "#c8ff63",
        "size": 1700
    },
    "tammy._.1218": {
        "level": 5,
        "at": [
            "tina._.0429",
            "zzq_0119",
            "cyt_0129",
            "_zjlx.10"
        ],
        "url": "https://www.instagram.com/tammy._.1218/",
        "state": {
            "tina._.0429": "<|-|>",
            "zzq_0119": "-|>",
            "cyt_0129": "-|>",
            "_zjlx.10": "-|>"
        },
        "color": "#ffd263",
        "size": 1700
    },
    "yue._.lxmi": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/yue._.lxmi/",
        "state": {},
        "color": "#97ff63",
        "size": 1100
    },
    "_cn._102": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/_cn._102/",
        "state": {},
        "color": "#93ff63",
        "size": 1100
    },
    "zy_6.24": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/zy_6.24/",
        "state": {},
        "color": "#95ff63",
        "size": 1100
    },
    "yunn._1107": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/yunn._1107/",
        "state": {},
        "color": "#9cff63",
        "size": 1100
    },
    "sunnyy_1015": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/sunnyy_1015/",
        "state": {},
        "color": "#9eff63",
        "size": 1100
    },
    "leo98_0324": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/leo98_0324/",
        "state": {},
        "color": "#99ff63",
        "size": 1100
    },
    "pn.07.06": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/pn.07.06/",
        "state": {},
        "color": "#9cff63",
        "size": 1100
    },
    "zzq_0119": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/zzq_0119/",
        "state": {},
        "color": "#9eff63",
        "size": 1100
    },
    "cyt_0129": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/cyt_0129/",
        "state": {},
        "color": "#a1ff63",
        "size": 1100
    },
    "_zjlx.10": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/_zjlx.10/",
        "state": {},
        "color": "#95ff63",
        "size": 1100
    },
    "lzh__215": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/lzh__215/",
        "state": {},
        "color": "#a1ff63",
        "size": 1100
    },
    "lun_court": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/lun_court/",
        "state": {},
        "color": "#9fff63",
        "size": 1100
    },
    "0124_wow": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/0124_wow/",
        "state": {},
        "color": "#9aff63",
        "size": 1100
    },
    "b_doy0000": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/b_doy0000/",
        "state": {},
        "color": "#9bff63",
        "size": 1100
    },
    "s_m_i_l_e_9_9": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/s_m_i_l_e_9_9/",
        "state": {},
        "color": "#94ff63",
        "size": 1100
    },
    "cheng941027": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/cheng941027/",
        "state": {},
        "color": "#9cff63",
        "size": 1100
    },
    "_1yunny": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/_1yunny/",
        "state": {},
        "color": "#a0ff63",
        "size": 1100
    },
    "yccc8_": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/yccc8_/",
        "state": {},
        "color": "#97ff63",
        "size": 1100
    },
    "yn._.9.24_": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/yn._.9.24_/",
        "state": {},
        "color": "#95ff63",
        "size": 1100
    },
    "lzyh_0527": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/lzyh_0527/",
        "state": {},
        "color": "#94ff63",
        "size": 1100
    },
    "yujie.10": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/yujie.10/",
        "state": {},
        "color": "#9eff63",
        "size": 1100
    },
    "cuteicebaby2020": {
        "level": 5,
        "at": [
            "kiko990825",
            "lin._.980115",
            "i_am_ann123"
        ],
        "url": "https://www.instagram.com/cuteicebaby2020/",
        "state": {
            "i_am_ann123": "<|-|>",
            "kiko990825": "-|>",
            "lin._.980115": "-|>"
        },
        "color": "#ffd063",
        "size": 1700
    },
    "nn._.731": {
        "level": 5,
        "at": [
            "i_am_ann123",
            "citra._.08",
            "paulweng_.09",
            "nxy_.0925"
        ],
        "url": "https://www.instagram.com/nn._.731/",
        "state": {
            "i_am_ann123": "<|-|>",
            "citra._.08": "-|>",
            "paulweng_.09": "-|>",
            "nxy_.0925": "-|>"
        },
        "color": "#ffc863",
        "size": 1700
    },
    "paulweng_.09": {
        "level": 5,
        "at": [],
        "url": "https://www.instagram.com/paulweng_.09/",
        "state": {},
        "color": "#a2ff63",
        "size": 1700
    },
    "hesiiiimi": {
        "level": 5,
        "at": [
            "iyruins"
        ],
        "url": "https://www.instagram.com/hesiiiimi/",
        "state": {
            "iyruins": "<|-|>"
        },
        "color": "#c8ff63",
        "size": 1700
    },
    "emma971005": {
        "level": 5,
        "at": [
            "zounixuan",
            "chen.l.0501",
            "lin_.329",
            "train._.0416",
            "zys.1123",
            "wf._.908",
            "emma_10.05"
        ],
        "url": "https://www.instagram.com/emma971005/",
        "state": {
            "zounixuan": "<|-|>",
            "chen.l.0501": "-|>",
            "lin_.329": "-|>",
            "train._.0416": "-|>",
            "zys.1123": "<|-|>",
            "wf._.908": "-|>",
            "emma_10.05": "-|>"
        },
        "color": "#ff2863",
        "size": 1700
    },
    "yuting._.0930": {
        "level": 5,
        "at": [],
        "url": "https://www.instagram.com/yuting._.0930/",
        "state": {},
        "color": "#98ff63",
        "size": 1700
    },
    "zys.1123": {
        "level": 5,
        "at": [
            "yne.1214",
            "chloeyeh0619",
            "tang_.1023",
            "_a.cy_96",
            "zounixuan",
            "emma971005",
            "yuting._.0930",
            "wsofia_02_16"
        ],
        "url": "https://www.instagram.com/zys.1123/",
        "state": {
            "zounixuan": "<|-|>",
            "emma971005": "<|-|>",
            "yne.1214": "-|>",
            "chloeyeh0619": "-|>",
            "tang_.1023": "-|>",
            "_a.cy_96": "-|>",
            "yuting._.0930": "-|>",
            "wsofia_02_16": "-|>"
        },
        "color": "#ff0063",
        "size": 1700
    },
    "_yulia__1008": {
        "level": 5,
        "at": [
            "yuliaaaa1008",
            "blackpinkofficial",
            "babymonster_ygofficial",
            "_yiting__"
        ],
        "url": "https://www.instagram.com/_yulia__1008/",
        "state": {
            "yuliaaaa1008": "-|>",
            "blackpinkofficial": "-|>",
            "babymonster_ygofficial": "-|>",
            "_yiting__": "-|>"
        },
        "color": "#ffaa63",
        "size": 1700
    },
    "junjunwang26": {
        "level": 5,
        "at": [
            "zounixuan"
        ],
        "url": "https://www.instagram.com/junjunwang26/",
        "state": {
            "zounixuan": "<|-|>"
        },
        "color": "#d2ff63",
        "size": 1700
    },
    "lunayu593": {
        "level": 5,
        "at": [],
        "url": "https://www.instagram.com/lunayu593/",
        "state": {},
        "color": "#96ff63",
        "size": 1700
    },
    "kiko990825": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/kiko990825/",
        "state": {},
        "color": "#9eff63",
        "size": 1100
    },
    "lin._.980115": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/lin._.980115/",
        "state": {},
        "color": "#9bff63",
        "size": 1100
    },
    "citra._.08": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/citra._.08/",
        "state": {},
        "color": "#9dff63",
        "size": 1100
    },
    "nxy_.0925": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/nxy_.0925/",
        "state": {},
        "color": "#9eff63",
        "size": 1100
    },
    "yne.1214": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/yne.1214/",
        "state": {},
        "color": "#95ff63",
        "size": 1100
    },
    "chloeyeh0619": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/chloeyeh0619/",
        "state": {},
        "color": "#9fff63",
        "size": 1100
    },
    "tang_.1023": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/tang_.1023/",
        "state": {},
        "color": "#a2ff63",
        "size": 1100
    },
    "_a.cy_96": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/_a.cy_96/",
        "state": {},
        "color": "#a0ff63",
        "size": 1100
    },
    "wsofia_02_16": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/wsofia_02_16/",
        "state": {},
        "color": "#96ff63",
        "size": 1100
    },
    "chen.l.0501": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/chen.l.0501/",
        "state": {},
        "color": "#98ff63",
        "size": 1100
    },
    "lin_.329": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/lin_.329/",
        "state": {},
        "color": "#9aff63",
        "size": 1100
    },
    "train._.0416": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/train._.0416/",
        "state": {},
        "color": "#93ff63",
        "size": 1100
    },
    "wf._.908": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/wf._.908/",
        "state": {},
        "color": "#96ff63",
        "size": 1100
    },
    "emma_10.05": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/emma_10.05/",
        "state": {},
        "color": "#97ff63",
        "size": 1100
    },
    "yuliaaaa1008": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/yuliaaaa1008/",
        "state": {},
        "color": "#a2ff63",
        "size": 1100
    },
    "blackpinkofficial": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/blackpinkofficial/",
        "state": {},
        "color": "#99ff63",
        "size": 1100
    },
    "babymonster_ygofficial": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/babymonster_ygofficial/",
        "state": {},
        "color": "#a3ff63",
        "size": 1100
    },
    "_yiting__": {
        "level": 6,
        "at": [],
        "url": "https://www.instagram.com/_yiting__/",
        "state": {},
        "color": "#98ff63",
        "size": 1100
    }
}
    graph = PeopleGraph(people)
    graph.show_graph("Sample",None)

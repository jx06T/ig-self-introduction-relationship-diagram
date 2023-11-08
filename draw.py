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
    
            for aAt in value["at"]:
                # print(key,aAt)
                if  aAt in self.people[key]["state"]:
                    if self.people[key]["state"][aAt] == '<|-|>':
                        continue

                self.G.add_edge(key, aAt)
                self.people[key]["state"][aAt] = '-|>'
                if aAt not in self.people:
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
    people = {'xy__0823': {'level': 0, 'at': ['chia_yun24', 'citra._.08', 'millie.sun26', '_823yee']}, 'chia_yun24': {'level': 1, 'at': ['kali_.0117']}, 'citra._.08': {'level': 1, 'at': []}, 'millie.sun26': {'level': 1, 'at': ['m.wildlife_', 'liyliy_0911', 'agnes101229']}, '_823yee': {'level': 1, 'at': ['ting_yuuu0710', '___yue.h', 'joytseng_76', 'bella._.wee', 'lei._10.28', 'ly._09_11', 'ninibaba0223', 'li7nniuy.__']}, 'm.wildlife_': {'level': 2, 'at': []}, 'liyliy_0911': {'level': 2, 'at': []}, 'agnes101229': {'level': 2, 'at': ['su_athena', '101229_luna']}, 'kali_.0117': {'level': 2, 'at': ['yun_tseng7', 'i42kip']}, 'ting_yuuu0710': {'level': 2, 'at': []}, '___yue.h': {'level': 2, 'at': ['39saku_chan']}, 'joytseng_76': {'level': 2, 'at': []}, 'bella._.wee': {'level': 2, 'at': []}, 'lei._10.28': {'level': 2, 'at': []}, 'ly._09_11': {'level': 2, 'at': ['yu.0218_qq', 'riky.820', '7zqx__', '_cl.920']}, 'ninibaba0223': {'level': 2, 'at': ['smile0223__', 'ccc.___.0812', 'zyutong1208', 'zoey_.0919']}, 'li7nniuy.__': {'level': 2, 'at': ['panyunlin7_amis', 'lin._.3.22']}, 'su_athena': {'level': 3, 'at': []}, '101229_luna': {'level': 3, 'at': []}, 'yun_tseng7': {'level': 3, 'at': ['ck_yu_2534', 'wzh_.shiyu_u']}, 'i42kip': {'level': 3, 'at': []}, '39saku_chan': {'level': 3, 'at': []}, 'yu.0218_qq': {'level': 3, 'at': []}, 'riky.820': {'level': 3, 'at': []}, '7zqx__': {'level': 3, 'at': ['cshs102__']}, '_cl.920': {'level': 3, 'at': ['roses_are_rosie', '_zjlx.10', 'cnm._.0121', 'yuu._1110', 'esa.0726']}, 'panyunlin7_amis': {'level': 3, 'at': []}, 'lin._.3.22': {'level': 3, 'at': ['tongu._', 'hcy.0821_']}, 'smile0223__': {'level': 3, 'at': []}, 'ccc.___.0812': {'level': 3, 'at': []}, 'zyutong1208': {'level': 3, 'at': []}, 'zoey_.0919': {'level': 3, 'at': ['zoey.0919', 'jdy.__0811']}, 'ck_yu_2534': {'level': 4, 'at': []}, 'wzh_.shiyu_u': {'level': 4, 'at': ['saythename_17', 'wayvofficial', 'zb1official', 'le_vtime']}, 'cshs102__': {'level': 4, 'at': ['68_wlsh_102']}, 'roses_are_rosie': {'level': 4, 'at': []}, '_zjlx.10': {'level': 4, 'at': ['lu.981105', 'czh._10', '_cty.__.0210', 'tammy._.1218', 'qiaoshi._.1222']}, 'cnm._.0121': {'level': 4, 'at': ['mina1003691', 'zhu.xianzhen', 'che._.0415']}, 'yuu._1110': {'level': 4, 'at': ['lily._.ann1017', 'dora._0306']}, 'esa.0726': {'level': 4, 'at': ['7_y5kl', 'phoe.be410', 'shylie._.1022', 'c.c._y10']}, 'tongu._': {'level': 4, 'at': ['xrx_.10', '09._jing', 'tseng._.0203', 'cy_9926']}, 'hcy.0821_': {'level': 4, 'at': ['lzu_09_802', 'yr__.09___0902.__', 'wwwnmybb', 'j._.gone', 'vanessa_hsu.0108']}, 'zoey.0919': {'level': 4, 'at': []}, 'jdy.__0811': {'level': 4, 'at': []}, 'saythename_17': {'level': 5, 'at': []}, 'wayvofficial': {'level': 5, 'at': []}, 'zb1official': {'level': 5, 'at': []}, 'le_vtime': {'level': 5, 'at': []}, '68_wlsh_102': {'level': 5, 'at': []}, '7_y5kl': {'level': 5, 'at': []}, 'phoe.be410': {'level': 5, 'at': []}, 'shylie._.1022': {'level': 5, 'at': []}, 'c.c._y10': {'level': 5, 'at': []}, 'lzu_09_802': {'level': 5, 'at': []}, 'yr__.09___0902.__': {'level': 5, 'at': []}, 'wwwnmybb': {'level': 5, 'at': []}, 'j._.gone': {'level': 5, 'at': []}, 'vanessa_hsu.0108': {'level': 5, 'at': []}, 'xrx_.10': {'level': 5, 'at': []}, '09._jing': {'level': 5, 'at': []}, 'tseng._.0203': {'level': 5, 'at': []}, 'cy_9926': {'level': 5, 'at': []}, 'lily._.ann1017': {'level': 5, 'at': []}, 'dora._0306': {'level': 5, 'at': []}, 'mina1003691': {'level': 5, 'at': []}, 'zhu.xianzhen': {'level': 5, 'at': []}, 'che._.0415': {'level': 5, 'at': []}, 'lu.981105': {'level': 5, 'at': []}, 'czh._10': {'level': 5, 'at': []}, '_cty.__.0210': {'level': 5, 'at': []}, 'tammy._.1218': {'level': 5, 'at': []}, 'qiaoshi._.1222': {'level': 5, 'at': []}}
    people = {'elsie__12__': {'level': 0, 'at': ['jx06_t'], 'url': 'https://www.instagram.com/elsie__12__/?next=%2F'}, 'jx06_t': {'level': 1, 'at': ['elsie__12__', 'lsie__12__在追蹤'], 'url': 'https://www.instagram.com/jx06_t/?next=%2F'}}
    people = {'yuann0722': {'level': 0, 'at': ['rii.1oo', 'nuo971225', 'lsie__12__在追蹤'], 'url': 'https://www.instagram.com/yuann0722/'}, 'rii.1oo': {'level': 1, 'at': ['yuann0722', '1'], 'url': 'https://www.instagram.com/rii.1oo/'}, 'nuo971225': {'level': 1, 'at': ['uo971225', 'iyruins', 'yuann0722', 'i_am_ann123', '97.12.02ww', 'gl.link/nuo971225'], 'url': 'https://www.instagram.com/nuo971225/'}, 'iyruins': {'level': 2, 'at': ['yruins', 'hesiiiimi'], 'url': 'https://www.instagram.com/iyruins/'}, 'i_am_ann123': {'level': 2, 'at': ['nuo971225', 'cuteicebaby2020', 'nn._.731', 'paulweng_.09'], 'url': 'https://www.instagram.com/i_am_ann123/'}, '97.12.02ww': {'level': 2, 'at': ['7.12.02ww', 'nuo971225', 'gl.link/97.12.02ww1'], 'url': 'https://www.instagram.com/97.12.02ww/'}, 'cuteicebaby2020': {'level': 3, 'at': ['kiko990825', 'lin._.980115', 'i_am_ann123'], 'url': 'https://www.instagram.com/cuteicebaby2020/'}, 'nn._.731': {'level': 3, 'at': ['n._.731', 'i_am_ann123', 'citra._.08', 'paulweng_.09', 'nxy_.0925'], 'url': 'https://www.instagram.com/nn._.731/'}, 'paulweng_.09': {'level': 3, 'at': [], 'url': 'https://www.instagram.com/paulweng_.09/'}, 'hesiiiimi': {'level': 3, 'at': ['esiiiimi', 'iyruins'], 'url': 'https://www.instagram.com/hesiiiimi/'}, 'citra._.08': {'level': 4, 'at': ['xy__0823', 'gl.link/citra._.08'], 'url': 'https://www.instagram.com/citra._.08/'}, 'nxy_.0925': {'level': 4, 'at': ['xy_.0925', '08', '新北', '非單', 'anninmirudayo', 'hoshi._.970217', 'nn._.731', 'tangyuxuan201', '9czxin._', 'di._.308', 'gl.link/nxy_.0925'], 'url': 'https://www.instagram.com/nxy_.0925/'}, 'kiko990825': {'level': 4, 'at': ['cuteicebaby2020', 'kiko._.aurora'], 'url': 'https://www.instagram.com/kiko990825/'}, 'lin._.980115': {'level': 4, 'at': ['xinn._.14', 'ling._.980522', 'yun.love.justin', 'cuteicebaby2020', 'li._.jiexin'], 'url': 'https://www.instagram.com/lin._.980115/'}, 'anninmirudayo': {'level': 5, 'at': ['nninmirudayo', 'ww.youtube.com/c/AnninMiruChannel'], 'url': 'https://www.instagram.com/anninmirudayo/'}, 'hoshi._.970217': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/hoshi._.970217/'}, 'tangyuxuan201': {'level': 5, 'at': ['angyuxuan201', 'nicolecuic', 'janic_e0522', 'cy__.29', 'emo._.2735', 'mr.__.0522', 'nxy_.0925', 'lmx._.210', 'huangbrotherss'], 'url': 'https://www.instagram.com/tangyuxuan201/'}, '9czxin._': {'level': 5, 'at': ['czxin._', 'bibi_1223_', 'nxy_.0925', 'yuu._.pq', 'jing._.822_'], 'url': 'https://www.instagram.com/9czxin._/'}, 'di._.308': {'level': 5, 'at': ['0123_.xin', 'nxy_.0925', 'luo.__15', 'zuiyyy_21'], 'url': 'https://www.instagram.com/di._.308/'}, 'xy__0823': {'level': 5, 'at': ['y__0823', 'chia_yun24', 'citra._.08', 'millie.sun26', '_823yee', 'gl.link/xyee2'], 'url': 'https://www.instagram.com/xy__0823/'}, 'xinn._.14': {'level': 5, 'at': ['ccccc__.13', 'lin._.980115', 'chian_.ning', 'nina.liu__'], 'url': 'https://www.instagram.com/xinn._.14/'}, 'ling._.980522': {'level': 5, 'at': ['ing._.980522', 'yu_hsin204', 'an._.1023', 'lin._.980115', 'huayu_0608'], 'url': 'https://www.instagram.com/ling._.980522/'}, 'yun.love.justin': {'level': 5, 'at': [], 'url': 'https://www.instagram.com/yun.love.justin/'}, 'li._.jiexin': {'level': 5, 'at': ['l.jun_217', 'w.y.c0227_', 'yxc.c_xc', 'hsin_______970913', 'lin._.980115', 'linpeiyi79', 'lin._.chiying', 'pinky._.0526', 'ellonym.me/li._.jiexin'], 'url': 'https://www.instagram.com/li._.jiexin/'}, 'kiko._.aurora': {'level': 5, 'at': ['kiko990825'], 'url': 'https://www.instagram.com/kiko._.aurora/'}, '0123_.xin': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/0123_.xin/'}, 'luo.__15': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/luo.__15/'}, 'zuiyyy_21': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/zuiyyy_21/'}, 'bibi_1223_': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/bibi_1223_/'}, 'yuu._.pq': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/yuu._.pq/'}, 'jing._.822_': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/jing._.822_/'}, 'nicolecuic': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/nicolecuic/'}, 'janic_e0522': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/janic_e0522/'}, 'cy__.29': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/cy__.29/'}, 'emo._.2735': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/emo._.2735/'}, 'mr.__.0522': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/mr.__.0522/'}, 'lmx._.210': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/lmx._.210/'}, 'huangbrotherss': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/huangbrotherss/'}, 'chia_yun24': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/chia_yun24/'}, 'millie.sun26': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/millie.sun26/'}, '_823yee': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/_823yee/'}, 'ccccc__.13': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/ccccc__.13/'}, 'chian_.ning': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/chian_.ning/'}, 'nina.liu__': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/nina.liu__/'}, 'yu_hsin204': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/yu_hsin204/'}, 'an._.1023': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/an._.1023/'}, 'huayu_0608': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/huayu_0608/'}, 'l.jun_217': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/l.jun_217/'}, 'w.y.c0227_': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/w.y.c0227_/'}, 'yxc.c_xc': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/yxc.c_xc/'}, 'hsin_______970913': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/hsin_______970913/'}, 'linpeiyi79': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/linpeiyi79/'}, 'lin._.chiying': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/lin._.chiying/'}, 'pinky._.0526': {'level': 6, 'at': [], 'url': 'https://www.instagram.com/pinky._.0526/'}}
    # people = {'shawn_.00': {'level': 0, 'at': ['h__h0813', 'yuan_moche'], 'url': 'https://www.instagram.com/shawn_.00/'}, 'h__h0813': {'level': 1, 'at': ['lzh__215', 'lun_court', 'yuan_moche', 'shawn_.00'], 'url': 'https://www.instagram.com/h__h0813/'}, 'yuan_moche': {'level': 1, 'at': ['h__h0813', 'lzh__215', 'lun_court', '0124_wow'], 'url': 'https://www.instagram.com/yuan_moche/'}, 'lzh__215': {'level': 2, 'at': [], 'url': 'https://www.instagram.com/lzh__215/'}, 'lun_court': {'level': 2, 'at': [], 'url': 'https://www.instagram.com/lun_court/'}, '0124_wow': {'level': 2, 'at': [], 'url': 'https://www.instagram.com/0124_wow/'}}
    graph = PeopleGraph(people)
    graph.show_graph("Sample",None)

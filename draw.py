import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
import datetime
import os
class PeopleGraph:
    def __init__(self, people):
        self.people = people
        self.G = nx.DiGraph()
        self.SIZE = len(self.people) // 3.5 if len(self.people) // 3.5> 10 else 10
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
        for key, value in self.TempPeople.items():
            self.people[key]["state"] = {}

        for key, value in self.TempPeople.items():
            self.G.add_node(key)
            self.people[key]["color"] = self.generate_hex_color((len(value["at"]) + 1) * random.randint(37, 53))
            self.people[key]["size"] = (5 - value["level"]) * 600 + 500
    
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
                    self.people[aAt]["color"] = "#FF3F00"
                    self.people[aAt]["state"] = {}
                    self.people[aAt]["at"] = []
                    continue

                if key in self.people[aAt]["at"]:
                    self.people[key]["state"][aAt] = '<|-|>'
                    self.people[aAt]["state"][key] = "<|-|>"
        pos = nx.spring_layout(self.G)
        
        for node in self.G.nodes:
            nx.draw_networkx_nodes(self.G, pos, nodelist=[node], node_color=self.people[node]["color"], node_size=self.people[node]["size"])
        
        for edge in self.G.edges:
            source_node, target_node = edge
            x1, y1 = pos[source_node]
            x2, y2 = pos[target_node]
            dx = x2 - x1
            dy = y2 - y1
            t2 = 100000
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
        
        if filename == "":
            filename = "people_graph"

        filename = f"output/{filename}_{Getdatetime()}.png"
        plt.savefig(filename, format="png",dpi=100)

        current_directory = os.getcwd()
        local_file_path = 'file://' + os.path.join(current_directory, filename)
        self.driver.execute_script("window.open('" + local_file_path + "', '_blank');")

        # plt.show()


def Getdatetime():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%y%m%d_%H_%M")
    return formatted_datetime
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
    graph = PeopleGraph(people)
    graph.show_graph("Sample")

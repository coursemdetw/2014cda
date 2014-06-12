
import cherrypy

import os
import sys

# 確定程式檔案所在目錄, 在 Windows 有最後的反斜線
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
# 將所在目錄設為系統搜尋目錄
sys.path.append(_curdir)

# 這是 Gear 設計類別的定義
'''
# 在 application 中導入子模組
import programs.cdag30.gear as cdag30_gear
# 加入 cdag30 模組下的 gear.py 且以子模組 gear 對應其 MAIN() 類別
root.cdag30.gear= cdag30_gear.MAIN()

# 完成設定後, 可以利用
/cdag30/gear
# 呼叫 gear.py 中 MAIN 類別的 index 方法, 執行正齒輪齒面寬設計運算

lewis.db 中有兩個資料表, steel 與 lewis

 CREATE TABLE steel ( 
    serialno      INTEGER,
    unsno         TEXT,
    aisino        TEXT,
    treatment     TEXT,
    yield_str     INTEGER,
    tensile_str   INTEGER,
    stretch_ratio INTEGER,
    sectional_shr INTEGER,
    brinell       INTEGER 
);

CREATE TABLE lewis ( 
    serialno INTEGER PRIMARY KEY
                     NOT NULL,
    gearno   INTEGER,
    type1    NUMERIC,
    type4    NUMERIC,
    type3    NUMERIC,
    type2    NUMERIC 
);
'''
# 這個程式要計算正齒輪的齒面寬, 資料庫連結希望使用 pybean 與 SQLite
# 導入 pybean 模組與所要使用的 Store 及 SQLiteWriter 方法
from pybean import Store, SQLiteWriter
import math

class MAIN(object):
    @cherrypy.expose
    def interpolation(self, small_gear_no=18, gear_type=1):
        SQLite連結 = Store(SQLiteWriter(_curdir+"/lewis.db", frozen=True))
        # 使用內插法求值
        # 找出比目標齒數大的其中的最小的,就是最鄰近的大值
        lewis_factor = SQLite連結.find_one("lewis","gearno > ?",[small_gear_no])
        if(gear_type == 1):
            larger_formfactor = lewis_factor.type1
        elif(gear_type == 2):
            larger_formfactor = lewis_factor.type2
        elif(gear_type == 3):
            larger_formfactor = lewis_factor.type3
        else:
            larger_formfactor = lewis_factor.type4
        larger_toothnumber = lewis_factor.gearno
     
        # 找出比目標齒數小的其中的最大的,就是最鄰近的小值
        lewis_factor = SQLite連結.find_one("lewis","gearno < ? order by gearno DESC",[small_gear_no])
        if(gear_type == 1):
            smaller_formfactor = lewis_factor.type1
        elif(gear_type == 2):
            smaller_formfactor = lewis_factor.type2
        elif(gear_type == 3):
            smaller_formfactor = lewis_factor.type3
        else:
            smaller_formfactor = lewis_factor.type4
        smaller_toothnumber = lewis_factor.gearno
        calculated_factor = larger_formfactor + (small_gear_no - larger_toothnumber) * (larger_formfactor - smaller_formfactor) / (larger_toothnumber - smaller_toothnumber)
        # 只傳回小數點後五位數
        return str(round(calculated_factor, 5))

    # 改寫為齒面寬的設計函式
    @cherrypy.expose
    def gear_width(self, horsepower=100, rpm=1000, ratio=4, toothtype=1, safetyfactor=2, material_serialno=1, npinion=18):
        SQLite連結 = Store(SQLiteWriter(_curdir+"/lewis.db", frozen=True))
        outstring = ""
        # 根據所選用的齒形決定壓力角
        if(toothtype == 1 or toothtype == 2):
            壓力角 = 20
        else:
            壓力角 = 25
     
        # 根據壓力角決定最小齒數
        if(壓力角== 20):
            最小齒數 = 18
        else:
            最小齒數 = 12
     
        # 直接設最小齒數
        if int(npinion) <= 最小齒數:
            npinion = 最小齒數
        # 大於400的齒數則視為齒條(Rack)
        if int(npinion) >= 400:
            npinion = 400
     
        # 根據所選用的材料查詢強度值
        # 由 material之序號查 steel 表以得材料之降伏強度S單位為 kpsi 因此查得的值要成乘上1000
        # 利用 Store  建立資料庫檔案對應物件, 並且設定 frozen=True 表示不要開放動態資料表的建立
        #SQLite連結 = Store(SQLiteWriter("lewis.db", frozen=True))
        # 指定 steel 資料表
        steel = SQLite連結.new("steel")
        # 資料查詢
        #material = SQLite連結.find_one("steel","unsno=? and treatment=?",[unsno, treatment])
        material = SQLite連結.find_one("steel","serialno=?",[material_serialno])
        # 列出 steel 資料表中的資料筆數
        #print(SQLite連結.count("steel"))
        #print (material.yield_str)
        strengthstress = material.yield_str*1000
        # 由小齒輪的齒數與齒形類別,查詢lewis form factor
        # 先查驗是否有直接對應值
        on_table = SQLite連結.count("lewis","gearno=?",[npinion])
        if on_table == 1:
            # 直接進入設計運算
            #print("直接運算")
            #print(on_table)
            lewis_factor = SQLite連結.find_one("lewis","gearno=?",[npinion])
            #print(lewis_factor.type1)
            # 根據齒形查出 formfactor 值
            if(toothtype == 1):
                formfactor = lewis_factor.type1
            elif(toothtype == 2):
                formfactor = lewis_factor.type2
            elif(toothtype == 3):
                formfactor = lewis_factor.type3
            else:
                formfactor = lewis_factor.type4
        else:
            # 沒有直接對應值, 必須進行查表內插運算後, 再執行設計運算
            #print("必須內插")
            #print(interpolation(npinion, gear_type))
            formfactor = self.interpolation(npinion, toothtype)
     
        # 開始進行設計運算
     
        ngear = int(npinion) * int(ratio)
     
        # 重要的最佳化設計---儘量用整數的diametralpitch
        # 先嘗試用整數算若 diametralpitch 找到100 仍無所獲則改用 0.25 作為增量再不行則宣告 fail
        counter = 0
        i = 0.1
        facewidth = 0
        circularpitch = 0
        while (facewidth <= 3 * circularpitch or facewidth >= 5 * circularpitch):
            diametralpitch = i
            #circularpitch = 3.14159/diametralpitch
            circularpitch = math.pi/diametralpitch
            pitchdiameter = int(npinion)/diametralpitch
            #pitchlinevelocity = 3.14159*pitchdiameter*rpm/12
            pitchlinevelocity = math.pi*pitchdiameter * float(rpm)/12
            transmittedload = 33000*float(horsepower)/pitchlinevelocity
            velocityfactor = 1200/(1200 + pitchlinevelocity)
            # formfactor is Lewis form factor
            # formfactor need to get from table 13-3 and determined ty teeth number and type of tooth
            # formfactor = 0.293
            # 90 is the value get from table corresponding to material type
            facewidth = transmittedload*diametralpitch*float(safetyfactor)/velocityfactor/formfactor/strengthstress
            if(counter>5000):
                outstring += "超過5000次的設計運算,仍無法找到答案!<br />"
                outstring += "可能所選用的傳遞功率過大,或無足夠強度的材料可以使用!<br />"
                # 離開while迴圈
                break
            i += 0.1
            counter += 1
        facewidth = round(facewidth, 4)
        if(counter<5000):
            outstring = "進行"+str(counter)+"次重複運算後,得到合用的facewidth值為:"+str(facewidth)
        return outstring

    # 各組利用 index 引導隨後的程式執行
    @cherrypy.expose
    def index(self, *args, **kwargs):
        # 進行資料庫檔案連結,  並且取出所有資料
        try:
            # 利用 Store  建立資料庫檔案對應物件, 並且設定 frozen=True 表示不要開放動態資料表的建立
            # 因為程式以 application 所在目錄執行, 因此利用相對目錄連結 lewis.db 資料庫檔案
            SQLite連結 = Store(SQLiteWriter(_curdir+"/lewis.db", frozen=True))
            #material = SQLite連結.find_one("steel","serialno = ?",[序號])
            # str(SQLite連結.count("steel")) 將傳回 70, 表示資料庫中有 70 筆資料
            material = SQLite連結.find("steel")
            # 所傳回的 material 為 iterator
            '''
            outstring = ""
            for material_item in material:
                outstring += str(material_item.serialno) + ":" + material_item.unsno + "_" + material_item.treatment + "<br />"
            return outstring
            '''
        except:
            return "抱歉! 資料庫無法連線<br />"

        outstring = '''
<form id=entry method=post action="gear_width">
請填妥下列參數，以完成適當的齒尺寸大小設計。<br />
馬達馬力:<input type=text name=horsepower id=horsepower value=100 size=10>horse power<br />
馬達轉速:<input type=text name=rpm id=rpm value=1120 size=10>rpm<br />
齒輪減速比: <input type=text name=ratio id=ratio value=4 size=10><br />
齒形:<select name=toothtype id=toothtype>
<option value=type1>壓力角20度,a=0.8,b=1.0
<option value=type2>壓力角20度,a=1.0,b=1.25
<option value=type3>壓力角25度,a=1.0,b=1.25
<option value=type4>壓力角25度,a=1.0,b=1.35
</select><br />
安全係數:<input type=text name=safetyfactor id=safetyfactor value=3 size=10><br />
齒輪材質:<select name=material_serialno id=material_serialno>
'''
        for material_item in material:
            outstring += "<option value=" + str(material_item.serialno) + ">UNS - " + \
                material_item.unsno + " - " + material_item.treatment
        outstring += "</select><br />"
        
        outstring += "小齒輪齒數:<input type=text name=npinion id=npinion value=18 size=10><br />"
        outstring += "<input type=submit id=submit value=進行運算>"
        outstring += "</form>"
    
        return outstring

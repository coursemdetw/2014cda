import cherrypy
 
# 這是 MAN 類別的定義
'''
# 在 application 中導入子模組
import programs.cdag10.remsub6 as cdag10_remsub6
# 加入 cdag10 模組下的 remsub6.py 且以子模組 remsub6 對應其 remsub6() 類別
root.cdag10.remsub6 = cdag10_remsub6.remsub6()
 
# 完成設定後, 可以利用
/cdag10/remsub6/assembly
# 呼叫 man.py 中 MAN 類別的 assembly 方法
'''
class remsub6(object):
    # 各組利用 index 引導隨後的程式執行
    @cherrypy.expose
    def index(self, *args, **kwargs):
        outstring = '''
這是 2014CDA 協同專案下的 cdag10 模組下的 MAN 類別.<br /><br />
<!-- 這裡採用相對連結, 而非網址的絕對連結 (這一段為 html 註解) -->
<a href="assembly">執行  MAN 類別中的 assembly 方法</a><br /><br />
請確定下列零件於 V:/home/lego/man 目錄中, 且開啟空白 Creo 組立檔案.<br />
<a href="/static/lego_man.7z">lego_man.7z</a>(滑鼠右鍵存成 .7z 檔案)<br />
'''
        return outstring
 
    @cherrypy.expose
    def assembly(self, *args, **kwargs):
        outstring =         '''
        <!DOCTYPE html> 
        <html>
        <head>
        <meta http-equiv="content-type" content="text/html;charset=utf-8">
        <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
        </head>
        <body>
        </script><script language="JavaScript">
/*設計一個零件組立函示
get 組立
get part
抓取約束元素 in part and asm
選擇約束型式
應用在 part 上
*/
/*
軸面接
axis_plane_assembly(session, assembly, transf, featID, constrain_way, part2, axis1, plane1, axis2, plane2)
====================
assembly 組立檔案
transf 座標矩陣
feadID 要組裝的父
part2 要組裝的子
 
constrain_way 參數
1 對齊 對齊
2 對齊 貼合
else 按照 1
 
plane1~plane2 要組裝的父 參考面
plane3~plane4 要組裝的子 參考面
*/
function axis_plane_assembly(file_location, session, assembly, transf, featID, constrain_way, axis1, plane1, axis2, plane2) {
    //設定part2 路徑
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName(file_location);
    //嘗試從 session 中取得 part2
    var componentModel = session.GetModelFromDescr(descr);
    //取得失敗 status null
    if (componentModel == null) {
        document.write("在session 取得不到零件" + file_location);
        //從路逕取得 part2
        componentModel = session.RetrieveModel(descr);
        //仍然取得失敗 表示無此零件
        if (componentModel == null) {
            // 此發錯誤
            throw new Error(0, "Current componentModel is not loaded.");
        }
    }
    //假如 part2 有取得到
    if (componentModel != void null) {
        //將part2 放入 組立檔案, part2 在組立檔案裡面為 組立 component
        var asmcomp = assembly.AssembleComponent(componentModel, transf);
    }
 
    //組立父 featID list 形態, 為整數型態 list
    var ids = pfcCreate("intseq");
    //當有提供 要組裝的父
    if (featID != -1) {
        //將要組裝的父 加入 list
        ids.Append(featID);
        //取得組裝路徑
        //建立路徑變數，CreateComponentPath:回傳組件的路徑物件，把組立模型和的ID路徑給所需的組件。
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        var subassembly = subPath.Leaf;
    } else {
        // 假如沒有提供 要組裝的父
        // asm 基本 就當作父零件
        var subassembly = assembly;
        //取得組裝路徑
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    }
 
    //父參考 element
    var asmDatums = new Array(axis1, plane1);
    //子參考 element
    var compDatums = new Array(axis2, plane2);
 
    //約數型態
    if (constrain_way == 1) {
        var relation = new Array(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
    } else if (constrain_way == 2) {
        var relation = new Array(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
    } else {
        var relation = new Array(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
 
    }
 
    //選擇元素 形態 (ITEM_AXIS) 軸 (ITEM_SURFACE) 面
    var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
    //約束 list 等下要應用於 子
    var constrs = pfcCreate("pfcComponentConstraints");
 
    for (var i = 0; i < 2; i++) {
        //選擇 父元素
        var asmItem = subassembly.GetItemByName(relationItem[i], asmDatums[i]);
        if (asmItem == void null) {
            interactFlag = true;
            continue;
        }
        //選擇 子元素
        var compItem = componentModel.GetItemByName(relationItem[i], compDatums[i]);
        if (compItem == void null) {
            interactFlag = true;
            continue;
        }
 
        //採用互動式設定相關的變數
        var MpfcSelect = pfcCreate("MpfcSelect");
        //互動式設定 選擇元素 父
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        //互動式設定 選擇元素 子
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        //選擇約束形態
        var constr = pfcCreate("pfcComponentConstraint").Create(relation[i]);
        //約束選擇 剛剛得父元素
        constr.AssemblyReference = asmSel;
        //約束選擇 剛剛得子元素
        constr.ComponentReference = compSel;
        //設定約束屬性
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create(true, false);
        //加入此約束 至 約束 list
        constrs.Append(constr);
    }
    //約束 list應用至 子
    asmcomp.SetConstraints(constrs, void null);
    //回傳 component id
    return asmcomp.Id;
}
// 以上為 axis_plane_assembly() 函式
/*
三面接
three_plane_assembly(session, assembly, transf, featID, constrain_way, part2, plane1, plane2, plane3, plane4, plane5, plane6)
=====================
assembly 組立檔案
transf 座標矩陣
feadID 要組裝的父
part2 要組裝的子
 
constrain_way 參數
1 對齊
2 貼合
else 按照 1
 
plane1~plane3 要組裝的父 參考面
plane4~plane6 要組裝的子 參考面
*/
function three_plane_assembly(file_location, session, assembly, transf, featID, constrain_way, plane1, plane2, plane3, plane4, plane5, plane6) {
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName(file_location);
    var componentModel = session.GetModelFromDescr(descr);
    if (componentModel == null) {
        document.write("在session 取得不到零件" + file_location);
        componentModel = session.RetrieveModel(descr);
        if (componentModel == null) {
            throw new Error(0, "Current componentModel is not loaded.");
        }
    }
    if (componentModel != void null) {
        var asmcomp = assembly.AssembleComponent(componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    //假如  asm 有零件時候
    if (featID != -1) {
 
        ids.Append(featID);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        var subassembly = subPath.Leaf;
    }
    // 假如是第一個零件 asm 就當作父零件
    else {
        var subassembly = assembly;
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    }
 
 
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++) {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
 
        if (asmItem == void null) {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null) {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        if (constrain_way == 1) {
            var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
        } else if (constrain_way == 2) {
            var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
        } else {
            var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
        }
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create(false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    return asmcomp.Id;
}
// 以上為 three_plane_assembly() 函式
 
 
//1軸2面
function one_axis_two_plane_assembly(file_location, session, assembly, transf, featID, constrain_way, axis1, plane1_1, plane1_2, axis2, plane2_1, plane2_2) {
    //設定part2 路徑
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName(file_location);
    //嘗試從 session 中取得 part2
    var componentModel = session.GetModelFromDescr(descr);
    //取得失敗 status null
    if (componentModel == null) {
        document.write("在session 取得不到零件" + file_location);
        //從路逕取得 part2
        componentModel = session.RetrieveModel(descr);
        //仍然取得失敗 表示無此零件
        if (componentModel == null) {
            // 此發錯誤
            throw new Error(0, "Current componentModel is not loaded.");
        }
    }
    //假如 part2 有取得到
    if (componentModel != void null) {
        //將part2 放入 組立檔案, part2 在組立檔案裡面為 組立 component
        var asmcomp = assembly.AssembleComponent(componentModel, transf);
    }
 
    //組立父 featID list 形態, 為整數型態 list
    var ids = pfcCreate("intseq");
    //當有提供 要組裝的父
    if (featID != -1) {
        //將要組裝的父 加入 list
        ids.Append(featID);
        //取得組裝路徑
        //建立路徑變數，CreateComponentPath:回傳組件的路徑物件，把組立模型和的ID路徑給所需的組件。
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        var subassembly = subPath.Leaf;
    } else {
        // 假如沒有提供 要組裝的父
        // asm 基本 就當作父零件
        var subassembly = assembly;
        //取得組裝路徑
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    }
 
    //父參考 element
    var asmDatums = new Array(axis1, plane1_1, plane1_2);
    //子參考 element
    var compDatums = new Array(axis2, plane2_1, plane2_2);
 
    //約數型態
    var ConstraintType = pfcCreate("pfcComponentConstraintType");
    if (constrain_way == 1) {
        var relation = new Array(ConstraintType.ASM_CONSTRAINT_ALIGN, ConstraintType.ASM_CONSTRAINT_MATE, ConstraintType.ASM_CONSTRAINT_AUTO);
    } else if (constrain_way == 2) {
        var relation = new Array(ConstraintType.ASM_CONSTRAINT_ALIGN, ConstraintType.ASM_CONSTRAINT_ALIGN, ConstraintType.ASM_CONSTRAINT_MATE);
    } else if (constrain_way == 3) {
        var relation = new Array(ConstraintType.ASM_CONSTRAINT_ALIGN, ConstraintType.ASM_CONSTRAINT_MATE, ConstraintType.ASM_CONSTRAINT_MATE);
    } else {
        var relation = new Array(ConstraintType.ASM_CONSTRAINT_ALIGN, ConstraintType.ASM_CONSTRAINT_ALIGN, ConstraintType.ASM_CONSTRAINT_ALIGN);
 
    }
 
    //選擇元素 形態 (ITEM_AXIS) 軸 (ITEM_SURFACE) 面
    var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE, pfcCreate("pfcModelItemType").ITEM_SURFACE);
    //約束 list 等下要應用於 子
    var constrs = pfcCreate("pfcComponentConstraints");
 
    for (var i = 0; i < 3; i++) {
        //選擇 父元素
        var asmItem = subassembly.GetItemByName(relationItem[i], asmDatums[i]);
        if (asmItem == void null) {
            interactFlag = true;
            continue;
        }
        //選擇 子元素
        var compItem = componentModel.GetItemByName(relationItem[i], compDatums[i]);
        if (compItem == void null) {
            interactFlag = true;
            continue;
        }
 
        //採用互動式設定相關的變數
        var MpfcSelect = pfcCreate("MpfcSelect");
        //互動式設定 選擇元素 父
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        //互動式設定 選擇元素 子
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        //選擇約束形態
        var constr = pfcCreate("pfcComponentConstraint").Create(relation[i]);
        //約束選擇 剛剛得父元素
        constr.AssemblyReference = asmSel;
        //約束選擇 剛剛得子元素
        constr.ComponentReference = compSel;
        //設定約束屬性
        //constr.Attributes = pfcCreate("pfcConstraintAttributes").Create(true, false);
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create(true, false);
        //加入此約束 至 約束 list
        constrs.Append(constr);
    }
    //約束 list應用至 子
    asmcomp.SetConstraints(constrs, void null);
    //回傳 component id
    return asmcomp.Id;
}
 
 
//
// 假如 Creo 所在的操作系統不是 Windows 環境
if (!pfcIsWindows()) {
    // 則啟動對應的 UniversalXPConnect 執行權限 (等同 Windows 下的 ActiveX)
    netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
}
// pfcGetProESession() 是位於 pfcUtils.js 中的函式, 確定此 JavaScript 是在嵌入式瀏覽器中執行
var session = pfcGetProESession();
// 設定 config option, 不要使用元件組立流程中內建的假設約束條件
session.SetConfigOption("comp_placement_assumptions", "no");
// 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate() 建立
var identityMatrix = pfcCreate("pfcMatrix3D");
// 建立 identity 位置矩陣
for (var x = 0; x < 4; x++) {
    for (var y = 0; y < 4; y++) {
        if (x == y) {
            identityMatrix.Set(x, y, 1.0);
        } else {
            identityMatrix.Set(x, y, 0.0);
        }
    }
}
// 利用 identityMatrix 建立 transf 座標轉換矩陣
var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
// 取得目前的工作目錄
var currentDir = session.getCurrentDirectory();
// 以目前已開檔的空白組立檔案, 作為 model
var model = session.CurrentModel;
// 查驗有無 model, 或 model 類別是否為組立件, 若不符合條件則丟出錯誤訊息
if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
    throw new Error(0, "Current model is not an assembly.");
// 將此模型設為組立物件
var assembly = model;
 
/*
three_plane_assembly(session, assembly, transf, featID, constrain_way, part2, plane1, plane2, plane3, plane4, plane5, plane6)
=====================
assembly 組立檔案
transf 座標矩陣
feadID 要組裝的父
part2 要組裝的子
 
constrain_way 參數
1 對齊
2 貼合
else 按照 1
 
plane1~plane3 要組裝的父 參考面
plane4~plane6 要組裝的子 參考面
 
axis_plane_assembly(session, assembly, transf, featID, constrain_way, part2, axis1, plane1, axis2, plane2)
====================
assembly 組立檔案
transf 座標矩陣
feadID 要組裝的父
part2 要組裝的子
 
constrain_way 參數
1 對齊 對齊
2 對齊 貼合
else 按照 1
 
plane1~plane2 要組裝的父 參考面
plane3~plane4 要組裝的子 參考面
*/
 
var work_directory = "V:/home/lego/";

alert("test");
//function three_plane_assembly(file_location, session, assembly, transf, featID, constrain_way, plane1, plane2, plane3, plane4, plane5, plane6) {
var body_id = three_plane_assembly(work_directory + 'beam_angle.prt', session, assembly, transf, -1, 1, "ASM_FRONT", "ASM_TOP", "ASM_RIGHT", "FRONT", "TOP", "RIGHT");
//function one_axis_two_plane_assembly(file_location, session, assembly, transf, featID, constrain_way, axis1, plane1_1, plane1_2, axis2, plane2_1, plane2_2)
var alex_10 = one_axis_two_plane_assembly(work_directory + 'axle_10.prt', session, assembly, transf, body_id, 1, "A_25", "FRONT", "TOP", "A_1", "FRONT", "TOP");
 
var alex_5 = one_axis_two_plane_assembly(work_directory + 'axle_5.prt', session, assembly, transf, body_id, 1, "A_26", "DTM2", "TOP", "A_1", "RIGHT", "TOP");

/* 
var crossblock_2_left = one_axis_two_plane_assembly(work_directory + 'crossblock_2.prt', session, assembly, transf, body_id, 1, "A_25", "DTM3","FRONT",  "A_16", "DTM4", "DTM1");
 
var crossblock_2_right = one_axis_two_plane_assembly(work_directory + 'crossblock_2.prt', session, assembly, transf, body_id, 1, "A_25", "DTM1","FRONT",  "A_16", "DTM5", "DTM1");
 
var crossblock_2_left_front = one_axis_two_plane_assembly(work_directory + 'crossblock_2.prt', session, assembly, transf, body_id, 2, "A_26", "DTM4", "DTM1",  "A_16", "DTM1", "DTM4");
 
var crossblock_2_right_front = one_axis_two_plane_assembly(work_directory + 'crossblock_2.prt', session, assembly, transf, body_id, 2, "A_26", "DTM4", "DTM3",  "A_16", "DTM1", "DTM5");
 
var crossblock_2_left_2 = one_axis_two_plane_assembly(work_directory + 'crossblock_2.prt', session, assembly, transf, crossblock_2_left, 2, "A_16", "DTM2", "DTM5",  "A_16", "DTM1", "DTM4");
 
var crossblock_2_right_2 = one_axis_two_plane_assembly(work_directory + 'crossblock_2.prt', session, assembly, transf, crossblock_2_right, 2, "A_16", "DTM2", "DTM4",  "A_16", "DTM1", "DTM5");
 
var conn_3_left = axis_plane_assembly(work_directory + 'conn_3.prt', session, assembly, transf, crossblock_2_left, 1, "A_17", "DTM10", "A_20", "DTM1");
 
var conn_3_left = axis_plane_assembly(work_directory + 'conn_3.prt', session, assembly, transf, crossblock_2_right, 1, "A_17", "DTM10", "A_20", "DTM1");
 
var beam_3 = one_axis_two_plane_assembly(work_directory + 'beam_3.prt', session, assembly, transf, crossblock_2_right, 3,
    "A_17", "DTM7","FRONT",  "A_37", "BOTTOM", "RIGHT");
 */
assembly.Regenerate (void null);
session.GetModelWindow (assembly).Repaint();
</script>
</body>
</html>
'''
        return outstring
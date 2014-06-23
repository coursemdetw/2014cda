import cherrypy
 
# 這是 MAN 類別的定義
'''
# 在 application 中導入子模組
import programs.cdag30.man as cdag30_man
# 加入 cdag30 模組下的 man.py 且以子模組 man 對應其 MAN() 類別
root.cdag30.man = cdag30_man.MAN()
 
# 完成設定後, 可以利用
/cdag30/man/assembly
# 呼叫 man.py 中 MAN 類別的 assembly 方法
'''
class phone(object):
    # 各組利用 index 引導隨後的程式執行
    @cherrypy.expose
    def index(self, *args, **kwargs):
        outstring = '''
這是 2014CDA 協同專案下的 cdag4 模組下的 phone 類別.<br /><br />
<!-- 這裡採用相對連結, 而非網址的絕對連結 (這一段為 html 註解) -->
<a href="assembly">執行  phone 類別中的 assembly 方法</a><br /><br />
請確定下列零件於 V:/home/phone/ 目錄中, <br />
<a href="/static/phone.7z">phone.7z</a>(滑鼠右鍵存成 .7z 檔案)<br />
'''
        return outstring
 
    @cherrypy.expose
    def assembly(self, *args, **kwargs):
        outstring =          '''                <html>                <head>
                <meta http-equiv="content-type" content="text/html;charset=utf-8">
                <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
                </head>
                <body>
                </script><script language="JavaScript">
        //選擇型態 dictionary
        pfcModelItemType = pfcCreate("pfcModelItemType");
        relation_map = {
            "axis": pfcModelItemType.ITEM_AXIS, //Datum point
            "point": pfcModelItemType.ITEM_POINT, //Datum axis
            "datum": pfcModelItemType.ITEM_SURFACE, //Datum plane
            "csys": pfcModelItemType.ITEM_COORD_SYS, //Coordinate system datum
            "feature": pfcModelItemType.ITEM_FEATURE, //Feature
            "edge": pfcModelItemType.ITEM_EDGE, //Edge (solid or datum surface)
            "sldege": pfcModelItemType.ITEM_EDGE, //Edge (solid only)
            "qltedge": pfcModelItemType.ITEM_EDGE, //Edge (datum surface only)
            "curve": pfcModelItemType.ITEM_CURVE, //Datum curve
            "comp_crv": pfcModelItemType.ITEM_CURVE, //Composite curve
            "surface": pfcModelItemType.ITEM_SURFACE, //Surface (solid or quilt)
            "sldface": pfcModelItemType.ITEM_SURFACE, //Surface (solid)
            "qltface": pfcModelItemType.ITEM_SURFACE, //Surface (datum surface)
            "dtmqlt": pfcModelItemType.ITEM_QUILT, //Quilt
            "dimension": pfcModelItemType.ITEM_DIMENSION, //Dimension
            "ref_dim": pfcModelItemType.ITEM_REF_DIMENSION, //Reference dimension
            "ipar": pfcModelItemType.ITEM_DIMENSION, //Integer parameter
            "membfeat": pfcModelItemType.ITEM_FEATURE, //Component or feature
            "dtl_symbol": pfcModelItemType.ITEM_DTL_SYM_INSTANCE, //Detail symbol
            "any_note": pfcModelItemType.ITEM_NOTE, //Note
            "draft_ent": pfcModelItemType.ITEM_DTL_ENTITY, //Draft entity
            "dwg_table": pfcModelItemType.ITEM_TABLE, //Table
            "table_cell": pfcModelItemType.ITEM_TABLE //Table cell
        };
         
        //約束型態 dictionary
        ComponentConstraintType = pfcCreate("pfcComponentConstraintType");
        constrian_map = {
            "mate": ComponentConstraintType.ASM_CONSTRAINT_MATE,
            //Use this option to make two surfaces touch one another,
            //that is coincident and facing each other
            "mate_off": ComponentConstraintType.ASM_CONSTRAINT_MATE_OFF,
            //Use this option to make two planar surfaces parallel and facing each other
            "align": ComponentConstraintType.ASM_CONSTRAINT_ALIGN,
            //Use this option to make two planes coplanar, two axes coaxial and two points
            //coincident. You can also align revolved surfaces or edges
            "align_off": ComponentConstraintType.ASM_CONSTRAINT_ALIGN_OFF,
            //Use this option to align two planar surfaces at an offset
            "insert": ComponentConstraintType.ASM_CONSTRAINT_INSERT,
            //Use this option to insert a "male" revolved surface into a ``female'' revolved
            //surface, making their respective axes coaxial
            "orient": ComponentConstraintType.ASM_CONSTRAINT_ORIENT,
            //Use this option to make two planar surfaces to be parallel in the same direction
            "csys": ComponentConstraintType.ASM_CONSTRAINT_CSYS,
            //Use this option to place a component in an assembly by aligning the coordinate
            //system of the component with the coordinate system of the assembly
            "tangent": ComponentConstraintType.ASM_CONSTRAINT_TANGENT,
            //Use this option to control the contact of two surfaces at their tangents
            "put_on_srf": ComponentConstraintType.ASM_CONSTRAINT_PNT_ON_SRF,
            //Use this option to control the contact of a surface with a point
            "edge_on_srf": ComponentConstraintType.ASM_CONSTRAINT_EDGE_ON_SRF,
            //Use this option to control the contact of a surface with a straight edge
            "def_place": ComponentConstraintType.ASM_CONSTRAINT_DEF_PLACEMENT,
            //Use this option to align the default coordinate system of the component
            // tothe default coordinate system of the assembly
            "substitute": ComponentConstraintType.ASM_CONSTRAINT_SUBSTITUTE,
            //Use this option in simplified representations when a component has been
            //substituted with some other model
            "put_on_line": ComponentConstraintType.ASM_CONSTRAINT_PNT_ON_LINE,
            //Use this option to control the contact of a line with a point
            "fix": ComponentConstraintType.ASM_CONSTRAINT_FIX,
            //Use this option to force the component to remain in its current packaged position
            "auto": ComponentConstraintType.ASM_CONSTRAINT_AUTO
            //Use this option in the user interface to allow an automatic choice of constraint type
            //based upon the references
        };
         
        //
        //test_assembly(session, assembly, transf, featID, file_location, 
        //["align", "mate"],  
        //["axis", "datum"],["axis", "datum"],
        //["A_1", "DTM1"], ["A_9", "DTM9"]);
        //使用方式
        //test_assembly(使用的 session, 組立檔案, 參照座標準矩陣, 父組立零件ID, 欲組立零件位置,
        //約束型態矩陣, 父零件元素挑選型態矩陣, 欲組立零件挑選型態矩陣,
        //父零件參照矩陣, 欲組立零件參照矩陣);
        //五個矩陣請保持相同長度
        //假如 父組立零件ID 為 -1 則是與組立檔本身來組立
        function test_assembly(session, assembly, transf, featID, file_location, constrain_type, asm_pick_type, part_pick_type, asm_component_ref, part_component_ref) {
            /*
            make sure asm_reference and component_reference and constrain and 
            pickway are same length.
            */
            if (constrain_type.length != asm_pick_type.length ||
                constrain_type.length != part_pick_type.length ||
                constrain_type.length != asm_component_ref.length ||
                constrain_type.length != part_component_ref.length) {
                throw new Error(0, "please check array constrain_type and asm_pick_type and part_pick_type and asm_component_ref and part_component_ref must be same length.");
            }
            //設定part2 路徑
            var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName(file_location);
            //嘗試從 session 中取得 part2
            var componentModel = session.GetModelFromDescr(descr);
            //取得失敗 status null
            if (componentModel == null) {
                document.write("在session 取得不到零件" + file_location + "<br />");
                //從路逕取得 part2
                componentModel = session.RetrieveModel(descr);
                //仍然取得失敗 表示無此零件
                if (componentModel == null) {
                    // 此發錯誤
                    document.write("please check again your part location");
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
         
            //約束 list 等下要應用於 子
            var constrs = pfcCreate("pfcComponentConstraints");
         
            for (var i = 0; i < constrain_type.length; i++) {
                //選擇 父元素
                var asmItem = subassembly.GetItemByName(relation_map[asm_pick_type[i]], asm_component_ref[i]);
                if (asmItem == void null) {
                    throw new Error(0, "Can't get the reference " + asm_component_ref[i] + " from asm component.");
                }
                //選擇 子元素
                var compItem = componentModel.GetItemByName(relation_map[part_pick_type[i]], part_component_ref[i]);
                if (compItem == void null) {
                    throw new Error(0, "Can't get the reference " + part_component_ref[i] + " from part component.");
                }
                //採用互動式設定相關的變數
                var MpfcSelect = pfcCreate("MpfcSelect");
                //互動式設定 選擇元素 父
                var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
                //互動式設定 選擇元素 子
                var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
                //選擇約束形態
                var constr = pfcCreate("pfcComponentConstraint").Create(constrian_map[constrain_type[i]]);
                //約束選擇 剛剛得父元素
                constr.AssemblyReference = asmSel;
                //約束選擇 剛剛得子元素
                constr.ComponentReference = compSel;
                //設定約束屬性
                constr.Attributes = pfcCreate("pfcConstraintAttributes").Create(true, false);
                //close chain will be false false
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
         
        var work_directory = 'V:/home/phone/';
         
        //使用方式
        //test_assembly(使用的 session, 組立檔案, 參照座標準矩陣, 父組立零件ID, 欲組立零件位置,
        //約束型態矩陣, 父零件元素挑選型態矩陣, 欲組立零件挑選型態矩陣,
        //父零件參照矩陣, 欲組立零件參照矩陣);

        //------範例說明----
        //var body_id = test_assembly(session, assembly, transf, -1,work_directory + 'beam_angle.prt',
        //    ["align","align","align"],   限制條件
        //    ["datum","datum","datum"],["datum","datum","datum"],   告訴CREO選擇面or線or點
        //    ["ASM_FRONT", "ASM_TOP", "ASM_RIGHT"], ["FRONT", "TOP", "RIGHT"]);    面or線or點的代號

        var body_id = test_assembly(session, assembly, transf, -1,work_directory + 'prt0002.prt',
            ["align","align","align"],
            ["datum","datum","datum"],["datum","datum","datum"],
            ["ASM_FRONT", "ASM_TOP", "ASM_RIGHT"], ["FRONT", "TOP", "RIGHT"]);
        var body_id1 = test_assembly(session, assembly, transf, body_id,work_directory + 'prt0001.prt',
            ["align","align"],
            ["datum","axis"],["datum","axis"],
            ["DTM1", "A_2"], ["DTM1", "A_3"]);
        var body_id3 = test_assembly(session, assembly, transf, body_id1,work_directory + 'prt0002.prt',
            ["align","align"],
            ["datum","axis"],["datum","axis"],
            ["DTM1", "A_1"], ["DTM1", "A_2"]);
            
        var body_id4 = test_assembly(session, assembly, transf, body_id1,work_directory + 'prt0002.prt',
            ["align","align"],
            ["datum","axis"],["datum","axis"],
            ["DTM1", "A_2"], ["DTM1", "A_2"]);
            
        var body_id5 = test_assembly(session, assembly, transf, body_id,work_directory + 'prt0001.prt',
            ["align","align"],
            ["datum","axis"],["datum","axis"],
            ["DTM2", "A_3"], ["DTM2", "A_3"]);
            
        assembly.Regenerate(void null);
        session.GetModelWindow(assembly).Repaint();
        </script>
        </body>
        </html>
        '''


        return outstring
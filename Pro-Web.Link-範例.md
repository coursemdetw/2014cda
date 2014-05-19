var drwmodels = drawing.ListModels();
newWin.document.writeln ("&lt;br>" + "Drawing: " + drawing.FileName + " ( "
+ drwmodels.Count + " drw models )");

var modelitemtype = pfcCreate("pfcModelItemType");

/*--Retrieve the symbol definition from the system--*/

var symDef = drawing.RetrieveSymbolDefinition ("sym_name", void null, void null, true);

for (var i = 0; i &lt; drwmodels.Count; i++) {

drwmodel = drwmodels.Item(i);
var showndims = drawing.ListShownDimensions(drwmodel, modelitemtype.ITEM_DIMENSION);
newWin.document.writeln ("&lt;br>" + " &nbsp; Model " + (i+1) + ": "
+ drwmodel.FileName + " ( " + showndims.Count + " shown dims )");

for (var j = 0; j &lt; showndims.Count; j++) {

var pnt3d = void null;
var showndim = showndims.Item(j);
var symbol = showndim.Symbol;
var value = showndim.DimValue;
pnt3d = showndim.Location;

newWin.document.writeln ("&lt;br>" + " &nbsp; &nbsp; Dim " + (j+1) + ": "
+ symbol + " = " + value + " ( " + pnt3d.Item(0)
+ " , " + pnt3d.Item(1) + " , " + pnt3d.Item(2) + " )");

var position = void null;
var instrs = pfcCreate ("pfcDetailSymbolInstInstructions").Create (symDef);
position = pfcCreate ("pfcFreeAttachment").Create (pnt3d);
var allAttachments = pfcCreate ("pfcDetailLeaders").Create ();

position.AttachmentPoint = pnt3d;
allAttachments.ItemAttachment = position;
instrs.InstAttachment = allAttachments;

/*--Set the VariantTexts (for var text)--*/

var vtpp = pfcCreate ("pfcDetailVariantText").Create ("vartext", j+1);
var vtpp2 = pfcCreate ("pfcDetailVariantTexts");
vtpp2.append(vtpp);
instrs.TextValues = vtpp2;

/*--Create and display the symbol--*/

var symInst = drawing.CreateDetailItem (instrs);
symInst.Show();
}
}

pfcWindow.Window.ExportRasterImage to save graphics

ProWindowPanZoomMatrixSet 

ComponentConstraintType—Using the TYPE options, you can specify the placement constraint types. They
are as follows:

ASM_CONSTRAINT_MATE—Use this option to make two surfaces touch one another, that is coincident and
facing each other.

ASM_CONSTRAINT_MATE_OFF—Use this option to make two planar surfaces parallel and facing each other.

ASM_CONSTRAINT_ALIGN—Use this option to make two planes coplanar, two axes coaxial and two points
coincident. You can also align revolved surfaces or edges.
○ 
ASM_CONSTRAINT_ALIGN_OFF—Use this option to align two planar surfaces at an offset.

ASM_CONSTRAINT_INSERT—Use this option to insert a "male" revolved surface into a ``female'' revolved
surface, making their respective axes coaxial.

ASM_CONSTRAINT_ORIENT—Use this option to make two planar surfaces to be parallel in the same direction.

ASM_CONSTRAINT_CSYS—Use this option to place a component in an assembly by aligning the coordinate
system of the component with the coordinate system of the assembly.

ASM_CONSTRAINT_TANGENT—Use this option to control the contact of two surfaces at their tangents.

ASM_CONSTRAINT_PNT_ON_SRF—Use this option to control the contact of a surface with a point.

ASM_CONSTRAINT_EDGE_ON_SRF—Use this option to control the contact of a surface with a straight edge.

ASM_CONSTRAINT_DEF_PLACEMENT—Use this option to align the default coordinate system of the component tothe default coordinate system of the assembly.

ASM_CONSTRAINT_SUBSTITUTE—Use this option in simplified representations when a component has been
substituted with some other model
 
ASM_CONSTRAINT_PNT_ON_LINE—Use this option to control the contact of a line with a point.

ASM_CONSTRAINT_FIX—Use this option to force the component to remain in its current packaged position.

ASM_CONSTRAINT_AUTO—Use this option in the user interface to allow an automatic choice of constraint type based upon the references.

getBodyDiagonalInfo: function() {
  try {
    var cModel = this.getCurrentModel();                
    var mitems = cModel.ListItems(pfcCreate("pfcModelItemType").ITEM_COORD_SYS);
    var cor = mitems.Item(0);
    var trans3 = cor.CoordSys;
 
    var modtyp = pfcCreate("pfcModelItemTypes");
    var item1 = pfcCreate("pfcModelItemType").ITEM_AXIS;
    var item2 = pfcCreate("pfcModelItemType").ITEM_POINT;
    var item3 = pfcCreate("pfcModelItemType").ITEM_COORD_SYS;
 
    modtyp.Insert(0,item1);
    modtyp.Insert(1,item2);
    modtyp.Insert(2,item3);
    var outline = cModel.EvalOutline(trans3,modtyp);
    var point2 = outline.Item(0);
    var x = point2.Item(0);
    var y = point2.Item(1);
    var z = point2.Item(2);
    var point3 = outline.Item(1);
    var p = point3.Item(0);
    var q = point3.Item(1);
    var r = point3.Item(2);
    var sum = Math.pow(p - x, 2) + Math.pow(q - y, 2) + Math.pow(r - z, 2);
    var diagonal = Math.sqrt(sum);
    return diagonal;
  } catch (e) {
    throw e;
  }
}

建立元件的約束物件

pfcComponentConstraint.Create()


ComponentConstraintType Using the TYPE options, you can specify the placement constraint types. They are as follows:

兩平面進行面接約束 (ASM_CONSTRAINT_MATE)

○ ASM_CONSTRAINT_MATE Use this option to make two surfaces touch one another, that is coincident and facing each other.

兩平面進行面接約束, 且相隔一段距離 (ASM_CONSTRAINT_MATE_OFF)

○ ASM_CONSTRAINT_MATE_OFF Use this option to make two planar surfaces parallel and facing each other.

兩平面或兩軸對齊 (ASM_CONSTRAINT_ALIGN)

○ ASM_CONSTRAINT_ALIGN Use this option to make two planes coplanar, two axes coaxial and two points coincident. You can also align revolved surfaces or edges.

兩平面或兩軸對齊, 且維持一特定距離 (ASM_CONSTRAINT_ALIGN_OFF)

○ ASM_CONSTRAINT_ALIGN_OFF Use this option to align two planar surfaces at an offset.

插入約束 (ASM_CONSTRAINT_INSERT)

○ ASM_CONSTRAINT_INSERT Use this option to insert a "male" revolved surface into a ``female'' revolved surface, making their respective axes coaxial.

同方位約束 (ASM_CONSTRAINT_ORIENT)

○ ASM_CONSTRAINT_ORIENT Use this option to make two planar surfaces to be parallel in the same direction.

座標系統定位約束 (ASM_CONSTRAINT_CSYS)

○ ASM_CONSTRAINT_CSYS Use this option to place a component in an assembly by aligning the coordinate system of the component with the coordinate system of the
assembly.

垂直約束 (ASM_CONSTRAINT_TANGENT)

○ ASM_CONSTRAINT_TANGENT Use this option to control the contact of two surfaces at their tangents.

控制與某曲面上一點接觸約束 (ASM_CONSTRAINT_PNT_ON_SRF)

○ ASM_CONSTRAINT_PNT_ON_SRF Use this option to control the contact of a surface with a point.

控制與某曲面上一線接觸約束 (ASM_CONSTRAINT_EDGE_ON_SRF)

○ ASM_CONSTRAINT_EDGE_ON_SRF Use this option to control the contact of a surface with a straight edge.

與組立中的特定座標系統對齊 (ASM_CONSTRAINT_DEF_PLACEMENT)

○ ASM_CONSTRAINT_DEF_PLACEMENT Use this option to align the default coordinate system of the component to the default coordinate system of the assembly.

取代約束 (ASM_CONSTRAINT_SUBSTITUTE)

○ ASM_CONSTRAINT_SUBSTITUTE Use this option in simplified representations when a component has been substituted with some other model

線與點進行接觸約束 (ASM_CONSTRAINT_PNT_ON_LINE)

○ ASM_CONSTRAINT_PNT_ON_LINE Use this option to control the contact of a line with a point.

固定約束 (ASM_CONSTRAINT_FIX)

○ ASM_CONSTRAINT_FIX Use this option to force the component to remain in its current packaged position.

○ ASM_CONSTRAINT_AUTO Use this option in the user interface to allow an automatic choice of constraint type based upon the references.AssemblyDatumSide Orientation of the assembly. This can have the following values:

進行正面方向約束

○ Yellow The primary side of the datum plane which is the default direction of the
arrow.

進行反面方向約束

○ Red The secondary side of the datum plane which is the direction opposite to that of
the arrow.

ComponentReference A reference on the placed component.

ComponentDatumSide Orientation of the assembly component. This can have the
following values:

正面約束

○ Yellow The primary side of the datum plane which is the default direction of the
arrow.

反面約束
○ Red The secondary side of the datum plane which is the direction opposite to that of
the arrow.

Offset The mate or align offset value from the reference.

In Pro/ENGINEER, a component's constraints are defined to restrict its movement with respect to other components. Under certain conditions, a component's definition dialog box shows an option to "Allow assumptions" on the component.

When you select this option, Pro/ENGINEER adds more constraints to completely constrain the component's motion with respect to its connected, neighboring components.

Because these extra constraints are hidden, the exporter cannot accurately determine the DoF restrictions between a component and its connected, neighboring components.

To Allow Constraint Orientation Assumptions

The Allow Assumptions check box, located in the Placement Status area of the Component Placement dialog box, allows you to switch system constraint orientation assumptions on and off. The Allow Assumptions check box is available whenever assumptions are made or could be made; when a component is fully constrained, the check box disappears. The setting of Allow Assumptions is component specific, and the setting is saved with the component.

Allow assumptions - will allow Pro/E to make assumptions as to what you think something to be fully constrained, like a bushing in a cylinder after you use the insert and align will be listed as fully constrained even though a rotational degree of freedom still exist.

Typically, three placement constraints are required to fully constrain a component. Fewer constraints may be applied if the system is able to position the component by making assumptions regarding orientation.

In reality, there is still a rotational degree of freedom open for this component, but that may not be critical in our design, so we can allow the system to fix this rotational degree of freedom for us. If we were to uncheck the “Allow Assumptions” box, we would have to define additional placement constraints to fix this rotational degree of freedom.
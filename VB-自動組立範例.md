http://inversionconsulting.blogspot.in/2008/06/proe-vb-api-not-just-for-visual-basic.html

'Code for Auto Assembly Program
Imports pfcls
Imports System
Imports System.IO

Public Class Form1
Private Sub Button1_Click(ByVal sender As System.Object, ByVal e As System.EventArgs_
)Handles Button1.Click
Dim conn As IpfcAsyncConnection = Nothing
Dim session As IpfcBaseSession
Dim pat, pat1 As String
Dim model As IpfcModel
Dim modelDesc As IpfcModelDescriptor
Dim modelDesc1 As IpfcModelDescriptor
Dim i, k As Integer
Dim win As IpfcWindow
Dim loc As String
Dim modelnames As String() = Nothing
Dim asmModels As Cstringseq
Dim drawingPath As String
Dim drawingName, drawingName1 As String Dim drawingName2() As String
Dim errMsg As String = ""

'For Assembly constraints
Dim components As IpfcFeatures
Dim component As IpfcComponentFeat
Dim compConstraints As IpfcComponentConstraints
Dim compConstraint As IpfcComponentConstraint
Dim Constraint1 As IpfcComponentConstraint
Dim Constraints1 As ipfcComponentConstraints
Dim assembly As IpfcAssembly
Dim assemblyDatums(2) As String
Dim componentDatums(2) As String
Dim asmReference As IpfcSelection
Dim compReference As IpfcSelection
Dim constraintType As String
Dim componentModel As IpfcSolid
Dim asmcomp As IpfcComponentFeat

If Not System.Diagnostics.Process.GetProcessesByName("nmsd").Length > 0 Then 
errMsg =_ "Name service is not running on the system."
End If 

If System.Environment.GetEnvironmentVariable("PRO_COMM_MSG_EXE") = "" Then
If errMsg = "" Then errMsg = "Environment variable 'PRO_COMM_MSG_EXE' has not been_ set."
Else 

errMsg = errMsg + Chr(13).ToString + "Environment variable_ 'PRO_COMM_MSG_EXE' has not been set."

End If
End If

If System.Environment.GetEnvironmentVariable("PRO_DIRECTORY") Is Nothing Then 

If errMsg = "" Then
errMsg = "Environment variable 'PRO_DIRECTORY' has not been set."
Else 

errMsg = errMsg + Chr(13).ToString + "Environment variable 'PRO_DIRECTORY' has not been set."

End If 

End If 'If Services are not running Exit Application 

If Not errMsg = "" Then 
errMsg = errMsg + Chr(13).ToString + "These may lead to errors in running the application." 
MsgBox(errMsg, MsgBoxStyle.Critical) 

Else 'Connect to Pro/Engineer 

If conn Is Nothing OrElse Not conn.IsRunning Then 
conn = (New CCpfcAsyncConnection).Connect(Nothing, Nothing, Nothing, Nothing)
session = conn.Session 

If session Is Nothing Then 
Throw New Exception("Session does not exist")
Else 
session.EraseUndisplayedModels() 

'Directory for Pro/E Models

loc = "d:\proemodels\".ToLower
asmModels = session.ListFiles("*.asm", EpfcFileListOpt.EpfcFILE_LIST_LATEST, loc)

If asmModels.Count <> 0 Then

k = 0 

For k = 0 To asmModels.Count - 1
drawingPath = asmModels.Item(k)
drawingName = drawingPath.Substring(loc.Length) 
drawingName1 = drawingName.Substring(0, drawingName.Length - 4) 
drawingName2 = drawingName1.Split("-") 
pat1 = drawingName.Substring(0, 1).ToUpper & "SAMPLE" & drawingName2(1).ToUpper & ".prt"
drawingName1 = drawingName1.Substring(drawingName1.Length - 7, 7).ToUpper

modelDesc1 = (New CCpfcModelDescriptor).Create(0, drawingName, Nothing) 
session.RetrieveModel(modelDesc1) 
session.OpenFile(modelDesc1).Activate() 
model = session.CurrentModel
assembly = CType(model, IpfcAssembly) 
modelDesc = (New CCpfcModelDescriptor).Create(1, pat1, Nothing) 
componentModel = session.RetrieveModel(modelDesc) 
pat1 = pat1.Substring(0, pat1.Length - 4)
components = assembly.ListFeaturesByType(False, EpfcFeatureType.EpfcFEATTYPE_COMPONENT) 

'Search through the models in the current assembly

For i = 0 To components.Count - 1 
component = components.Item(i) 
modelDesc = component.ModelDescr 

If modelDesc.InstanceName = pat1 Then 
compConstraints = component.GetConstraints() 
Constraints1 = New CpfcComponentConstraints
asmcomp = assembly.AssembleComponent(componentModel, Nothing) 

For j = 0 To compConstraints.Count - 1
compConstraint = compConstraints.Item(j) 
constraintType = constraintTypeToString(compConstraint.Type) 
asmReference = compConstraint.AssemblyReference 
compReference = compConstraint.ComponentReference

Select Case (constraintType) 

Case "Mate"
Constraint1 = (New CCpfcComponentConstraint).Create_(EpfcComponentConstraintType.EpfcASM_CONSTRAINT_MATE) 
Constraint1.AssemblyReference = asmReference 
Constraint1.ComponentReference = compReference 
Constraints1.Insert(Constraints1.Count, Constraint1)

Case "Align"
Constraint1 = (New CCpfcComponentConstraint).Create_(EpfcComponentConstraintType.EpfcASM_CONSTRAINT_ALIGN_OFF) 
Constraint1.AssemblyReference = asmReference 
Constraint1.ComponentReference = compReference 
Constraints1.Insert(Constraints1.Count, Constraint1)

Case "Align Offset"
Constraint1 = (New CCpfcComponentConstraint).Create_(EpfcComponentConstraintType.EpfcASM_CONSTRAINT_ALIGN) 
Constraint1.AssemblyReference = asmReference 
Constraint1.ComponentReference = compReference 
Constraint1.Offset = 10 
Constraints1.Insert(Constraints1.Count, Constraint1) 

End Select 

Next 

asmcomp.SetConstraints(Constraints1, Nothing)
assembly.Regenerate(Nothing)
session.GetModelWindow(assembly).Repaint()
model.Save() 

End If 

Next

session.CurrentWindow.Activate()
win = session.CurrentWindow
Next conn.Disconnect(2) 

End If

End If

End If

End If

End Sub


Private Function constraintTypeToString(ByVal type As Integer) As String 

Select Case (type)

Case EpfcComponentConstraintType.EpfcASM_CONSTRAINT_MATE
Return ("Mate")

Case EpfcComponentConstraintType.EpfcASM_CONSTRAINT_MATE_OFF
Return ("Mate Offset")

Case EpfcComponentConstraintType.EpfcASM_CONSTRAINT_ALIGN
Return ("Align")

Case EpfcComponentConstraintType.EpfcASM_CONSTRAINT_ALIGN_OFF
Return ("Align Offset")

Case EpfcComponentConstraintType.EpfcASM_CONSTRAINT_INSERT
Return ("Insert")

Case EpfcComponentConstraintType.EpfcASM_CONSTRAINT_ORIENT
Return ("Orient")

Case EpfcComponentConstraintType.EpfcASM_CONSTRAINT_CSYS
Return ("Csys")

Case EpfcComponentConstraintType.EpfcASM_CONSTRAINT_TANGENT
Return ("Tangent")

Case EpfcComponentConstraintType.EpfcASM_CONSTRAINT_PNT_ON_SRF
Return ("Point on Surf")

Case EpfcComponentConstraintType.EpfcASM_CONSTRAINT_EDGE_ON_SRF
Return ("Edge on Surf")

Case EpfcComponentConstraintType.EpfcASM_CONSTRAINT_DEF_PLACEMENT
Return ("Default")

Case EpfcComponentConstraintType.EpfcASM_CONSTRAINT_SUBSTITUTE
Return ("Substitute")

Case EpfcComponentConstraintType.EpfcASM_CONSTRAINT_PNT_ON_LINE
Return ("Point on Line")

Case EpfcComponentConstraintType.EpfcASM_CONSTRAINT_FIX
Return ("Fix")

Case EpfcComponentConstraintType.EpfcASM_CONSTRAINT_AUTO
Return ("Auto")

End Select

Return ("Unrecognized Type")
End Function
End Class
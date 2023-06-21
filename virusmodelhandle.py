import os
from pywinauto.application import Application
import time
import shutil

def handleModels(filepath):
    exeFileList = []
    jsFileList = []
    vbsFileList = []
    zipFileList = []
    rarFileList = []
    if os.path.exists(filepath):
        fileNameList = os.listdir(filepath)
        for i in fileNameList:
            if os.path.splitext(i)[-1] == '.exe':
                exeFileList.append(i)
            elif os.path.splitext(i)[-1] == '.js':
                jsFileList.append(i)
            elif os.path.splitext(i)[-1] == '.vbs':
                vbsFileList.append(i)
            elif os.path.splitext(i)[-1] == '.zip':
                zipFileList.append(i)
            elif os.path.splitext(i)[-1] == '.rar':
                rarFileList.append(i)
            else:
                path = filepath + '\\' +i
                os.remove(path)
    else:
        print("the file not exited")
    return exeFileList,jsFileList,vbsFileList,zipFileList,rarFileList

def afterhandle(filepath,exeFileList):
    EXList = []
    FileNameList = os.listdir(filepath)
    for i in FileNameList:
        if os.path.splitext(i)[-1] in ['.exe','.js','.vbs','.zip','.rar']:
            pass
        elif os.path.splitext(i)[-1] == '.EX~':
            EXList.append(os.path.splitext(i)[0][0:6].lower())
            path = filepath + '\\' + i
            os.remove(path)
        else:
            path = filepath + '\\' + i
            os.remove(path)
    for file in exeFileList:
        if file[0:6] not in EXList:
            path = filepath + '\\' + file
            os.remove(path)

def exeFileHandle(exeFileList,upxpath,filepath):
    app = Application().start(upxpath)
    dlg = app.window(title = 'UPX Tool+')
    #dlg.print_control_edentifiers()
    edit = dlg['Edit']
    for exefile in exeFileList:
        file = filepath + '\\'+exefile
        edit.set_text(r'')
        edit.type_keys(file,with_spaces=True)
        dlg.Button4.click()
        time.sleep(2)
        print("文件加壳处理完成: " + exefile)
    print("handle file finished")

if __name__ =="__main__":
    filepath = input("please enter the filepath: ")
    upxpath = r'C:\Users\admin\Desktop\工具\可用夹克工具\UPX Tool+ 1.1.1\UPXTool+.exe'
    handleModelsResult = handleModels(filepath)
    exeFileHandle(handleModelsResult[0],upxpath,filepath)
    afterhandle(filepath,handleModelsResult[0])








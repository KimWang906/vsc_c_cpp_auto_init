"""
Written by Hoplin(https://github.com/J-hoplin1)
Version : v 1.0.3
Last Editted 2021 / 12 / 20
Python Version : 3.7.5
"""
import os,sys,yaml,platform,zipfile,shutil
import subprocess
from enum import Enum
from pathlib import Path

releaseversion = "1.0.3(Release : 2021_12_20)"

class textColor:
    '''
    Class : For text color in CLI UI
    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class GlobalUtilities(object):
    '''
    class : Global Utilities
    optionInitiator : Execute method with eval
    clearconsole : clear console ui
    pressKeyToContinue : Press enter to next step
    checkDirectoryExist : Check if argument : directory is existing directory
    endProcess : Close this software session
    warningMessageHandler : Form of Warning message
    errorMessageHandler : Form of error message
    '''

    def __init__(self):
        pass

    @classmethod
    def clearConsole(cls) -> None:
        #Windows Clear Console
        if platform.system() == "Windows":
            os.system('cls')
        #Darwin Clear Console
        else:
            os.system('clear')

    @classmethod
    def pressKeyToContinue(cls) -> None:
        input("Press any key to continue...")

    def checkDirectoryExist(self,directory) -> bool:
        try:
            res = Path(directory).is_dir()
            return res
        except OSError as p:
            return False

    @classmethod
    def endProcess(cls) -> None:
        sys.exit()

    @staticmethod
    def globalWarningMessageHandler(message) -> None:
        print(f"{textColor.WARNING}{message}{textColor.ENDC}")

    def warningMessageHandler(self,message) -> None:
        print(f"{textColor.WARNING}{message}{textColor.ENDC}")

    def errorMessageHandler(self,message,additionalmsg="Additional Message Not Exist") -> None:
        #print(dir(message))
        #print(message.strerror)
        print(f"{textColor.FAIL}Error Occured : {message.strerror} / {additionalmsg}{textColor.ENDC}")
        self.pressKeyToContinue()
        self.clearConsole()
        self.endProcess()
#ENV initiator
class FeatureProcessors(GlobalUtilities):
    '''
    Class : It's a class that handles each option functionally.
    returnProjectDirectory : return list of project Directory
    projectDirectoryChecker : if project directory not exist it genereate new directory user designate
    help : print document
    '''
    __CDirectory = 'C:\\'
    __GCCDirectory = 'C:\\mingw64\\bin'
    __minGWzipfile = os.getcwd() + "\\mingw\\mingw64.zip"
    __batchfilesDirectory = os.getcwd() + "\\batchfiles"
    __decompressDirectory = 'C:\\mingw64'
    __ProjectDirectory = None

    def __init__(self,bitselection="64bit") -> None:
        self.__optionMapper = {
            1: self.help,
            2: self.installAndBuildENV,
            3: self.openExistingProject,
            4: self.deleteExistingProject,
            5: self.initiateNewProject,
            6: self.changeProjectDirectory,
            7: self.viewSettings
        }
        try:
            with open('config.yml') as f:
                self.yml = yaml.load(f,yaml.FullLoader)
                self.directoryInfo = self.yml['directories']
                self.__ProjectDirectory = self.directoryInfo['Project_Directory']
                self.projectDirectoryChecker(self.__ProjectDirectory,True)
        except FileNotFoundError as e:
            self.errorMessageHandler(e,"Config.yml not found! Please regenerate config.yml. Program close")

    @classmethod
    def returnStaticVariableGCCDir(cls) -> str:
        return cls.__gccdirectory

    def returnProjectDirectory(self):
        return os.listdir(self.__ProjectDirectory)

    def projectDirectoryChecker(self,rp,forceclose=False):
        # If user designated project directory exist save directory
        if self.checkDirectoryExist(rp):
            return True
        # If user designated project directory didn't exist make directory
        else:
            try:
                os.mkdir(rp)
                print(f"Project directory : {rp} generated, due to non exist directory")
                return True
            except OSError as e:
                if forceclose:
                    self.errorMessageHandler(e,"Can't generate directory. Check if directory has the proper directory form.")
                    return False
                else:
                    return False

    def executeMethod(self,optNum):
        self.__optionMapper[optNum]()

    def help(self) -> None:
        try:
            self.clearConsole()
            print(f"""
        <Document : About function per each Option>

        ※ Basic Command
        /exit : You can exit this program. You can use this command in main

        /back : You can go back to before state. You can use this command in option 3,4,5

        1. Help

        -> show this documentation

        2. Install MinGW 64bit and build basic ENV

        {textColor.WARNING}* Warning : This option require VS Code to be in PATH. If not installation may be in process abnormally.{textColor.ENDC}
        * Neccessary :  Check windows environment variable, VSCode Extension if successfully install, enroll
        -> Unzip MinGW GCC Compiler(Standard : 64bit / v 8.1.0) and enroll to environment variable. After this it enroll    GCC to environment variable, next it install Basic C/C++ VS Code Extension.

        3. Open Existing Project

        -> You can select project directory and open it with vscode

         4. Delete Existing Project

         {textColor.WARNING}* Warning : You can't recover delete file after remove.{textColor.ENDC}
         -> You can delete project which you generated before

         5. Initiate New Project

         -> You can initiate new C/C++ Project at VSCode
         6. View Settings
         -> You can see basic information about this software
            """)
            self.pressKeyToContinue()
            self.clearConsole()
        except KeyboardInterrupt as e:
            self.clearConsole()
            return


    def installAndBuildENV(self):
        try:
            if self.checkDirectoryExist(self.__GCCDirectory):
                self.warningMessageHandler(
                    f"Directory : {self.__GCCDirectory} already exist! Please check if MingW has already been installed")
            else:
                try:
                    print("Decompressing minGW64. This might take some time. Please wait a moment.")
                    print(f"Decompressing to : {self.__decompressDirectory}")
                    self.clearConsole()
                    with zipfile.ZipFile(self.__minGWzipfile, 'r') as z:
                        z.extractall(self.__decompressDirectory)
                except FileNotFoundError as e:
                    self.errorMessageHandler(e, "mingw64/mingw64.zip not found. Program close")
                    # Add minGW64 GCC/G++ to Windows PATH : run batch file
                batname_enrollvariable = self.__batchfilesDirectory + "\\enrollvariable.bat"
                subprocess.run([batname_enrollvariable])
                print(
                    "Install C/C++ Extension to Visual Studio Code. Make sure extension installed completely after this process.")
                batname_installExtension = self.__batchfilesDirectory + "\\installCExtension.bat"
                subprocess.run([batname_installExtension])
        except KeyboardInterrupt as e:
            self.warningMessageHandler("You forcely stop while progressing setting! This could cause abnormal operation in the future.  ")
            pass

    def openExistingProject(self):
        dir_list = self.returnProjectDirectory()
        if not dir_list:
            self.warningMessageHandler(f"Warning : Project Directory({self.__ProjectDirectory}) you designated is empty!")
            self.pressKeyToContinue()
            self.clearConsole()
        else:
            while True:
                print("Select project you want to open with Visual Studio Code.\nEnter '/back' to go back to main.")
                print(f"{'-' * 15}")
                for n, i in enumerate(dir_list, start=1):
                    print(f"{n}. {i}",end='\n')
                print(f"{'-' * 15}")
                try:
                    selection = input(">> ")
                    if selection.lower() == "/back":
                        self.clearConsole()
                        break
                    elif 1 <= int(selection) <= len(dir_list):
                        projectName = dir_list[int(selection) - 1]
                        projectdir = self.__ProjectDirectory + f"\\{projectName}"
                        batname_openproject = self.__batchfilesDirectory + "\\openproject.bat"
                        subprocess.run([batname_openproject,projectdir])
                        print(f"Successfully open project : {projectName}")
                        self.pressKeyToContinue()
                        self.clearConsole()
                        break
                    else:
                        self.clearConsole()
                        self.warningMessageHandler("Warning : 잘못된 값이 입력되었습니다.")
                except ValueError:
                    self.clearConsole()
                    self.warningMessageHandler("Warning : 정확한 값을 입력해주세요.")
                    pass
                except KeyboardInterrupt:
                    self.clearConsole()
                    self.warningMessageHandler("Warning : 뒤로가기 위해서는 '/back'을 입력해주세요")

    def changeProjectDirectory(self):
        while True:
            print("Enter directory you want to change as project directory.")
            print(f"Project Directory you designated : {self.__ProjectDirectory}\n")
            inpLoop = True
            while inpLoop:
                try:
                    prj_dir = input(">> ")
                    inpLoop = False
                except KeyboardInterrupt as e:
                    self.clearConsole()
                    self.warningMessageHandler("Warning : 뒤로가기 위해서는 '/back'을 입력해주세요")

            if prj_dir == "/back":
                self.clearConsole()
                break
            else:
                if not prj_dir:
                    prj_dir = "C:\\"
                res = self.projectDirectoryChecker(prj_dir,False)
                if res:
                    self.__ProjectDirectory = prj_dir
                    self.directoryInfo['Project_Directory'] = prj_dir
                    with open('config.yml', 'w') as f:
                        yaml.dump(self.yml, f)
                    print(f"Successfully change Project Directory : {prj_dir}")
                    self.pressKeyToContinue()
                    self.clearConsole()
                    break
                else:
                    self.clearConsole()
                    self.warningMessageHandler("Warning : Fail to change Project Directory... Try again")

    def deleteExistingProject(self):
        dir_list = self.returnProjectDirectory()
        if not dir_list:
            self.warningMessageHandler(f"Warning : Project Directory({self.__ProjectDirectory}) you designated is empty!")
            self.pressKeyToContinue()
            self.clearConsole()
        else:
            while True:
                print("Select project you want to delete.")
                print(f"{'-' * 15}")
                for n, i in enumerate(dir_list, start=1):
                    print(f"{n}. {i}", end='\n')
                print(f"{'-' * 15}")
                try:
                    selection = input(">> ")
                    if selection.lower() == "/back":
                        self.clearConsole()
                        break
                    elif 1 <= int(selection) <= len(dir_list):
                        self.clearConsole()
                        projectName = dir_list[int(selection) - 1]
                        projectdir = self.__ProjectDirectory + f"\\{projectName}"
                        while True:
                            self.warningMessageHandler(f"Warning : 삭제된 디렉토리는 어떠한 방법으로도 복구할 수 없습니다. 진행하시겠습니까?(Yes / No)\n현재 선택한 프로젝트 이름 : {projectName} ")
                            try:
                                opt = input("yes 혹은 no를 입력하여 승인 혹은 보류하기 >> ")
                                if opt.lower() == "yes":
                                    shutil.rmtree(projectdir)
                                    print(f"Successfully remove project : {projectName}")
                                    self.pressKeyToContinue()
                                    self.clearConsole()
                                    break
                                elif opt.lower() == "no":
                                    self.clearConsole()
                                    break
                                else:
                                    self.clearConsole()
                                    self.warningMessageHandler("Warning : yes 혹은 no만 입력가능합니다.")
                            except ValueError as e:
                                self.clearConsole()
                                self.warningMessageHandler("Warning : 잘못된 값이 입력되었습니다.")
                            except PermissionError as e:
                                self.clearConsole()
                                self.warningMessageHandler("Warning : 윈도우 권한오류. 해당 디렉토리의 모든 프로세스가 종료되었는지 확인해주세요.")
                        break
                    else:
                        self.clearConsole()
                        self.warningMessageHandler("Warning : 잘못된 값이 입력되었습니다.")
                except ValueError:
                    self.clearConsole()
                    self.warningMessageHandler("Warning : 정확한 값을 입력해주세요.")
                    pass
                except KeyboardInterrupt:
                    self.clearConsole()
                    self.warningMessageHandler("Warning : 뒤로가기 위해서는 '/back'을 입력해주세요")

    def initiateNewProject(self):
        while True:
            try:
                print("Please enter the name of the project to be initialized.")
                print(f"* Project directory will be generated at {self.__ProjectDirectory}\n")
                projectName = input(">> ")
                if projectName.lower() == "/back":
                    self.clearConsole()
                    break
                try:
                    projectName = '_'.join(projectName.split(' '))
                    newProjectDirectory = str(self.__ProjectDirectory + f"\\{projectName}")
                    batname_initiateProject = self.__batchfilesDirectory + "\\initiateProject.bat"
                    batname_openproject = self.__batchfilesDirectory + "\\openproject.bat"
                    print(f"{textColor.OKBLUE}Generating Project Directory : {newProjectDirectory} {textColor.ENDC}")
                    os.mkdir(newProjectDirectory)
                    print(f"{textColor.OKBLUE}Generating VSCode Configuration File : {newProjectDirectory}{textColor.ENDC}")
                    subprocess.run([batname_initiateProject, newProjectDirectory])
                    print(f"Open initiated project at Visual Studio Code...")
                    subprocess.run([batname_openproject, newProjectDirectory])
                    self.pressKeyToContinue()
                    self.clearConsole()
                    break
                except OSError as e:
                    self.clearConsole()
                    self.warningMessageHandler("Warning : 이 오류에는 몇가지 가능성이 있습니다. \n 1. Winodws 폴더 이름 생성 규정 위반 \n 2. 이미 존재하는 디렉토리 이름 \n 3. '/back'이라는 단어는 소프트웨어 커맨드로 사용되고 있습니다. 다른이름을 사용해주세요")
            except ValueError:
                self.clearConsole()
                self.warningMessageHandler("Warning : 정확한 값을 입력해주세요.")
                pass
            except KeyboardInterrupt:
                self.clearConsole()
                self.warningMessageHandler("Warning : 뒤로가기 위해서는 '/back'을 입력해주세요")

    def viewSettings(self) -> None:
        try:
            print(f"""
        <Settings>

        ac : Able to change in config.yml
        nc : Unable to change this value

        1. nc - Basic GCC Directory( + to Path) : {self.__GCCDirectory}
        2. ac - Where did my project saved in this session? : {self.__ProjectDirectory}
        3. nc - Support Language / Compiler Info : C_C++ / MinGW64 GCC Compiler 8.1.0 64bit(x86_64-posix-seh)      
        4. nc - Support Tool : Visual Studio Code

        * MinGW URL : https://sourceforge.net/projects/mingw-w64/files/mingw-w64
        * You can change your project directory from 'config.yml - Project_Directory'
        * This software source code is open source : https://github.com/J-hoplin1/VSCode_C_CPP_Env_Initiator
        * If you find some bugs or additional features you want to add, please leave a comment at https://github.com/J-hoplin1/VSCode_C_CPP_Env_Initiator/issues
        * License : MIT License
        """)
            self.pressKeyToContinue()
            self.clearConsole()
        except KeyboardInterrupt as e:
            self.clearConsole()
            return

# CLI UI class
class CliUI(GlobalUtilities):
    '''
    Class : It's a class that processes the CLI UI environment-related parts.
    '''
    def __init__(self) -> None:
        self.__options = Enum('option', ['Help', 'Install_MinGW_64bit_and_build_basic_ENV', 'Open_existing_project_VSCode','Delete_existing_project','Initiate_new_C_C++_Project','Change_Project_Directory','View settings'])

    def option_selector(self) -> Enum:
        opt = [f'{i.value}. {i.name}' for i in self.__options]

        while True:
            print("\nStandard : MinGW GCC / G++ 8.1.0")
            print(f"System Info : {platform.system()} {platform.architecture()[0]} | Version : {releaseversion}")
            print("Enter '/exit' to end program.")
            print(f"{'-' * 15}")
            for l in opt:
                print(l,end='\n')
            print(f"{'-' * 15}")
            try:
                select = input(">> ")
                if select.lower() == '/exit':
                    self.clearConsole()
                    self.endProcess()
                elif 1 <= int(select) <= len(opt):
                    self.clearConsole()
                    return self.__options(int(select))
                else:
                    self.clearConsole()
                    self.warningMessageHandler("Warning : 잘못된 값이 입력되었습니다.")
            except ValueError:
                self.clearConsole()
                self.warningMessageHandler("Warning : 정확한 값을 입력해주세요.")
            except KeyboardInterrupt:
                self.clearConsole()
                self.warningMessageHandler("Warning : 종료를 하기 위해 /exit를 입력해주시기 바랍니다")

    def returnUserOption(self):
        selectedOption = self.option_selector()
        #return value of options
        return selectedOption.value



if __name__=="__main__":
    #This software is only compatible for Windows OS
    #Check system OS
    platf = platform.system()
    if platf == "Windows":
        GlobalUtilities.clearConsole()
        ftpr = FeatureProcessors()
        cli = CliUI()
        while True:
            # Option : User selection
            optionSelect = cli.returnUserOption()
            ftpr.executeMethod(optionSelect)
    else:
        GlobalUtilities.globalWarningMessageHandler("This program only compatible for Windows OS. Sorry")
        GlobalUtilities.pressKeyToContinue()
        GlobalUtilities.clearConsole()
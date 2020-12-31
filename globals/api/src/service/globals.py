import os, sys, subprocess, site, importlib
from pathlib import Path
from python_helper import Constant as c
from python_helper import log, StringHelper, SettingHelper, EnvironmentHelper

class AttributeKey:

    KW_API = 'api'
    KW_NAME = 'name'
    KW_EXTENSION = 'extension'
    KW_DEPENDENCY = 'dependency'
    KW_LIST = 'list'
    KW_WEB = 'web'
    KW_LOCAL = 'local'
    KW_UPDATE = 'update'
    KW_RESOURCE = 'resource'

    GLOBALS_API_LIST = f'{KW_API}.{KW_LIST}'

    API_NAME = f'{KW_API}.{KW_NAME}'
    API_EXTENSION = f'{KW_API}.{KW_EXTENSION}'
    UPDATE_GLOBALS = f'{KW_UPDATE}-globals'
    PRINT_STATUS = 'print-status'
    DEPENDENCY_UPDATE = f'{KW_API}.{KW_DEPENDENCY}.{KW_UPDATE}'
    DEPENDENCY_LIST_WEB = f'{KW_API}.{KW_DEPENDENCY}.{KW_LIST}.{KW_WEB}'
    DEPENDENCY_LIST_LOCAL = f'{KW_API}.{KW_DEPENDENCY}.{KW_LIST}.{KW_LOCAL}'
    DEPENDENCY_RESOURCE_LIST = f'{KW_API}.{KW_DEPENDENCY}.{KW_LIST}.{KW_LOCAL}'
    PYTHON_VERSION = 'python.version'

    def getKey(api,key):
        return f'{Globals.__name__}.{key}'

    def getKeyByClassNameAndKey(cls,key):
        return f'{cls.__name__}.{key}'

def importResource(resourceName, resourceModuleName=None) :
    if not resourceName in IGNORE_REOURCE_LIST :
        resource = None
        module = None
        if not resourceModuleName :
            resourceModuleName = resourceName
        try :
            module = importlib.import_module(resourceModuleName)
        except Exception as exception:
            log.warning(importResource, f'Not possible to import "{resourceName}" resource from "{resourceModuleName}" module. Going for a second attempt')
            try :
                module = __import__(resourceModuleName)
            except :
                log.error(importResource, f'Not possible to import "{resourceName}" resource from "{resourceModuleName}" module in the second attempt either', exception)
        if module :
            try :
                resource = getattr(module, resourceName)
            except Exception as exception :
                log.warning(importResource, f'Not possible to import "{resourceName}" resource from "{resourceModuleName}" module. cause: {str(exception)}')
            return resource

class Globals:

    OS_SEPARATOR = os.path.sep

    ### There are 'places' where backslash is not much wellcome
    ### Having it stored into a variable helps a lot
    TAB_UNITS = 4
    SPACE = ''' '''
    TAB = TAB_UNITS * SPACE
    BACK_SLASH = '''\\'''
    SLASH = '''/'''
    HASH_TAG = '''#'''
    COLON = ''':'''
    COMA = ''','''
    SPACE = ''' '''
    DOT = '''.'''
    NEW_LINE = '''\n'''
    BAR_N = '''\\n'''
    NOTHING = ''''''
    SINGLE_QUOTE = """'"""
    DOUBLE_QUOTE = '''"'''
    TRIPLE_SINGLE_QUOTE = """'''"""
    TRIPLE_DOUBLE_QUOTE = '''"""'''
    DASH = '''-'''
    SPACE_DASH_SPACE = ''' - '''
    UNDERSCORE = '''_'''
    COLON_SPACE = ': '

    EXTENSION = 'yml'
    PYTHON_EXTENSION = 'py'

    ENCODING = 'utf-8'
    OVERRIDE = 'w+'
    READ = 'r'

    API_BACK_SLASH = f'api{OS_SEPARATOR}'
    SRC_BACK_SLASH = f'src{OS_SEPARATOR}'
    BASE_API_PATH = f'{API_BACK_SLASH}{SRC_BACK_SLASH}'

    GLOBALS_BACK_SLASH = f'globals{OS_SEPARATOR}'
    FRAMEWORK_BACK_SLASH = f'framework{OS_SEPARATOR}'
    SERVICE_BACK_SLASH = f'service{OS_SEPARATOR}'
    RESOURCE_BACK_SLASH = f'resource{OS_SEPARATOR}'
    REPOSITORY_BACK_SLASH = f'repository{OS_SEPARATOR}'
    DEPENDENCY_BACK_SLASH = f'dependency{OS_SEPARATOR}'

    LOCAL_GLOBALS_API_PATH = f'{SERVICE_BACK_SLASH}{FRAMEWORK_BACK_SLASH}{GLOBALS_BACK_SLASH}'

    TOKEN_PIP_USER = '__TOKEN_PIP_USER__'
    KW_SPACE_PIP_USER = f'{c.SPACE}--user'
    PIP_INSTALL = f'python -m pip install --upgrade{TOKEN_PIP_USER} --force-reinstall'
    UPDATE_PIP_INSTALL = f'python -m pip install --upgrade{TOKEN_PIP_USER} pip'

    CHARACTERE_FILTER = [
        '__'
    ]

    NODE_IGNORE_LIST = [
        '.git',
        'distribution',
        'dist',
        '__pycache__',
        '__init__',
        '__main__',
        'image',
        'audio',
        '.heroku',
        '.profile.d'
    ]

    STRING = 'str'
    INTEGER = 'int'
    BOOLEAN = 'bool'

    TRUE = 'True'
    FALSE = 'False'

    OPEN_TUPLE_CLASS = 'tuple'
    OPEN_LIST_CLASS = 'list'
    DICTIONARY_CLASS = 'dict'
    OPEN_TUPLE = '('
    OPEN_LIST = '['
    OPEN_SET = '{'
    OPEN_DICTIONARY = '{'

    SAFE_AMOUNT_OF_TRIPLE_SINGLE_OR_DOUBLE_QUOTES_PLUS_ONE = 4

    LIB = 'lib'
    STATIC_PACKAGE_PATH = f'{OS_SEPARATOR}statics'
    TOKEN_PYTHON_VERSION = '__TOKEN_PYTHON_VERSION__'
    HEROKU_PYTHON = f'{OS_SEPARATOR}lib{OS_SEPARATOR}python{TOKEN_PYTHON_VERSION}{OS_SEPARATOR}site-packages'

    DEBUG =     '[DEBUG  ] '
    ERROR =     '[ERROR  ] '
    WARNING =   '[WARNING] '
    SUCCESS =   '[SUCCESS] '
    FAILURE =   '[FAILURE] '
    SETTING =   '[SETTING] '

    OPEN_SETTING_INJECTION = '${'
    CLOSE_SETTING_INJECTION = '}'

    DEFAULT_LOG_STATUS = False
    DEFAULT_SUCCESS_STATUS = False
    DEFAULT_SETTING_STATUS = False
    DEFAULT_DEBUG_STATUS = False
    DEFAULT_WARNING_STATUS = False
    DEFAULT_FAILURE_STATUS = False
    DEFAULT_ERROR_STATUS = False

    APPLICATION = 'application'

    def __init__(self, filePath,
        settingsFileName=APPLICATION,
        logStatus = DEFAULT_LOG_STATUS,
        successStatus = DEFAULT_SUCCESS_STATUS,
        settingStatus = DEFAULT_SETTING_STATUS,
        debugStatus = DEFAULT_DEBUG_STATUS,
        warningStatus = DEFAULT_WARNING_STATUS,
        failureStatus = DEFAULT_FAILURE_STATUS,
        errorStatus = DEFAULT_ERROR_STATUS,
        encoding = ENCODING,
        printRootPathStatus = False,
        globalsEverything = False
    ):

        clear = lambda: os.system('cls')
        ###- clear() # or simply os.system('cls')

        self.filePath = filePath
        self.settingsFileName = self.getSettingsFileName(settingsFileName)
        self.logStatus = EnvironmentHelper.setEnvironmentValue(log.LOG, logStatus, default=Globals.DEFAULT_LOG_STATUS)
        self.successStatus = EnvironmentHelper.setEnvironmentValue(log.SUCCESS, successStatus, default=Globals.DEFAULT_SUCCESS_STATUS)
        self.settingStatus = EnvironmentHelper.setEnvironmentValue(log.SETTING, settingStatus, default=Globals.DEFAULT_SETTING_STATUS)
        self.debugStatus = EnvironmentHelper.setEnvironmentValue(log.DEBUG, debugStatus, default=Globals.DEFAULT_DEBUG_STATUS)
        self.warningStatus = EnvironmentHelper.setEnvironmentValue(log.WARNING, warningStatus, default=Globals.DEFAULT_WARNING_STATUS)
        self.failureStatus = EnvironmentHelper.setEnvironmentValue(log.FAILURE, failureStatus, default=Globals.DEFAULT_FAILURE_STATUS)
        self.errorStatus = EnvironmentHelper.setEnvironmentValue(log.ERROR, errorStatus, default=Globals.DEFAULT_ERROR_STATUS)
        log.loadSettings()
        self.printRootPathStatus = printRootPathStatus
        self.globalsEverything = globalsEverything
        basicSettingsAsDictionary = {
            'activeEnvironment' : self.activeEnvironment,
            'successStatus' : self.successStatus,
            'settingStatus' : self.settingStatus,
            'debugStatus' : self.debugStatus,
            'warningStatus' : self.warningStatus,
            'failureStatus' : self.failureStatus,
            'errorStatus' : self.errorStatus,
            'logStatus' : self.logStatus,
            'globalsEverything' : self.globalsEverything,
            'printRootPathStatus' : self.printRootPathStatus
        }
        self.setting(self.__class__,f'Basic settings: {StringHelper.prettyPython(basicSettingsAsDictionary, tabCount=1)}')
        self.debug(f'{self.__class__.__name__}.instance.filePath = {self.filePath}')
        self.debug(f'{self.__class__.__name__}.filePath = {__file__}')

        self.charactereFilterList = Globals.CHARACTERE_FILTER
        self.nodeIgnoreList = Globals.NODE_IGNORE_LIST
        self.encoding = self.getEncoding(encoding)

        self.buildApplicationPath()

        self.settingTree = self.getSettingTree()
        self.staticPackage = self.getStaticPackagePath()
        self.apiName = self.getApiName()
        self.extension = self.getExtension()

        self.printStatus = self.getSetting(AttributeKey.PRINT_STATUS)
        self.apiNameList = self.getSetting(AttributeKey.GLOBALS_API_LIST)

        if self.printStatus :
            print(f'''            {self.__class__.__name__} = {self}
            {self.__class__.__name__}.staticPackage =   {self.staticPackage}
            {self.__class__.__name__}.currentPath =     {self.currentPath}
            {self.__class__.__name__}.localPath =       {self.localPath}
            {self.__class__.__name__}.baseApiPath =     {self.baseApiPath}
            {self.__class__.__name__}.apiPath =         {self.apiPath}
            {self.__class__.__name__}.apisRoot =        {self.apisRoot}
            {self.__class__.__name__}.apisPath =        {self.apisPath}
            {self.__class__.__name__}.apiPackage =      {self.apiPackage}
            {self.__class__.__name__}.apiName =         {self.apiName}
            {self.__class__.__name__}.extension =       {self.extension}\n''')

            self.printTree(self.settingTree,f'{self.__class__.__name__} settings tree')

        self.updateDependencyStatus = self.getSetting(AttributeKey.DEPENDENCY_UPDATE)
        self.rootPathTree = {}
        self.update()

    def getSettingsFileName(self, settingsFileName) :
        self.mainSettingsFileName = settingsFileName
        self.activeEnvironment = SettingHelper.getActiveEnvironment()
        if SettingHelper.DEFAULT_ENVIRONMENT == self.activeEnvironment :
            return settingsFileName
        else :
            return f'{settingsFileName}{c.DASH}{self.activeEnvironment}'

    def buildApplicationPath(self):
        if self.filePath :
            self.currentPath = f'{str(Path(self.filePath).parent.absolute())}{self.OS_SEPARATOR}'
        else :
            self.currentPath = f'{str(Path(__file__).parent.absolute())}{self.OS_SEPARATOR}'
        self.localPath = str(Path.home())
        if not self.localPath[-1] == str(self.OS_SEPARATOR) :
            self.localPath = f'{self.localPath}{self.OS_SEPARATOR}'

        self.baseApiPath = Globals.BASE_API_PATH
        self.apiPath = self.currentPath.split(self.baseApiPath)[0]

        lastLocalPathPackage = self.localPath.split(self.OS_SEPARATOR)[-2]
        firstBaseApiPath = self.baseApiPath.split(self.OS_SEPARATOR)[0]
        lastLocalPathPackageNotFound = True
        self.apiPackage = c.NOTHING
        for currentPackage in self.currentPath.split(self.OS_SEPARATOR) :
            if lastLocalPathPackageNotFound :
                if currentPackage == lastLocalPathPackage :
                    lastLocalPathPackageNotFound = False
            elif not currentPackage or currentPackage == firstBaseApiPath :
                break
            else :
                self.apiPackage = currentPackage

        if self.apiPackage != c.NOTHING :
            if len(self.currentPath.split(self.localPath)[1].split(self.apiPackage)) > 1:
                self.apisRoot = self.currentPath.split(self.localPath)[1].split(self.apiPackage)[0]
            self.apisPath = f'{self.currentPath.split(self.apiPackage)[0]}'
        else :
            self.apisRoot = c.NOTHING
            self.apisPath = c.NOTHING

    def getApiPath(self,apiPackageName):
        if not apiPackageName == c.NOTHING :
             return f'{self.localPath}{self.apisRoot}{apiPackageName}{self.OS_SEPARATOR}'###-'{self.baseApiPath}'
        if self.apisPath :
            return self.apisPath
        if self.localPath :
            return self.localPath
        return f'{self.OS_SEPARATOR}'

    def update(self) :
        self.updateDependencies()
        self.makeApiAvaliable(self.apiPackage)
        self.makeApisAvaliable(self.apisPath)
        self.spotRootPath(self.localPath)

    def makeApiAvaliable(self,apiPackageName) :
        self.apiTree = {}
        try :
            apiPath = self.getApiPath(apiPackageName)
            self.apiTree[apiPackageName] = self.makePathTreeVisible(self.getApiPath(apiPackageName))
        except Exception as exception :
            self.error(self.__class__,f'Not possible to make {apiPackageName} api avaliable',exception)
        if self.debugStatus :
            self.printTree(self.apiTree,'Api tree')

    def makeApisAvaliable(self,apisPath):
        if self.globalsEverything :
            try :
                apiPackageList = os.listdir(apisPath)
                for apiPackage in apiPackageList :
                    if not apiPackage in list(self.apiTree.keys()) :
                        self.apiTree[apiPackage] = self.makePathTreeVisible(f'{apisPath}{apiPackage}')
                if self.debugStatus :
                    self.printTree(self.apiTree,f'{c.DEBUG}Api tree (globalsEverithing is active)')
            except Exception as exception :
                self.error(self.__class__,f'Not possible to run makeApisAvaliable({apisPath}) rotine',exception)

    def spotRootPath(self,rootPath) :
        if self.printRootPathStatus :
            try :
                apiPackageList = os.listdir(rootPath)
                for apiPackage in apiPackageList :
                    self.rootPathTree[apiPackage] = self.addNode(f'{rootPath}{apiPackage}')
                if self.debugStatus :
                    self.printTree(self.rootPathTree,f'{c.DEBUG}Root tree (printRootPathStatus is active)')
            except Exception as exception :
                self.error(self.__class__,f'Not possible to run spotRootPath({rootPath}) rotine',exception)

    def giveLocalVisibilityToFrameworkApis(self,apiPackageNameList):
        if apiPackageNameList :
            localPackageNameList = os.listdir(self.apisPath)
            for packageName in localPackageNameList :
                if packageName not in self.apiTree.keys() and packageName in apiPackageNameList :
                    packagePath = f'{self.apisPath}{packageName}'
                    try :
                        self.apiTree[packageName] = self.makePathTreeVisible(packagePath)
                    except :
                        self.apiTree[packageName] = c.NOTHING
            if self.debugStatus :
                self.printTree(self.apiTree,f'{c.DEBUG}Api tree')

    def makePathTreeVisible(self,path):
        node = {}
        nodeSons = os.listdir(path)
        for nodeSon in nodeSons :
            if self.nodeIsValid(nodeSon) :
                nodeSonPath = f'{path}{self.OS_SEPARATOR}{nodeSon}'
                try :
                    node[nodeSon] = self.makePathTreeVisible(nodeSonPath)
                except :
                    node[nodeSon] = c.NOTHING
        sys.path.append(path)
        return node

    def addNode(self,nodePath):
        node = {}
        try :
            nodeSons = os.listdir(nodePath)
            for nodeSon in nodeSons :
                nodeSonPath = f'{nodePath}{self.OS_SEPARATOR}{nodeSon}'
                try :
                    node[nodeSon] = self.addNode(nodeSonPath)
                except :
                    node[nodeSon] = c.NOTHING
        except Exception as exception :
            self.error(self.__class__,f'Not possible to run addNode({nodePath}) rotine',exception)
        return node

    def nodeIsValid(self,node):
        return self.nodeIsValidByFilter(node) and (node not in self.nodeIgnoreList)

    def nodeIsValidByFilter(self,node):
        for charactere in self.charactereFilterList :
            if not len(node.split(charactere)) == 1 :
                return False
        return True

    def getPathTreeFromPath(self,path):
        node = {}
        nodeSons = os.listdir(path)
        for nodeSon in nodeSons :
            if self.nodeIsValid(nodeSon) :
                nodeSonPath = f'{path}{self.OS_SEPARATOR}{nodeSon}'
                try :
                    node[nodeSon] = self.getPathTreeFromPath(nodeSonPath)
                except : pass
        return node

    def lineAproved(self,settingLine) :
        approved = True
        if c.NEW_LINE == settingLine  :
            approved = False
        if c.HASH_TAG in settingLine :
            filteredSettingLine = self.filterString(settingLine)
            if None == filteredSettingLine or c.NOTHING == filteredSettingLine or c.NEW_LINE == filteredSettingLine :
                approved = False
        return approved

    def overrideApiTree(self,apiName,package=None):
        if package :
            actualPackage = package + self.OS_SEPARATOR
        else :
            actualPackage = apiName + self.OS_SEPARATOR
        self.apiName = apiName
        self.apiPackage = package
        self.apiPath = f'{self.apisPath}{actualPackage}'
        settingFilePath = f'{self.apiPath}{Globals.API_BACK_SLASH}{Globals.RESOURCE_BACK_SLASH}{self.settingsFileName}.{Globals.EXTENSION}'
        self.settingTree = self.getSettingTree(settingFilePath=settingFilePath,settingTree=self.settingTree)


    def getSettingTree(self,settingFilePath=None,settingTree=None) :
        if not settingFilePath :
            settingFilePath = f'{self.apiPath}{Globals.API_BACK_SLASH}{Globals.RESOURCE_BACK_SLASH}{self.settingsFileName}.{Globals.EXTENSION}'
        return SettingHelper.getSettingTree(settingFilePath)

    def addTree(self,settingFilePath):
        newSetting = self.getSettingTree(settingFilePath=settingFilePath)
        for settingKey,settingValue in newSetting.items() :
            self.settingTree[settingKey] = settingValue

    def concatenateTree(self,settingFilePath,tree):
        newSetting = self.getSettingTree(settingFilePath=settingFilePath)
        for settingKey in newSetting :
            tree[settingKey] = newSetting[settingKey]

    def getApiSetting(self,nodeKey):
        return self.getSetting(nodeKey)

    def getSetting(self,nodeKey,settingTree=None) :
        if not settingTree :
            settingTree = self.settingTree
        return SettingHelper.getSetting(nodeKey,self.settingTree)

    def accessTree(self,nodeKey,tree) :
        return SettingHelper.getSetting(nodeKey,tree)

    def printTree(self,tree,name,depth=0):
        SettingHelper.printSettings(tree,name)

    def updateDependencies(self):
        try :
            if self.updateDependencyStatus :
                moduleList = self.getSetting(AttributeKey.DEPENDENCY_LIST_WEB)
                localPackageNameList = self.getSetting(AttributeKey.DEPENDENCY_LIST_LOCAL)
                if moduleList or localPackageNameList :
                    self.runUpdateCommand(Globals.UPDATE_PIP_INSTALL)
                if moduleList :
                    for module in moduleList :
                        command = f'{Globals.PIP_INSTALL} {module}'
                        self.runUpdateCommand(command)
                if localPackageNameList :
                    for localPackageName in localPackageNameList :
                        localPackagePath = f'"{self.apiPath}{Globals.API_BACK_SLASH}{Globals.RESOURCE_BACK_SLASH}{Globals.DEPENDENCY_BACK_SLASH}{localPackageName}"'
                        command = f'{Globals.PIP_INSTALL} {localPackagePath}'
                        self.runUpdateCommand(command)
        except Exception as exception :
            self.error(self.__class__,'Not possible to update dependencies',exception)

    def runUpdateCommand(self,command):
        commonExceptionMessage = 'Not possible to update dependencies'
        LOG_FIRST_TRY =     '[FIRST_TRY ]'
        LOG_SECOND_TRY =    '[SECOND_TRY]'
        LOG_COMMAND = f'command'
        LOG_RESPONSE = f'response'
        LOG_SUCCESS = 'SUCCESS'
        LOG_FAIL = 'FAIL'
        KW_DIDNT_RUN = 'DIDNT_RUN'
        def getCommandLog(tryOrder,command):
            return f'{tryOrder}{c.SPACE}{LOG_COMMAND}{c.COLON_SPACE}{command}'
        def getResponseLog(tryOrder,command,response):
            logResponse = f'{tryOrder}{c.SPACE}{LOG_COMMAND}{c.COLON_SPACE}{command}'
            logResponse = f'{logResponse}{c.SPACE_DASH_SPACE}{LOG_RESPONSE}{c.COLON_SPACE}'
            if 1 == response :
                return f'{logResponse}{LOG_FAIL}'
            elif 0 == response :
                return f'{logResponse}{LOG_SUCCESS}'
            else :
                return f'{logResponse}{response}'
        commandFirstTry = command.replace(self.TOKEN_PIP_USER,self.KW_SPACE_PIP_USER)
        self.debug(getCommandLog(LOG_FIRST_TRY,commandFirstTry))
        responseFirstTry = KW_DIDNT_RUN
        try :
            responseFirstTry = subprocess.Popen(commandFirstTry).wait()
            self.debug(getResponseLog(LOG_FIRST_TRY,commandFirstTry,responseFirstTry))
        except Exception as exceptionFirstTry :
            self.error(self.__class__,f'{commonExceptionMessage}',exceptionFirstTry)
        if KW_DIDNT_RUN == responseFirstTry or 1 == responseFirstTry :
            commandSecondTry = command.replace(self.TOKEN_PIP_USER,c.NOTHING)
            self.debug(getCommandLog(LOG_SECOND_TRY,commandSecondTry))
            responseSecondTry = KW_DIDNT_RUN
            try :
                responseSecondTry = subprocess.Popen(commandSecondTry).wait()
                self.debug(getResponseLog(LOG_SECOND_TRY,commandSecondTry,responseSecondTry))
            except Exception as exceptionSecondTry :
                self.error(self.__class__,f'{commonExceptionMessage}',exceptionSecondTry)
            if KW_DIDNT_RUN == responseFirstTry and KW_DIDNT_RUN == responseSecondTry :
                log.error(self.__class__,f'Not possible to run {commandFirstTry}',Exception(f'Both attempt failed'))

    def getApiName(self):
        try :
            return self.getSetting(AttributeKey.API_NAME)
        except Exception as exception :
            self.failure(self.__class__,'Not possible to get api name', exception)

    def getExtension(self):
        extension = Globals.EXTENSION
        try :
            extension = self.getSetting(AttributeKey.API_EXTENSION)
        except Exception as exception :
            self.failure(self.__class__,'Not possible to get api extenion. Returning default estension', exception)
        return extension

    def getSettingFromSettingFilePathAndKeyPair(self,path,settingKey) :
        self.debug(f'''Getting {settingKey} from {path}''')
        with open(path,c.READ,encoding=c.ENCODING) as settingsFile :
            allSettingLines = settingsFile.readlines()
        for line, settingLine in enumerate(allSettingLines) :
            depth = self.getDepth(settingLine)
            setingKeyLine = self.getAttributeKey(settingLine)
            if settingKey == setingKeyLine :
                settingValue = self.getAttibuteValue(settingLine)
                self.debug(f'''{c.TAB}key : value --> {settingKey} : {settingValue}''')
                return settingValue

    def getStaticPackagePath(self) :
        staticPackageList = site.getsitepackages()
        self.debug(f'Static packages list: {StringHelper.prettyJson(staticPackageList)}. Picking the first one')
        staticPackage = str(staticPackageList[0])
        staticPackage = staticPackage.replace(f'{c.BACK_SLASH}{c.BACK_SLASH}',Globals.OS_SEPARATOR)
        staticPackage = staticPackage.replace(c.BACK_SLASH,Globals.OS_SEPARATOR)
        staticPackage = staticPackage.replace(f'{c.SLASH}{c.SLASH}',Globals.OS_SEPARATOR)
        staticPackage = staticPackage.replace(c.SLASH,Globals.OS_SEPARATOR)
        if staticPackage[-1] == str(Globals.OS_SEPARATOR) :
            staticPackage = staticPackage[:-1]
        herokuPythonLibPath = Globals.HEROKU_PYTHON.replace(Globals.TOKEN_PYTHON_VERSION, str(self.getSetting(AttributeKey.PYTHON_VERSION)))
        if staticPackage.endswith(herokuPythonLibPath) :
            staticPackage = staticPackage.replace(herokuPythonLibPath,c.NOTHING)
        staticPackage = f'{staticPackage}{Globals.STATIC_PACKAGE_PATH}'
        self.debug(f'Static package: "{staticPackage}"')
        return staticPackage

    def searchTreeList(self,search,tree):
        return searchTreeList(search,tree)

    def getEncoding(self, encoding) :
        if encoding :
            return encoding
        else :
            return c.ENCODING

    def debug(self,message):
        if 'True' == self.debugStatus :
            log.debug(self.__class__,message)

    def warning(self,message):
        if 'True' == self.warningStatus :
            log.warning(self.__class__,message)

    def error(self,classRequest,message,exception):
        if 'True' == self.errorStatus :
            log.error(classRequest,message,exception)

    def success(self,classRequest,message):
        if 'True' == self.successStatus :
            log.success(classRequest,message)

    def failure(self,classRequest,message,exception):
        if 'True' == self.failureStatus :
            log.failure(classRequest,message,exception)

    def setting(self,classRequest,message):
        if 'True' == self.settingStatus :
            log.setting(classRequest,message)

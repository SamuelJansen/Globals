# Globals
This library allows global access to different python api classes and functions

# Simplest way to use it

- put all your git projects you wanna exchange classes between them in a single folder
```
C:\Users\my_user\path\path\path\all_my_git_projects
```

- on the directory you wanna launch the "main api" (the one that will consume other projects classes and funtions), 
you put the PathMannanger.py file following this path tree:
```
C:\Users\my_user\path\path\path\all_my_git_projects\my_launcher_api\api\src\domain\control\PathMannanger.py
```

- put the following code right on top of the __main__ class of your api
```
from api.src.domain.control import PathMannanger
PathMannanger.PathMannanger(mode = 'WRONG_WAY_TO_MAKE_IT_WORKS',printStatus = True)
```

- be happy


# Aboute the proper way to use this library
I'll be implementing more funcionalities in order to make it extendable and more compatible to python framewors in general.
If you want more information or just want to contribute a litle bit, please hit me up.

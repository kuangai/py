
import os
a=0
for (root, dirs, files) in os.walk(os.getcwd()+"/img"):
    print("root:" + root)
    print("dirs: " + str(dirs))
    print("files:" + str(files))
    a=a+1
    print("循环次数：",a)
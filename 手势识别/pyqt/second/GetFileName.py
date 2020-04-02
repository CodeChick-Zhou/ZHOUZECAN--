
path = []
stars = []
curstars = 0
curpathindex = 0


def GetFileName():
    index = 0
    file_name = 'backimage.txt'
    with open(file_name) as file_obj:
        for content in file_obj:
            if "curpathindex" in content:
                i = content.find(':')
                index = int(content[i+1:-1])
                break

    return index


def readfile():
    global path,stars,curstars,curpathindex

    file_name = 'backimage.txt'

    Firstflag = True
    path = []
    stars = []

    curstars = 0
    with open(file_name) as file_obj:
        for content in file_obj:
            if Firstflag:
                curstars = int(content[6:-1])
                Firstflag = False
            elif "curpathindex" in content:
                cur = content.find(':')
                curpathindex = int(content[cur+1:-1])
                print("content[cur+1:-1]",content[cur+1:-1])
            else:
                index = content.find(' ')
                path.append(content[6:index - 1])
                stars.append(content[index + 6:-1])

    print("self.curstars",curstars)
    print("self.path",path)
    print("self.stars",stars)

    # file_data = ""
    # with open(file_name) as file_obj:
    #     for content in file_obj:
    #         if self.path[0] in content:
    #             content = "path:\"../images/screen4\" stat:1\n"
    #         file_data += content
    #
    # with open(file_name, "w", encoding="utf-8") as f:
    #     f.write(file_data)
    # print(file_data)

def writefile():
    global path, stars, curstars, curpathindex
    file_name = 'backimage.txt'
    file_data = ""
    with open(file_name) as file_obj:
        for content in file_obj:
            if "curpathindex" in content:
                content = "curpathindex:"+str(curpathindex)+"\n"
            file_data += content

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(file_data)
    print(file_data)



def writefilestar():
    global path, stars, curstars, curpathindex
    file_name = 'backimage.txt'
    file_data = ""
    with open(file_name) as file_obj:
        for content in file_obj:
            if "stars" in content:
                content = "stars:"+str(curstars)+"\n"
            file_data += content

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(file_data)
    print(file_data)
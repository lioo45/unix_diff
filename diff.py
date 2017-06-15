import re

class DiffCommandsError(Exception):
    def __int__(self,cause):
        super().__init__(cause)


class DiffCommands(object):

    def __init__(self,path,commands='mark'):
        if not commands.__eq__('mark'):
            self.commands=commands
            return
        with open(path,'r') as f:
            self.commands=f.readlines()
        cause="Cannot possibly be the commands for the diff of two files"
        # use for logical error
        x = y = 0
        for one in self.commands:
            one=one[:-1]
            # lexical error
            r = re.match(r'^\d+(,\d+)?[dac]+\d+(,\d+)?$',one)
            if not r:
                raise DiffCommandsError(cause)

            #  syntax error
            #  the number of operands on the  right side of operator 'change' or 'add'
            #  is more than one.
            if one.__contains__("d"):
                if len(one.split('d')[1].split(','))>1:
                    raise DiffCommandsError(cause)
            if one.__contains__("a"):
                if len(one.split('a')[0].split(','))>1:
                    raise DiffCommandsError(cause)

            """
                logical error
                according diff format legal LCS
                baseIndex x=y=0
                let a<->b represent that originFile's a-th line equals newFile's b-th line
                f1,f2 op s1,s2  maybe f1=f2 or s1=s2
                1.op=delete, a=f2+1,b=y+1
                    test a-x>b-y and f1-1-x==s1-y
                    x=a,y=b
                2.op=add, a=f1+1,b=s2+1
                    test a-x<b-y and f1+1-x==s1-y
                    x=a y=b
                3.op=change, a=f2+1,b=s2+1
                    test (a-x>1 and b-y>1) and f1-x==s1-y
                    x=a y=b
            """
            op=re.findall(r'[dac]',one)[0]
            params = one.split(op)[0].split(',')


            if len(params) > 1:
                f1, f2 = int(params[0]), int(params[1])
            else:
                f1 = f2 = int(params[0])

            params = one.split(op)[1].split(',')
            if len(params) > 1:
                s1, s2 = int(params[0]), int(params[1])
            else:
                s1 = s2 = int(params[0])

            if op=='d':
                if f2+1-x<=1 or f1-1-x!=s1-y:
                    raise DiffCommandsError(cause)
                x=f2+1
                y=s1+1

            elif op=='a':
                if f1+1-x>=s2+1 or f1+1-x!=s1-y:
                    raise DiffCommandsError(cause)
                x=f1+1
                y=s2+1

            elif op=='c':
                if not (f2+1-x>1 and s2+1-y>1) or f1-x!=s1-y:
                    raise DiffCommandsError(cause)
                x=f2+1
                y=s2+1

    def __str__(self):
        return "".join(self.commands)



class OriginalNewFiles(object):


    # 大致步骤:
    def __init__(self,path1,path2):
        # parse files to form of string array.
        with open(path1,'r') as f1:
            self.originFileStr=f1.readlines()
            self.originFileStr.insert(0,"")
        with open(path2, 'r') as f2:
            self.newFileStr = f2.readlines()
            self.newFileStr.insert(0, "")

        self.LCSs=[]
        self.lenOfMaxLCS=0
        self.diffs=[]

        self.getAllLCS()
        self.getDiffs()

        self.diffsContent=[]
        # self.generateDiffContents()


    """
        use DP to get all the longest common subsequences
        the return is a list of LCS formed of following:
            numLineOfOriginFile,numLineOfNewFile
            for example:
                2,3
        represent that  the second line's content of originFile equals
        the third line's content of newFile
    """
    def getAllLCS(self):
        # init result set
        # don't calculate repeatedly
        if len(self.LCSs)<=0:
            dp=[]
            for  i in range(len(self.originFileStr)):
                dp.append([])
                for j in range(len(self.newFileStr)):
                    # dp[i][j]=0
                    dp[i].append(0)
            for i in range(1,len(dp)):
                for j in range(1,len(dp[0])):
                    if self.originFileStr[i]==self.newFileStr[j]:
                        dp[i][j]=dp[i-1][j-1]+1
                    else:
                        dp[i][j]=max(dp[i-1][j],dp[i][j-1])

            self.lenOfMaxLCS=dp[len(dp)-1][len(dp[0])-1]

            # generate LCSs
            cache=[]
            for i in range(len(dp)):
                cache.append([])
                for j in range(len(dp[0])):
                    cache[i].append(False)

            self.LCSs=self.generateLCSs(dp,len(dp)-1,len(dp[0])-1,cache)

        return self.LCSs


    # according the result of the first DP, using DP to generate LCSs
    def generateLCSs(self,dp,x,y,cache):
        if x <= 0 or y <= 0:
            return []
        result=[]
        if self.originFileStr[x]==self.newFileStr[y]:
            # select [x-1][y-1]
            r=self.generateLCSs(dp,x-1,y-1,cache) if not cache[x-1][y-1] else cache[x-1][y-1]
            result.extend([one.copy() for one in r])
            s=str(x)+","+str(y)
            for one in result:
                one.append(s)
            if len(result)<=0:
                result.append([s])
            # select [x-1][y]
            if dp[x][y]==dp[x-1][y]:
                r=self.generateLCSs(dp,x-1,y,cache) if not cache[x-1][y] else cache[x-1][y]
                result.extend([one.copy() for one in r if one not in result])
            # select [x][y-1]
            if dp[x][y]==dp[x][y-1]:
                r=self.generateLCSs(dp,x,y-1,cache) if not cache[x][y-1] else cache[x][y-1]
                result.extend([one.copy() for one in r if one not in result])


        else:
            if dp[x - 1][y] == dp[x][y]:
                r=self.generateLCSs(dp,x-1,y,cache) if not cache[x-1][y] else cache[x-1][y]
                result.extend([one.copy() for one in r if one not in result])

            if dp[x][y-1]==dp[x][y]:
                r=self.generateLCSs(dp,x,y-1,cache) if not cache[x][y-1] else cache[x][y-1]
                result.extend([one.copy() for one in r if one not in result])

        cache[x][y]=result.copy()
        return result

    """
        according LCSs,
        for each LCS in LCSs format a diif.

        the  originRowIndex = newFileRowIndex = 0.
        originRowIndex mean that now the program is processing which line of originFile


        the main of core is following four status:
            1. LCSIndexOfOrigin-originRowIndex>1 and LCSIndexOfNewFile-newFileRowIndex>1
                the status is change
            2.LCSIndexOfOrigin-originRowIndex<LCSIndexOfNewFile-newFileRowIndex
                the status is add
            3.LCSIndexOfOrigin-originRowIndex > LCSIndexOfNewFile-newFileRowIndex
                the status is delete
            4.LCSIndexOfOrigin-originRowIndex==1 and LCSIndexOfNewFile-newFileRowIndex==1
                the status is ignore
            implements in the method getOneRecord()
    """
    def getDiffs(self):
        #don't calculate repeatedly
        if len(self.diffs)<=0:
            for LCS in self.LCSs:
                diff=[]
                originRowIndex = newFileRowIndex = 0
                buff=list.copy(LCS)
                buff.append(str(len(self.originFileStr)-1)+","+str(len(self.newFileStr)-1))
                for one in buff:
                    indexs=one.split(',')
                    LCSIndexOfOrigin,LCSIndexOfNewFile=int(indexs[0]),int(indexs[1])
                    record=self.getOneRecord(originRowIndex,newFileRowIndex,
                            LCSIndexOfOrigin,LCSIndexOfNewFile)
                    if len(record)>0:
                        diff.append(record+"\n")
                    originRowIndex=LCSIndexOfOrigin
                    newFileRowIndex=LCSIndexOfNewFile

                self.diffs.append(diff)

        return self.diffs

    def getOneRecord(self,originRowIndex,newFileRowIndex,LCSIndexOfOrigin,LCSIndexOfNewFile):
        result=''
        # change
        if LCSIndexOfOrigin-originRowIndex>1 and LCSIndexOfNewFile-newFileRowIndex>1:
            status='c'
            firstNum=originRowIndex+1
            str1=str(firstNum)
            if firstNum<LCSIndexOfOrigin-1:
                str1+=","+str(LCSIndexOfOrigin-1)
            secondNum=newFileRowIndex+1
            str2=str(secondNum)
            if secondNum<LCSIndexOfNewFile-1:
                str2+=","+str(LCSIndexOfNewFile-1)
            result=str1+status+str2

        # add
        elif LCSIndexOfOrigin-originRowIndex< LCSIndexOfNewFile-newFileRowIndex:
            status = 'a'
            str1 = str(originRowIndex)
            secondNum = newFileRowIndex + 1
            str2 = str(secondNum)
            if secondNum < LCSIndexOfNewFile-1:
                str2 += "," + str(LCSIndexOfNewFile - 1)
            result=str1 + status + str2
        # delete
        elif LCSIndexOfOrigin-originRowIndex > LCSIndexOfNewFile-newFileRowIndex:
            status = 'd'
            firstNum = originRowIndex + 1
            str1 = str(firstNum)
            if firstNum < LCSIndexOfOrigin-1:
                str1 += "," + str(LCSIndexOfOrigin - 1)
            str2 = str(newFileRowIndex)
            result=str1 + status + str2
        #    ignore
        elif LCSIndexOfOrigin-originRowIndex==1 and LCSIndexOfNewFile-newFileRowIndex==1:
            return result
        return result


    def generateDiffContents(self,diff_):
    # def generateDiffContents(self,):
        op=""
        f1=f2=s1=s2=0
        # for diff in self.diffs:
        content=[]
        diff_=diff_.commands
        # for oneRecord in diff:
        for oneRecord in diff_:
            oneRecord=oneRecord[:-1]
            for c in oneRecord:
                if c.isalpha():
                    op=c
                    break

            num=oneRecord.split(op)
            n = num[0].split(",")
            if len(n)<=1:
                f1=f2=int(num[0])
            else:
                f1=int(n[0])
                f2=int(n[1])
            n = num[1].split(",")
            if len(n) <= 1:
                s1 = s2 = int(num[1])
            else:
                s1=int(n[0])
                s2 = int(n[1])

            str = []
            if op == 'c':
                for i in range(f1, f2 + 1):
                    str.append("< " + self.originFileStr[i])
                str.append("---\n")
                for i in range(s1, s2 + 1):
                    str.append("> " + self.newFileStr[i])
            elif op=='a':
                for i in range(s1,s2+1):
                    str.append("> "+self.newFileStr[i])
            elif op=='d':
                for i in range(f1,f2+1):
                    str.append("< "+self.originFileStr[i])
            content.append("".join(str))

        # self.diffsContent.append(content)
        return content

    def output_diff(self,diff_):
        content=self.generateDiffContents(diff_)

        for i,j in zip(diff_.commands,content):
            # for i,j in zip(diff,content):
            print(i,end='')
            print(j,end="")

    def is_a_possible_diff(self,diff_):
        return  diff_.commands in self.diffs

    def output_LCS(self,diff_,fileStr,pos):
        num = 1
        for diff, LCS in zip(self.diffs, self.LCSs):
            if diff_.commands == diff:
                for one in LCS:
                    index = int(one.split(',')[pos])
                    if num != index:
                        print("...")
                    print(fileStr[index], end='')
                    num = index + 1
                if int(LCS[-1].split(",")[pos])!=len(fileStr)-1:
                    print("...")
                break

    def output_unmodified_from_original(self,diff_):
        self.output_LCS(diff_,self.originFileStr,0)

    def output_unmodified_from_new(self,diff_):
        self.output_LCS(diff_,self.newFileStr,1)

    def get_all_diff_commands(self):
        result=["".join(diff) for diff in self.diffs]
        return [DiffCommands("",commands=one) for one in result ]

    # def output_diff(self):
    #     for diff,content in zip(self.diffs,self.diffsContent):
    #         for i,j in zip(diff,content):
    #             print(i,end='')
    #             print(j,end="")
    #         print("-------我是分割线--------")






if __name__ == '__main__':
    # for test
    path1="/Users/pro/Downloads/Assignment3/file_1_1.txt"
    path2="/Users/pro/Downloads/Assignment3/file_1_2.txt"

    path1 = "/Users/pro/Downloads/Assignment3/file_2_1.txt"
    path2 = "/Users/pro/Downloads/Assignment3/file_2_2.txt"

    path1="/Users/pro/Downloads/Assignment3/file_3_1.txt"
    path2="/Users/pro/Downloads/Assignment3/file_3_2.txt"

    o=OriginalNewFiles(path1,path2)

    diff_1Path="/Users/pro/Downloads/Assignment3/diff_1.txt"
    diff_2Path="/Users/pro/Downloads/Assignment3/diff_2.txt"
    diff_3Path="/Users/pro/Downloads/Assignment3/diff_3.txt"

    diff_1=DiffCommands(diff_1Path)
    deff_2=DiffCommands(diff_2Path)
    deff_3=DiffCommands(diff_3Path)

    # print(o.is_a_possible_diff(diff_1))
    # o.output_diff(diff_1)
    # o.output_unmodified_from_original(diff_1)

    # o.output_unmodified_from_original(deff_2)
    o.output_unmodified_from_original(deff_3)
    print("-----分割线-----")
    o.output_unmodified_from_new(deff_3)
    print("-----分割线-----")
    diffs=o.get_all_diff_commands()
    for one in diffs:
        print(one)
    # wrongPath='/Users/pro/Downloads/Assignment3/wrong_1.txt'
    # d=DiffCommands(wrongPath)

    # wrongPath='/Users/pro/Downloads/Assignment3/wrong_2.txt'
    # d=DiffCommands(wrongPath)

    # wrongPath='/Users/pro/Downloads/Assignment3/wrong_3.txt'
    # d=DiffCommands(wrongPath)

    # wrongPath='/Users/pro/Downloads/Assignment3/wrong_4.txt'
    # d=DiffCommands(wrongPath)

    # wrongPath='/Users/pro/Downloads/Assignment3/wrong_5.txt'
    # d=DiffCommands(wrongPath)


    # wrongPath='/Users/pro/Downloads/Assignment3/wrong_6.txt'
    # d=DiffCommands(wrongPath)

    # wrongPath='/Users/pro/Downloads/Assignment3/wrong_7.txt'
    # d=DiffCommands(wrongPath)




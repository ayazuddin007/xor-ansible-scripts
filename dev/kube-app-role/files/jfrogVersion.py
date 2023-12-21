from artifactory import ArtifactoryPath
import requests
import sys

# accessing the Jfrog repo
def accessRepo():
    aql = ArtifactoryPath("https://xoriant.jfrog.io/artifactory",
                           auth=('xoriant-jenkins', 'Admin@123'))

    return aql

def isSmallerThanEqualTo(range1,range2):

    if range1[0] > range2[0]:
        return False
    else:
        if range1[1] > range2[1]:
            return False
        else:
            return True



def pullDockerUrl():


    aql = accessRepo()
    repo = aql.find_repository("xoriant-maven")
    nameList = []

    repoNameAndgroupId = sys.argv[1]
    repoNameAndgroupId = repoNameAndgroupId.split(":")


    repoName = repoNameAndgroupId[1]
    repoName = repoName.lstrip()
    repoName = repoName.rstrip()


    groupId = repoNameAndgroupId[0].replace(".","/")
    groupId = groupId.lstrip()
    groupId = groupId.rstrip()

    # print(repoName,groupId)


    # link = "xoriant-maven.eu-central-1.artifactory.wexapps.com"
    link = "xoriant-maven/"+groupId+"/"+repoName


    tempRanges = sys.argv[2]
    tempRanges = tempRanges.split(",")
    #print(tempRanges)


    for r in range(0,len(tempRanges)):
        tempRanges[r] = tempRanges[r].lstrip()
        tempRanges[r] = tempRanges[r].rstrip()

    repoPath = "https://xoriant.jfrog.io/artifactory/xoriant-maven/"+groupId+"/"+"repoName"
    path = groupId+"/"+repoName
    aqlpath = ArtifactoryPath(repoPath,
                                  auth=('xoriant-jenkins', 'Admin@123'))

    if len(tempRanges) == 1:
        flag=False
        path = groupId+"/"+repoName
        version = tempRanges[0]

        dlPath = path
        dlArtifact = aqlpath.aql("items.find", {"type": "folder","path":path}, ".sort", {"$desc": ["created"]})
        # print(version)
        # print(dlArtifact)

        for a in dlArtifact:
            if a["name"] == version:
                if len(dlArtifact)!=0:
                    dlLink = link+"/"+version+"/"+repoName+"-"+version+"-kubernetes-manifests.zip"
                    print(dlLink)
                    flag = True

        if flag != True:
            print(flag)


    else:

        try:
            artifacts = aqlpath.aql("items.find", {"type": "folder","path":path})

            artifacts =  [ a for a in artifacts if "SNAPSHOT" not in a["name"] ]
            artifacts =  [ a for a in artifacts if "." in a["name"] ]
            artifacts =  [ a for a in artifacts if not(a["name"].lower().islower()) ]
            

            range1= tempRanges[0].split(".")
            range2= tempRanges[1].split(".")

            range1 = [int(x) for x in range1]
            range2 = [int(x) for x in range2]

            # print(range1,range2)


            # print(artifacts)

            for a in artifacts:
                a["versionNum"] = a["name"].split(".")
                a["versionNum"] = [int(x) for x in a["versionNum"]]


                nameList.append(a["name"])

            artifacts = sorted(artifacts, key = lambda i: (i['versionNum'][0],i['versionNum'][1]),reverse=True)

            artifacts = [a for a in artifacts if isSmallerThanEqualTo(range1,a["versionNum"]) and isSmallerThanEqualTo(a["versionNum"],range2)]

            if len(artifacts)==0:
                print("False")
                return
            # for a in artifacts:
            #     print(a)



            # currBuildVersion= artifacts[0]
        except IndexError:
            print("False")
            return

        greatestInd = 0

        for i in range(0,len(artifacts)-1):
            if isSmallerThanEqualTo(artifacts[i]["versionNum"],artifacts[i+1]["versionNum"]):

                greatestInd = i+1
                # print(artifacts[i]["versionNum"],artifacts[i+1]["versionNum"],"G",artifacts[greatestInd]["versionNum"])


        dlLink = link+"/"+artifacts[0]["name"]+"/"+repoName+"-"+artifacts[0]["name"]+"-kubernetes-manifests.zip"
        print(dlLink)







if __name__ == "__main__":
    pullDockerUrl()

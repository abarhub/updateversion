import os
import subprocess
import sys

SNAPSHOT = '-SNAPSHOT'


def getVersion(path):
    res = subprocess.run(["mvn", "help:evaluate", "-Dexpression=project.version", "-q", "-DforceStdout", "-f",
                          path + "/pom.xml"], stdout=subprocess.PIPE, text=True, shell=True)
    if res.returncode == 0:
        return res.stdout
    else:
        raise Exception("Erreur pour la commande")


def updateVersion(path, version):
    res = subprocess.run(["mvn", "versions:set", "-DnewVersion=" + version, "-DgenerateBackupPoms=false", "-f",
                          path + "/pom.xml"], stdout=subprocess.PIPE, text=True, shell=True)
    if res.returncode == 0:
        return res.stdout
    else:
        print("code retour:" + str(res.returncode))
        print("stdout:" + str(res.stdout))
        print("stderr:" + str(res.stderr))
        raise Exception("Erreur pour la commande")


def check_int(s):
    if s[0] in ('-', '+'):
        return False
    return s.isdigit()


def choixVersion(versionActuelle):
    if versionActuelle.endswith(SNAPSHOT):
        version = versionActuelle[0:len(versionActuelle) - len(SNAPSHOT)]
    else:
        version = versionActuelle
    tmp = version.split('.')
    tab = []
    for i in range(len(tmp)):
        val = tmp[i]
        if check_int(val):
            n = int(val)
            n = n + 1
            res = ''
            for j in range(len(tmp)):
                if j > 0:
                    res += '.'
                if j < i:
                    res += tmp[j]
                elif j == i:
                    res += str(n)
                else:
                    res += '0'
            if len(res) > 0:
                res += SNAPSHOT
            tab.append(res)

    if len(tab) > 0:
        print("selectionnez la version :")
        i = 1
        for s in tab:
            print(str(i) + ") version=" + s)
            i += 1
        choixAutre = i
        print(str(i) + ") autre")
        print("0) quitter")

        for line in sys.stdin:
            s = line.rstrip()
            if '0' == s:
                return ''
            if check_int(s):
                n2 = int(s)
                if n2 > 0 and n2 <= len(tab):
                    return tab[n2 - 1]
                elif n2 == choixAutre:
                    nouvelleVersion = input("Saisissez la version:")
                    if nouvelleVersion != '':
                        nouvelleVersion = nouvelleVersion.strip()
                    if nouvelleVersion != '':
                        return nouvelleVersion
    else:
        return ''


def updateMaven(path):
    if (os.path.isfile(path + "/pom.xml")):
        print("chemin=" + path)
        version = getVersion(path)
        print('version actuelle=' + version)
        versionModifiee = choixVersion(version)
        if len(versionModifiee) > 0:
            print('version modifiee=' + versionModifiee)
            updateVersion(path, versionModifiee)
    else:
        raise Exception('Le répertoire \'' + path + '\' n\'est pas un répertoir maven')


# main
if __name__ == '__main__':

    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = os.getcwd()
    updateMaven(path)

import lxml.etree as ET
import git
import xlsxwriter
import datetime;

ct = datetime.datetime.now()
created_date_time=ct.strftime("%m_%d_%Y_%H_%M_%S")
workbook = xlsxwriter.Workbook(f"Telephony_Apps_Java_Version_and_Packaging_Type{created_date_time}.xlsx")
worksheet = workbook.add_worksheet()
index = 1
worksheet.write('A'+str(index), "Module Name")
worksheet.write('B'+str(index), "Java Version")
worksheet.write('C'+str(index), "Packaging Type")

username = "pillupriya"
password = "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"
gitUrls = ["helloWorld"]
for url in gitUrls:
 gitUrl = f"https://{username}:{password}@github.com/pillupriya/{url}.git"
 full_local_path = f"/Users/C21549/agnes/script/COX_Repo{created_date_time}/{url}/"
 repo = git.Repo.clone_from(gitUrl, full_local_path)
 # You need to check out the branch after creating it if you want to use it
 repo.git.checkout('python_script_test')
 # backup of master to new branch 
 repo.git.push('origin', '-u', 'python_script_test')
 xmlTree = ET.parse(f'{full_local_path}pom.xml')
 rootElement = xmlTree.getroot()
 index = index+1
 if rootElement.find("{http://maven.apache.org/POM/4.0.0}properties").find("{http://maven.apache.org/POM/4.0.0}java.version") != None:
     java_version = rootElement.find("{http://maven.apache.org/POM/4.0.0}properties").find(
         "{http://maven.apache.org/POM/4.0.0}java.version").text
     worksheet.write('B'+str(index), java_version)
 if rootElement.find("{http://maven.apache.org/POM/4.0.0}artifactId") != None:
     modulename = rootElement.find(
         "{http://maven.apache.org/POM/4.0.0}artifactId").text
     worksheet.write('A'+str(index), modulename)
 jar_or_war = "not given in pom"
 if rootElement.find("{http://maven.apache.org/POM/4.0.0}packaging") != None:
     jar_or_war = rootElement.find(
         "{http://maven.apache.org/POM/4.0.0}packaging").text
     worksheet.write('C'+str(index), jar_or_war)
 else:
     if rootElement.find("{http://maven.apache.org/POM/4.0.0}build") != None:
         list_plugins = rootElement.find("{http://maven.apache.org/POM/4.0.0}build").find("{http://maven.apache.org/POM/4.0.0}plugins").findall("{http://maven.apache.org/POM/4.0.0}plugin")
     list_artifactId=[]
     for plugin in list_plugins:
         list_artifactId.append(plugin.find("{http://maven.apache.org/POM/4.0.0}artifactId").text)
     if "maven-jar-plugin" in list_artifactId:
         jar_or_war="jar"
     if "maven-war-plugin" in list_artifactId:
         jar_or_war="war"
     worksheet.write('C'+str(index), jar_or_war)
 rootElement.find("{http://maven.apache.org/POM/4.0.0}parent").find("{http://maven.apache.org/POM/4.0.0}version").text = '2.4.5'
 xmlTree.write(f'{full_local_path}pom.xml',encoding='UTF-8',xml_declaration=True)
workbook.close()

import time
import datetime
import os, errno
import urllib.request

def getHtml(url):
     
     req = urllib.request.Request(url)
     try: 
          html = urllib.request.urlopen(req).read().decode('utf8')
     except urllib.error.URLError as e:
          html = ""
          
     return html
     
def getOpenPositions():
     
     html = getHtml('https://www.oculus.com/careers/')

     jobsInfo = html.split('_3cs-')

     jobs = []
     for jobInfo in jobsInfo:

          rawInfo = jobInfo.split('</a></div>')[0]
          if len(rawInfo) < 1500:
          
               job = []
               
               jobID = rawInfo.split('careers')[1].split('/')[1].split('<')[0].split('\\')[0]
               jobTitle = rawInfo.split('_3ct0')[1].split('>')[1].split('<')[0].split('\\')[0]  
               jobArea = rawInfo.split('_3ct1')[1].split('>')[1].split('<')[0].split('\\')[0]
               
               job.append(jobID)
               job.append(jobTitle)
               job.append(jobArea)
               
               added = 0
               for tempJob in jobs:
                    if tempJob[0] == jobID:
                         added = 1     
               if added == 0:
                    jobs.append(job)
                    
     return jobs
     
def updatePositions(newJobs):

     #Removes data file
     try:
          os.remove('jobs.csv')
     except OSError:
          pass

     with open('jobs.csv', 'a') as f:
          for job in newJobs:
               i = 0
               for jobInfo in job:
                    f.write(jobInfo) 
                    if i < len(job):
                         f.write(";")
                    i += 1
               f.write("\n")
               
def getSavedPositions():
               
     jobs = []
     with open('jobs.csv', 'r') as f:
     
          for line in f:
               
               job = []
               
               jobID = line.split(';')[0]
               jobTitle = line.split(';')[1]  
               jobArea = line.split(';')[2]
               
               job.append(jobID)
               job.append(jobTitle)
               job.append(jobArea)
               
               jobs.append(job)

     return jobs
     
def jobIdExist(jobs, jobID):

     exist = 0
     for job in jobs:
          if job[0] == jobID:
               exist = 1
               
     return exist 
     
def addDateToJob(jobs, jobID):

     now = datetime.datetime.now()
     date = now.strftime("%Y-%m-%d")
     
     for job in jobs:
          if job[0] == jobID:
               job.append(date)     
     
#-----Main code-----  
     
oldPositions = getSavedPositions()
currentPositions = getOpenPositions()

positionsRemoved = 0
for job in oldPositions:

     if not jobIdExist(currentPositions, job[0]):
     
          addDateToJob(oldPositions, job[0])
          positionsRemoved += 1
          
newPositions = 0
for job in currentPositions:

     if not jobIdExist(oldPositions, job[0]):
     
          oldPositions.append(job)
          newPositions += 1
          
updatePositions(oldPositions)

print("Positions removed:\t" + str(positionsRemoved))
print("Positions added:\t" + str(newPositions))
          

          

          
          

     
     














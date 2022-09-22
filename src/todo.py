class TodoList(object):
    def __init__(self):
        self.list = []

    def getList(self):
        return self.list

    def addTask(self,task):
        self.list.append(task)

    def deleteTask(self,tasknum):
        self.list.pop(tasknum)


class Task():
    def __init__(self, title, desc, deadline, status, importance):
        self.title = title
        self.desc = desc
        self.deadline = deadline
        self.status = status
        self.importance = importance

    def getTitle(self):
        return self.title

    def setTitle(self,title):
        self.title = title
    
    def getDesc(self):
        return self.desc

    def setDesc(self, desc):
        self.desc = desc
    
    def getDeadline(self):
        return self.deadline
    
    def setDeadline(self, deadline):
        self.deadline = deadline   
    
    def getStatus(self):
        return self.status
    
    def setStatus(self, status):
        self.status = status   
    
    def getImportance(self):
        return self.importance
    
    def setImportance(self, importance):
        self.importance = importance   
from pymongo import MongoClient

URI = "mongodb+srv://QuasarQueryDB131:2Qno28f782A37hyK@quasarquery.7p3b7.mongodb.net/?retryWrites=true&w=majority&appName=QuasarQuery"
Client = MongoClient(URI)
Database = Client["QuasarQuery"]
CollectionActivities = Database["Activities"]

class ActivityClass:
    
    def __init__(self, name: str, description: str, tags: list, level: int, questions: str):
        self.name = name
        self.description = description
        self.tags = tags
        self.level = level
        self.questions = questions
        
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "level": self.level,
            "questions": self.questions
        }

def CreateActivity(name: str, description: str, level: int, tags: list, questions: str):

    name_taken = CollectionActivities.find_one({'name': name})
    
    if not name_taken:
        CollectionActivities.insert_one(ActivityClass(name, description, tags, level, questions).to_dict())

def GetActivities(level: int, tags: list):
    level = int(level)
    regex_tags = [{"tags": {"$regex": f"^{tag}$", "$options": "i"}} for tag in tags]
    level_activities = CollectionActivities.find({
        "level": level,
        "$or": regex_tags
    })
    matching_activities = []
    for activity in level_activities:
        activity['_id'] = str(activity['_id'])
        matching_activities.append(activity)

    return matching_activities


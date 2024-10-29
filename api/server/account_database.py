from pymongo import MongoClient

URI = "mongodb+srv://QuasarQueryDB131:2Qno28f782A37hyK@quasarquery.7p3b7.mongodb.net/?retryWrites=true&w=majority&appName=QuasarQuery"
Client = MongoClient(URI)
Database = Client["QuasarQuery"]
CollectionAccounts = Database["Accounts"]

class AccountClass:
    
    def __init__(self, username: str, password: str, email: str, account_level: int, tags: list, subscription_level: int, organization: str):
        self.username = username
        self.password = password
        self.email = email
        self.account_level = account_level
        self.tags = tags
        self.subscription_level = subscription_level
        self.organization = organization
        
    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "account_level": self.account_level,
            "account_activities_tags": self.tags,
            "subscription_level": self.subscription_level,
            "organization": self.organization
        }

def CreateAccount(Account: object):
    
    NameTaken = CollectionAccounts.find_one({'username': Account.username})
    if Account and not NameTaken:
        CollectionAccounts.insert_one(Account.to_dict())
        return Account.username, 200
    else:
        return 400
    
def LoginToAccount(Email: str, Password: str):
    
    Account = CollectionAccounts.find_one({'email': Email})
    
    if Account and Account['password'] == Password:
        return Account['username'], 200
    else:
        return 400

def ValidateAccount(Username: str):
    
    Account = CollectionAccounts.find_one({'username': Username})
    
    if Account:
        return {
            'username': Account['username'],
            'account_level': Account['account_level'],
            'account_activities_tags': Account['account_activities_tags']
        }
    else:
        return 400

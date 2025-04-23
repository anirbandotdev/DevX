import aiofiles
import json

class Database:

    def __init__(self , FILE):
        self.data = []
        self.FILE  = FILE
        
    async def init(self):
        self.data = await self.read()
        
    async def write(self , data : list):
        async with aiofiles.open(self.FILE , mode="w") as f:
            json_str = json.dumps(data , indent=4)
            await f.write(json_str)
    
    async def read(self) -> list:
        try:
                
            async with aiofiles.open(self.FILE , mode='r') as f:
                contents = await f.read()
                return json.loads(contents)
        except:
            return []
        
class UserDatabase(Database):
    
    def __init__(self , FILE):
        super().__init__(FILE)
    
    async def create(self ,user_id):
        for user in self.data:
            if user_id == user["id"]:
                return False
        
        self.data.append({
            "id" : user_id,
            "exp" : 0,
            "lvl" : "0",
            "yesterday" : [],
            "today" : []
        })
        await self.write(self.data)
        return True

class ChallengeDatabase(Database):
    
    def __init__(self , FILE):
        super().__init__(FILE)
    
    async def init(self):
        self.data = await self.read()
        if not self.data:
            self.data.append({ "professional" : [] , "personal" : [] , "health" : [] })
            await self.write(self.data)

    async def create(self , category , challenge):
        
        if (self.data)[0]:
            if challenge in ((self.data)[0])[category]:
                return False
            ((self.data)[0])[category].append(challenge)
            await self.write(self.data)
            return True
    
    
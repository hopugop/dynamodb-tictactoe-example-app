# Copyright 2014. Amazon Web Services, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from boto.dynamodb2.table   import Table
from uuid                   import uuid4

class ConnectionManager:

    def __init__(self, mode=None, config=None, endpoint=None, port=None):
        self.db = None
        self.gamesTable = None
        
        if mode == "local":
            if config is not None:
                raise Exception('Cannot specify config when in local mode')
            if endpoint is None:
                endpoint = 'localhost'
            if port is None:
                port = 8000
            self.db = getDynamoDBConnection(endpoint=endpoint, port=port, local=True)
        elif mode == "service":
            self.db = getDynamoDBConnection(config=config, endpoint=endpoint)
        else:
            raise Exception("Invalid arguments, please refer to usage.");

        self.setupGamesTable()

    def setupGamesTable(self):
        try:
            self.gamesTable = Table("Games", connection=self.db)
        except Exception, e:
            raise e, "There was an issue trying to retrieve the Games table."

    def getGamesTable(self):
        if self.gamesTable == None:
            self.setupGamesTable()
        return self.gamesTable

    def createGamesTable(self):
        self.gamesTable = createGamesTable(self.db)

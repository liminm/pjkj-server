REST API
========

TOC:
- [Teams](#teams)
- [Players](#players)
- [Games](#games)
- [Events](#events)

## Allgemeine Statuscodes:

 Code				| Bedeutung
--------------------|------------------------------------------------------
 200 OK				| Default for GET
 201 Created		| Default for POST
 400 Bad request	| Syntax or format error
 401 Unauthorized	| Authorization header missing
 403 Forbidden		| Not allowed for given token's user
 404 Not found		| Resource does not exist
 409 Conflict		| Something doesn't fit (e.g. move on completed game)





## Teams

### Create Team
```javascript
POST /api/teams
{
  "name": "<string>",
  "isisName": "<string>",
  "type": "jumpSturdy" || "racingKings"
}

201 CREATED
{
  "id": "<string>",
  "token": "<string>"
}
```

### Log in Team
```javascript
GET /api/teamlogin
Authorization: Basic <teamToken>

200 OK
{
	"id": "<string teamID>",
	"valid": <boolean>
}
```

### List Teams
```javascript
GET /api/teams?count=<count>&start=<start>

200 OK
{
 "<teamID>": {
    "name": "<string>",
    "isisName": "<string>",
    "type": "jumpSturdy" || "racingKings"
  },
  ...
}
```

### Get Team
```javascript
GET /api/team/<teamID>

200 OK
{
  "name": "<string>",
  "isisName": "<string>",
  "type": "jumpSturdy" || "racingKings"
}
```








## Players
(AI or Human)

### Create Player
```javascript
POST /api/players
Authorization: Basic <teamToken>
{
  "name": "<string>"
}

201 CREATED
{
  "id": "<string>",
  "token": "<string>"
}
```

### Log in Player
```javascript
GET /api/playerlogin
Authorization: Basic <playerToken>

200 OK
{
	"id": "<string playerID>",
	"valid": <boolean>
}
```

### List Players
```javascript
GET /api/players?count=<count>&start=<start>

200 OK
{
  "<playerID>": {
    "name": "<string>",
    "team": "<string teamID>"
  },
  ...
}
```

### Get Player
```javascript
GET /api/player/<playerID>

200 OK
{
  "name": "<string>",
  "team": "<string teamID>"
}
```







## Games

### Create Game
```javascript
POST /api/games
{
  "name": "<string>",
  "type": "jumpSturdy" || "racingKings",
  "players": {
    "playerA": "<string playerID>",
    "playerB": "<string playerID>"
  },
  "settings": {
    "initialFEN": "<string fen>",
    "timeBudget": <int ms>,
    "timeout": <int ms>
  }
}

201 CREATED
{
  "id": "<string>"
}
```

### List Games
```javascript
GET /api/games?count=<count>&start=<start>&state=[planned|running|completed]

200 OK
{
  "<id>" {
    "name": "<string>",
    "type": "jumpSturdy" || "racingKings",
    "playerNames": {
      "playerNameA": "<string>",
      "playerNameB": "<string>"
    },
    "state": {
      "state": "planned" || "running" || "completed",
      "winner": "playerA" || "playerB" || "draw" || null
    }
  }
}
```

### Get Game
```javascript
GET /api/game/<gameID>

200 OK
{
  "name": "<string>",
  "type": "jumpSturdy" || "racingKings",
  "players": {
    "playerA": {
      "id": "<string playerID>",
      "name": "<string>"
    },
    "playerB": {
      "id": "<string playerID>",
      "name": "<string>"
    }
  },
  "settings": {
    "initialFEN": "<string fen>",
    "timeBudget": <int ms>,
    "timeout": <int ms>
  },
  "state": {
    "state": "planned" || "running" || "completed",
    "winner": "playerA" || "playerB" || "draw" || null,
    "fen": "<string>",
    "timeBudgets": {
      "playerA": <int ms>,
      "playerB": <int ms>
    }
  }
}
```








## Events

### Send Event
```javascript
POST /api/game/<gameId>/events
Authorization: Basic <playerToken>
{
  "type": "move" || "surrender",
  "details": {
    "move": "<string uci (a1b2; e7e8q; 0000)>"
  }
}

201 CREATED
{
  "valid": <boolean>,
  "reason": "<string>"
}
```

### Get past & new Events
[SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) format
```javascript
GET /api/game/<GameId>/events

200 OK
data: {
  "type": "move" || "gameEnd" || "timeout" || "timeBudget" || "serverMessage",
  "player": "playerA" || "playerB" || null,
  "timestamp": "<string iso utc>",
  "details": {
    "move": "<string uci (a1b2; e7e8q; 0000)>",
    "postFEN": "<string fen after move>",
    "time": <int ms>
  } || {
    "type": "win" || "surrender" || "draw" || "timeout" || "timeBudget" || "50move" || "repState",
    "winner": "playerA" || "playerB" || "draw"
  } || {
    "timeout": <int ms>
  } || {
    "timeBudget": <int ms>
  } || {
    "messageText": "<string>"
  }
}

data: ...
```
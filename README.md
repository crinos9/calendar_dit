Martin Pinka, D13126650

URL: missing

Usage:
  creating calendar: 
    URL: http://localhost:5000/
    HTTP method: GET
    
    curl http://localhost:5000/ -X POST
    
    returns new returned calendar = {}


  new entry:
    URL: http://localhost:5000/<calendar_id>
    HTTP method: POST
    
    <calendar_id> is numbered from 0
    Required parameters are "date", "from", "to", "description".

    curl http://localhost:5000/0 -H "Content-type: application/json" -X POST -d '{"date":"14-05-2014", "from":"10:00", "to":"15:00", "description":"meeting"}'
  
    returns: {"from": "10:00", "description": "meeting", "to": "15:00", "location": "", "date": "14-05-2014", "repeats": 0}
  
  list of all entries for specific calendar:
    URL: http://localhost:5000/<calendar_id>
    HTTP method: GET
    
    <calendar_id> is numbered from 0
    
    curl http://localhost:5000/0 -X GET
    
    returns: {"1": {"from": "10:00", "description": "meeting", "to": "15:00", "location": "", "date": "14-05-2014", "repeats": 0}}
  
  modify entry:
    URL: http://localhost:5000/<calendar_id>/<entry_id>
    HTTP method: PUT
    
    entry_id you can obtain from list of calendar's entries 

    curl http://localhost:5000/0/2 -H "Content-type: application/json" -X PUT -d '{"date":"15-05-2014"}'
    
    returns: {"1": {"from": "10:00", "description": "meeting", "to": "15:00", "location": "", "date": "15-05-2014", "repeats": 0}}
    


---
Appgain backend position technical task
===
The API is deployed and running on heroku at https://flashorter.herokuapp.com/
The Database is a free tier test Database running on Mlab

running API:
- /shortlinks (GET,POST)
- /shortlinks/<-slug->  (GET,PUT)
### Example API URI (active): 
https://flashorter.herokuapp.com/shortlinks (GET/POST)

https://flashorter.herokuapp.com/shortlinks/exampleslug (GET/PUT)
| Endpoint   |      Operation      |
|----------|:-------------:|
| /shortlinks (GET) |    Returns a json list of all the recorded shortened links   |
| /shortlinks (POST) | Puts a new entry in the DB with the provided json content, will generate a slug if not provided |
| /shortlinks/<-slug-> (PUT) | Updates a DB entry with the unique slug attribute with the provided json data |
|/shortlinks/<-slug-> (GET) | (Extra) redirects the user to the url with the slug attribute according to their platform (no fallback availability check)|

---
## JSON requests models
### Complete data json model 
```json
{"slug": "",
"ios":[
  {"primary": ""},
  {"fallback": ""}]
,
"android":[
  {"primary": ""},
  {"fallback": ""}],
"web": ""}
```
### Put (single update) data model examples 
```json
 {
    "android": [
      {
        "fallback": ""
      }]
  }
```

```json
 {
    "ios": [
      {
        "primary": ""
      }]
  }
```

```json
 {
    "web": ""
  }
```
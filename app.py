import hashlib
from flask import Flask , request, render_template, redirect, url_for, jsonify
import flask, flask_login, os
import pymongo
import os
'''
data_model = {"slug": "slug",
"ios":[
  {"primary": ""},
  {"fallback": ""}]
,
"android":[
  {"primary": ""},
  {"fallback": ""}],
"web": ""}
'''
class url():
    slug = ""
    ios_primary = ""
    ios_secondary = ""
    android_primary = ""
    android_secondary = ""
    web = ""
    data = {}
    def getJson(self):
        data = {"slug": self.slug,
            "ios":[
            {"primary": self.ios_primary },
            {"fallback": self.ios_secondary}]
            ,
            "android":[
            {"primary": self.android_primary},
            {"fallback": self.android_secondary}],
            "web": self.web}
        return data

    


app = Flask(__name__)
app.config.from_pyfile('config.py')

SECRET_KEY = os.getenv("SECRET_KEY")
DB_LINK = os.getenv("DB_LINK")
DB_COLLECTION = os.getenv("DB_COLLECTION")
#collection.insert_one(data_model)
#print(collection.find_one())

#hashids = Hashids(min_length=4,salt=SECRET)


@app.route('/shortlinks', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        '''fresh connection to db'''
        client = pymongo.MongoClient(DB_LINK)
        db = client.urls
        collection = db[DB_COLLECTION]
        
        #print(request.is_json)
        content = request.get_json(force=True)
        #print(content)
        slug = content['slug']
        ios = content['ios']
        android = content['android']
        web = content['web']
        print(ios[0]['primary'])
        if not slug:
            slug = hashlib.sha1((web+ios[0]['primary']+android[0]['primary']).encode("utf-8")).hexdigest()[:8]
            print("generated slug: " + str(slug))

        newurl = url()
        newurl.slug = slug 
        newurl.android_primary = android[0]['primary']
        newurl.android_secondary = android[1]['fallback']
        newurl.ios_primary = ios[0]['primary']
        newurl.ios_secondary = ios[1]['fallback']
        newurl.web = web 
        #newurl.getJson()  
        
        collection.insert_one(newurl.getJson())

        '''clean up db connection'''
        client.close()

        #return render_template('index.html')

        return newurl.getJson()
    elif request.method == 'GET':
        '''fresh connection to db'''
        client = pymongo.MongoClient(DB_LINK)
        db = client.urls
        collection = db[DB_COLLECTION]
        response =[]
        for url in collection.find({},{'_id': 0}):
            response.append(url)
            print(url)
        client.close()

        return jsonify(response)


@app.route('/shortlinks/<slug>', methods=('PUT',))
def update_url(slug):
    #print("request platform: " + request.user_agent.platform)

    '''fresh connection to db'''
    client = pymongo.MongoClient(DB_LINK)
    db = client.urls
    collection = db[DB_COLLECTION]
    content = request.get_json(force=True)
    #print(slug)
    #print(content)
    #print(content['ios'][0]['primary'])
    #This is messy because of the way the data scheme is but oh well too lazy to think of a better way
    if content['ios']:
        if content['ios'][0]['primary']:
            print(collection.find_one({"ios.primary":content['ios'][0]['primary']}))

            collection.find_one_and_update({"slug":slug},{'$set':{"ios.$[].primary":content['ios'][0]['primary']},})
        else:
            collection.update_one({"slug":slug},{"ios.$[].fallback":content['ios'][0]['fallback']})
    elif content['android']:
        if content['android'][0]['primary']:
            collection.update_one({"slug":slug},{"android.$[].primary":content['android'][0]['primary']})
        else:
            collection.update_one({"slug":slug},{"android.$[].fallback":content['android'][0]['fallback']})
    elif content['web']:
        collection.update_one({"slug":slug},{"web":content['web']})
        


if __name__ == "__main__":
    app.run(debug=True)
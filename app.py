from flask import Flask, render_template , redirect
import pymongo

import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)


# Connect to a database. Will create one if not already available.
db = client.mars_db

# Drops collection if available to remove duplicates
#db.mars.drop()
print('test')
#  create route that renders index.html template and finds documents from mongo
@app.route("/")
def index():
    mars = db.mars.find_one()
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    mars = db.mars
    mars_data = scrape_mars.scrape()

    mars = {
        "news_text": mars_data["news_text"],
        "news_p": mars_data["news_p"],
        "featured_image_url": mars_data["featured_image_url"], 
        "mars_weather": mars_data["mars_weather"],
        "html_table": mars_data["html_table"],
        "hemisphere_image_urls": mars_data["hemisphere_image_urls"]
        } 
    
    # # Insert mars factoids into database
    #db.mars.insert_one(mars)
    db.mars.update({}, mars, upsert=True)
    # Redirect back to home page
    return redirect("/", code=302)

    
if __name__ == "__main__":
    app.run(debug=True)



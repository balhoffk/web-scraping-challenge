from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#create route that renders index.html template and finds documents from mongo
@app.route("/")
def index():
    #find data
    scrape_mars = mongo.db.collection.find()
    #return template and data
    return render_template("index.html", scrape_mars=scrape_mars)

# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():
    mars = scrape_info.scrape_mars()
    scrape_mars = {
        "news_title"= mars["news_title"]
        "news_text"=mars["news_text"]
        "img_url"=mars["img_url"]
        "weather"=mars["weather"]
        "html_facts"=mars["html_facts"],
        "hemis"=mars["hemisphere_img_urls"]
    }
        
    mongo.db.collection.insert_one(mars_scrape)
    #redirect to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

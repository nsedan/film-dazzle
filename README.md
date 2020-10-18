# [Film Dazzle.](https://filmdazzle.herokuapp.com/)

> A movie database website. Ratings, reviews and more.

---

![Screenshots](static/images/screenshot.png)

---

## Purpose

This project is aimed at film enthusiasts eager to leave an opinion for a recently released title, as well as to the occasional viewer looking for a next film to enjoy. The site offers a custom rating system, generated from user reviews, the rating from IMDb and Metacritic. This application is completely free and there is no need to be a professional critic to leave a review or rate movies.

#### User Stories

- As a user I want to be able to know more details about a particular movie.
- As a user I want to be able to look for a movie and see what other people think about it.
- As a user I want to be able to give my opinion for a movie a saw.
- As a user I want to be able to leave a rating for a movie even if I don't want to give a full review.
- As a user I want to be able to edit or delete previous entries without issue.

## Features

- The home page has a coming soon section for movies to be released, recently reviewed titles and a top 10 box office.
- Search movies by title, achieved with the OMDB API, later the titles are stored in MongoDB.
- A register and login to allow the user to fully interact with the site.
- Leave a review with a rating system, with full CRUD functionality.
- Randomize feature, allow the user to find a random title from the DB.
- A worldwide box office success ranking.
- A top 10 ranking by rating, according IMDb, Metacritic and Film Dazzle.

## Technologies Used

This website was developed mainly with **Python** and some **Javascript**.

Additionally, the next technologies were used:

- [Flask](https://flask.palletsprojects.com/)

  - This project uses **Flask** for routing.

- [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)

  - This project uses **Jinja** as templating language.

- [PyMongo](https://pymongo.readthedocs.io/en/stable/)

  - This project uses **PyMongo** to handle the interaction between Python and MongoDB.

- [MongoDB](https://www.mongodb.com/)

  - This project uses **MongoBD** database to store all data.

- [Bootstrap](https://getbootstrap.com/)

  - This project uses **Bootstrap** to style layout and elements.

- [Sass](https://sass-lang.com/)

  - This project uses **SCSS** for styling.

- [JQuery](https://jquery.com)

  - This project uses **JQuery** to simplify DOM manipulation.

- [Heroku](https://www.heroku.com/)

  - This project uses **Heroku** to host the app.

## Testing

The main objective was to test that all routes and templates worked correctly. Also some tests were made to check the responsiveness of the site, mainly on how the different devices adapt to the changes in the layout. Python unit testing was considered but proved unnecessary as very few functions return a specific int or string result and all routes were manually tested.

#### Code Validation

For code validation [w3 Validation Service](https://w3.org/) was used for HTML and CSS. For Python [ExtendsClass](https://extendsclass.com/python-tester.html) and [JSHint](https://jshint.com/) for JS.

#### The devices that this site was test were:

- Samsung Galaxy S6
- Samsung Galaxy A50
- Samsung Galaxy A70
- Iphone 8 Plus
- Laptop ASUS S510UA, 15.6"
- Desktop PC, 27"
- Tablet was tested with Chrome developer tools.
- Also, the site was tested on Firefox and Microsoft Edge.

#### User Tests: 

Several user tests were made throughout the project to reveal errors or to add/change features:

- A user is requested to search for a movie and click a particular choice to render more information about it.
- A user is requested to leave a review for a movie, at this stage there is no login feature in place.
- Randomize feature is added after a user suggested a way to find a random movie.
- At this stage a complete test was done with a few testers, to avoid broken links and check responsiveness.
- A user is requested to register to leave a review and click on it to read more. No issues were found but a new rating style was added at this stage to make it more user friendly.
- After adding edit and delete features, this was tested with several users.
- A final run to test routing, it was requested to specifically try the review system to add, read, edit and delete.


## Contribute
All contributions are welcomed and encouraged.

### Deploy your own
To deploy this application on Heroku using GitHub and MongoDB follow this instruction:

- Clone the repository.
- Install the necessary dependencies using "pip3 install -r requirments.txt".
- Get a API key from [OMDb](http://www.omdbapi.com/)
- Get a API key from [YouTube Data API](https://developers.google.com/youtube/v3/getting-started)
- Create a [MongoDB](https://www.mongodb.com/) database with the same naming conventions which can be found in app.py. 
- Create a file in the main directory called ‘env.py’ based on the ‘env.example.py’ and add all your environment variables. Don’t forget to add a secret key for your app.
- Create a [Heroku](https://www.heroku.com/) app and connect it to your GitHub repo. In Heroku (App > Settings > GitHub) to complete the connection.
- Add your environment variables on Heroku as well, on the “Config Vars” section. When adding the DEBUG key, leave the value empty to set it to False.
- Complete a commit, push it to GitHub and using ‘git push heroku master’ command push it to Heroku.

## Credits

- To [w3shools](https://www.w3schools.com/)
- To [MDN web docs](https://developer.mozilla.org/)
- To [Stack Overflow](https://stackoverflow.com/)
- To [OMDb API](http://www.omdbapi.com/)
- To [Font Awesome](https://fontawesome.com/)
- To [Pretty Printed](https://prettyprinted.com/)

#### Acknowledgements

I received inspiration for this project from:

- [IMDb](https://www.imdb.com/)
- [Rotten Tomatoes](https://www.rottentomatoes.com/)
- [Metacritic](https://www.metacritic.com/)

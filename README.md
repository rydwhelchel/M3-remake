# Artist Summary App

https://song-displayer.herokuapp.com/

## Technologies, frameworks and libraries
1. [Flask](https://flask.palletsprojects.com/en/2.0.x/) is a [microframework](https://en.wikipedia.org/wiki/Microframework) used as a backend for web apps. It is used here for exactly that; a web server backend.
2. [python-dotenv](https://github.com/theskumar/python-dotenv) is a library used for accessing a `.env` file which contains sensitive information. The sensitive information in contains can vary, but usually it is used for containing API keys and secrets. This is convenient as it allows you to easily keep Git from pushing sensitive data by ignoring the `.env` file. 
3. [requests](https://docs.python-requests.org/en/latest/) is used for handling requests sent to APIs easily in Python.
4. [Heroku](https://www.heroku.com/) is a cloud service platform used for easily deploying webapps with as little overhead as possible. Heroku allows you to install dependencies on the host for your webapp as well as create a domain name for free.
5. [flask-login](https://flask-login.readthedocs.io/en/latest/) is a framework which is used to aid user management. 
6. [SQLAlchemy](https://www.sqlalchemy.org/) is a tool to help bridge the gap between Python and SQL-style query languages.
7. [PostgresQL](https://www.postgresql.org/) is an object-relational database which can easily be integrated with Heroku. 
-----
## APIs accessed

1. Spotify API is used here for the following:
   1. Finding songs by artists
   2. Accessing previews of said songs
   3. Getting album art
2. Genius API is used strictly for finding lyrics for the above songs. The lyrics are accessed directly from Genius' website.
-----
## How to set up:

1. Create a folder which will contain the webapp
2. Open a terminal and change directory into the newly created folder:
   
```cd <directory-name>```

3. Fork the repository into this folder:

`git clone https://github.com/csc4350-f21/project1-rydwhelchel.git`

4. Create a Spotify account at https://developer.spotify.com/dashboard/login
5. Accept the terms
6. Create an app; the name and description do not matter.
7. Select the app
8. Locate the Client ID and Client Secret (click "Show client secret"). You will need these later. (.env and Heroku secret section)
   ![](https://i.ibb.co/7CWhVKG/mspaint-LJe1-Mmgwez.png?raw=true)
9.  Create a Genius account by going to https://genius.com/developers and clicking "Create an API Client"
10. Create a new API client
    1.  Fill out the App Name field
    2.  Leave Icon URL field blank
    3.  Put https://example.com for the App Website URL (or whatever you want)
    4.  Leave the Redirect URI field blank
11. Click `Generate Access Token` and save the token for later. (.env and Heroku secret section)
![](https://i.ibb.co/5ch1dBn/image.png?raw=true)

-----
### For running local webapp
This is for running a app locally. This is useful if you just want to preview the webapp or if you want to test changes you make to the app. If you only interested 

1. Install the requirements. If you don't have pip (and are on a linux based operating system) use: `sudo apt-get update` followed by `sudo apt install pip`
  
   1. `pip3 install requests`
   2. `pip3 install python-dotenv`
   3. `pip3 install Flask`
   4. `sudo apt install postgresql`
   5. `sudo -u postgres psql`
   6. `pip install Flask-SQLAlchemy==2.1`
   7. 
2. Create a file called `.env` in the root directory of `project1-rydwhelchel` (or whatever you renamed the folder to).
3. Add the following lines to the `.env` file:
   1. `export SPOT_SECRET='<your spotify secret here>'`
   2. `export SPOT_ID='<your spotify id here>'`
   3. `export GEN_ACCESS='<your genius access key here>'`
4. Ensure that there is a `.gitignore` file in the root directory (wherever app.py is located).
5. Ensure that in the `.gitignore` file, there is a line that says `.env`. Add it if there isn't.
6. In app.py, change `app.run(...)` line to just `app.run(debug=True)`. This allows you to launch the app locally. If you don't need to be able to make changes on the fly while the app is up, you can simply change it to `app.run()`.
7. You're good to go! Just run app.py and click "Open Browser" on the prompt that appears (if you are using VSCode). If you aren't using VSCode, open your browser and enter `http://127.0.0.1` in the address bar. 
8. If you are running this on a VM, you likely will have to forward a port to access it on your local machine. I recommend using VSCode to automate this process.

-----
### To redeploy using Heroku
This is if you want to deploy this app using Heroku on your own. 
1. To start, ensure that in `app.py`, the `app.run(...)` line contains the arguments `host='0.0.0.0'` and `port=int(os.getenv('PORT', 8080))`. IE: 
   ```
   app.run(
    host='0.0.0.0',
    port=int(os.getenv('PORT', 8080)),
   )
   ```
2. Install Heroku using `sudo snap install --classic heroku`. While this is downloading complete steps 3-
3. Make a Heroku account at https://dashboard.heroku.com/
4. Create a `requirements.txt`. Note that there may already be a `requirements.txt` file. In which case, you only need to ensure that all appropriate packages are listed in it.
5. Ensure that the following lines are included in `requirements.txt`
   - `Flask`
   - `python-dotenv`
   - `requests`
   - `psycopg2`
   - `flask_login`
   - `flask_SQLAlchemy`
  
6. Add any additional packages that you have decided to add to the webapp. If you haven't added any additional third party packages ignore this step.
7. Create a `Procfile`. A `Procfile` is the trigger file used by Heroku to decide how to run your app. In this case, the file is simply called `Procfile` (with no file extensions). In this file, include the line `web: python app.py` This file may need to be modified if you have made modifications to the application. 
         
         Note: this file may already be included.
8. Add and commit all changes made to files with Git
   1. `git add -A`
   2. `git commit -m "<your message here>"`
9. Assuming your Heroku install has finished use the following to login to Heroku via your terminal/bash
   1.  `heroku login -i`
10. Create a Heroku app: `heroku create`. This will create the Heroku URL as well as the associated git URL which you can push your application to. You can push to this the same way you push to `origin` by using the name `heroku` instead. 

         Note: You may run into issues if your `main` branch is instead named `master`. Highly recommend renaming your `master` branch to `main` before continuning.
11. Next we need to create a Heroku database for this app: `heroku addons:create heroku-postgresql:hobby-dev -a <app-name>` where `<app-name>` is the name of the Heroku app you just created.
12. Next, get the Heroku DB URL by running `heroku config` and copy the value for DATABASE_URL.
13. Enter this value in your `.env` file with the line `export DATABASE_URL='<url>'`
14. Change the value in the `DATABASE_URL` from `postgres:...` to `postgresql:...`.
15. Now push your project to heroku: `git push heroku main`
16. Next we need to give Heroku our API IDs, secrets and tokens. If you created the .env file earlier, you can refer to that. Otherwise refer to [steps 4-11 in this section.](#how-to-set-up) 
17. Log in to https://dashboard.heroku.com/apps/
18. Select the app you created earlier in the terminal/bash.
19. Select `Settings` 
    ![](https://i.ibb.co/7WCktzB/image.png?raw=true)
20. Scroll down to `Config Vars` and click `Reveal Config Vars`
    ![](https://i.ibb.co/DRtjpZk/image.png?raw=true)
21. Input the following, fields are seperated by colons:
    1.  `GEN_ACCESS` : `<your genius API access token here>`
    2.  `SPOT_ID` : `<your spotify ID here>`
    3.  `SPOT_SECRET` : `<your spotify secret here>`
   ![](https://i.ibb.co/yBrhCW0/image.png?raw=true)
18.  In order to correct the Heroku database url, cd to the correct directory and run the following commands in terminal: 
   ```
   heroku addons:attach heroku-postgresql -a <app_name> --as HEROKU_DATABASE
   heroku addons:detach DATABASE -a <app_name>
   heroku config:add DATABASE_URL=<database_url>
   ```
   Where `<app_name>` is the name of your Heroku app and `<database_url>` is the database url with `postgresql` prepended instead of `postgres`.

19.  Note that the order does not matter, however the variable names must be exactly as shown above. 
20.  Everything should be handled! Try typing `heroku open` into terminal/bash to open your newly deployed webapp!

---

## Known Problems
1. Lyric links are not 100% accurate
   
   This is a problem that was expected, as our access of the Genius API currently only *searches* the site and takes the top result. Sometimes that top result isn't exactly what we want.
2. Runtime is longer than desired
   
   This is covered above in the technical issues section. As of right now, over half of runtime is spent accessing Genius API to get a lyrics link for each song. A solution is in the making, stay tuned!
3. Error thrown when accessing some artists
   
   When attempting to show the songs of an artist who does not have 10 songs or is a podcaster, an error will be thrown Not a perfect solution, but simply rerandomizes the artist if this issue is run into.
4. Display issues on mobile devices and smaller displays
   
   When accessing site on mobile devices, the preview player covers the lyrics link.
   On smaller displays, the album images can take up too much real estate

## What would I do to improve my project in the future?
1. Adding a "guessing game" bit:
   - The idea is that you display the song preview and either list several artists for the user to pick from or, if you're confident in your ability to match user input to the artist, let the user type in what they think the artist's name is. Difficulty would be deciding the list of artists to randomly pick from.


## Milestone 2 Questions

### Known Problems
1. I would consider it a problem that there is no password for your account. A lack of password security feels almost as if it is no longer your account at all. You could also list this as a future feature. 
2. I think my code is currently leaning towards spaghetti. On working on this milestone, I realized that many of the things I have done in this project could be further modularized and be much easier to modify and much cleaner to read. Where this is most obvious is in my routed methods (the methods within app.py). I call `get_gen_access` and `get_spot_access` too often, I could just as easily call those methods within methods such as `get_artist_id` to avoid repeating myself too often in the main routing methods. I think this problem was originally created because I thought it would be less repetition to call them in the routed methods, but I quickly realized during this milestone that you can have a ton of routed methods depending on requests sent.

### Technical Issues
1. The first issue that jumps out to me is the issue of handling information per user. This is my first foray into handling user data within a database and it took me some time to wrap my head around the flow of it. I originally was trying to create a seperate table for each user so that each users' data would be private. I eventually realized that this wasn't quite how it worked. Storing all of the favorite artists in one table and then querying for a specific users favorite artists was much, much easier and more effective than whatever it was I trying to do. I solved this by researching how others handle user specific data, and I wish I had researched it earlier. After researching this in particular, the answer practically jumped out at me.
2. I originally had issues with initializing the database due to circular imports. I went through some comments in a forum and saw that in would be beneficial to break up the logic for initializing the app and the database into 3 files rather than just 2. Utilizing this method fixed my problem immediately.

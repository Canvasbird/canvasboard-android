<p align="center">
<img alt="Logo" height="80" src="https://github.com/Canvasbird/canvasboard/blob/master/src/assets/home/logo_bw.png?raw=true" width="80">
<br>
<br>
<strong>Canvasbird Organization</strong>
<br>
<strong>Project: Canvasboard Android</strong>
<br>
<br>
<a href="#">
The whole purpose of education is to turn mirrors into windows.
</a>
<br>
<code href="#">
- Sydney J. Harris
</code>
</p>

## Canvasboard Android

Canvasboard Android is a hybrid android application which makes use of AI for real time communication to organize the live class on the Canvas Web Board and schedule the timing of classes for the students.

**Functionality:**
* Live Class: Teachers can conduct live classes from their mobile and it will appear real time on the board.
* Schedule a Class: Teachers can schedule a class through the android application. The teachers and the students will get a notification for the scheduled class 10 mins before.
* View Scheduled Class: Teachers and students

**To setup the project on your local machine:**

1. Click on `Fork`.
2. Go to your fork and `clone` the project to your local machine.
3. Create virtual enviroment by python3 -m virtualenv env
4. Activate it by source env/bin/activate
5. Install the requirements `pip install -r requirements.txt`.
Steps to run the project

-> running the python server (ML API in flask)
	dependencies -> flask, opencv, pillow, flask-cors
	steps:
		create virtual enviromet using python3 -m virtualenv env
		after installation activate the enviroment using
			-> source env/bin/activate
		install the above packages using pip
			->pip install flask
			->pip install opencv-python
			->pip install Pillow
			->pip install flask-cors	
		run the server using
			-> python app.py

Steps to run the front end

-> open the file canvas-board project in terminal
1. install the node modules required
	-- npm install
2. to run the app use the following command
	-- ionic serve
	-- the project opens in browser at localhost:9000
3. now open the server folder in the front end project (this folder contains js client to receive live stream from mobile and also sends the stream to flask server via api call)
	
	-- in this folder just open another terminal and type
		python -m http.server (if on windows) 
		sh ./run.sh (if on linux)
		
		this will serve the client

4. now every thing is ready just open the application in mobile give access to camera
after wards click the connect button after the camera has loaded

	now we can see the stream from phone is been displayed on client web page
	and also we can observe the stream send to send to server for preprocessing and received 	back	

5. to make a production build off the app aun the command
	npm run build

**To contribute to the project:**

1. Choose any open issue from.
2. Comment on the issue: `Can I work on this?` and get assigned.
3. Make changes to your fork and send a PR.

**To create a PR:**

Follow the given link to make a successful and valid PR: https://help.github.com/articles/creating-a-pull-request/

**To send a PR, follow these rules carefully,**otherwise your PR will be closed**:**

1. Make PR title in this format: `Fixes #IssueNo : Name of Issue`

For any doubts related to the issues, i.e., to understand the issue better etc, comment down your queries on the respective issue.


**License**

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/Canvasbird/canvasboard-android/blob/master/LICENSE) file for details


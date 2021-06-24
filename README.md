This is my third year research project.
The educational platform Modeus that students of the University of Tyumen are required to use does not have a convenient mobile version.
Besides using a desktop computer, there is no way to quickly check the schedule.
This project aims to solve this problem by developing an extension for the Russian virtual voice assistant Alice.
The extension provides students quick access to their schedule on Modeus using voice recognition.
It also connects to another educational platform, Canvas, so the students will be able to ask Alice about their upcoming assignments and unread inbox messages as well.
The extension consists of the data parser software, that logs into user’s account on both platforms and downloads all required data from them and the so-called “skill” for Alice,
which is able to analyze the incoming voice command, find specific keywords and return the required website data to the user with a built-in text-to-speech Alice module.

The project includes:

> modeuspluscanvas.py - this is the core file of the Alice skill.

> data.json - this is the output file of the data parser program (which is not made yet).
	The parse was made on 09.04.2020. Currently, the word "today" will mean the day when the data was parsed.

> data_screenshots - this folder contains screenshots made on 09.04.2020.
	They include my Modeus timetable, Canvas Dashboard and Canvas Inbox.
	They are the reference to compare them with the data.json file.
	
Currently, the skill is not complete enough for Yandex moderators to approve it and add to the skill lists.
However, you can still test it right now.
To do so, you will need a software named ngrok (https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip).

To test the skill in Yandex.dialogs:

	1. Type "ngrok http 5000" without quotes in the ngrok application.
	2. Open Yandex.dialogs (https://dialogs.yandex.ru/) and register here.
	3. Create new skill and put the "https" link ngrok gave you into the "Webhook URL" field, adding "/post" after it.
	4. Launch modeuspluscanvas.py
	5. Open "Testing" tab in Yandex.dialogs and start using the skill.
	
Alternatively, if you want to talk and listen to the skill:
	You can simulate it on the website https://station.aimylogic.com/
	Just enter the "https" link ngrok gave you, adding "/post" after it into the "Webhook URL" field.
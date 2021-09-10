BOT AGENDA

----------------------------------------------------------------

BOT AGENDA is a discord.py bot that can be used as a collective agenda. Using commands such as add and del you can change the tasks in the agenda.
You can see the agenda by using the command ?agenda and you can see the calendar using the command ?calendario

LINK:

https://discord.com/api/oauth2/authorize?client_id=814508098681176095&permissions=8&scope=bot

----------------------------------------------------------------

COMMANDS

----------------------------------------------------------------

?agenda - Show all tasks and their details like, platform, subject and enddate.

?add "(task name)" "(enddate(dd/mm/yyyy))" - Adds tasks to the agenda, this command when used will open a menu where the user will select the platform and subject, after that, the user must click on the confirm button.

?del (task name) - Removes specific task from the agenda.

?calendario (day of the week or hoje"(optional)) - This command shows the classes of each day of the week, if a specific day is passed then only show classes for this day, if hoje is passed, then it shows classes for the current day of the week.

?clear - Deletes all tasks from the agenda.

?update - This command is made exclusively to my school. This command takes all the current homework assigned on the platform geekie one and adds it to the agenda.

---------------------------------------------------------------

LIBRARIES USED

---------------------------------------------------------------

discord.py - Although the only mainteiner recently left the project, it's still the best and most simple python library for making discord bots.

discord_components - This library enables feautures used to make the menu where the user can select and click on buttons.

datetime - Used to keep track of time and work with enddates.

firebase_admin - Used to connect the application to a firebase database to save data and enable integration with other platforms.

asyncio - Used to handle async code.

requests - Used to make http requests to the geekie one platform.

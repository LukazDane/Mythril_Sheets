### Project Title: Mythril Sheets(Working Title)

##### Character, spell, and info Tracker for D&D(MakeDungeons)

---

#### [Live](https://mythril-sheets.herokuapp.com/)

---

#### Utilizes Python-Flask and a Sql-Database

#### To Run:

To view current progress, run as you would any other python app.

- Clone
- pip install requirements.txt
- python3 app.py
  > This project will combine the front end mockups from SPD(Mythril Sheets_v1), with the backend/database from BEW(Mythril Spellbook) and will eventually build into intensives (Mythril Library).

---

Challanges and notes to self:

- Heroku and Flask-Login:
  > While the login and registratin works fine locally, there's a persisting error when live on Heroku
- Database Structuring:
  > I massively over estimated my abilities to deal with databases. On Tuesday after getting Users working, creating a new user would cause the site to crash because of issues connecing the user to the ccharacter sheets.
- Mac Updates:
  > After an automatic mac update I found myself experiencing a plethora of errors and bugs. After spending hours coding around those bugs it came to my attention that my terminal, interpreter, and linter had all defaulted back to python 2.7, xcode had become out of date.

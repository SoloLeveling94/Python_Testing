import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for, abort


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

max_places = "12"

for comp in competitions:
    for c in clubs:
        comp[c['name']] = max_places


print(competitions)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    except IndexError:
        flash("Your email is not registered!")
        return redirect(url_for('index'))
    return render_template('welcome.html', date=date, club=club, competitions=competitions,
                           listClubs=sorted(clubs, key=lambda x: int(x['points'])))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]

        if date > foundCompetition['date']:
            flash("Choose an another competition. The date has expired!")
            return render_template('welcome.html', club=club, competitions=competitions, date=date)

        if foundClub and foundCompetition:
            return render_template('booking.html', club=foundClub, competition=foundCompetition, date=date,
                                   listClubs=sorted(clubs, key=lambda x: int(x['points'])))
    except IndexError:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions, date=date)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        placesRequired = int(request.form['places'])

        if placesRequired > int(club['points']) // 3:
            flash(f"You do not have enough points ({club['points']}) to purchase this places!")
            return render_template('booking.html', club=club, competition=competition)

        elif int(competition['numberOfPlaces']) < placesRequired:
            flash(f"You can not purchase more than the number of places available ({competition['numberOfPlaces']})!")
            return render_template('booking.html', club=club, competition=competition)

        elif placesRequired < 1:
            flash(f"Enter a positive number to book it!")
            return render_template('booking.html', club=club, competition=competition)

        elif placesRequired > int(competition[club['name']]):
            flash(f"You can not book more {competition[club['name']]} places in this competition")
            return render_template('booking.html', club=club, competition=competition)

        else:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            club['points'] = int(club['points']) - placesRequired * 3
            competition[club['name']] = int(competition[club['name']]) - placesRequired

            flash('Great-booking complete!')
            return render_template('welcome.html', club=club, competitions=competitions, date=date,
                                   listClubs=sorted(clubs, key=lambda x: int(x['points'])))

    except ValueError:
        flash("Enter a number!")
        return render_template('booking.html', club=club, competition=competition)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

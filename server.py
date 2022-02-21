import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


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
dict_points = {c['name']: 12 for c in competitions}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        # date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    except IndexError:
        flash("Your email is not registered!")
        return redirect(url_for('index'))
    return render_template('welcome.html', date=date, club=club,
                           competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition, dict_points=dict_points)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    # date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        placesRequired = int(request.form['places'])
        numberPlaceCompetitionByClub = dict_points.get(competition['name'])

        if placesRequired > int(club['points']):
            flash("You do not have enough points to purchase this places!")
            return render_template('booking.html', dict_points=dict_points, club=club, competition=competition)

        if int(competition['numberOfPlaces']) < placesRequired:
            flash("You can not purchase more than the number of places available!")
            return render_template('booking.html', dict_points=dict_points, club=club, competition=competition)

        if placesRequired < 1:
            flash("Enter a positive number to book it!")
            return render_template('booking.html', dict_points=dict_points, club=club, competition=competition)

        if placesRequired <= numberPlaceCompetitionByClub:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            dict_points.update({competition['name']: numberPlaceCompetitionByClub - placesRequired})
            club['points'] = int(club['points']) - placesRequired
            flash('Great-booking complete!')
            return render_template('welcome.html', dict_points=dict_points, club=club,
                                   competitions=competitions,)
            # return render_template('welcome.html', dict_points=dict_points, date=date, club=club,
            #                        competitions=competitions,)
        else:
            flash('You can only book 12 places max for this competition')
            return render_template('booking.html', dict_points=dict_points, club=club, competition=competition)

    except ValueError:
        flash("Enter a number!")
        return render_template('booking.html', dict_points=dict_points, club=club, competition=competition)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

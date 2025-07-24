from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from models import db, Candidate, Vote
from forms import VoteForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Proper way to run setup code in Flask 3.x
@app.before_request
def initialize_database():
    if not hasattr(app, 'db_initialized'):
        with app.app_context():
            db.create_all()
            # Add sample candidates if none exist
            if Candidate.query.count() == 0:
                candidates = [
                    Candidate(name="Alice Smith", party="Party A"),
                    Candidate(name="Bob Johnson", party="Party B"),
                    Candidate(name="Charlie Lee", party="Party C"),
                ]
                db.session.bulk_save_objects(candidates)
                db.session.commit()
            app.db_initialized = True  # Prevent repeat init

@app.route('/')
def index():
    return redirect(url_for('vote'))

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    form = VoteForm()
    form.candidate.choices = [(c.id, f"{c.name} ({c.party})") for c in Candidate.query.all()]
    if form.validate_on_submit():
        vote = Vote(voter_name=form.voter_name.data.strip(), candidate_id=form.candidate.data)
        try:
            db.session.add(vote)
            db.session.commit()
            flash("Your vote has been cast successfully!", "success")
            return redirect(url_for('results'))
        except IntegrityError:
            db.session.rollback()
            flash("You have already voted. Duplicate voting is not allowed.", "danger")
    return render_template('vote.html', form=form)

@app.route('/results')
def results():
    candidates = Candidate.query.all()
    results = []
    for c in candidates:
        vote_count = Vote.query.filter_by(candidate_id=c.id).count()
        results.append({'candidate': c, 'votes': vote_count})
    return render_template('results.html', results=results)

@app.route('/candidates')
def candidates():
    candidates = Candidate.query.all()
    return render_template('candidates.html', candidates=candidates)

if __name__ == '__main__':
    app.run(debug=True)

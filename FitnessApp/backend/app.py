from flask import Flask, request
from datetime import datetime
from .models import db, User, Workout, Exercise, Measurement, BodyMeasurement

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db.init_app(app)

@app.route('/user', methods=['POST'])
def create_user():
    name = request.form.get('name')
    height = float(request.form.get('height'))
    weight = float(request.form.get('weight'))
    
    user = User(name=name, height=height, weight=weight)
    db.session.add(user)
    db.session.commit()

    return {'id': user.id}

@app.route('/workout', methods=['POST'])
def create_workout():
    user_id = int(request.form.get('user_id'))
    date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
    exercises = request.form.get
    exercises = request.form.get('exercises')  # Assume this is a list of dictionaries with 'name', 'sets', 'reps'
    
    workout = Workout(user_id=user_id, date=date)
    db.session.add(workout)
    db.session.commit()

    for exercise in exercises:
        db_exercise = Exercise(workout_id=workout.id, name=exercise['name'], sets=exercise['sets'], reps=exercise['reps'])
        db.session.add(db_exercise)

    db.session.commit()

    return {'id': workout.id}

@app.route('/measurement', methods=['POST'])
def create_measurement():
    user_id = int(request.form.get('user_id'))
    date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
    weight = float(request.form.get('weight'))
    body_measurements = request.form.get('body_measurements')  # Assume this is a list of dictionaries with 'part', 'measurement'
    
    measurement = Measurement(user_id=user_id, date=date, weight=weight)
    db.session.add(measurement)
    db.session.commit()

    for body_measurement in body_measurements:
        db_body_measurement = BodyMeasurement(measurement_id=measurement.id, part=body_measurement['part'], measurement=body_measurement['measurement'])
        db.session.add(db_body_measurement)

    db.session.commit()

    return {'id': measurement.id}

if __name__ == "__main__":
    app.run(debug=True)
from flask_jwt_extended import unset_jwt_cookies
from flask import Flask, jsonify, request, Response
from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models import ma, db, bcrypt, User, Theatre, Shows, user_schema, theatre_schema, theatres_schema, show_schema, shows_schema, TransactionTable,transaction_schema, booking_schema
from flask_restful import Api
from sqlalchemy import and_, or_, func
from datetime import datetime
from tools import workers, task
import matplotlib.pyplot as plt
import numpy as np
import io
import csv

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
cache = Cache(app)
db.init_app(app)
app.app_context().push()
db.create_all()

bcrypt.init_app(app)
ma.init_app(app)
CORS(app, supports_credentials=True)
api = Api(app)

celery = workers.celery

celery.conf.update(
        broker_url='redis://localhost:6379/1',
        result_backend='redis://localhost:6379/2'
    )
celery.Task = workers.ContextTask
app.app_context().push()

# API for users

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    name = request.json.get('name')
    city = request.json.get('city')
    password = request.json.get('password')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 409

    new_user = User(email=email, name=name, city=city, password=password)

    try:
        db.session.add(new_user)
        db.session.commit()

        result = user_schema.dump(new_user)
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while registering user: {str(e)}")
        return jsonify({'message': 'Error occurred while registering user'}), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'isLoggedIn': False, 'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity={
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'is_admin': user.is_admin,
        'isLoggedIn': True
    })

    return jsonify({'access_token': access_token}), 200


@app.route('/getuserinfo', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])

    if not user:
        return jsonify({'isLoggedIn': False,'message': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'is_admin': user.is_admin,
        'isLoggedIn': True
    }), 200


@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'message': 'Logout successful'})
    unset_jwt_cookies(response)
    return response, 200

# APIs for theatres

@app.route('/theatres', methods=['POST'])
@jwt_required()
def create_theatre():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])

    if not user or not user.is_admin:
        return jsonify({'message': 'Access denied. You must be an admin to create a theatre.'}), 403

    data = request.json
    name = data.get('name')
    place = data.get('place')
    location = data.get('location')
    capacity = data.get('capacity')

    if not name or not place or not location or not capacity:
        return jsonify({'message': 'All fields are required'}), 400

    new_theatre = Theatre(name=name, place=place, location=location,
                          capacity=capacity, created_by=user.id)

    try:
        db.session.add(new_theatre)
        db.session.commit()

        return jsonify({'message': 'Theatre created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while creating theatre: {str(e)}")
        return jsonify({'message': 'Error occurred while creating theatre'}), 500


@app.route('/theatres', methods=['GET'])
@jwt_required()
def get_all_theatres():
    current_user = get_jwt_identity()
    theatres = Theatre.query.filter_by(created_by=current_user['id']).all()
    result = theatres_schema.dump(theatres)
    return jsonify(result), 200


@app.route('/theatres/<int:theatre_id>', methods=['GET'])
@jwt_required()
def get_theatre(theatre_id):
    theatre = Theatre.query.get(theatre_id)
    if not theatre:
        return jsonify({'message': 'Theatre not found'}), 404

    result = theatre_schema.dump(theatre)
    return jsonify(result), 200


@app.route('/theatres/<int:theatre_id>', methods=['PUT'])
@jwt_required()
def update_theatre(theatre_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])

    if not user or not user.is_admin:
        return jsonify({'message': 'Access denied. You must be an admin to edit a theatre.'}), 403

    theatre = Theatre.query.get(theatre_id)
    if not theatre:
        return jsonify({'message': 'Theatre not found'}), 404

    data = request.json
    name = data.get('name')
    place = data.get('place')
    location = data.get('location')
    capacity = data.get('capacity')

    if not name or not place or not location or not capacity:
        return jsonify({'message': 'All fields are required'}), 400

    theatre.name = name
    theatre.place = place
    theatre.location = location
    theatre.capacity = capacity

    try:
        db.session.commit()
        return jsonify({'message': 'Theatre updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while updating theatre: {str(e)}")
        return jsonify({'message': 'Error occurred while updating theatre'}), 500


@app.route('/theatres/<int:theatre_id>', methods=['DELETE'])
@jwt_required()
def delete_theatre(theatre_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])

    if not user or not user.is_admin:
        return jsonify({'message': 'Access denied. You must be an admin to delete a theatre.'}), 403

    theatre = Theatre.query.get(theatre_id)
    if not theatre:
        return jsonify({'message': 'Theatre not found'}), 404

    try:

        associated_shows = Shows.query.filter_by(theatre_id=theatre_id).all()
        for show in associated_shows:

            associated_transactions = TransactionTable.query.filter_by(show_id=show.id).all()
            for transaction in associated_transactions:
                db.session.delete(transaction)

            db.session.delete(show)


        db.session.delete(theatre)
        db.session.commit()

        return jsonify({'message': 'Theatre and associated shows and transactions deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while deleting theatre: {str(e)}")
        return jsonify({'message': 'Error occurred while deleting theatre'}), 500


# APIs for shows

@app.route('/theatres/<int:theatre_id>/shows', methods=['GET'])
def get_shows_by_theatre(theatre_id):
    try:
        shows = Shows.query.filter_by(theatre_id=theatre_id).all()
        return shows_schema.jsonify(shows)
    except Exception as e:
        return jsonify({'message': 'Error occurred while fetching shows', 'error': str(e)}), 500


@app.route('/theatres/<int:theatre_id>/shows', methods=['POST'])
@jwt_required()  
def add_show_to_theatre(theatre_id):
    try:

        current_user = get_jwt_identity()
        if not current_user['is_admin']:
            return jsonify({'message': 'Unauthorized. Only admin users can access this action.'}), 403

        data = request.get_json()
        name = data['name']
        tags = data['tags']
        rating = 0
        date_str = (data['date'])
        start_time_str = data['start_time']
        end_time_str = data['end_time']
        price = data['price']
        sold_ticket_count = 0

 
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()

        # Check if the show timings overlap with existing shows in the same theatre
        existing_shows = Shows.query.filter(
            Shows.theatre_id == theatre_id,
            Shows.date == date,
            or_(
                and_(Shows.start_time <= start_time,
                     Shows.end_time > start_time),
                and_(Shows.start_time < end_time, Shows.end_time >= end_time),
            ),
        ).all()

        if existing_shows:
            return jsonify({'message': 'Show timings overlap with existing shows.'}), 400


        new_show = Shows(name, theatre_id, rating, tags, date,
                         start_time, end_time, price, sold_ticket_count)
        db.session.add(new_show)
        db.session.commit()

        return show_schema.jsonify(new_show)
    except Exception as e:
        return jsonify({'message': 'Error occurred while adding the show', 'error': str(e)}), 500


@app.route('/shows/<int:show_id>', methods=['GET'])
def get_show(show_id):
    try:
        show = Shows.query.filter_by(id=show_id).first()
        theatre = Theatre.query.get(show.theatre_id)
        remaining_tickets = theatre.capacity - show.sold_ticket_count
        data = {
            'show': show_schema.dump(show),
            'remaining_tickets': remaining_tickets,
        }
        if not show:
            return jsonify({'message': 'Show not found'}), 404
        return jsonify(data)

    except Exception as e:
        return jsonify({'message': 'Error occurred while fetching the show', 'error': str(e)}), 500


@app.route('/theatres/<int:theatre_id>/shows/<int:show_id>', methods=['PUT'])
@jwt_required() 
def edit_show(theatre_id, show_id):
    try:

        current_user = get_jwt_identity()
        if not current_user['is_admin']:
            return jsonify({'message': 'Unauthorized. Only admin users can access this action.'}), 403


        show = Shows.query.filter_by(id=show_id, theatre_id=theatre_id).first()

        if not show:
            return jsonify({'message': 'Show not found'}), 404

        data = request.get_json()
        name = data['name']
        tags = data['tags']
        date_str = data['date']
        start_time_str = data['start_time']
        end_time_str = data['end_time']
        price = data['price']

        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()

        # Check if the show timings overlap with existing shows in the same theatre
        existing_shows = Shows.query.filter(
            Shows.theatre_id == theatre_id,
            Shows.date == date,
            Shows.id != show_id,
            or_(
                and_(Shows.start_time <= start_time,
                     Shows.end_time > start_time),
                and_(Shows.start_time < end_time,
                     Shows.end_time >= end_time),
            ),
        ).all()

        if existing_shows:
            return jsonify({'message': 'Show timings overlap with existing shows.'}), 400

        show.name = name
        show.tags = tags
        show.date = date
        show.start_time = start_time
        show.end_time = end_time
        show.price = price

        db.session.commit()

        return show_schema.jsonify(show)

    except Exception as e:
        return jsonify({'message': 'Error occurred while handling the show', 'error': str(e)}), 500


@app.route('/theatres/<int:theatre_id>/shows/<int:show_id>', methods=['DELETE'])
@jwt_required()  
def delete_show(theatre_id, show_id):
    try:

        current_user = get_jwt_identity()
        if not current_user['is_admin']:
            return jsonify({'message': 'Unauthorized. Only admin users can access this action.'}), 403

        show = Shows.query.filter_by(id=show_id, theatre_id=theatre_id).first()

        if not show:
            return jsonify({'message': 'Show not found'}), 404
        
        transactions = TransactionTable.query.filter_by(show_id=show_id).all()
        for transaction in transactions:
            db.session.delete(transaction)

        db.session.delete(show)
        db.session.commit()

        return jsonify({'message': 'Show deleted successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'Error occurred while deleting the show', 'error': str(e)}), 500





# USER SEES THEATRE AND SHOWS
# API to get all theatres and their shows that haven't started yet
@app.route('/alltheatres', methods=['GET'])
def get_all_theatres_with_shows():
    try:
        theatres = Theatre.query.all()

        current_date = datetime.now().date()
        current_time = datetime.now().time()

        upcoming_shows = []
        for theatre in theatres:
            shows = Shows.query.filter_by(theatre_id=theatre.id).filter(
                Shows.date > current_date,
                or_(
                    Shows.date == current_date,
                    Shows.date.isnot(None),
                )
            ).all()

            # Filter shows that haven't started yet
            shows = [show for show in shows if show.date > current_date or (show.date == current_date and show.start_time > current_time)]

            if shows:
                theatre_data = {
                    'id': theatre.id,
                    'name': theatre.name,
                    'place': theatre.place,
                    'location': theatre.location,
                    'capacity': theatre.capacity,
                    'shows': shows_schema.dump(shows),
                }
                upcoming_shows.append(theatre_data)

        return jsonify(upcoming_shows)
    except Exception as e:
        return jsonify({'message': 'Error occurred while fetching theatres and shows', 'error': str(e)}), 500


# book tickets for a show

@app.route('/book_ticket/<int:show_id>', methods=['POST'])
@jwt_required() 
def book_ticket(show_id):
    try:
        
        current_user = get_jwt_identity()
        user_id = current_user['id']

        show = Shows.query.get(show_id)
        show_name = show.name
        start_time = show.start_time.strftime('%H:%M')
        end_time = show.end_time.strftime('%H:%M')
        show_date = show.date.strftime('%Y-%m-%d')
        theatre_name = Theatre.query.get(show.theatre_id).name

        if not show:
            return jsonify({'message': 'Show not found'}), 404

        data = request.get_json()
        no_of_tickets = data['no_of_tickets']

        if no_of_tickets <= 0:
            return jsonify({'message': 'Invalid number of tickets'}), 400

        amount = no_of_tickets * show.price

        # Check if there are enough tickets available
        theatre = Theatre.query.get(show.theatre_id)
        remaining_tickets = theatre.capacity - show.sold_ticket_count
        if remaining_tickets < no_of_tickets:
            return jsonify({'message': 'Not enough tickets available'}), 400

        show.sold_ticket_count += no_of_tickets

        new_transaction = TransactionTable(user_id=user_id, show_id=show_id, date=datetime.today(), no_of_tickets=no_of_tickets, amount=amount)
        db.session.add(new_transaction)
        db.session.commit()

        # Send an email to the user with the ticket details
        task.ticket_mail.delay(user_id, show_name, no_of_tickets, amount, start_time, end_time, show_date, theatre_name)

        return transaction_schema.jsonify(new_transaction)

    except Exception as e:
        return jsonify({'message': 'Error occurred while booking the ticket', 'error': str(e)}), 500



# API endpoint to fetch bookings along with related Theatre and Show information
@app.route('/my_bookings', methods=['GET'])
@jwt_required()
def my_bookings():
    try:

        current_user = get_jwt_identity()
        user_id = current_user['id']


        bookings = TransactionTable.query \
            .join(Shows, TransactionTable.show_id == Shows.id) \
            .join(Theatre, Shows.theatre_id == Theatre.id) \
            .add_columns(TransactionTable.id,
                         TransactionTable.user_id,
                         TransactionTable.show_id,
                         TransactionTable.date,
                         TransactionTable.no_of_tickets,
                         TransactionTable.amount,
                         TransactionTable.rating,
                         Theatre.name.label('theatre_name'),
                         Shows.name.label('show_name')) \
            .filter(TransactionTable.user_id == user_id) \
            .all()


        booking_data = [booking_schema.dump(row._asdict()) for row in bookings]

        return jsonify(booking_data)

    except Exception as e:
        return jsonify({'message': 'Error occurred while fetching bookings', 'error': str(e)}), 500


# API endpoint to update the rating for a booking
@app.route('/update_rating', methods=['POST'])
@jwt_required()
def update_rating():
    try:
        data = request.json
        booking_id = data.get('booking_id')
        rating = data.get('rating')

        current_user = get_jwt_identity()
        user_id = current_user['id']
        booking = TransactionTable.query.filter_by(id=booking_id, user_id=user_id).first()

        if not booking:
            return jsonify({'message': 'Booking not found or does not belong to the current user'}), 404

        booking.rating = rating
        db.session.commit()

        show_id = booking.show_id
        average_rating = db.session.query(func.avg(TransactionTable.rating)).filter_by(show_id=show_id).scalar()

        show = Shows.query.filter_by(id=show_id).first()
        show.rating = average_rating
        db.session.commit()

        return jsonify({'message': 'Rating updated successfully'})

    except Exception as e:
        return jsonify({'message': 'Error occurred while updating rating', 'error': str(e)}), 500


#Plotting the graphs
@app.route('/admin_ticket_stats', methods=['GET'])
@jwt_required()
@cache.cached(timeout=600)
def admin_ticket_stats():
    try:
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return jsonify({'message': 'Access denied. Only ADMINs can access this endpoint.'}), 403

        ticket_stats = db.session.query(
            db.func.date(TransactionTable.date).label('date'),
            db.func.sum(TransactionTable.no_of_tickets).label('total_tickets')
        ).join(TransactionTable.show).join(Shows.theatre).filter(Shows.theatre.has(created_by=current_user['id'])).group_by(db.func.date(TransactionTable.date)).all()
        print(ticket_stats)
        dates = [row.date for row in ticket_stats]
        total_tickets = [row.total_tickets for row in ticket_stats]

        plt.figure(figsize=(10, 6))
        plt.plot(dates, total_tickets, marker='o')
        plt.title('Total Tickets Sold per Day by ADMIN')
        plt.xlabel('Date')
        plt.ylabel('Total Tickets Sold')
        plt.xticks(rotation=45)
        plt.tight_layout()

        plot_filename = 'admin_ticket_stats_plot.png'
        plt.savefig(plot_filename)

        plt.close()

        return jsonify({'message': 'Line chart generated successfully.', 'plot_url': plot_filename})

    except Exception as e:
        return jsonify({'message': 'Error occurred while generating line chart', 'error': str(e)}), 500

@app.route('/admin_show_revenue_stats', methods=['GET'])
@jwt_required()
@cache.cached(timeout=600)
def admin_show_revenue_stats():
    try:

        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return jsonify({'message': 'Access denied. Only ADMINs can access this endpoint.'}), 403

        show_revenue_stats = db.session.query(
            Shows.name.label('show_name'),
            db.func.sum(TransactionTable.amount).label('total_revenue')).join(Shows.theatre).join(TransactionTable, TransactionTable.show_id == Shows.id).filter(Shows.theatre.has(created_by=current_user['id'])).group_by(Shows.name).all()


        show_names = [row.show_name for row in show_revenue_stats]
        total_revenues = [row.total_revenue for row in show_revenue_stats]

        plt.figure(figsize=(10, 6))
        x = np.arange(len(show_names))
        plt.bar(x, total_revenues, tick_label=show_names)
        plt.title('Revenues from Shows Created by ADMIN')
        plt.xlabel('Show Name')
        plt.ylabel('Total Revenue')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        plot_filename = 'admin_show_revenue_plot.png'
        plt.savefig(plot_filename)

        plt.close()
    
        return jsonify({'message': 'Bar graph generated successfully.', 'plot_url': plot_filename})

    except Exception as e:
        return jsonify({'message': 'Error occurred while generating bar graph', 'error': str(e)}), 500

from flask import send_file

@app.route('/plot_images/<filename>', methods=['GET'])
def serve_plot_image(filename):
    return send_file(f'{filename}', mimetype='image/png')

@app.route('/generate_csv', methods=['GET'])
@cache.cached(timeout=600)
@jwt_required()
def generate_csv():
    current_user = get_jwt_identity()

    user = User.query.get(current_user['id'])
    if not user.is_admin:
        return Response('You do not have permission to access this resource', status=403)

    transactions = db.session.query(TransactionTable, User, Shows, Theatre) \
        .join(Shows, TransactionTable.show_id == Shows.id) \
        .join(Theatre, Shows.theatre_id == Theatre.id) \
        .filter(Theatre.created_by == User.id, User.is_admin == True) \
        .all()

    # Prepare CSV data
    output = io.StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerow(['Transaction ID', 'User Name', 'Show Name', 'Theatre', 'Date', 'No of Tickets', 'Total Amount'])

    for transaction, user, show, theatre in transactions:
        user_who_booked = User.query.get(transaction.user_id)
        csv_writer.writerow([
            transaction.id,
            user_who_booked.name,
            show.name,
            theatre.name,
            transaction.date,
            transaction.no_of_tickets,
            transaction.amount
        ])

    response = Response(output.getvalue(), content_type='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=transactions.csv'
    return response

@app.route('/clear_cache', methods=['POST'])
@jwt_required()
def clear_cache():
    current_user = get_jwt_identity()
    if current_user.get('is_admin'):
        cache.clear()
        return jsonify({'message': 'Cache cleared successfully'}), 200
    else:
        return jsonify({'message': 'Access denied. Only ADMINs can clear the cache.'}), 403

if __name__ == "__main__":
    app.run(debug=True)

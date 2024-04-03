from .workers import celery
from celery.schedules import crontab
from flask import render_template
from models import User, Theatre, Shows, TransactionTable, db
from .mailer import send_email
from sqlalchemy import and_
from datetime import datetime, timedelta

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    #sender.add_periodic_task(crontab(hour=10, minute=0), daily_reminder.s(), name='every_day_at_10_AM')
    sender.add_periodic_task(crontab(minute='*/1'), monthly_report.s(), name='every 1 minutes')
    #sender.add_periodic_task(crontab(minute=0, hour=0, day_of_month=1), monthly_report.s(), name='At 00:00 on day-of-month 1')

@celery.task
def add_together():
    a=1
    b=2
    return a+b

@celery.task
def ticket_mail(user_id, show_name, no_of_tickets, amount, start_time, end_time, show_date, theatre_name):
    user = query_user(user_id)
    subject = "Your Ticket was Successfully Booked!"
    body = render_template(
        'booked.html',
        user=user,
        show_name=show_name,
        no_of_tickets=no_of_tickets,
        amount=amount,
        start_time=start_time,
        end_time=end_time,
        show_date=show_date,
        theatre_name=theatre_name
    )
    send_email(user.email, subject, body)

@celery.task
def daily_reminder():
    users = query_all_users()
    for user in users:
        if not find_if_booked_yesterday(user.id) and not user.is_admin:
            dailymail(user)

@celery.task
def monthly_report():
    users = query_all_users()
    for user in users:
        email = user.email
        subject = "Your Monthly Report"
        (show_info_list, highest_rated_show, total_tickets_bought) = monthly_mail(user)
        body = render_template('report.html', show_info_list=show_info_list, highest_rated_show=highest_rated_show, total_tickets_bought=total_tickets_bought)
        send_email(email, subject, body)


def dailymail(user):
    name = user.name
    email = user.email
    subject = "Daily Reminder"
    body = f"Hi {name},\n\nWe missed you, you haven't booked any tickets yesterday\n\nRegards,\nTicketShow Team"
    send_email(email, subject, body)
    
def find_if_booked_yesterday(user_id):
    today = datetime.today().date()
    yesterday = today - datetime.timedelta(days=1)

    bookings = TransactionTable.query.filter_by(user_id=user_id, date=yesterday).all()

    if bookings:
        return True
    else:
        return False

def query_all_users():
    users = User.query.all()
    return users

def query_user(user_id):
    user = User.query.get(user_id)
    return user

def monthly_mail(user):

    today = datetime.today().date()
    last_month = today - timedelta(days=30)
    shows_watched_last_month = (db.session.query(TransactionTable, Shows).join(Shows, TransactionTable.show_id == Shows.id).filter(
            and_(
                TransactionTable.user_id == user.id,
                TransactionTable.date >= last_month,
                TransactionTable.date <= today
            )
        )
        .all()
    )

    show_info_list = []
    highest_rated_show = None
    highest_rating = 0.0
    total_tickets_bought = 0

    for transaction, show in shows_watched_last_month:
        show_info = {
            "name": show.name,
            "date": transaction.date,
            "no_of_tickets": transaction.no_of_tickets,
            "rating": transaction.rating,
        }
        show_info_list.append(show_info)

        if transaction.rating is not None and transaction.rating > highest_rating:
            highest_rated_show = show.name
            highest_rating = transaction.rating

        total_tickets_bought += transaction.no_of_tickets

    return (show_info_list, highest_rated_show, total_tickets_bought)
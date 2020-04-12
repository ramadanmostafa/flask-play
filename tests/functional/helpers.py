from app import app, db
from sure import scenario


def before_each_test(context):
    app.config.from_object('config_testing')
    db.session.close()
    db.drop_all()
    db.create_all()
    context.web = app
    context.http = context.web.test_client()


def after_each_test(context):
    # I would clean up the database here, if I had one
    db.session.close()
    db.drop_all()


web_test = scenario(before_each_test, after_each_test)

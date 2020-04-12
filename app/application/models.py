from app import db

from .utils import get_md5


class Base(db.Model):

    __abstract__ = True

    id  = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class User(Base):

    __tablename__ = 'auth_user'

    # User Name
    first_name = db.Column(db.String(128),  nullable=False)

    uuid = db.Column(db.String, unique=True)
    email = db.Column(db.String(128),  nullable=False, unique=True)
    password = db.Column(db.String(192),  nullable=False)

    def __repr__(self):
        return self.email

    def update_user(self, first_name, email, password):
        if first_name:
            self.first_name = first_name
        if email:
            self.email = email
        if password:
            self.password = get_md5(password)
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'email': self.email,
            'uuid': self.uuid,
        }

    @staticmethod
    def create_user(first_name, email, password):
        user = User(
            first_name=first_name,
            email=email,
            password=get_md5(password),
            uuid=get_md5(data='{}:{}'.format(first_name, email))
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def delete_by_email(email: str) -> (bool, dict):
        user = User.query.filter_by(email=email).first()
        if not user:
            return False, {}
        db.session.delete(user)
        db.session.commit()
        return True, user.to_dict()

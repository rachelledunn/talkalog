"""Models and database functions for Hackbright project."""

from flask_sqlalchemy import SQLAlchemy

# Connection to the SQLite database via Flask-SQLAlchemy helper library. 
# On this, we can find the `session` object.

db = SQLAlchemy()

##############################################################################
# Model definitions

class User(db.Model):
    """User of audio website."""

    __tablename__ = "Users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id: %s email: %s first_name: %s last_name: %s>" % (
        self.user_id, self.email, self.first_name, self.last_name)


class Upload(db.Model):
    """Uploaded items of website."""

    __tablename__ = "Uploads"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    title = db.Column(db.String, nullable=False, default='Untitled')
    description = db.Column(db.String)
    path = db.Column(db.String(50)) # arecording.mp3
    mimetype = db.Column(db.String(50)) # jpg, mp3

    user = db.relationship("User", backref=db.backref("uploads", order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Upload id: %s user_id: %s title: %s description: %s path: %s mimetype: %s>" % (
        self.id, self.user_id, self.title, self.description, self.path, self.mimetype)


class RequestURLs(db.Model):
    """Request URLs: id will be a unique hashed string associated
    with one user account. When a file is recorded at that page,
    path is then stored in Uploads and associated with user id."""

    __tablename__ = "RequestURLs"

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    upload_id = db.Column(db.Integer, db.ForeignKey('Uploads.id'), nullable=False)

    user = db.relationship("User", backref=db.backref("collections", order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Request URL id: %s user_id: %s upload_id: %s>" % (
        self.id, self.user_id, self.upload_id)


class Collection(db.Model):
    """Collections of uploads"""

    __tablename__ = "Collections"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    title = db.Column(db.String, nullable=False, default='Untitled Collection')
    description = db.Column(db.String)

    user = db.relationship("User", backref=db.backref("collections", order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Collection id: %s user_id: %s title: %s description: %s>" % (
        self.id, self.user_id, self.title, self.description)


class CollectionsUsers(db.Model):
    """Association table: which users have access to 
    which collections."""

    __tablename__ = "CollectionsUsers"

    id = db.Column(db.String, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('Collections.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)

    collection = db.relationship("Collection", backref=db.backref("collectionsusers", order_by=id))
    user = db.relationship("User", backref=db.backref("collectionsusers", order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<CollectionsUsers id: %s collection_id: %s user_id: %s>" % (
        self.id, self.collection_id, self.user_id)


class CollectionsUploads(db.Model):
    """Association table: which uploads are included within
    which collections."""

    __tablename__ = "CollectionsUploads"

    id = db.Column(db.String, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('Collections.id'), nullable=False)
    upload_id = db.Column(db.Integer, db.ForeignKey('Uploads.id'), nullable=False)

    collection = db.relationship("Collection", backref=db.backref("collectionsuploads", order_by=id))
    upload = db.relationship("Upload", backref=db.backref("collectionsuploads", order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<CollectionsUsers id: %s collection_id: %s user_id: %s>" % (
        self.id, self.collection_id, self.user_id)


# Helper functions

def connect_to_db(app):
    """Connect the database to Flask app."""

    # Configure to use SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audiomemo.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # If this module is run interactively, enable
    # work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
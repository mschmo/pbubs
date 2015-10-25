from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def full_commit():
    """A convenience function for executing a transaction with automatic
    rollback when an exception occurs. The exception is re-raised.
    """
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise


class ActiveModel(object):
    """A mixin intended to provide convenient functions for repeated SQLAlchemy
    patterns.
    """
    def save(self, commit=True, *args, **kwargs):
        """Adds the current state of the object to the db session and COMMITs
        the transaction if requested.

        Returns a reference to self for convenience
        """
        db.session.add(self)
        if commit:
            full_commit()
        return self

    def remove(self, commit=True):
        """Deletes the current state of the object in the db session and COMMITs
        the transaction if requested.

        Returns a reference to self for convenience
        """
        db.session.delete(self)
        if commit:
            full_commit()
        return self

    def refresh(self):
        """Immediately re-load attributes from the db.
        """
        db.session.refresh(self)

    def expire(self):
        """Mark the object so that on next access the attributes are refreshed.
        """
        db.session.expire(self)
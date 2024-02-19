from app import db
from application.models import User, Role, Section, Book
import json

db.create_all()


## roles json
roley = [{"id":1,"name":"admin","description":"girlboss librarian admin"},
         {"id":2,"name":"basicuser","description":"basic user"},
         {"id":3,"name":"issuer","description":"currently has reading access to book till return date"},
         {"id":4,"name":"has_read","description":"has been issued book at some point so can review"},
         {"id":5,"name":"owner","description":"purchased book so lifetime reading access and can download book as pdf"}]

## sections json
secs = [{"id":1,"title":"Fantasy","date_created":"2024-02-10","description":"Fantasy is a genre of fiction that features imaginary and unrealistic elements. It often involves supernatural powers, like magic and magical creatures.","avg_rating":None},
        {"id":2,"title":"Horror","date_created":"2024-02-11","description":"Horror is a genre of fiction that is intended to disturb, frighten or scare. Horror is often divided into the sub-genres of psychological horror and supernatural horror, which are in the realm of speculative fiction.","avg_rating":None},
        {"id":3,"title":"Science Fiction","date_created":"2024-02-12","description":"Science fiction (sometimes shortened to SF or sci-fi) is a genre of speculative fiction, which typically deals with imaginative and futuristic concepts such as advanced science and technology, space exploration, time travel, parallel universes, and extraterrestrial life.","avg_rating":None},
        {"id":4,"title":"Classics","date_created":"2024-02-19","description":"A classic stands the test of time. The work is usually considered to be a representation of the period in which it was written; and the work merits lasting recognition.","avg_rating":None}]


# adding roles

for role in roley:
    new_role = Role(name=role['name'], description=role['description'])
    db.session.add(new_role)
db.session.commit()

# adding an admin and a user
girl = User(username='athena', password='admin1234')
cat = User(username='ara', password='1234')
db.session.add(girl)
db.session.add(cat)
db.session.commit()

# adding roles to users
girl.roles.append(Role.query.filter_by(name='admin').first())
cat.roles.append(Role.query.filter_by(name='basicuser').first())
db.session.commit()


# create starter sections

for section in secs:
    new_section = Section(title=section['title'], description=section['description'])
    db.session.add(new_section)
db.session.commit()



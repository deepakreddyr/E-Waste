from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash,request
from flask_bootstrap import Bootstrap5
# from flask_ckeditor import CKEditor
# from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

from forms import  RegisterForm, LoginForm



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


equip_dict={
        'Central Heating ( household installed )':5000,
       'Photovoltaic Panels ( ind . inverters )':5000,
       'Professional Heating & Ventilation ( excl . cooling equipment )':5000,
       'Dishwashers':5000,
       'Kitchen equipment ( eg . large furnaces , ovens , cooking equipment )':5000,
       'Washing Machines ( ind , combined dryers )':5000,
       'Dryers ( wash dryers , centrifuges )':5000,
       'Household Heating & Ventilation ( eg , hoods , ventilators , space heaters )':5000,
       'Fridges ( incl . combi Indges )':5000, 'Freezers':5000,
       'Air Conditioners ( household installed and portable )':5000,
       'Other cooling equipment ( eg , dehumidifiers , heat pump dryers )':5000,
       'Professional cooling equipment\n( eg , large air conditioners , cooling displays )':5000,
       'Microwaves ( inc , combined ex . grils )':2000,
       'Other small household equipment\n( e.g. small ventilators , irons , clocks , adapters )':2000,
       'Equipment for food preparation\n( e.g. toaster , grills , food processing , frying pans )':2000,
       'Small household equipment for hot water preparation\n( eg , coffee , tea , water cookers )':2000,
       'Vacuum Cleaners ( exc . professional )':2000,
       'Personal Care equipment ( eg toothbrushes , hairdryers , razors )':2000,
       'Small IT equipment\n( eg , routers , mice , keyboards , external drives & accessories )':1000,
       'Desktop PCs ( excl monitors , accessories )':1000,
       'Laptops ( incl . tablets )':1000,
       'Printers ( e.g. scanners , multi - functionals , faxes )':1000,
       'Telecommunication equipment ( e.g. cordless phones , answering machines )':1000,
       'Mobile Phones ( ind , smartphones , pagers )':1000,
       'Professional IT equipment ( e.g. servers , routers , data storage , copiers )':1000,
       'Cathode Ray Tube Monitors':500,
       'Fat Display Panel Monitors ( LCD , LED )':750,
       'Small Consumer Electronics ( eg , headphones , remote controls )':150,
       'Portable Audio & Video ( eg MP3 , e - readers , carnavigation )':150,
       'Music Instruments , Radio , Hi - Fi ( incl . audio sets )':150,
       'Video ( eg Video recorders , DVD , Blue Ray , set - top boxes ) and projectors':1500,
       'Speakers':500,
       'Cameras ( eg , camcorders , photo & digital still cameras )':1000,
       "Cathode Ray Tube TV's":250,
       'Flat Display Panel TVs ( LCD , LED , Plasma )':800,
       'Small lighting equipment ( exd . LED & incandescent )':50,
       'Compact Fluorescent Lamps ( ind retrofit & non - retrofit )':50,
       'Straight Tube Fluorescent Lamps':50,
       'Special Lamps ( eg professional mercury high & low pressure sodium )':50,
       'LED Lamps ( incl retrofit LED lamps )':70,
       'Household Luminaires ( ind , household incandescent fittings & household LED\nLuminaires )':50,
       'Professional Luminaires ( offices public space , industry )':70,
       'Professional Luminaires ( offices , public space , industry )':70,
       'Household Tools ( eg , drils , saws , high pressure cleaners , lawn mowers )':700,
       'Professional Tools ( eg , for welding , soldering , miling )':700,
       'Toys ( eg , car racing sets , electric trains , music toys .\nbiking computers , drones )':0,
       'Game Consoles':500,
       'Leisure equipment ( eg sports equipment , electric bikes , juke boxes )':4500,
       'Household medical equipment( eg thermometers , blood pressure meters )':50,
       'Professional medical equipment ( e.g. hospital , dentist , diagnostics )':5000,
       'Household Monitoring & Control equipment\n( alarm , heat , smoke , excl screens )':75,
       'Professional Monitoring & Control equipment\n( eg , laboratory , control panel )':500,
}


from flask_wtf import FlaskForm
from wtforms import SelectField

class EquipmentForm(FlaskForm):
    equipment = SelectField('Select an item', choices=[
        ('item1', 'Central Heating (household installed)'),
        ('item2', 'Photovoltaic Panels (ind. inverters)'),
        ("item3", "Professional Heating & Ventilation (excl. cooling equipment)"),
        ("item4", "Dishwashers"),
        ("item5", "Kitchen equipment (e.g. large furnaces, ovens, cooking equipment)"),
        ("item6", "Washing Machines (ind, combined dryers)"),
        ("item7", "Dryers (wash dryers, centrifuges)"),
        ("item8", "Household Heating & Ventilation (e.g., hoods, ventilators, space heaters)"),
        ("item9", "Fridges (incl. combi fridges)"),
        ("item10", "Freezers"),
        ("item11", "Air Conditioners (household installed and portable)"),
        ("item12", "Other cooling equipment (e.g., dehumidifiers, heat pump dryers)"),
        ("item13", "Professional cooling equipment (e.g., large air conditioners, cooling displays)"),
        ("item14", "Microwaves (incl. combined ex. grills)"),
        ("item15", "Other small household equipment (e.g., small ventilators, irons, clocks, adapters)"),
        ("item16", "Equipment for food preparation (e.g., toaster, grills, food processing, frying pans)"),
        ("item17", "Small household equipment for hot water preparation (e.g., coffee, tea, water cookers)"),
        ("item18", "Vacuum Cleaners (exc. professional)"),
        ("item19", "Personal Care equipment (e.g., toothbrushes, hairdryers, razors)"),
        ("item20", "Small IT equipment (e.g., routers, mice, keyboards, external drives & accessories)"),
        ("item21", "Desktop PCs (excl monitors, accessories)"),
        ("item22", "Laptops (incl. tablets)"),
        ("item23", "Printers (e.g. scanners, multi-functionals, faxes)"),
        ("item24", "Telecommunication equipment (e.g. cordless phones, answering machines)"),
        ("item25", "Mobile Phones (ind, smartphones, pagers)"),
        ("item26", "Professional IT equipment (e.g. servers, routers, data storage, copiers)"),
        ("item27", "Cathode Ray Tube Monitors"),
        ("item28", "Flat Display Panel Monitors (LCD, LED)"),
        ("item29", "Small Consumer Electronics (e.g., headphones, remote controls)"),
        ("item30", "Portable Audio & Video (e.g. MP3, e-readers, car navigation)"),
        ("item31", "Music Instruments, Radio, Hi-Fi (incl. audio sets)"),
        ("item32", "Video (e.g. Video recorders, DVD, Blue Ray, set-top boxes) and projectors"),
        ("item33", "Speakers"),
        ("item34", "Cameras (e.g., camcorders, photo & digital still cameras)"),
        ("item35", "Cathode Ray Tube TV's"),
        ("item36", "Flat Display Panel TVs (LCD, LED, Plasma)"),
        ("item37", "Small lighting equipment (excl. LED & incandescent)"),
        ("item38", "Compact Fluorescent Lamps (ind retrofit & non-retrofit)"),
        ("item39", "Straight Tube Fluorescent Lamps"),
        ("item40", "Special Lamps (e.g. professional mercury high & low-pressure sodium)"),
        ("item41", "LED Lamps (incl retrofit LED lamps)"),
        ("item42", "Household Luminaires (ind, household incandescent fittings & household LED Luminaires)"),
        ("item43", "Professional Luminaires (offices public space, industry)"),
        ("item44", "Professional Luminaires (offices, public space, industry)"),
        ("item45", "Household Tools (e.g., drills, saws, high-pressure cleaners, lawn mowers)"),
        ("item46", "Professional Tools (e.g., for welding, soldering, milling)"),
        ("item47", "Toys (e.g., car racing sets, electric trains, music toys, biking computers, drones)"),
        ("item48", "Game Consoles"),
        ("item49", "Leisure equipment (e.g. sports equipment, electric bikes, jukeboxes)"),
        ("item50", "Household medical equipment (e.g. thermometers, blood pressure meters)"),
        ("item51", "Professional medical equipment (e.g. hospital, dentist, diagnostics)"),
        ("item52", "Household Monitoring & Control equipment (alarm, heat, smoke, excl screens)"),
        ("item53", "Professional Monitoring & Control equipment (e.g. laboratory, control panel)"),
        ("item54", "Non-cooled Dispensers (e.g. for vending, hot drinks, tickets, money)"),
        ("item55", "Cooled Dispensers (e.g. for vending, cold drinks)")
    ])
    

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Users, user_id)


# For adding profile images to the comment section


# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WASTE.db'
db = SQLAlchemy()
db.init_app(app)




# Create a User table for all your registered users
class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    reward=db.Column(db.Integer, default=0)



with app.app_context():
    db.create_all()


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        result = db.session.execute(db.select(Users).where(Users.email == form.email.data))
        user = result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = Users(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("get_reward"))
    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(Users).where(Users.email == form.email.data))
        user = result.scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            print(f"WELCOME {user.name}")
            login_user(user)
            return redirect(url_for('get_reward'))

    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def get_reward():
    current_user.reward = 10
    db.session.commit()
    print(f'Your reward is: {current_user.reward}')
    form = EquipmentForm()
    if form.validate_on_submit():
        equipment_value = form.equipment.data
        if equipment_value in equip_dict:
            print("This form is working")
            reward_points = equip_dict[equipment_value]
            current_user.reward = 15
            db.session.commit()
            print(f'Your reward is: {current_user.reward}')
            return redirect(url_for("get_reward"))
    return render_template("index.html", form=form, current_user=current_user)

@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/contact")
def contact():
    return render_template("contact.html", current_user=current_user)


if __name__ == "__main__":
    app.run(debug=True, port=5001)

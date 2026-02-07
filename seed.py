from datetime import date
from flask import Flask
from config import Config
from models import db, Politician, Campaign, Promise, PromiseUpdate, User

def make_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

app = make_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    db.session.add_all([
        User(username="admin", password="admin123", role="admin"),
        User(username="user",  password="user123",  role="user"),
    ])

    pols = [
        Politician(politician_id="12345678", name="Ananda K.", party="Future Party"),
        Politician(politician_id="23456789", name="Benja S.", party="People First"),
        Politician(politician_id="34567891", name="Chai W.", party="Green Nation"),
        Politician(politician_id="45678912", name="Dara P.", party="Unity Bloc"),
        Politician(politician_id="56789123", name="Ekkachai R.", party="Progress Thai"),
        Politician(politician_id="67891234", name="Fah N.", party="New Horizon"),
        Politician(politician_id="78912345", name="Kawin T.", party="Citizen Power"),
        Politician(politician_id="89123456", name="Lalita M.", party="Forward Vision"),
        Politician(politician_id="91234567", name="Narin P.", party="Green Future"),
        Politician(politician_id="19876543", name="Somchai D.", party="Thai Development"),
    ]
    db.session.add_all(pols)

    db.session.add_all([
        Campaign(year_of_campaign=2022, electoral_district="Bangkok เขต 1", politician_id="12345678"),
        Campaign(year_of_campaign=2022, electoral_district="Chiang Mai เขต 2", politician_id="23456789"),
        Campaign(year_of_campaign=2022, electoral_district="Chonburi เขต 3", politician_id="34567891"),
        Campaign(year_of_campaign=2023, electoral_district="Khon Kaen เขต 1", politician_id="45678912"),
        Campaign(year_of_campaign=2023, electoral_district="Phuket เขต 2", politician_id="56789123"),
        Campaign(year_of_campaign=2023, electoral_district="Nakhon Ratchasima เขต 4", politician_id="67891234"),
        Campaign(year_of_campaign=2024, electoral_district="Songkhla เขต 1", politician_id="78912345"),
        Campaign(year_of_campaign=2024, electoral_district="Udon Thani เขต 2", politician_id="89123456"),
        Campaign(year_of_campaign=2024, electoral_district="Rayong เขต 3", politician_id="91234567"),
        Campaign(year_of_campaign=2025, electoral_district="Nonthaburi เขต 1", politician_id="19876543"),
    ])

    promises = [
        Promise(politician_id="12345678", promise_details="Reduce public transport fares.", date_of_announcement=date(2022,5,10), promise_status="Has Begun"),
        Promise(politician_id="12345678", promise_details="Build 3 new community hospitals.", date_of_announcement=date(2022,5,15), promise_status="On Process"),

        Promise(politician_id="23456789", promise_details="Increase minimum wage to 450 THB/day.", date_of_announcement=date(2022,5,9), promise_status="On Process"),
        Promise(politician_id="23456789", promise_details="Free textbooks for all public schools.", date_of_announcement=date(2022,5,20), promise_status="No update"),

        Promise(politician_id="34567891", promise_details="Plant 1 million trees nationwide.", date_of_announcement=date(2022,4,28), promise_status="Has Begun"),
        Promise(politician_id="34567891", promise_details="Subsidy for solar rooftop installations.", date_of_announcement=date(2022,5,22), promise_status="No update"),

        Promise(politician_id="45678912", promise_details="One-stop digital government services.", date_of_announcement=date(2022,5,2), promise_status="On Process"),
        Promise(politician_id="45678912", promise_details="Improve flood drainage system.", date_of_announcement=date(2022,5,18), promise_status="Has Begun"),

        Promise(politician_id="56789123", promise_details="Free Wi-Fi in all public parks.", date_of_announcement=date(2022,5,5), promise_status="No update"),
        Promise(politician_id="56789123", promise_details="Support SMEs with low-interest loans.", date_of_announcement=date(2022,5,12), promise_status="On Process"),

        Promise(politician_id="67891234", promise_details="Develop EV charging stations nationwide.", date_of_announcement=date(2023,1,10), promise_status="Has Begun"),
        Promise(politician_id="67891234", promise_details="Reduce plastic waste by 30%.", date_of_announcement=date(2023,2,5), promise_status="On Process"),

        Promise(politician_id="78912345", promise_details="Free basic internet for rural areas.", date_of_announcement=date(2023,3,1), promise_status="No update"),
        Promise(politician_id="78912345", promise_details="Upgrade public libraries.", date_of_announcement=date(2023,3,15), promise_status="Has Begun"),

        Promise(politician_id="89123456", promise_details="Healthcare mobile units for remote villages.", date_of_announcement=date(2023,4,10), promise_status="On Process"),
        Promise(politician_id="89123456", promise_details="Mental health support hotline 24/7.", date_of_announcement=date(2023,4,20), promise_status="Has Begun"),

        Promise(politician_id="91234567", promise_details="Protect wetlands and wildlife areas.", date_of_announcement=date(2024,1,5), promise_status="No update"),
        Promise(politician_id="91234567", promise_details="Community recycling centers.", date_of_announcement=date(2024,1,18), promise_status="On Process"),

        Promise(politician_id="19876543", promise_details="Scholarships for low-income students.", date_of_announcement=date(2024,2,1), promise_status="Has Begun"),
        Promise(politician_id="19876543", promise_details="Reduce household electricity bills.", date_of_announcement=date(2024,2,14), promise_status="No update"),
    ]
    db.session.add_all(promises)
    db.session.commit()

    def add_updates(promise_details, updates):
        p = Promise.query.filter_by(promise_details=promise_details).first()
        for d, text in updates:
            db.session.add(PromiseUpdate(
                promise_id=p.promise_id,
                date_of_update=d,
                progress_details=text
            ))

    add_updates("Reduce public transport fares.", [
        (date(2022,6,1), "Draft policy submitted to council."),
        (date(2022,7,10), "Pilot program started on 2 lines."),
    ])

    add_updates("Build 3 new community hospitals.", [
        (date(2022,6,20), "Site survey completed for first hospital."),
    ])

    add_updates("Increase minimum wage to 450 THB/day.", [
        (date(2022,6,5), "Committee discussion ongoing."),
        (date(2022,8,1), "Draft law prepared."),
    ])

    add_updates("Plant 1 million trees nationwide.", [
        (date(2022,6,12), "Partnership with NGOs signed."),
    ])

    add_updates("Develop EV charging stations nationwide.", [
        (date(2023,3,20), "First 50 stations installed."),
        (date(2023,6,10), "Expanded to 120 stations."),
    ])

    add_updates("Upgrade public libraries.", [
        (date(2023,5,1), "Budget approved for 20 libraries."),
    ])

    db.session.commit()
    print("Seed complete with more sample data. Run: python app.py")

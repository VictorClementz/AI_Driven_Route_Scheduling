from datetime import datetime, time
from ..models.cleaner import Cleaner, Skill, WorkingHours
from ..models.job import Job, Priority
from typing import List

class DummyDataGenerator:
    """Generate realistic dummy data for Stockholm area"""

    @staticmethod
    def create_cleaners() -> List[Cleaner]:
        """Create sample cleaners with Stockholm-area addresses"""
        return [
            Cleaner(
                id="cleaner_001",
                name="Anna Andersson",
                email="anna@example.com",
                phone="070-123-4567",
                home_address="Södermalm, Stockholm",
                home_coordinates=(59.3165, 18.0707),  # ✅ Korrekt
                skills=[Skill.OFFICE_CLEANING, Skill.WINDOW_CLEANING, Skill.HOME_CLEANING, Skill.SNOW_SHOWELING, Skill.OUTDOOR_CLEANING, Skill.APARTMENT_CLEANING],
                languages=["svenska", "engelska"],
                working_hours=WorkingHours(start_time=time(8, 0), end_time=time(17, 0)),
                max_daily_hours=8.5
            ),
            Cleaner(
                id="cleaner_002",
                name="Erik Eriksson",
                email="erik@example.com",
                phone="070-234-5678",
                home_address="Vasastan, Stockholm",
                home_coordinates=(59.3433, 18.0521),  # ✅ Korrekt
                skills=[Skill.OFFICE_CLEANING, Skill.WINDOW_CLEANING, Skill.HOME_CLEANING, Skill.SNOW_SHOWELING, Skill.OUTDOOR_CLEANING, Skill.APARTMENT_CLEANING],
                languages=["svenska"],
                working_hours=WorkingHours(start_time=time(7, 0), end_time=time(16, 0)),
                max_daily_hours=9.0
            ),
            Cleaner(
                id="cleaner_006",
                name="Lina Berg",
                email="lina@example.com",
                phone="070-678-9012",
                home_address="Täby, Stockholm",
                home_coordinates=(59.4439, 18.0687),  # ⚠️ KORRIGERAD
                skills=[Skill.HOME_CLEANING, Skill.OFFICE_CLEANING, Skill.WINDOW_CLEANING],
                languages=["svenska", "engelska"],
                working_hours=WorkingHours(start_time=time(7, 30), end_time=time(16, 30)),
                max_daily_hours=8.0
            ),
            Cleaner(
                id="cleaner_007",
                name="Ali Mahmoud",
                email="ali@example.com",
                phone="070-789-0123",
                home_address="Sundbyberg, Stockholm",
                home_coordinates=(59.3630, 17.9723),  # ✅ Korrekt
                skills=[Skill.OUTDOOR_CLEANING, Skill.SNOW_SHOWELING, Skill.OFFICE_CLEANING],
                languages=["svenska", "arabiska", "engelska"],
                working_hours=WorkingHours(start_time=time(6, 0), end_time=time(15, 0)),
                max_daily_hours=8.5
            ),
            Cleaner(
                id="cleaner_008",
                name="Karin Larsson",
                email="karin@example.com",
                phone="070-890-1234",
                home_address="Huddinge, Stockholm",
                home_coordinates=(59.2371, 17.9819),  # ⚠️ KORRIGERAD
                skills=[Skill.HOME_CLEANING, Skill.APARTMENT_CLEANING, Skill.WINDOW_CLEANING],
                languages=["svenska"],
                working_hours=WorkingHours(start_time=time(8, 0), end_time=time(17, 0)),
                max_daily_hours=8.0
            ),
            Cleaner(
                id="cleaner_009",
                name="David Lindström",
                email="david@example.com",
                phone="070-901-2345",
                home_address="Vallentuna, Stockholm",
                home_coordinates=(59.5344, 18.0776),  # ⚠️ KORRIGERAD
                skills=[Skill.SNOW_SHOWELING, Skill.OUTDOOR_CLEANING, Skill.WINDOW_CLEANING],
                languages=["svenska", "engelska"],
                working_hours=WorkingHours(start_time=time(7, 0), end_time=time(16, 30)),
                max_daily_hours=9.0
            ),
            Cleaner(
                id="cleaner_010",
                name="Natalie Pettersson",
                email="natalie@example.com",
                phone="070-012-3456",
                home_address="Tyresö, Stockholm",
                home_coordinates=(59.2445, 18.2286),  # ⚠️ KORRIGERAD (Tyresö Centrum)
                skills=[Skill.HOME_CLEANING, Skill.APARTMENT_CLEANING],
                languages=["svenska", "ryska"],
                working_hours=WorkingHours(start_time=time(9, 0), end_time=time(18, 0)),
                max_daily_hours=8.5
            ),
            Cleaner(
                id="cleaner_005",
                name="Sara Karlsson",
                email="sara@example.com",
                phone="070-567-8901",
                home_address="Nacka, Stockholm",
                home_coordinates=(59.3109, 18.1647),  # ✅ Korrekt
                skills=[Skill.OFFICE_CLEANING, Skill.WINDOW_CLEANING, Skill.HOME_CLEANING, Skill.SNOW_SHOWELING, Skill.OUTDOOR_CLEANING, Skill.APARTMENT_CLEANING],
                languages=["svenska", "engelska"],
                working_hours=WorkingHours(start_time=time(8, 0), end_time=time(16, 30)),
                max_daily_hours=8.5
            ),
            Cleaner(
                id="cleaner_011",
                name="Johan Nilsson",
                email="johan@example.com",
                phone="070-111-2222",
                home_address="Järfälla, Stockholm",
                home_coordinates=(59.4235, 17.8357),  # Järfälla centrum
                skills=[Skill.OFFICE_CLEANING, Skill.HOME_CLEANING, Skill.SNOW_SHOWELING],
                languages=["svenska", "engelska"],
                working_hours=WorkingHours(start_time=time(7, 30), end_time=time(16, 30)),
                max_daily_hours=8.5
            ),
            Cleaner(
                id="cleaner_012",
                name="Maria Olsson",
                email="maria@example.com",
                phone="070-333-4444",
                home_address="Haninge, Stockholm",
                home_coordinates=(59.1697, 18.1425),  # Haninge centrum
                skills=[Skill.HOME_CLEANING, Skill.APARTMENT_CLEANING, Skill.WINDOW_CLEANING],
                languages=["svenska", "polska"],
                working_hours=WorkingHours(start_time=time(8, 0), end_time=time(17, 0)),
                max_daily_hours=8.0
            )
        ]

    @staticmethod
    def create_jobs() -> List[Job]:
        """Create sample jobs across Stockholm area"""
        now = datetime.now()
        return [
            Job(
                id="job_001",
                client_name="Swedbank Huvudkontor",
                address="Landsvägen 40, Sundbyberg",
                coordinates=(59.3613, 17.9711),
                required_skills=[Skill.OFFICE_CLEANING],
                estimated_duration_hours=2.5,
                preferred_start_time=time(9, 0),
                latest_start_time=time(11, 0),
                priority=Priority.HIGH,
                instructions="Konferensrum behöver extra uppmärksamhet",
                created_at=now
            ),
            Job(
                id="job_002",
                client_name="Konsulthuset Stockholm",
                address="Kungsgatan 12, Stockholm",
                coordinates=(59.3326, 18.0649),
                required_skills=[Skill.OFFICE_CLEANING],
                estimated_duration_hours=3.0,
                preferred_start_time=time(10, 0),
                latest_start_time=time(12, 0),
                priority=Priority.MEDIUM,
                instructions="Städa reception och mötesrum",
                created_at=now
            ),
            Job(
                id="job_003",
                client_name="Villa Södermalm",
                address="Folkungagatan 15, Stockholm",
                coordinates=(59.3135, 18.0785),
                required_skills=[Skill.HOME_CLEANING],
                estimated_duration_hours=4.0,
                preferred_start_time=time(10, 0),
                latest_start_time=time(13, 0),
                priority=Priority.URGENT,
                instructions="Djupstädning efter renovation",
                created_at=now
            ),
            Job(
                id="job_004",
                client_name="Kontorshuset Sollentuna",
                address="Tureberg centrum, Sollentuna",
                coordinates=(59.4280, 17.9510),
                required_skills=[Skill.WINDOW_CLEANING],
                estimated_duration_hours=1.5,
                preferred_start_time=time(13, 0),
                latest_start_time=time(15, 0),
                priority=Priority.LOW,
                instructions="Endast utsida av fönster",
                created_at=now
            ),
            Job(
                id="job_005",
                client_name="Lägenhet Östermalm",
                address="Strandvägen 25, Stockholm",
                coordinates=(59.3328, 18.0847),
                required_skills=[Skill.APARTMENT_CLEANING],
                estimated_duration_hours=2.0,
                preferred_start_time=time(11, 0),
                latest_start_time=time(14, 0),
                priority=Priority.MEDIUM,
                instructions="3-rummare, extra noggrann städning",
                created_at=now
            ),
            Job(
                id="job_006",
                client_name="Utomhusstädning Vasaparken",
                address="Vasaparken, Stockholm",
                coordinates=(59.3431, 18.0465),
                required_skills=[Skill.OUTDOOR_CLEANING],
                estimated_duration_hours=3.5,
                preferred_start_time=time(8, 0),
                latest_start_time=time(10, 0),
                priority=Priority.HIGH,
                instructions="Rensa löv och skräp från parkområde",
                created_at=now
            ),
            Job(
                id="job_007",
                client_name="Snöröjning Kista Centrum",
                address="Kista Centrum, Stockholm",
                coordinates=(59.4032, 17.9448),
                required_skills=[Skill.SNOW_SHOWELING],
                estimated_duration_hours=2.0,
                preferred_start_time=time(6, 0),
                latest_start_time=time(8, 0),
                priority=Priority.URGENT,
                instructions="Rensa entréer och parkeringsplatser",
                created_at=now
            ),
            Job(
                id="job_008",
                client_name="Fönsterputs Gallerian",
                address="Hamngatan 37, Stockholm",
                coordinates=(59.3325, 18.0685),
                required_skills=[Skill.WINDOW_CLEANING],
                estimated_duration_hours=4.0,
                preferred_start_time=time(9, 0),
                latest_start_time=time(11, 0),
                priority=Priority.MEDIUM,
                instructions="Alla våningar, både in- och utsida",
                created_at=now
            ),
            Job(
                id="job_009",
                client_name="Kontor Barkarby",
                address="Barkarbyvägen 35, Järfälla",
                coordinates=(59.4140, 17.8720),
                required_skills=[Skill.OFFICE_CLEANING],
                estimated_duration_hours=2.0,
                preferred_start_time=time(9, 30),
                latest_start_time=time(11, 0),
                priority=Priority.MEDIUM,
                instructions="Extra fokus på kök och fikarum",
                created_at=now
            ),
            Job(
                id="job_010",
                client_name="Villa Tyresö Strand",
                address="Strandvägen 3, Tyresö",
                coordinates=(59.2380, 18.2290),
                required_skills=[Skill.HOME_CLEANING],
                estimated_duration_hours=2.5,
                preferred_start_time=time(12, 0),
                latest_start_time=time(14, 0),
                priority=Priority.LOW,
                instructions="Husdjur i hemmet, använd allergivänliga produkter",
                created_at=now
            ),
            Job(
                id="job_011",
                client_name="Radhus Huddinge",
                address="Kvarnbergsplan 1, Huddinge",
                coordinates=(59.2361, 17.9813),
                required_skills=[Skill.HOME_CLEANING],
                estimated_duration_hours=2.0,
                preferred_start_time=time(10, 0),
                latest_start_time=time(12, 0),
                priority=Priority.MEDIUM,
                instructions="Dammsugning av hela övervåningen",
                created_at=now
            ),
            Job(
                id="job_012",
                client_name="Lager Tumba",
                address="Tumbavägen 12, Tumba",
                coordinates=(59.1990, 17.8335),
                required_skills=[Skill.OUTDOOR_CLEANING],
                estimated_duration_hours=3.0,
                preferred_start_time=time(8, 0),
                latest_start_time=time(9, 30),
                priority=Priority.HIGH,
                instructions="Sopa upp sand från infart och lastzon",
                created_at=now
            ),
            Job(
                id="job_013",
                client_name="Förskola Haninge",
                address="Handenterminalen 5, Haninge",
                coordinates=(59.1678, 18.1395),
                required_skills=[Skill.OFFICE_CLEANING],
                estimated_duration_hours=2.5,
                preferred_start_time=time(13, 0),
                latest_start_time=time(15, 0),
                priority=Priority.MEDIUM,
                instructions="Sanering av lekrum efter magsjuka",
                created_at=now
            ),
            Job(
                id="job_014",
                client_name="Villa Täby Kyrkby",
                address="Kyrkvägen 15, Täby",
                coordinates=(59.4970, 18.0570),
                required_skills=[Skill.HOME_CLEANING],
                estimated_duration_hours=2.0,
                preferred_start_time=time(11, 0),
                latest_start_time=time(13, 0),
                priority=Priority.HIGH,
                instructions="Fokus på badrum och kök",
                created_at=now
            ),
            Job(
                id="job_015",
                client_name="Städning Brommaplan",
                address="Brommaplan 401, Bromma",
                coordinates=(59.3394, 17.9390),
                required_skills=[Skill.APARTMENT_CLEANING],
                estimated_duration_hours=2.5,
                preferred_start_time=time(9, 0),
                latest_start_time=time(11, 30),
                priority=Priority.MEDIUM,
                instructions="Fönsterputs inkluderat",
                created_at=now
            ),
            Job(
                id="job_016",
                client_name="Skola Nacka",
                address="Forumvägen 12, Nacka",
                coordinates=(59.3108, 18.1631),
                required_skills=[Skill.OFFICE_CLEANING],
                estimated_duration_hours=3.0,
                preferred_start_time=time(10, 0),
                latest_start_time=time(12, 0),
                priority=Priority.HIGH,
                instructions="Lärarrum samt gemensamma ytor",
                created_at=now
            ),
            Job(
                id="job_017",
                client_name="Snöröjning Jakobsberg",
                address="Järfällavägen 110, Järfälla",
                coordinates=(59.4235, 17.8340),
                required_skills=[Skill.SNOW_SHOWELING],
                estimated_duration_hours=2.5,
                preferred_start_time=time(6, 0),
                latest_start_time=time(8, 0),
                priority=Priority.URGENT,
                instructions="Gångvägar runt centrum",
                created_at=now
            ),
            Job(
                id="job_018",
                client_name="Butik Skärholmen",
                address="Bredholmsgatan 4, Skärholmen",
                coordinates=(59.2751, 17.9071),
                required_skills=[Skill.WINDOW_CLEANING],
                estimated_duration_hours=2.0,
                preferred_start_time=time(11, 0),
                latest_start_time=time(13, 0),
                priority=Priority.MEDIUM,
                instructions="Skyltfönster mot gatan",
                created_at=now
            ),
            Job(
                id="job_019",
                client_name="Terrass Rengöring Ekerö",
                address="Ekerö Centrum, Ekerö",
                coordinates=(59.2887, 17.8136),
                required_skills=[Skill.OUTDOOR_CLEANING],
                estimated_duration_hours=2.0,
                preferred_start_time=time(8, 30),
                latest_start_time=time(10, 0),
                priority=Priority.LOW,
                instructions="Skrubba trätrall på uteplats",
                created_at=now
            ),
            Job(
                id="job_020",
                client_name="Kundservicekontor Länna",
                address="Lännavägen 25, Huddinge",
                coordinates=(59.2225, 18.0740),
                required_skills=[Skill.OFFICE_CLEANING],
                estimated_duration_hours=2.5,
                preferred_start_time=time(10, 30),
                latest_start_time=time(12, 30),
                priority=Priority.HIGH,
                instructions="Datorutrustning kräver försiktig rengöring",
                created_at=now
            ),
            Job(
                id="job_021",
                client_name="Radhus Åkersberga",
                address="Storängsvägen 3, Åkersberga",
                coordinates=(59.4800, 18.3000),
                required_skills=[Skill.HOME_CLEANING],
                estimated_duration_hours=3.0,
                preferred_start_time=time(12, 30),
                latest_start_time=time(14, 30),
                priority=Priority.MEDIUM,
                instructions="Barnrum behöver extra dammsugning",
                created_at=now
            ),
            Job(
                id="job_022",
                client_name="Lägenhet Vällingby",
                address="Vällingby torg 9, Vällingby",
                coordinates=(59.3628, 17.8724),
                required_skills=[Skill.APARTMENT_CLEANING],
                estimated_duration_hours=2.0,
                preferred_start_time=time(13, 0),
                latest_start_time=time(14, 30),
                priority=Priority.LOW,
                instructions="Två sovrum och badrum",
                created_at=now
            ),
            Job(
                id="job_023",
                client_name="Lagerlokal Spånga",
                address="Finspångsgatan 44, Spånga",
                coordinates=(59.3820, 17.9250),
                required_skills=[Skill.OUTDOOR_CLEANING],
                estimated_duration_hours=2.5,
                preferred_start_time=time(7, 30),
                latest_start_time=time(9, 30),
                priority=Priority.HIGH,
                instructions="Skräp och löv runt lastportar",
                created_at=now
            ),
            Job(
                id="job_024",
                client_name="Villa Vällingby",
                address="Ångermannagatan 120, Vällingby",
                coordinates=(59.3612, 17.8720),
                required_skills=[Skill.HOME_CLEANING],
                estimated_duration_hours=2.0,
                preferred_start_time=time(10, 0),
                latest_start_time=time(12, 0),
                priority=Priority.MEDIUM,
                instructions="Fönsterputs på nedervåningen",
                created_at=now
            ),
            Job(
                id="job_025",
                client_name="Skola i Märsta",
                address="Stationsgatan 4, Märsta",
                coordinates=(59.6216, 17.8548),
                required_skills=[Skill.OFFICE_CLEANING],
                estimated_duration_hours=3.0,
                preferred_start_time=time(12, 30),
                latest_start_time=time(14, 30),
                priority=Priority.HIGH,
                instructions="Klassrum och lärarrum efter terminsslut",
                created_at=now
            ),
            Job(
                id="job_026",
                client_name="Lägenhet i Norsborg",
                address="Botkyrkavägen 3, Norsborg",
                coordinates=(59.2380, 17.7900),
                required_skills=[Skill.APARTMENT_CLEANING],
                estimated_duration_hours=2.5,
                preferred_start_time=time(11, 0),
                latest_start_time=time(13, 0),
                priority=Priority.LOW,
                instructions="Två badrum och kök",
                created_at=now
            ),
            Job(
                id="job_027",
                client_name="Villa Åkersberga",
                address="Centralvägen 42, Åkersberga",
                coordinates=(59.4802, 18.2955),
                required_skills=[Skill.HOME_CLEANING],
                estimated_duration_hours=2.0,
                preferred_start_time=time(13, 0),
                latest_start_time=time(14, 30),
                priority=Priority.MEDIUM,
                instructions="Storstädning av källare",
                created_at=now
            ),
            Job(
                id="job_028",
                client_name="Kontor i Sollentuna",
                address="Malaxgatan 3, Sollentuna",
                coordinates=(59.4358, 17.9375),
                required_skills=[Skill.OFFICE_CLEANING],
                estimated_duration_hours=2.0,
                preferred_start_time=time(8, 30),
                latest_start_time=time(10, 0),
                priority=Priority.HIGH,
                instructions="Ta bort byggdamm från nyinstallation",
                created_at=now
            ),
            Job(
                id="job_029",
                client_name="Butik i Lidingö Centrum",
                address="Stockholmsvägen 50, Lidingö",
                coordinates=(59.3645, 18.1315),
                required_skills=[Skill.WINDOW_CLEANING],
                estimated_duration_hours=2.5,
                preferred_start_time=time(10, 0),
                latest_start_time=time(12, 30),
                priority=Priority.MEDIUM,
                instructions="Skyltfönster plus entré",
                created_at=now
            ),
            Job(
                id="job_030",
                client_name="Terrasstvätt i Farsta",
                address="Farstagången 12, Farsta",
                coordinates=(59.2423, 18.0890),
                required_skills=[Skill.OUTDOOR_CLEANING],
                estimated_duration_hours=3.0,
                preferred_start_time=time(9, 0),
                latest_start_time=time(11, 0),
                priority=Priority.LOW,
                instructions="Högtryckstvätt av stenplattor",
                created_at=now
            ),
            Job(
                id="job_031",
                client_name="Radhus i Upplands Väsby",
                address="Hasselgatan 7, Upplands Väsby",
                coordinates=(59.5185, 17.9144),
                required_skills=[Skill.HOME_CLEANING],
                estimated_duration_hours=2.0,
                preferred_start_time=time(8, 30),
                latest_start_time=time(10, 30),
                priority=Priority.MEDIUM,
                instructions="Övervåning och trappor",
                created_at=now
            ),
            Job(
                id="job_032",
                client_name="Kontor i Bromma Blocks",
                address="Ulvsundavägen 185, Bromma",
                coordinates=(59.3521, 17.9435),
                required_skills=[Skill.OFFICE_CLEANING],
                estimated_duration_hours=2.5,
                preferred_start_time=time(14, 0),
                latest_start_time=time(15, 30),
                priority=Priority.HIGH,
                instructions="Töm papperskorgar och rengör skrivbord",
                created_at=now
            ),
            Job(
                id="job_033",
                client_name="Parkstädning i Tyresö",
                address="Farmarstigen 10, Tyresö",
                coordinates=(59.2445, 18.2230),
                required_skills=[Skill.OUTDOOR_CLEANING],
                estimated_duration_hours=2.5,
                preferred_start_time=time(8, 0),
                latest_start_time=time(10, 0),
                priority=Priority.HIGH,
                instructions="Rensa grus och plocka skräp",
                created_at=now
            )


        ]
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
                name="Anna jAndersson",
                email="anna@example.com",
                phone="070-123-4567",
                home_address="Södermalm, Stockholm",
                home_coordinates=(59.3165, 18.0707),  # Södermalm
                skills=[Skill.OFFICE_CLEANING, Skill.WINDOW_CLEANING, Skill.HOME_CLEANING, Skill.SNOW_SHOWELING, Skill.OUTDOOR_CLEANING, Skill.APARTMENT_CLEANING ],
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
                home_coordinates=(59.3433, 18.0521),  # Vasastan
                skills=[Skill.OFFICE_CLEANING, Skill.WINDOW_CLEANING, Skill.HOME_CLEANING, Skill.SNOW_SHOWELING, Skill.OUTDOOR_CLEANING, Skill.APARTMENT_CLEANING ],
                languages=["svenska"],
                working_hours=WorkingHours(start_time=time(7, 0), end_time=time(16, 0)),
                max_daily_hours=9.0
            ),
            Cleaner(
                id="cleaner_003",
                name="Maria Nilsson",
                email="maria@example.com",
                phone="070-345-6789",
                home_address="Östermalm, Stockholm",
                home_coordinates=(59.3378, 18.0832),  # Östermalm
                skills=[Skill.OFFICE_CLEANING, Skill.WINDOW_CLEANING, Skill.HOME_CLEANING, Skill.SNOW_SHOWELING, Skill.OUTDOOR_CLEANING, Skill.APARTMENT_CLEANING ],
                languages=["svenska", "engelska", "spanska"],
                working_hours=WorkingHours(start_time=time(9, 0), end_time=time(18, 0)),
                max_daily_hours=8.0
            ),
            Cleaner(
                id="cleaner_004",
                name="Johan Johansson",
                email="johan@example.com",
                phone="070-456-7890",
                home_address="Kista, Stockholm",
                home_coordinates=(59.4036, 17.9444),  # Kista
                skills=[Skill.OFFICE_CLEANING, Skill.WINDOW_CLEANING, Skill.HOME_CLEANING, Skill.SNOW_SHOWELING, Skill.OUTDOOR_CLEANING, Skill.APARTMENT_CLEANING ],
                languages=["svenska", "finska"],
                working_hours=WorkingHours(start_time=time(8, 30), end_time=time(17, 30)),
                max_daily_hours=8.0
            ),
            Cleaner(
                id="cleaner_005",
                name="Sara Karlsson",
                email="sara@example.com",
                phone="070-567-8901",
                home_address="Nacka, Stockholm",
                home_coordinates=(59.3109, 18.1647),  # Nacka
                skills=[Skill.OFFICE_CLEANING, Skill.WINDOW_CLEANING, Skill.HOME_CLEANING, Skill.SNOW_SHOWELING, Skill.OUTDOOR_CLEANING, Skill.APARTMENT_CLEANING ],
                languages=["svenska", "engelska"],
                working_hours=WorkingHours(start_time=time(8, 0), end_time=time(16, 30)),
                max_daily_hours=8.5
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
                address="Sundbybergs allé 1, Sundbyberg",
                coordinates=(59.3616, 17.9706),
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
                coordinates=(59.4036, 17.9444),
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

            #nya utspridda
            Job(
                id="job_009",
                client_name="Kontor Barkarby",
                address="Barkarbyvägen 35, Järfälla",
                coordinates=(59.4142, 17.8722),
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
                coordinates=(59.2350, 18.2289),
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
                coordinates=(59.1994, 17.8330),
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
                coordinates=(59.4977, 18.0572),
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
                coordinates=(59.4239, 17.8338),
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
                coordinates=(59.2220, 18.0745),
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
            )

        ]
# Importing necessary components from SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Setting up the base for declarative class definitions
Base = declarative_base()

# --- Band Model ---
class Band(Base):
    __tablename__ = 'bands'

    # Primary key column, automatically increments
    id = Column(Integer, primary_key=True)
    
    # Name of the band
    name = Column(String, nullable=False)
    
    # Hometown of the band
    hometown = Column(String, nullable=False)

    # Relationship to the Concert model, using back_populates to allow bidirectional access
    concerts = relationship('Concert', back_populates='band')

    # Method to return all the venues the band has performed at (using the concerts relationship)
    def get_venues(self):
        return {concert.venue for concert in self.concerts}

    # Method to create a new concert for the band in a specific venue on a given date
    def play_in_venue(self, venue, date):
        # Create a new concert instance and associate it with this band and the provided venue
        new_concert = Concert(band=self, venue=venue, date=date)
        
        # Add the new concert to the session and commit it to the database
        session.add(new_concert)
        session.commit()

    # Method to return all introductions for the band in all concerts
    def all_introductions(self):
        # Return a list of introductions for each concert the band has played
        return [concert.introduction() for concert in self.concerts]

    # Class method to return the band with the most concerts played
    @classmethod
    def most_performances(cls):
        # Query all bands and find the band with the maximum number of concerts
        return max(session.query(cls).all(), key=lambda b: len(b.concerts))


# --- Venue Model ---
class Venue(Base):
    __tablename__ = 'venues'

    # Primary key column, automatically increments
    id = Column(Integer, primary_key=True)
    
    # Title of the venue
    title = Column(String, nullable=False)
    
    # City where the venue is located
    city = Column(String, nullable=False)

    # Relationship to the Concert model, using back_populates for bidirectional access
    concerts = relationship('Concert', back_populates='venue')

    # Method to return all bands that have performed at this venue (using the concerts relationship)
    def get_bands(self):
        return {concert.band for concert in self.concerts}

    # Method to find the first concert at the venue on a specific date
    def concert_on(self, date):
        # Query the database for a concert at this venue on the provided date
        return session.query(Concert).filter_by(venue_id=self.id, date=date).first()

    # Method to return the band that has played the most concerts at this venue
    def most_frequent_band(self):
        # Dictionary to store the count of performances by each band
        band_performance_counts = {}

        # Loop through all concerts at this venue and count how many times each band performed
        for concert in self.concerts:
            band = concert.band
            band_performance_counts[band] = band_performance_counts.get(band, 0) + 1

        # Return the band that performed the most times
        return max(band_performance_counts, key=band_performance_counts.get)


# --- Concert Model ---
class Concert(Base):
    __tablename__ = 'concerts'

    # Primary key column, automatically increments
    id = Column(Integer, primary_key=True)
    
    # Foreign key to the Band table (many-to-one relationship)
    band_id = Column(Integer, ForeignKey('bands.id'))
    
    # Foreign key to the Venue table (many-to-one relationship)
    venue_id = Column(Integer, ForeignKey('venues.id'))
    
    # Date of the concert as a string (for simplicity)
    date = Column(String, nullable=False)

    # Relationship back to the Band model
    band = relationship('Band', back_populates='concerts')
    
    # Relationship back to the Venue model
    venue = relationship('Venue', back_populates='concerts')

    # Method to check if the concert is a hometown show for the band
    def hometown_show(self):
        # Check if the concert's venue city matches the band's hometown
        return self.band.hometown == self.venue.city

    # Method to generate the band's introduction for this concert
    def introduction(self):
        # Return a string with the band's introduction based on the concert's details
        return f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}"


# --- Database Setup ---
# Create a SQLite database in-memory for simplicity, you can change this to a file if needed
engine = create_engine('sqlite:///concerts.db', echo=True)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Create all tables based on the models defined above
Base.metadata.create_all(engine)


# --- Example Usage ---
# Adding some sample data to test the relationships and methods

# Creating two bands
band1 = Band(name="The Rolling Stones", hometown="London")
band2 = Band(name="The Beatles", hometown="Liverpool")

# Creating two venues
venue1 = Venue(title="Madison Square Garden", city="New York")
venue2 = Venue(title="Royal Albert Hall", city="London")

# Adding them to the session (transaction)
session.add_all([band1, band2, venue1, venue2])
session.commit()

# Creating concerts for each band at different venues
band1.play_in_venue(venue1, "2023-09-12")
band1.play_in_venue(venue2, "2024-01-15")
band2.play_in_venue(venue1, "2024-02-20")

# Query the database for the first band and list the venues they performed at
first_band = session.query(Band).first()
print(f"Venues for {first_band.name}: {[venue.title for venue in first_band.get_venues()]}")

# Test the hometown_show method
concert = session.query(Concert).first()
print(f"Is the first concert a hometown show? {concert.hometown_show()}")

# Test the introduction method
print(concert.introduction())

# Test the most_performances class method
print(f"Band with most performances: {Band.most_performances().name}")

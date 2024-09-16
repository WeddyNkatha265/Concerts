
# Concert App

This project is a database-driven application to manage bands, venues, and concerts using SQLAlchemy, a Python ORM (Object Relational Mapping) library. The application defines models for bands, venues, and concerts, and allows interaction between them, such as tracking which band performed at which venue on a specific date.

## Features

- **Bands, Venues, and Concerts**: 
  - Create, manage, and query relationships between bands, venues, and their concerts.
  
- **Track Performances**: 
  - Record when a band performs at a venue and query details of past performances.
  
- **Aggregate Functions**:
  - Find the band with the most performances.
  - Determine which band has performed the most at a specific venue.

## Models

### Band
- `id`: Unique identifier for each band.
- `name`: The band's name.
- `hometown`: The band's hometown.
- `concerts`: Relationship to the `Concert` model, representing all concerts the band has played.

#### Methods:
- `get_venues()`: Returns a set of all venues where the band has performed.
- `play_in_venue(venue, date)`: Schedules a concert for the band at a specific venue and date.
- `all_introductions()`: Retrieves introductions for all the band's concerts.
- `most_performances()`: Class method that returns the band with the most concerts.

### Venue
- `id`: Unique identifier for each venue.
- `title`: The venue's name.
- `city`: The city where the venue is located.
- `concerts`: Relationship to the `Concert` model, representing all concerts at this venue.

#### Methods:
- `get_bands()`: Returns a set of all bands that have performed at the venue.
- `concert_on(date)`: Finds the first concert held at the venue on a specific date.
- `most_frequent_band()`: Returns the band that has performed the most at the venue.

### Concert
- `id`: Unique identifier for each concert.
- `band_id`: Foreign key referencing the `Band` model.
- `venue_id`: Foreign key referencing the `Venue` model.
- `date`: Date of the concert.
- `band`: Relationship to the `Band` model, representing the band performing at the concert.
- `venue`: Relationship to the `Venue` model, representing the venue where the concert is held.

#### Methods:
- `hometown_show()`: Returns whether the concert is a hometown show (i.e., the band's hometown matches the concert's city).
- `introduction()`: Returns a formatted introduction for the concert.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd concert-organizer
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**:
   - The app uses SQLite by default.
   - Create the database and tables by running the Python script:
     ```bash
     python app.py
     ```

4. **Run Example**:
   The script includes sample data for testing. After running the script, you can test the relationships between bands, venues, and concerts:
   - List venues a band has performed at.
   - Check if a concert is a hometown show.
   - Get the introduction for a concert.
   - Find the band with the most performances.

## Example Usage

```python
# Query the first band and list the venues they performed at
first_band = session.query(Band).first()
print(f"Venues for {first_band.name}: {[venue.title for venue in first_band.get_venues()]}")

# Test the hometown_show method
concert = session.query(Concert).first()
print(f"Is the first concert a hometown show? {concert.hometown_show()}")

# Test the most_performances class method
print(f"Band with most performances: {Band.most_performances().name}")
```

## Future Improvements
- Adding more aggregate functions like `total_concerts_at_venue()`.
- Extending search filters by date or band name.
- Adding more robust error handling and input validation.

---

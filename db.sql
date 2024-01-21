DROP TABLE venue;

DROP TABLE show;

DROP TABLE user;

DROP TABLE show_tags;

DROP TABLE scheduled_at;

DROP TABLE booking;

-----
DELETE FROM venue;

DELETE FROM show;

DELETE FROM user;

DELETE FROM show_tags;

DELETE FROM scheduled_at;

DELETE FROM booking;

-------
CREATE TABLE
    venue (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, location TEXT, description TEXT, rating INTEGER, capacity INTEGER);

CREATE TABLE
    show (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT, category TEXT, rating INTEGER, ticket_price NUMERIC(2));

CREATE TABLE
    show_tags (show_id INTEGER, tag TEXT, PRIMARY KEY (show_id, tag), FOREIGN KEY (show_id) REFERENCES show (id) ON DELETE CASCADE);

CREATE TABLE
    scheduled_at (id INTEGER PRIMARY KEY AUTOINCREMENT, show_id INTEGER, venue_id INTEGER, show_date_time DATE, FOREIGN KEY (show_id) REFERENCES show (id) ON DELETE CASCADE, FOREIGN KEY (venue_id) REFERENCES venue (id) ON DELETE CASCADE);

CREATE TABLE
    booking (user_id INTEGER, svd_id INTEGER, PRIMARY KEY (user_id, svd_id), FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE, FOREIGN KEY (svd_id) REFERENCES scheduled_at (id) ON DELETE CASCADE);

CREATE TABLE
    user (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE NOT NULL, first_name TEXT NOT NULL, last_name TEXT, password TEXT NOT NULL, role TEXT);

-----------
-- Insert sample data into user table
INSERT INTO
    user (username, email, first_name, last_name, password, role)
VALUES
    ("devansh", "devansh@example.com", "Devansh", "Rathor", "dr123", "admin"),
    ("admin", "admin@ds.study.iitm.ac.in", "Admin", "", "admin@123", "admin"),
    ("user", "user@ds.study.iitm.ac.in", "User", "", "user@123", "user"),
    ('john', 'johndoe@example.com', 'John', 'Doe', 'pass123', 'user'),
    ('jane', 'janedoe@example.com', 'Jane', 'Doe', 'pass456', 'user');

-- Insert sample data into venue table
INSERT INTO
    venue (name, location, description, rating, capacity)
VALUES
    ("PVR Cinemas", "Lower Parel, Mumbai", "A popular cinema chain with state-of-the-art facilities", 4.2, 250),
    ("INOX", "Nariman Point, Mumbai", "A luxury cinema chain known for its plush seating and ambiance", 4.5, 200),
    ("Carnival Cinemas", "Wadala, Mumbai", "A budget-friendly cinema chain with good facilities", 3.8, 150),
    ("Cinepolis", "Andheri East, Mumbai", "A popular cinema chain with excellent sound and picture quality", 4.3, 180),
    ("IMAX Wadala", "Wadala, Mumbai", "A popular cinema chain with a large screen and high-quality sound", 4.1, 120),
    ("Regal Theatre", "Colaba, Mumbai", "One of the oldest and most iconic cinemas in Mumbai", 4.0, 100),
    ("PVR Phoenix", "Lower Parel, Mumbai", "A modern cinema complex with great amenities and comfortable seats", 4.4, 300),
    ("Cinemax Infiniti", "Malad West, Mumbai", "A cinema chain with spacious halls and good sound quality", 3.9, 200),
    ("Sterling Cinema", "Fort, Mumbai", "A classic cinema hall with an old-world charm and comfortable seats", 3.8, 150),
    ("Grand Cinema", "Vashi, Navi Mumbai", "A popular cinema chain with a range of amenities", 4.0, 220),
    ("Citylight Cinema", "Mahim, Mumbai", "A classic cinema hall with a history of screening Bollywood films", 3.7, 120),
    ("PVR ICON Cinemas", "Andheri West, Mumbai", "A luxury cinema chain known for its plush seating and ambiance", 4.6, 250),
    ("Le Reve Cinemas", "Sion, Mumbai", "A modern cinema complex with great amenities and comfortable seats", 4.2, 200),
    ("Movietime Cinemas", "Goregaon East, Mumbai", "A cinema chain with spacious halls and good sound quality", 3.8, 180),
    ("Raj Cinema", "Dadar, Mumbai", "A classic cinema hall with an old-world charm and comfortable seats", 3.9, 150),
    ("PVR Milap Cinema", "Kandivali West, Mumbai", "A popular cinema chain with state-of-the-art facilities", 4.1, 220),
    ("Cinemax Growels", "Kandivali East, Mumbai", "A cinema chain with good facilities and comfortable seats", 3.7, 200),
    ("Carnival Cinemas", "Chembur, Mumbai", "A budget-friendly cinema chain with good facilities", 3.8, 150),
    ("Miraj Cinema", "Vile Parle East, Mumbai", "A classic cinema hall with a history of screening films", 3.9, 120),
    ("INOX R-City", "Ghatkopar West, Mumbai", "A luxury cinema chain known for its plush seating and ambiance", 4.4, 300);

-- Insert sample data into show table
INSERT INTO
    show (name, description, category, rating, ticket_price)
VALUES
    ("Avengers: Endgame", "The Avengers take one final stand against Thanos", "Hollywood", 4.8, 120),
    ("Black Panther", "T'Challa, heir to the hidden but advanced kingdom of Wakanda, must step forward to lead his people into a new future and must confront a challenger from his country's past", "Hollywood", 4.3, 100),
    ("Joker", "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime. This path brings him face-to-face with his alter-ego: the Joker", "Hollywood", 4.5, 120),
    ("Baahubali: The Beginning", "In ancient India, an adventurous and daring man becomes involved in a decades-old feud between two warring peoples", "Bollywood", 4.1, 80),
    ("Chennai Express", "Rahul embarks on a journey to a small town in Tamil Nadu to fulfill the last wish of his grandfather: to have his ashes immersed in the Holy water of Rameshwaram. En route, he meets a woman hailing from a unique family down South. As they find love through this journey in the exuberant lands of South India, an unanticipated drive awaits them", "Bollywood", 3.8, 75),
    ("3 Idiots", "Two friends are searching for their long lost companion. They revisit their college days and recall the memories of their friend who inspired them to think differently, even as the rest of the world called them 'idiots'", "Bollywood", 4.2, 95),
    ("Dangal", "Former wrestler Mahavir Singh Phogat and his two wrestler daughters struggle towards glory at the Commonwealth Games in the face of societal oppression", "Bollywood", 4.3, 100),
    ("The Lion King", "After the murder of his father, a young lion prince flees his kingdom only to learn the true meaning of responsibility and bravery", "Hollywood", 4.7, 130),
    ("Bajirao Mastani", "The tale of romance between an Indian general, Peshwa Baji Rao I & his second wife, Mastani, a Muslim princess", "Bollywood", 4.1, 180),
    ("Star Wars: The Rise of Skywalker", "The surviving members of the resistance face the First Order once again, and the legendary conflict between the Jedi and the Sith reaches its peak bringing the Skywalker saga to its end", "Hollywood", 4.4, 125),
    ('Dilwale Dulhania Le Jayenge', 'When Raj meets Simran in Europe, it isn''t love at first sight but when Simran moves to India for an arranged marriage, love makes its presence felt', 'Bollywood', 4.5, 150),
    ('The Dark Knight', 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice', 'Hollywood', 4.8, 125),
    ('Kuch Kuch Hota Hai', 'During their college years, Anjali was in love with her best-friend Rahul, but he had eyes only for Tina. Years later, Rahul and the now-deceased Tina''s eight-year-old daughter attempts to reunite her father and Anjali', 'Bollywood', 4.2, 200),
    ('The Shawshank Redemption', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency', 'Hollywood', 4.9, 14.50),
    ('Lagaan', 'The people of a small village in Victorian India stake their future on a game of cricket against their ruthless British rulers', 'Bollywood', 4.3, 10.50),
    ('Inception', 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.', 'Hollywood', 4.7, 140),
    ('Kabhi Khushi Kabhie Gham', 'Yashvardhan Raichand lives a very wealthy lifestyle along with his wife, Nandini, and two sons, Rahul and Rohan. While Rahul has been adopted, Yashvardhan and Nandini treat him as their own. When their sons mature, they start to look for suitable brides for Rahul, and decide to get him married to a young woman named Naina. When Rahul refuses, he sets out to discover the truth behind his birth and find his biological mother', 'Bollywood', 4.1, 8.50),
    ('Forrest Gump', 'The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate, and other history unfold through the perspective of an Alabama man with an IQ of 75', 'Hollywood', 4.5, 300),
    ('Kabir Singh', 'Kabir Singh is a remake of a Telugu movie Arjun Reddy (2017), where a short-tempered house surgeon gets used to drugs and drinks when his girlfriend is forced to marry another person', 'Bollywood', 3.9, 200),
    ('The Godfather', 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son', 'Hollywood', 4.8, 12.50),
    ('Swades', 'A successful Indian scientist returns to an Indian village to take his nanny to America with him and in the process rediscovers his roots', 'Bollywood', 4.2, 90),
    ('The Matrix', 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers', 'Hollywood', 4.6, 130),
    ("Avatar", "A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.", "Hollywood", 4.3, 150),
    ("Baahubali 2: The Conclusion", "When Shiva, the son of Bahubali, learns about his heritage, he begins to look for answers. His story is juxtaposed with past events that unfolded in the Mahishmati Kingdom.", "Bollywood", 3.8, 100),
    ("Avengers: Infinity War", "The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe.", "Hollywood", 4.2, 220),
    ("Star Wars: The Force Awakens", "Three decades after the Empire's defeat, a new threat arises in the militant First Order. Defected stormtrooper Finn and the scavenger Rey are caught up in the Resistance's search for the missing Luke Skywalker.", "Hollywood", 4.9, 180),
    ("Jurassic Park", "During a preview tour, a theme park suffers a major power breakdown that allows its cloned dinosaur exhibits to run amok.", "Hollywood", 8, 170);

INSERT INTO
    show_tags (show_id, tag)
VALUES
    (1, 'action'),
    (1, 'adventure'),
    (1, 'superhero'),
    (2, 'action'),
    (2, 'adventure'),
    (2, 'superhero'),
    (3, 'thriller'),
    (3, 'drama'),
    (3, 'crime'),
    (4, 'action'),
    (4, 'drama'),
    (4, 'epic'),
    (5, 'romantic'),
    (5, 'comedy'),
    (5, 'drama'),
    (6, 'comedy'),
    (6, 'drama'),
    (6, 'inspirational'),
    (7, 'drama'),
    (7, 'biography'),
    (7, 'sports'),
    (8, 'adventure'),
    (8, 'drama'),
    (8, 'family'),
    (9, 'romantic'),
    (9, 'drama'),
    (9, 'historical'),
    (10, 'action'),
    (10, 'adventure'),
    (10, 'sci-fi'),
    (11, 'romantic'),
    (11, 'comedy'),
    (11, 'drama'),
    (12, 'drama'),
    (12, 'crime'),
    (12, 'superhero'),
    (13, 'drama'),
    (13, 'inspirational'),
    (13, 'friendship'),
    (14, 'drama'),
    (14, 'sports'),
    (14, 'epic'),
    (15, 'action'),
    (15, 'adventure'),
    (15, 'sci-fi'),
    (16, 'romantic'),
    (16, 'drama'),
    (16, 'family'),
    (17, 'drama'),
    (17, 'historical'),
    (17, 'musical'),
    (18, 'drama'),
    (18, 'comedy'),
    (18, 'romantic'),
    (19, 'drama'),
    (19, 'historical'),
    (19, 'inspirational'),
    (20, 'drama'),
    (20, 'romantic'),
    (20, 'comedy'),
    (21, 'drama'),
    (21, 'romantic'),
    (21, 'family'),
    (22, 'drama'),
    (22, 'historical'),
    (22, 'inspirational'),
    (23, 'drama'),
    (23, 'comedy'),
    (23, 'romantic'),
    (24, 'drama'),
    (24, 'historical'),
    (24, 'inspirational'),
    (25, 'drama'),
    (25, 'comedy'),
    (25, 'romantic');

INSERT INTO
    scheduled_at (show_id, venue_id, show_date_time)
VALUES
    (1, 8, '2023-09-17 20:00:00'),
    (1, 10, '2023-03-22 18:00:00'),
    (1, 10, '2023-10-11 20:00:00'),
    (1, 13, '2023-07-01 13:00:00'),
    (2, 2, '2023-06-21 23:00:00'),
    (2, 4, '2023-11-20 13:00:00'),
    (2, 20, '2023-03-11 23:00:00'),
    (2, 20, '2023-04-12 10:00:00'),
    (3, 6, '2023-05-27 00:00:00'),
    (4, 1, '2023-01-26 00:00:00'),
    (4, 2, '2023-07-09 23:00:00'),
    (4, 6, '2023-12-23 11:00:00'),
    (4, 12, '2023-12-04 20:00:00'),
    (4, 14, '2023-05-28 08:00:00'),
    (5, 16, '2023-05-01 09:00:00'),
    (5, 19, '2023-06-12 18:00:00'),
    (6, 4, '2023-08-25 18:00:00'),
    (6, 7, '2023-05-22 18:00:00'),
    (6, 14, '2023-08-02 22:00:00'),
    (6, 17, '2023-04-08 17:00:00'),
    (6, 17, '2023-06-29 19:00:00'),
    (6, 19, '2023-04-18 11:00:00'),
    (7, 3, '2023-04-14 08:00:00'),
    (7, 3, '2023-09-08 13:00:00'),
    (7, 7, '2023-10-20 00:00:00'),
    (8, 2, '2023-03-25 17:00:00'),
    (8, 4, '2023-11-01 23:00:00'),
    (8, 9, '2023-11-16 18:00:00'),
    (8, 11, '2023-02-12 10:00:00'),
    (8, 14, '2023-03-08 10:00:00'),
    (8, 17, '2023-08-16 11:00:00'),
    (8, 19, '2023-02-08 10:00:00'),
    (9, 4, '2023-12-23 09:00:00'),
    (9, 5, '2023-02-19 18:00:00'),
    (9, 8, '2023-10-23 23:00:00'),
    (9, 8, '2023-11-09 00:00:00'),
    (9, 14, '2023-11-18 20:00:00'),
    (10, 4, '2023-11-26 19:00:00'),
    (10, 9, '2023-02-16 22:00:00'),
    (10, 9, '2023-04-15 14:00:00'),
    (10, 15, '2023-03-18 21:00:00'),
    (10, 17, '2023-05-01 00:00:00'),
    (11, 13, '2023-11-18 15:00:00'),
    (12, 4, '2023-03-23 09:00:00'),
    (12, 8, '2023-06-03 23:00:00'),
    (12, 12, '2023-08-22 14:00:00'),
    (13, 14, '2023-07-18 15:00:00'),
    (13, 15, '2023-08-27 17:00:00'),
    (13, 19, '2023-11-25 14:00:00'),
    (14, 3, '2023-10-26 08:00:00'),
    (14, 7, '2023-01-27 11:00:00'),
    (14, 7, '2023-06-10 23:00:00'),
    (14, 9, '2023-05-31 14:00:00'),
    (15, 15, '2023-07-16 12:00:00'),
    (15, 18, '2023-12-18 20:00:00'),
    (17, 2, '2023-09-26 10:00:00'),
    (17, 3, '2023-07-12 19:00:00'),
    (17, 7, '2023-08-10 19:00:00'),
    (17, 7, '2023-08-26 13:00:00'),
    (17, 7, '2023-11-07 09:00:00'),
    (17, 20, '2023-03-18 00:00:00'),
    (18, 1, '2023-01-28 22:00:00'),
    (18, 1, '2023-05-18 23:00:00'),
    (18, 1, '2023-07-24 11:00:00'),
    (19, 1, '2023-01-25 08:00:00'),
    (19, 1, '2023-07-27 16:00:00'),
    (19, 3, '2023-07-01 19:00:00'),
    (19, 11, '2023-10-27 21:00:00'),
    (20, 1, '2023-12-01 16:00:00'),
    (20, 16, '2023-02-24 19:00:00'),
    (21, 4, '2023-01-11 12:00:00'),
    (21, 8, '2023-05-07 19:00:00'),
    (21, 16, '2023-02-26 21:00:00'),
    (22, 1, '2023-02-03 00:00:00'),
    (22, 7, '2023-03-25 15:00:00'),
    (22, 13, '2023-08-12 22:00:00'),
    (22, 14, '2023-11-19 08:00:00'),
    (22, 20, '2023-10-02 08:00:00'),
    (23, 4, '2023-10-13 23:00:00'),
    (23, 13, '2023-08-29 16:00:00'),
    (23, 14, '2023-05-11 19:00:00'),
    (23, 14, '2023-11-29 20:00:00'),
    (23, 20, '2023-10-31 16:00:00'),
    (23, 20, '2023-12-11 12:00:00'),
    (24, 9, '2023-04-09 12:00:00'),
    (24, 9, '2023-09-20 12:00:00'),
    (25, 6, '2023-05-18 16:00:00'),
    (25, 8, '2023-12-04 00:00:00'),
    (25, 18, '2023-11-15 17:00:00'),
    (25, 19, '2023-05-09 00:00:00'),
    (25, 20, '2023-11-02 23:00:00'),
    (25, 20, '2023-11-06 13:00:00'),
    (26, 5, '2023-09-04 16:00:00'),
    (26, 8, '2023-12-01 11:00:00'),
    (26, 9, '2023-10-27 16:00:00'),
    (26, 11, '2023-09-25 18:00:00'),
    (26, 13, '2023-09-24 09:00:00'),
    (26, 14, '2023-12-04 08:00:00'),
    (26, 18, '2023-12-15 20:00:00'),
    (27, 14, '2023-09-10 08:00:00');

INSERT INTO
    booking (user_id, svd_id, no_of_tickets)
VALUES
    (1, 9, 2),
    (1, 46, 4),
    (1, 54, 2),
    (1, 62, 2),
    (1, 93, 4),
    (2, 2, 5),
    (2, 11, 2),
    (2, 63, 3),
    (2, 85, 3),
    (3, 35, 2),
    (3, 60, 5),
    (3, 79, 4),
    (3, 84, 2),
    (4, 22, 5),
    (4, 46, 3),
    (4, 49, 2),
    (4, 89, 2),
    (4, 99, 4),
    (5, 10, 2),
    (5, 44, 4);
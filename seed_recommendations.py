#!/usr/bin/env python3
"""
Seed Recommendations Data for KidSpark
Populates the recommendations table with learning content for all subcategories, age groups, and levels
"""

import mysql.connector
from config import Config

def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )

def seed_recommendations():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Clear existing recommendations
    cursor.execute("DELETE FROM recommendations")
    
    recommendations = [
        # CRICKET - All age groups and levels (9 total)
        ('Cricket', '5-8', 'beginner', 'Catch the Ball Game', 'Practice catching a soft ball with both hands. Start close and move further away!', 'activity', '🏏'),
        ('Cricket', '5-8', 'intermediate', 'Mini Cricket Rules', 'Learn simple cricket rules with 6 players. Practice bowling underarm to hit the stumps.', 'activity', '🏏'),
        ('Cricket', '5-8', 'advanced', 'Cricket Team Captain', 'Lead your team! Learn where to place fielders and when to bowl or bat first.', 'project', '🏏'),
        
        ('Cricket', '9-12', 'beginner', 'Learn Basic Cricket Rules', 'Understand how runs, wickets and overs work in cricket. Practice catching a ball!', 'activity', '🏏'),
        ('Cricket', '9-12', 'intermediate', 'Batting Techniques', 'Learn the forward defensive shot, straight drive and cut shot with practice drills.', 'video', '🏏'),
        ('Cricket', '9-12', 'advanced', 'Cricket Statistics & Strategy', 'Study run rates, economy rates and field placement strategies used by professional teams.', 'project', '🏏'),
        
        ('Cricket', '13-14', 'beginner', 'Cricket Fundamentals', 'Master the basics: grip, stance, and swing. Practice with tennis ball first.', 'activity', '🏏'),
        ('Cricket', '13-14', 'intermediate', 'Advanced Bowling Techniques', 'Learn spin bowling, swing bowling, and yorker deliveries with proper technique.', 'video', '🏏'),
        ('Cricket', '13-14', 'advanced', 'Cricket Analytics Project', 'Analyze professional cricket data to predict match outcomes using statistics.', 'project', '🏏'),
        
        # FOOTBALL - All age groups and levels (9 total)
        ('Football', '5-8', 'beginner', 'Kick and Chase', 'Practice kicking the ball straight and running after it. Try to hit a target!', 'activity', '⚽'),
        ('Football', '5-8', 'intermediate', 'Dribbling Fun', 'Learn to dribble around cones. Keep the ball close to your feet!', 'activity', '⚽'),
        ('Football', '5-8', 'advanced', 'Mini Match Rules', 'Play 5v5 football and learn basic positions: goalkeeper, defenders, attackers.', 'project', '⚽'),
        
        ('Football', '9-12', 'beginner', 'Football Skills Basics', 'Learn proper kicking, passing, and ball control with both feet.', 'activity', '⚽'),
        ('Football', '9-12', 'intermediate', 'Team Positions & Tactics', 'Understand 4-4-2 formation and learn when to attack or defend as a team.', 'video', '⚽'),
        ('Football', '9-12', 'advanced', 'Football Strategy Analysis', 'Study famous football matches and analyze winning strategies and formations.', 'project', '⚽'),
        
        ('Football', '13-14', 'beginner', 'Football Fitness Training', 'Build stamina and agility with football-specific exercises and drills.', 'activity', '⚽'),
        ('Football', '13-14', 'intermediate', 'Advanced Ball Skills', 'Master stepovers, nutmegs, and advanced dribbling techniques.', 'video', '⚽'),
        ('Football', '13-14', 'advanced', 'Coach a Youth Team', 'Design training sessions and manage a junior football team for a season.', 'project', '⚽'),
        
        # DRAWING - All age groups and levels (9 total)
        ('Drawing', '5-8', 'beginner', 'Draw with Shapes', 'Make animals and houses using circles, squares, and triangles only!', 'activity', '✏️'),
        ('Drawing', '5-8', 'intermediate', 'Color Your World', 'Learn about warm and cool colors. Draw a sunset using only warm colors!', 'activity', '✏️'),
        ('Drawing', '5-8', 'advanced', 'Tell Stories with Pictures', 'Create a 4-panel comic strip about your favorite animal adventure.', 'project', '✏️'),
        
        ('Drawing', '9-12', 'beginner', 'Basic Shapes & Lines', 'Start with circles, squares and triangles. Try drawing a house using only basic shapes!', 'activity', '✏️'),
        ('Drawing', '9-12', 'intermediate', 'Shading Techniques', 'Learn how light and shadow work. Practice shading a sphere to make it look 3D.', 'activity', '✏️'),
        ('Drawing', '9-12', 'advanced', 'Perspective Drawing', 'Master one-point and two-point perspective to draw buildings and rooms.', 'project', '✏️'),
        
        ('Drawing', '13-14', 'beginner', 'Portrait Drawing Basics', 'Learn facial proportions and practice drawing realistic portraits.', 'activity', '✏️'),
        ('Drawing', '13-14', 'intermediate', 'Digital Art Introduction', 'Explore digital drawing tools and create your first digital artwork.', 'video', '✏️'),
        ('Drawing', '13-14', 'advanced', 'Art Portfolio Project', 'Create a complete art portfolio showcasing different styles and techniques.', 'project', '✏️'),
        
        # SINGING - All age groups and levels (9 total)
        ('Singing', '5-8', 'beginner', 'Animal Sound Songs', 'Sing songs that copy animal sounds. Practice making your voice high and low!', 'activity', '🎤'),
        ('Singing', '5-8', 'intermediate', 'Rhythm Clapping', 'Clap along to your favorite songs and learn to keep the beat steady.', 'activity', '🎤'),
        ('Singing', '5-8', 'advanced', 'Mini Concert Performance', 'Prepare and perform 3 songs for family and friends with actions!', 'project', '🎤'),
        
        ('Singing', '9-12', 'beginner', 'Breathing for Singing', 'Learn proper breathing techniques and practice scales to strengthen your voice.', 'activity', '🎤'),
        ('Singing', '9-12', 'intermediate', 'Harmony and Melody', 'Learn to sing in harmony with others and understand how melodies work.', 'video', '🎤'),
        ('Singing', '9-12', 'advanced', 'Write Your Own Song', 'Compose lyrics and melody for an original song about something you love.', 'project', '🎤'),
        
        ('Singing', '13-14', 'beginner', 'Vocal Technique Mastery', 'Develop proper posture, breathing, and vocal exercises for stronger singing.', 'activity', '🎤'),
        ('Singing', '13-14', 'intermediate', 'Music Theory for Singers', 'Understand scales, keys, and chord progressions to become a better performer.', 'video', '🎤'),
        ('Singing', '13-14', 'advanced', 'Record Your Album', 'Write, arrange, and record a 5-song EP showcasing your vocal abilities.', 'project', '🎤'),
        
        # MATHS - All age groups and levels (9 total)
        ('Maths', '5-8', 'beginner', 'Number Detective', 'Find numbers everywhere! Count toys, cookies, and steps. Make it a treasure hunt!', 'activity', '➕'),
        ('Maths', '5-8', 'intermediate', 'Shape Explorer', 'Hunt for circles, squares, and triangles in your house. Draw what you find!', 'activity', '➕'),
        ('Maths', '5-8', 'advanced', 'Money Math Game', 'Practice adding coins and notes. Plan how to spend your pocket money!', 'project', '➕'),
        
        ('Maths', '9-12', 'beginner', 'Fun Number Games', 'Play number puzzles and pattern games that make maths feel like a video game.', 'activity', '➕'),
        ('Maths', '9-12', 'intermediate', 'Cricket Maths Challenge', 'Calculate batting averages, run rates and team scores using real cricket match data.', 'project', '➕'),
        ('Maths', '9-12', 'advanced', 'Sports Statistics', 'Use probability and statistics to predict match outcomes and analyse player performance.', 'project', '➕'),
        
        ('Maths', '13-14', 'beginner', 'Real-World Problem Solving', 'Apply algebra and geometry to solve practical problems in daily life.', 'activity', '➕'),
        ('Maths', '13-14', 'intermediate', 'Data Analysis Project', 'Collect and analyze data from your school or community using statistical methods.', 'project', '➕'),
        ('Maths', '13-14', 'advanced', 'Mathematical Modeling', 'Create mathematical models to predict real-world phenomena like population growth.', 'project', '➕'),
        
        # SCIENCE - All age groups and levels (9 total)
        ('Science', '5-8', 'beginner', 'Kitchen Science Magic', 'Make volcanoes with baking soda and vinegar. Watch colors change with pH strips!', 'activity', '🔬'),
        ('Science', '5-8', 'intermediate', 'Plant Growing Experiment', 'Grow beans in different conditions. Which grows fastest: light, dark, or water?', 'activity', '🔬'),
        ('Science', '5-8', 'advanced', 'Weather Station Project', 'Build a simple weather station and track temperature and rain for a month.', 'project', '🔬'),
        
        ('Science', '9-12', 'beginner', 'Simple Chemistry Experiments', 'Explore chemical reactions with safe household items and learn the scientific method.', 'activity', '🔬'),
        ('Science', '9-12', 'intermediate', 'Physics in Sports', 'Understand how physics principles like force and motion apply to your favorite sports.', 'video', '🔬'),
        ('Science', '9-12', 'advanced', 'Environmental Science Project', 'Design and conduct an experiment to test water quality or air pollution in your area.', 'project', '🔬'),
        
        ('Science', '13-14', 'beginner', 'Laboratory Techniques', 'Master basic lab skills: measuring, mixing, observing, and recording results safely.', 'activity', '🔬'),
        ('Science', '13-14', 'intermediate', 'Biotechnology Basics', 'Explore DNA extraction, microscopy, and basic genetic principles through experiments.', 'video', '🔬'),
        ('Science', '13-14', 'advanced', 'Independent Research Project', 'Design and execute an original scientific investigation with hypothesis and analysis.', 'project', '🔬'),
        
        # CODING - All age groups and levels (9 total)
        ('Coding', '5-8', 'beginner', 'Code a Dancing Robot', 'Use Scratch Jr to make a robot dance and move around the screen!', 'activity', '💻'),
        ('Coding', '5-8', 'intermediate', 'Make Your First Game', 'Create a simple catching game where you collect falling objects for points.', 'activity', '💻'),
        ('Coding', '5-8', 'advanced', 'Interactive Story App', 'Build a choose-your-own-adventure story with different endings.', 'project', '💻'),
        
        ('Coding', '9-12', 'beginner', 'Programming Logic Games', 'Learn if-then statements and loops by programming a character through mazes.', 'activity', '💻'),
        ('Coding', '9-12', 'intermediate', 'Build a Calculator App', 'Create a working calculator that can add, subtract, multiply, and divide numbers.', 'project', '💻'),
        ('Coding', '9-12', 'advanced', 'Web Development Project', 'Design and code your own website with HTML, CSS, and basic JavaScript.', 'project', '💻'),
        
        ('Coding', '13-14', 'beginner', 'Python Programming Fundamentals', 'Master variables, functions, and control structures in Python programming.', 'activity', '💻'),
        ('Coding', '13-14', 'intermediate', 'Mobile App Development', 'Create your first mobile app using modern development frameworks.', 'video', '💻'),
        ('Coding', '13-14', 'advanced', 'AI and Machine Learning', 'Build a machine learning model to solve real-world problems using Python.', 'project', '💻'),
        
        # DANCING - All age groups and levels (9 total)
        ('Dancing', '5-8', 'beginner', 'Animal Dance Moves', 'Dance like different animals! Hop like a bunny, waddle like a penguin!', 'activity', '💃'),
        ('Dancing', '5-8', 'intermediate', 'Follow the Beat', 'Learn to dance to different rhythms. Fast songs, slow songs, and in-between!', 'activity', '💃'),
        ('Dancing', '5-8', 'advanced', 'Choreograph a Dance', 'Create your own 2-minute dance routine to your favorite song!', 'project', '💃'),
        
        ('Dancing', '9-12', 'beginner', 'Basic Dance Steps', 'Learn fundamental dance moves: step-touch, grapevine, and box step.', 'activity', '💃'),
        ('Dancing', '9-12', 'intermediate', 'Hip-Hop Dance Basics', 'Master popular hip-hop moves and learn to freestyle to different beats.', 'video', '💃'),
        ('Dancing', '9-12', 'advanced', 'Dance Performance Project', 'Choreograph and perform a group dance for a school talent show or event.', 'project', '💃'),
        
        ('Dancing', '13-14', 'beginner', 'Contemporary Dance Technique', 'Develop flexibility, strength, and expression through contemporary dance training.', 'activity', '💃'),
        ('Dancing', '13-14', 'intermediate', 'Dance Styles Exploration', 'Learn different dance styles: ballet, jazz, contemporary, and cultural dances.', 'video', '💃'),
        ('Dancing', '13-14', 'advanced', 'Dance Teaching Project', 'Teach younger students a dance routine and organize a performance showcase.', 'project', '💃'),
        
        # PAINTING - All age groups and levels (9 total)
        ('Painting', '5-8', 'beginner', 'Finger Paint Fun', 'Use your fingers to paint rainbows, flowers, and handprint animals!', 'activity', '🎨'),
        ('Painting', '5-8', 'intermediate', 'Brush Painting Basics', 'Learn to use different brush sizes to paint thick lines, thin lines, and dots.', 'activity', '🎨'),
        ('Painting', '5-8', 'advanced', 'Paint Your Pet Portrait', 'Paint a picture of your favorite animal using watercolors or poster paints.', 'project', '🎨'),
        
        ('Painting', '9-12', 'beginner', 'Color Mixing Magic', 'Learn primary and secondary colors. Mix paints to create every color of the rainbow!', 'activity', '🎨'),
        ('Painting', '9-12', 'intermediate', 'Landscape Painting', 'Paint outdoor scenes with trees, mountains, and skies using different techniques.', 'activity', '🎨'),
        ('Painting', '9-12', 'advanced', 'Art Exhibition Project', 'Create 5 paintings in different styles and organize your own art exhibition.', 'project', '🎨'),
        
        ('Painting', '13-14', 'beginner', 'Acrylic Painting Techniques', 'Master brush techniques, blending, and texture creation with acrylic paints.', 'activity', '🎨'),
        ('Painting', '13-14', 'intermediate', 'Oil Painting Introduction', 'Learn traditional oil painting methods and create realistic still life paintings.', 'video', '🎨'),
        ('Painting', '13-14', 'advanced', 'Mixed Media Art Project', 'Combine painting with other materials to create innovative mixed media artworks.', 'project', '🎨'),
    ]
    
    # Insert all recommendations
    insert_query = """
        INSERT INTO recommendations (subcategory, age_group, level, title, description, resource_type, icon) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor.executemany(insert_query, recommendations)
    conn.commit()
    
    print(f"✅ Inserted {len(recommendations)} recommendations")
    print("📊 Breakdown:")
    print(f"   - 9 subcategories × 3 age groups × 3 levels = 81 recommendations")
    print(f"   - Cricket: 9, Football: 9, Drawing: 9")
    print(f"   - Singing: 9, Maths: 9, Science: 9")
    print(f"   - Coding: 9, Dancing: 9, Painting: 9")
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    print("🌱 Seeding Recommendations Database...")
    seed_recommendations()
    print("🎉 Seeding complete!")

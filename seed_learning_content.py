#!/usr/bin/env python3
"""
Seed Learning Content and Quiz Questions for KidSpark
Populates hobby-themed lessons mapped to school subjects
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

def seed_learning_content():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM quiz_questions")
    cursor.execute("DELETE FROM learning_content")
    
    print("🌱 Seeding Learning Content...")
    
    # Learning content data: (subject, concept, hobby_context, age_group, lesson_title, lesson_body, hobby_example, fun_fact)
    learning_content = []
    
    # CRICKET + MATHS
    learning_content.append((
        'Maths', 'fractions', 'cricket', '9-12',
        'Cricket and Fractions',
        '''Fractions are parts of a whole number. In cricket, an over has 6 balls. If a bowler bowls 4 balls, they have bowled 4/6 of an over!

Fractions help us understand how much of something is done. Just like eating 3 out of 8 pizza slices means you ate 3/8 of the pizza, bowling 3 balls out of 6 means you bowled 3/6 (or 1/2) of an over.

When we simplify fractions, we find the smallest numbers that mean the same thing. 4/6 can be simplified to 2/3 by dividing both numbers by 2!''',
        'Virat Kohli scored 45 runs in 3/4 of an innings. If the innings has 50 overs total, how many overs did he bat? Answer: 3/4 of 50 = 37.5 overs!',
        'The highest batting average in cricket history is 99.94, held by Don Bradman! That means he scored almost 100 runs every time he batted.'
    ))
    
    learning_content.append((
        'Maths', 'averages', 'cricket', '9-12',
        'Cricket Batting Averages',
        '''A batting average tells us how many runs a player scores on average each time they bat. It is calculated by dividing total runs by number of times out.

For example, if a player scored 300 runs in 10 innings and got out 8 times, their average is 300 ÷ 8 = 37.5 runs per innings.

The higher the average, the better the batsman! Averages help us compare players fairly.''',
        'MS Dhoni scored 450 runs in 15 matches and got out 12 times. What is his batting average? Answer: 450 ÷ 12 = 37.5',
        'The world record for highest Test batting average is 99.94 by Don Bradman. To get 100, he needed just 4 runs in his last innings but got out for 0!'
    ))

    # CRICKET + SCIENCE
    learning_content.append((
        'Science', 'forces', 'cricket', '9-12',
        'Forces in Cricket',
        '''When a bowler throws a cricket ball, they use force to make it move. Force is a push or pull that makes things start moving, stop moving, or change direction.

The faster the bowler runs and the harder they throw, the more force they apply. This makes the ball travel faster towards the batsman!

Friction is another force that slows the ball down as it travels through the air and bounces on the ground.''',
        'A fast bowler can make the ball travel at 150 km/h! That is because they apply a lot of force. Try throwing a ball gently, then throw it hard. Feel the difference in force?',
        'The fastest cricket ball ever bowled was 161.3 km/h by Shoaib Akhtar! That is faster than most cars on a highway.'
    ))
    
    learning_content.append((
        'Science', 'motion', 'cricket', '9-12',
        'Motion and Speed in Cricket',
        '''Motion means movement from one place to another. In cricket, the ball is always in motion - from the bowler to the batsman, then to the fielders!

Speed tells us how fast something moves. We calculate speed by dividing distance by time. If a ball travels 20 meters in 1 second, its speed is 20 m/s.

Fast bowlers create more speed, while spin bowlers use less speed but make the ball change direction.''',
        'If a cricket ball travels 18 meters from bowler to batsman in 0.5 seconds, what is its speed? Answer: 18 ÷ 0.5 = 36 meters per second!',
        'A cricket ball can spin up to 2500 times per minute when bowled by a spin bowler! That is 41 spins every second.'
    ))

    # DRAWING + SCIENCE
    learning_content.append((
        'Science', 'light', 'drawing', '9-12',
        'Colour Science for Artists',
        '''When you mix paint colours, you are doing science! Red, blue and yellow are primary colours. You cannot make these by mixing other colours.

When light passes through a prism, it splits into 7 rainbow colours - the same colours you use in drawing! This is called the spectrum.

Your eyes have special cells called cones that detect red, green, and blue light. Your brain mixes these to see all the colours!''',
        'Mix red and blue paint. What do you get? Purple! Try mixing yellow and blue. You get green! The same thing happens with light waves in science.',
        'The human eye can see over 10 million different colours! But some animals like butterflies can see even more colours than we can.'
    ))
    
    learning_content.append((
        'Science', 'shadows', 'drawing', '9-12',
        'Light and Shadows in Art',
        '''Shadows are created when an object blocks light. The darker the shadow, the less light reaches that area. Artists use shadows to make drawings look 3D and realistic!

Light travels in straight lines. When it hits an object, it cannot bend around it, so a dark area (shadow) forms behind the object.

The size and shape of a shadow depends on where the light source is. Try moving a lamp around an object and watch the shadow change!''',
        'Hold your hand between a lamp and a wall. See the shadow? Now move your hand closer to the lamp. The shadow gets bigger! This is because your hand blocks more light.',
        'During a solar eclipse, the Moon creates a giant shadow on Earth! That is why the sky gets dark during the day.'
    ))

    # DRAWING + MATHS
    learning_content.append((
        'Maths', 'shapes', 'drawing', '9-12',
        'Geometry in Art',
        '''Shapes are everywhere in art! Circles, squares, triangles, and rectangles are basic shapes that artists use to build complex drawings.

Geometry is the study of shapes and their properties. A circle has no corners, a square has 4 equal sides, and a triangle has 3 sides.

Artists use geometric shapes to plan their drawings. Even complex things like faces and animals can be broken down into simple shapes!''',
        'Try drawing a cat using only circles and triangles! Use a circle for the head, triangles for ears, and ovals for the body. See how shapes build up?',
        'The famous artist Pablo Picasso used geometric shapes in his paintings. His style is called Cubism because everything looks like cubes and other shapes!'
    ))
    
    learning_content.append((
        'Maths', 'symmetry', 'drawing', '9-12',
        'Symmetry in Drawing',
        '''Symmetry means both sides of something look the same, like a mirror image. Many things in nature are symmetrical - butterflies, flowers, and even human faces!

A line of symmetry divides a shape into two identical halves. A circle has infinite lines of symmetry, but a rectangle has only 2.

Artists use symmetry to make their drawings balanced and pleasing to look at. Try folding your drawing in half - do both sides match?''',
        'Draw half of a butterfly on one side of a folded paper. Now trace it on the other side. When you open it, you have a perfectly symmetrical butterfly!',
        'The Taj Mahal in India is perfectly symmetrical! If you draw a line down the middle, both sides are exactly the same.'
    ))

    # FOOTBALL + MATHS
    learning_content.append((
        'Maths', 'angles', 'football', '9-12',
        'Angles in Football',
        '''An angle is formed when two lines meet at a point. In football, understanding angles helps players pass and shoot better!

Angles are measured in degrees. A right angle is 90°, like the corner of a square. A straight line is 180°, and a full circle is 360°.

When a player passes the ball at a 45° angle, it travels diagonally across the field. The best shooters know which angle gives them the best chance to score!''',
        'If you are standing at a 30° angle from the goal, where should you aim? Try different angles and see which gives you the best shot at scoring!',
        'The perfect free kick angle is between 20-30° from the goal! This gives the ball the best curve to go around the wall and into the net.'
    ))
    
    learning_content.append((
        'Maths', 'distance', 'football', '9-12',
        'Distance and Speed in Football',
        '''Distance is how far something travels. In football, players run many kilometers during a match! We measure distance in meters (m) or kilometers (km).

Speed is distance divided by time. If a player runs 100 meters in 10 seconds, their speed is 100 ÷ 10 = 10 m/s.

Professional footballers can run at speeds of 30 km/h or more! That is as fast as a car in a city.''',
        'A football field is 100 meters long. If you run from one end to the other in 15 seconds, what is your speed? Answer: 100 ÷ 15 = 6.67 m/s!',
        'Cristiano Ronaldo can run at 33.6 km/h! That is one of the fastest speeds ever recorded for a footballer.'
    ))

    # FOOTBALL + SCIENCE
    learning_content.append((
        'Science', 'energy', 'football', '9-12',
        'Energy in Football',
        '''Energy is the ability to do work. When you kick a football, you transfer energy from your leg to the ball, making it move!

There are different types of energy. Your body has chemical energy from food. When you run, this becomes kinetic energy (movement energy).

The harder you kick, the more energy you transfer to the ball. This makes it travel faster and farther!''',
        'Try kicking a ball gently, then kick it hard. The hard kick transfers more energy, so the ball goes farther. Where does this energy come from? Your muscles!',
        'A professional footballer can kick a ball at speeds over 130 km/h! That requires a lot of energy transfer from leg to ball.'
    ))
    
    learning_content.append((
        'Science', 'friction', 'football', '9-12',
        'Friction in Football',
        '''Friction is a force that slows things down when they rub against each other. In football, friction between the ball and the ground affects how it rolls.

On a wet field, there is less friction, so the ball slides faster. On dry grass, more friction slows the ball down.

Football boots have studs to increase friction with the ground. This stops players from slipping when they run and turn!''',
        'Roll a ball on smooth floor, then on carpet. Which surface has more friction? The carpet! That is why the ball stops faster on carpet.',
        'The dimples on a golf ball reduce air friction! But footballs are smooth because they need to travel fast through the air.'
    ))

    # SINGING + SCIENCE
    learning_content.append((
        'Science', 'sound', 'singing', '9-12',
        'Science of Sound and Music',
        '''Sound is created when something vibrates (moves back and forth quickly). When you sing, your vocal cords vibrate to create sound waves!

Sound travels through the air as waves. High notes have fast vibrations (high frequency), and low notes have slow vibrations (low frequency).

The loudness of sound is measured in decibels (dB). A whisper is 30 dB, normal talking is 60 dB, and singing can be 70-90 dB!''',
        'Put your hand on your throat while singing a high note, then a low note. Feel the vibrations? High notes vibrate faster than low notes!',
        'The loudest human voice ever recorded was 129 dB! That is as loud as a rock concert or a jet engine.'
    ))
    
    learning_content.append((
        'Science', 'waves', 'singing', '9-12',
        'Sound Waves and Pitch',
        '''Sound travels in waves through the air. These waves are invisible, but we can hear them! The shape and speed of the wave determines what we hear.

Pitch is how high or low a sound is. High pitch means fast vibrations, low pitch means slow vibrations. When you sing high notes, your vocal cords vibrate faster!

Different instruments and voices create different wave patterns. That is why a piano sounds different from a guitar, even when playing the same note.''',
        'Sing "Ahhh" in a low voice, then in a high voice. The high voice has a higher pitch because your vocal cords are vibrating faster!',
        'Dolphins can hear sounds at frequencies up to 150,000 Hz! Humans can only hear up to 20,000 Hz. That is why dog whistles are silent to us!'
    ))

    # SINGING + MATHS
    learning_content.append((
        'Maths', 'patterns', 'singing', '9-12',
        'Musical Patterns and Rhythm',
        '''Music is full of mathematical patterns! A rhythm is a repeating pattern of beats. In a song, beats repeat in patterns like 1-2-3-4, 1-2-3-4.

Time signatures in music are fractions! 4/4 means 4 beats per measure. 3/4 means 3 beats per measure, like in a waltz.

Patterns help us remember songs. Once you know the pattern, you can predict what comes next!''',
        'Clap this pattern: CLAP-clap-clap-CLAP-clap-clap. That is a 1-2-3 pattern! Now try: CLAP-CLAP-clap-clap. That is a 2-2 pattern.',
        'The song "Happy Birthday" is in 3/4 time! That means it has 3 beats per measure. Try counting 1-2-3, 1-2-3 while singing it.'
    ))
    
    learning_content.append((
        'Maths', 'fractions', 'singing', '9-12',
        'Musical Notes and Fractions',
        '''Musical notes are fractions of time! A whole note lasts for 4 beats. A half note lasts for 2 beats (1/2 of a whole note). A quarter note lasts for 1 beat (1/4 of a whole note).

When you add notes together, you are adding fractions! Two half notes (1/2 + 1/2) equal one whole note.

Understanding fractions helps you read music and keep the rhythm correctly!''',
        'If a song has 4 beats per measure and you sing 4 quarter notes, how many beats did you use? Answer: 4 × 1/4 = 1 beat each, so 4 beats total!',
        'The shortest note in music is a 128th note! It lasts for only 1/128 of a whole note. That is super fast!'
    ))

    # CODING + MATHS
    learning_content.append((
        'Maths', 'logic', 'coding', '9-12',
        'Logic and Coding',
        '''Logic is about making decisions based on rules. In coding, we use IF-THEN statements: IF something is true, THEN do this action.

Boolean logic uses TRUE or FALSE. For example: IF score > 10 THEN show "You Win!" This is logical thinking!

Programmers use logic every day to solve problems. Good logical thinking helps you write better code and solve puzzles faster.''',
        'IF you have more than 5 apples THEN you can make a pie. You have 7 apples. Can you make a pie? Yes! Because 7 > 5 is TRUE.',
        'The word "Boolean" comes from George Boole, a mathematician who invented this type of logic in 1854! Now it is used in every computer.'
    ))
    
    learning_content.append((
        'Maths', 'sequences', 'coding', '9-12',
        'Sequences and Loops in Coding',
        '''A sequence is a list of things in order. In coding, we write instructions in sequence: first do this, then do that, then do the next thing.

A loop repeats a sequence multiple times. Instead of writing "print hello" 10 times, we write a loop: REPEAT 10 TIMES: print hello.

Sequences and loops are fundamental to all programming! They help us write less code and do more work.''',
        'Write a sequence: 1. Wake up, 2. Brush teeth, 3. Eat breakfast. Now make it a loop: REPEAT every day! That is how computers work.',
        'The longest computer program ever written has over 50 million lines of code! Without loops and sequences, it would be impossible to write.'
    ))

    # CODING + SCIENCE
    learning_content.append((
        'Science', 'electricity', 'coding', '9-12',
        'How Computers Use Electricity',
        '''Computers run on electricity! Inside a computer, tiny switches called transistors turn on and off millions of times per second.

When electricity flows through a transistor, it represents 1 (ON). When no electricity flows, it represents 0 (OFF). This is called binary code!

Everything you see on a computer screen - games, videos, websites - is made from billions of 1s and 0s. That is how computers understand your code!''',
        'Try this: Light ON = 1, Light OFF = 0. Flash a light 3 times: ON-OFF-ON = 101 in binary! That is how computers send messages.',
        'A modern computer processor has over 10 billion transistors! Each one switches on and off billions of times per second.'
    ))
    
    learning_content.append((
        'Science', 'algorithms', 'coding', '9-12',
        'Algorithms in Nature and Coding',
        '''An algorithm is a step-by-step process to solve a problem. Cooking recipes are algorithms! Follow the steps in order and you get the result.

Nature uses algorithms too! Ants use algorithms to find the shortest path to food. Bees use algorithms to build perfect hexagonal honeycombs.

In coding, we write algorithms to tell computers how to solve problems. A good algorithm is fast and efficient!''',
        'Algorithm to make a sandwich: 1. Get bread, 2. Add filling, 3. Put bread on top. Now write an algorithm to tie your shoelaces!',
        'Google uses an algorithm called PageRank to decide which websites to show you first! It was invented by Larry Page and Sergey Brin.'
    ))
    
    # Insert all learning content
    insert_content_query = """
        INSERT INTO learning_content 
        (subject, concept, hobby_context, age_group, lesson_title, lesson_body, hobby_example, fun_fact) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor.executemany(insert_content_query, learning_content)
    conn.commit()
    
    print(f"✅ Inserted {len(learning_content)} learning content items")
    print(f"   - Cricket: {sum(1 for x in learning_content if x[2] == 'cricket')}")
    print(f"   - Drawing: {sum(1 for x in learning_content if x[2] == 'drawing')}")
    print(f"   - Football: {sum(1 for x in learning_content if x[2] == 'football')}")
    print(f"   - Singing: {sum(1 for x in learning_content if x[2] == 'singing')}")
    print(f"   - Coding: {sum(1 for x in learning_content if x[2] == 'coding')}")

    
    # Now seed quiz questions for each content
    print("\n🎯 Seeding Quiz Questions...")
    
    # Get all content IDs
    cursor.execute("SELECT content_id, lesson_title, concept FROM learning_content ORDER BY content_id")
    content_items = cursor.fetchall()
    
    quiz_questions = []
    
    for content in content_items:
        content_id = content[0]
        title = content[1]
        concept = content[2]
        
        # Generate 5 quiz questions based on the concept
        if concept == 'fractions' and 'Cricket' in title:
            quiz_questions.extend([
                (content_id, 'In cricket, one over has how many balls?', '4 balls', '5 balls', '6 balls', '8 balls', 'C', 'One over in cricket always has exactly 6 balls! So 3 overs = 18 balls total.'),
                (content_id, 'What fraction of an over is 3 balls?', '1/2', '1/3', '2/3', '3/4', 'A', '3 out of 6 balls = 3/6 = 1/2 of an over! Just like sharing a pizza equally.'),
                (content_id, 'If a bowler bowls 4 out of 6 balls, what fraction is left?', '1/6', '2/6', '3/6', '4/6', 'B', '6 - 4 = 2 balls left. So 2/6 of the over remains!'),
                (content_id, 'Simplify the fraction 4/6', '1/2', '2/3', '3/4', '4/5', 'B', '4/6 can be divided by 2 on both top and bottom: 4÷2 = 2, 6÷2 = 3. So 4/6 = 2/3!'),
                (content_id, 'A team scored 120 runs in 20 overs. What is the run rate per over?', '5', '6', '7', '8', 'B', 'Run rate = Total Runs ÷ Total Overs = 120 ÷ 20 = 6 runs per over!')
            ])
        
        elif concept == 'averages':
            quiz_questions.extend([
                (content_id, 'What is an average?', 'The biggest number', 'The total divided by count', 'The smallest number', 'The middle number', 'B', 'Average = Total ÷ Count. It tells us the typical value!'),
                (content_id, 'A player scored 30, 40, and 50 runs in 3 matches. What is the average?', '35', '40', '45', '50', 'B', 'Total = 30+40+50 = 120. Average = 120 ÷ 3 = 40 runs!'),
                (content_id, 'If a batsman scored 200 runs in 5 innings, what is the average per innings?', '30', '35', '40', '45', 'C', '200 ÷ 5 = 40 runs per innings!'),
                (content_id, 'A player has an average of 50 after 10 innings. How many total runs?', '400', '450', '500', '550', 'C', 'Total = Average × Count = 50 × 10 = 500 runs!'),
                (content_id, 'Which average is better for a batsman?', '25', '35', '45', '55', 'D', 'Higher average means more runs per innings! 55 is the best.')
            ])
        
        elif concept == 'forces':
            quiz_questions.extend([
                (content_id, 'What is a force?', 'A type of ball', 'A push or pull', 'A cricket team', 'A type of run', 'B', 'A force is a push or pull that makes things move, stop, or change direction!'),
                (content_id, 'What happens when a bowler applies more force to the ball?', 'It moves slower', 'It moves faster', 'It stops', 'It disappears', 'B', 'More force = more speed! That is why fast bowlers run fast before bowling.'),
                (content_id, 'Which force slows down a cricket ball as it travels?', 'Gravity', 'Friction', 'Magnetism', 'Electricity', 'B', 'Friction with air and ground slows the ball down!'),
                (content_id, 'What makes a ball fall to the ground after being hit?', 'Wind', 'Friction', 'Gravity', 'Force from bat', 'C', 'Gravity pulls everything down towards Earth!'),
                (content_id, 'A fast bowler runs before bowling to:', 'Look good', 'Apply more force', 'Confuse batsman', 'Save energy', 'B', 'Running builds up speed and force, making the ball travel faster!')
            ])
        
        elif concept == 'motion':
            quiz_questions.extend([
                (content_id, 'What is motion?', 'Standing still', 'Movement from one place to another', 'Sleeping', 'Sitting down', 'B', 'Motion means moving from one place to another!'),
                (content_id, 'How do we calculate speed?', 'Distance + Time', 'Distance - Time', 'Distance × Time', 'Distance ÷ Time', 'D', 'Speed = Distance ÷ Time. If you travel 100m in 10s, speed = 100÷10 = 10 m/s!'),
                (content_id, 'A ball travels 20 meters in 2 seconds. What is its speed?', '5 m/s', '10 m/s', '15 m/s', '20 m/s', 'B', '20 ÷ 2 = 10 meters per second!'),
                (content_id, 'Which has more speed?', 'A ball taking 5s to travel 50m', 'A ball taking 10s to travel 50m', 'Both same', 'Cannot tell', 'A', 'First ball: 50÷5=10 m/s. Second ball: 50÷10=5 m/s. First is faster!'),
                (content_id, 'What unit measures speed?', 'Meters', 'Seconds', 'Meters per second', 'Kilograms', 'C', 'Speed is measured in meters per second (m/s) or kilometers per hour (km/h)!')
            ])

        
        elif concept == 'light':
            quiz_questions.extend([
                (content_id, 'What are the three primary colours?', 'Red, Green, Blue', 'Red, Blue, Yellow', 'Orange, Purple, Green', 'Black, White, Grey', 'B', 'Primary colours are Red, Blue, and Yellow! You cannot make these by mixing other colours.'),
                (content_id, 'What colour do you get when you mix red and blue?', 'Green', 'Orange', 'Purple', 'Brown', 'C', 'Red + Blue = Purple! Try it with paint or crayons.'),
                (content_id, 'What colour do you get when you mix yellow and blue?', 'Green', 'Orange', 'Purple', 'Red', 'A', 'Yellow + Blue = Green! This is how artists make green paint.'),
                (content_id, 'How many colours are in a rainbow?', '5', '6', '7', '8', 'C', 'A rainbow has 7 colours: Red, Orange, Yellow, Green, Blue, Indigo, Violet!'),
                (content_id, 'What happens when white light passes through a prism?', 'It disappears', 'It splits into rainbow colours', 'It turns black', 'Nothing happens', 'B', 'A prism splits white light into 7 rainbow colours! This is called the spectrum.')
            ])
        
        elif concept == 'shadows':
            quiz_questions.extend([
                (content_id, 'What creates a shadow?', 'Wind', 'Sound', 'Light being blocked', 'Rain', 'C', 'A shadow forms when an object blocks light!'),
                (content_id, 'When is your shadow longest?', 'At noon', 'In the morning or evening', 'At midnight', 'Shadows are always same size', 'B', 'When the sun is low (morning/evening), shadows are longest!'),
                (content_id, 'What happens to a shadow when you move closer to a light source?', 'Gets smaller', 'Gets bigger', 'Stays same', 'Disappears', 'B', 'Moving closer to light makes your shadow bigger!'),
                (content_id, 'Can you have a shadow without light?', 'Yes', 'No', 'Sometimes', 'Only at night', 'B', 'No light = no shadow! You need light to create shadows.'),
                (content_id, 'Why do artists draw shadows?', 'To make drawings look 3D', 'To waste time', 'To use more pencils', 'Shadows are not important', 'A', 'Shadows make drawings look realistic and 3D!')
            ])
        
        elif concept == 'shapes':
            quiz_questions.extend([
                (content_id, 'How many sides does a triangle have?', '2', '3', '4', '5', 'B', 'A triangle has 3 sides and 3 corners!'),
                (content_id, 'Which shape has 4 equal sides?', 'Rectangle', 'Triangle', 'Square', 'Circle', 'C', 'A square has 4 equal sides and 4 right angles!'),
                (content_id, 'How many corners does a circle have?', '0', '1', '2', '4', 'A', 'A circle has no corners! It is perfectly round.'),
                (content_id, 'What is geometry?', 'Study of animals', 'Study of shapes', 'Study of plants', 'Study of weather', 'B', 'Geometry is the study of shapes and their properties!'),
                (content_id, 'Which shape has 4 sides but not all equal?', 'Square', 'Circle', 'Rectangle', 'Triangle', 'C', 'A rectangle has 4 sides, but only opposite sides are equal!')
            ])
        
        elif concept == 'symmetry':
            quiz_questions.extend([
                (content_id, 'What is symmetry?', 'Both sides look the same', 'Both sides look different', 'Only one side', 'No sides', 'A', 'Symmetry means both sides are mirror images of each other!'),
                (content_id, 'Which letter is symmetrical?', 'F', 'L', 'A', 'P', 'C', 'The letter A is symmetrical! Draw a line down the middle and both sides match.'),
                (content_id, 'How many lines of symmetry does a circle have?', '0', '1', '4', 'Infinite', 'D', 'A circle has infinite lines of symmetry! You can draw a line anywhere through the center.'),
                (content_id, 'Which animal is symmetrical?', 'Butterfly', 'Snail', 'Crab walking sideways', 'All animals', 'A', 'Butterflies are perfectly symmetrical! Both wings are mirror images.'),
                (content_id, 'How many lines of symmetry does a square have?', '1', '2', '3', '4', 'D', 'A square has 4 lines of symmetry: 2 diagonal and 2 through the middle!')
            ])
        
        elif concept == 'angles':
            quiz_questions.extend([
                (content_id, 'What is an angle?', 'A type of ball', 'Where two lines meet', 'A football player', 'A type of goal', 'B', 'An angle is formed where two lines meet at a point!'),
                (content_id, 'How many degrees in a right angle?', '45°', '60°', '90°', '180°', 'C', 'A right angle is exactly 90°, like the corner of a square!'),
                (content_id, 'How many degrees in a straight line?', '90°', '180°', '270°', '360°', 'B', 'A straight line is 180°, exactly half of a full circle!'),
                (content_id, 'How many degrees in a full circle?', '180°', '270°', '360°', '450°', 'C', 'A full circle is 360°! That is why we say "360 degree view".'),
                (content_id, 'What angle is less than 90°?', 'Right angle', 'Acute angle', 'Obtuse angle', 'Straight angle', 'B', 'An acute angle is less than 90°, like a sharp corner!')
            ])

        
        elif concept == 'distance':
            quiz_questions.extend([
                (content_id, 'What is distance?', 'How heavy something is', 'How far something travels', 'How fast something moves', 'How tall something is', 'B', 'Distance is how far something travels from one place to another!'),
                (content_id, 'A football field is 100 meters long. If you run from one end to the other, what distance did you cover?', '50m', '75m', '100m', '200m', 'C', 'You covered the full length = 100 meters!'),
                (content_id, 'If you run 100m in 20 seconds, what is your speed?', '3 m/s', '5 m/s', '10 m/s', '20 m/s', 'B', 'Speed = Distance ÷ Time = 100 ÷ 20 = 5 m/s!'),
                (content_id, 'Which unit measures distance?', 'Seconds', 'Meters', 'Kilograms', 'Degrees', 'B', 'Distance is measured in meters (m) or kilometers (km)!'),
                (content_id, 'If you run around a 400m track twice, what total distance?', '400m', '600m', '800m', '1000m', 'C', '400m × 2 = 800 meters total!')
            ])
        
        elif concept == 'energy':
            quiz_questions.extend([
                (content_id, 'What is energy?', 'The ability to do work', 'A type of food', 'A football move', 'A team name', 'A', 'Energy is the ability to do work or make things move!'),
                (content_id, 'Where does your body get energy from?', 'Air', 'Food', 'Water only', 'Sleep only', 'B', 'Your body gets chemical energy from food! This powers your muscles.'),
                (content_id, 'What type of energy does a moving ball have?', 'Chemical energy', 'Light energy', 'Kinetic energy', 'Sound energy', 'C', 'Kinetic energy is movement energy! A moving ball has kinetic energy.'),
                (content_id, 'When you kick a ball, you transfer energy from:', 'Ball to leg', 'Leg to ball', 'Ground to ball', 'Air to ball', 'B', 'You transfer energy from your leg to the ball, making it move!'),
                (content_id, 'What happens when you kick a ball harder?', 'Less energy transferred', 'Same energy transferred', 'More energy transferred', 'No energy transferred', 'C', 'Kicking harder transfers more energy, so the ball goes farther!')
            ])
        
        elif concept == 'friction':
            quiz_questions.extend([
                (content_id, 'What is friction?', 'A force that speeds things up', 'A force that slows things down', 'A type of energy', 'A football move', 'B', 'Friction is a force that slows things down when surfaces rub together!'),
                (content_id, 'Where is there more friction?', 'Ice', 'Smooth floor', 'Rough carpet', 'Water', 'C', 'Rough surfaces like carpet have more friction than smooth surfaces!'),
                (content_id, 'Why do football boots have studs?', 'To look cool', 'To increase friction', 'To decrease friction', 'To make noise', 'B', 'Studs increase friction with the ground, stopping players from slipping!'),
                (content_id, 'On which surface will a ball roll farther?', 'Rough grass', 'Smooth floor', 'Sand', 'Gravel', 'B', 'Smooth floor has less friction, so the ball rolls farther!'),
                (content_id, 'What happens to friction on a wet field?', 'Increases', 'Decreases', 'Stays same', 'Disappears', 'B', 'Water acts like a lubricant, reducing friction!')
            ])
        
        elif concept == 'sound':
            quiz_questions.extend([
                (content_id, 'How is sound created?', 'By light', 'By vibrations', 'By colors', 'By smell', 'B', 'Sound is created when something vibrates (moves back and forth quickly)!'),
                (content_id, 'What vibrates when you sing?', 'Your teeth', 'Your vocal cords', 'Your ears', 'Your nose', 'B', 'Your vocal cords vibrate to create sound when you sing or talk!'),
                (content_id, 'Which note has faster vibrations?', 'Low note', 'High note', 'Both same', 'Neither vibrates', 'B', 'High notes have faster vibrations (high frequency)!'),
                (content_id, 'What is loudness measured in?', 'Meters', 'Decibels', 'Kilograms', 'Degrees', 'B', 'Loudness is measured in decibels (dB)!'),
                (content_id, 'How does sound travel?', 'As waves through air', 'As light beams', 'As electricity', 'It does not travel', 'A', 'Sound travels as waves through air, water, or solid objects!')
            ])

        
        elif concept == 'waves':
            quiz_questions.extend([
                (content_id, 'What is pitch?', 'How loud a sound is', 'How high or low a sound is', 'How long a sound lasts', 'How fast sound travels', 'B', 'Pitch is how high or low a sound is!'),
                (content_id, 'High pitch means:', 'Slow vibrations', 'Fast vibrations', 'No vibrations', 'Medium vibrations', 'B', 'High pitch = fast vibrations! Low pitch = slow vibrations.'),
                (content_id, 'Sound travels as:', 'Straight lines', 'Waves', 'Circles', 'Squares', 'B', 'Sound travels in waves through the air!'),
                (content_id, 'Can sound travel through space?', 'Yes', 'No', 'Sometimes', 'Only at night', 'B', 'No! Space has no air, so sound cannot travel. That is why space is silent!'),
                (content_id, 'Why does a piano sound different from a guitar?', 'Different wave patterns', 'Different colors', 'Different sizes only', 'They sound the same', 'A', 'Different instruments create different wave patterns, giving them unique sounds!')
            ])
        
        elif concept == 'patterns':
            quiz_questions.extend([
                (content_id, 'What is a pattern?', 'Something that repeats', 'Something random', 'Something that never repeats', 'Something invisible', 'A', 'A pattern is something that repeats in a predictable way!'),
                (content_id, 'In music, what is a rhythm?', 'A type of instrument', 'A repeating pattern of beats', 'A type of song', 'A music note', 'B', 'Rhythm is a repeating pattern of beats in music!'),
                (content_id, 'What does 4/4 time signature mean?', '4 beats per measure', '4 songs', '4 instruments', '4 singers', 'A', '4/4 means 4 beats per measure! It is the most common time signature.'),
                (content_id, 'Which is a pattern?', '1-2-3-1-2-3-1-2-3', '5-7-2-9-1-4-8', 'Random numbers', 'No numbers', 'A', '1-2-3 repeats, so it is a pattern!'),
                (content_id, 'Patterns in music help us:', 'Forget the song', 'Remember and predict what comes next', 'Make mistakes', 'Stop singing', 'B', 'Patterns help us remember songs and predict what comes next!')
            ])
        
        elif concept == 'logic':
            quiz_questions.extend([
                (content_id, 'What is logic?', 'Making random choices', 'Making decisions based on rules', 'Guessing', 'Ignoring rules', 'B', 'Logic is making decisions based on rules and reasoning!'),
                (content_id, 'In coding, IF-THEN means:', 'Do nothing', 'If something is true, then do an action', 'Always do everything', 'Never do anything', 'B', 'IF-THEN: If a condition is true, then perform an action!'),
                (content_id, 'What are the two values in Boolean logic?', 'Yes and No', 'TRUE and FALSE', '1 and 2', 'On and Off', 'B', 'Boolean logic uses TRUE and FALSE!'),
                (content_id, 'IF score > 10 THEN "You Win!". If score = 15, what happens?', 'Nothing', 'You Win!', 'You Lose', 'Error', 'B', '15 > 10 is TRUE, so "You Win!" is shown!'),
                (content_id, 'Logic helps programmers:', 'Write confusing code', 'Solve problems and make decisions', 'Avoid thinking', 'Make errors', 'B', 'Logic helps programmers solve problems and write better code!')
            ])
        
        elif concept == 'sequences':
            quiz_questions.extend([
                (content_id, 'What is a sequence?', 'Random things', 'Things in order', 'Things backwards', 'No things', 'B', 'A sequence is a list of things in a specific order!'),
                (content_id, 'In coding, what is a loop?', 'A mistake', 'Repeating a sequence multiple times', 'Writing code once', 'Deleting code', 'B', 'A loop repeats a sequence of instructions multiple times!'),
                (content_id, 'Which is a sequence?', '1, 2, 3, 4, 5', '5, 2, 9, 1, 7', 'Random letters', 'No order', 'A', '1, 2, 3, 4, 5 is in order, so it is a sequence!'),
                (content_id, 'Why use loops in coding?', 'To write more code', 'To write less code and do more work', 'To make errors', 'To confuse people', 'B', 'Loops help us write less code and do more work efficiently!'),
                (content_id, 'What comes next in this sequence: 2, 4, 6, 8, ?', '9', '10', '11', '12', 'B', 'The pattern adds 2 each time: 2, 4, 6, 8, 10!')
            ])
        
        elif concept == 'electricity':
            quiz_questions.extend([
                (content_id, 'What do computers run on?', 'Water', 'Electricity', 'Wind', 'Food', 'B', 'Computers run on electricity!'),
                (content_id, 'What is a transistor?', 'A type of computer game', 'A tiny switch inside computers', 'A computer screen', 'A keyboard', 'B', 'A transistor is a tiny switch that turns on and off!'),
                (content_id, 'In binary code, what does 1 represent?', 'OFF', 'ON', 'Maybe', 'Error', 'B', 'In binary: 1 = ON (electricity flowing), 0 = OFF (no electricity)!'),
                (content_id, 'What is binary code made of?', 'Letters', '1s and 0s', 'Colors', 'Sounds', 'B', 'Binary code uses only 1s and 0s!'),
                (content_id, 'How do computers understand your code?', 'They read English', 'They convert it to binary (1s and 0s)', 'They guess', 'They do not understand', 'B', 'Computers convert everything to binary code (1s and 0s)!')
            ])
        
        elif concept == 'algorithms':
            quiz_questions.extend([
                (content_id, 'What is an algorithm?', 'A type of computer', 'A step-by-step process to solve a problem', 'A programming language', 'A computer game', 'B', 'An algorithm is a step-by-step process to solve a problem!'),
                (content_id, 'Which is an example of an algorithm?', 'A cooking recipe', 'A random action', 'Doing nothing', 'Guessing', 'A', 'A recipe is an algorithm! Follow the steps in order to get the result.'),
                (content_id, 'Do algorithms exist in nature?', 'No, only in computers', 'Yes, ants and bees use algorithms', 'Only in books', 'Only in games', 'B', 'Yes! Ants use algorithms to find food, bees use them to build hives!'),
                (content_id, 'A good algorithm should be:', 'Slow and confusing', 'Fast and efficient', 'Random', 'Impossible to follow', 'B', 'A good algorithm is fast, efficient, and easy to follow!'),
                (content_id, 'What does Google use to find websites?', 'Random guessing', 'An algorithm called PageRank', 'Magic', 'Nothing', 'B', 'Google uses the PageRank algorithm to decide which websites to show first!')
            ])
    
    # Insert all quiz questions
    insert_quiz_query = """
        INSERT INTO quiz_questions 
        (content_id, question_text, option_a, option_b, option_c, option_d, correct_option, explanation) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor.executemany(insert_quiz_query, quiz_questions)
    conn.commit()
    
    print(f"✅ Inserted {len(quiz_questions)} quiz questions")
    print(f"   - Average {len(quiz_questions) // len(content_items)} questions per lesson")
    
    cursor.close()
    conn.close()
    
    print("\n🎉 Seeding complete!")
    print(f"\n📊 Summary:")
    print(f"   - {len(learning_content)} learning content items")
    print(f"   - {len(quiz_questions)} quiz questions")
    print(f"   - 5 hobby contexts covered")
    print(f"   - 3 subjects covered (Maths, Science, English)")

if __name__ == '__main__':
    print("🌱 Starting Learning Content Seeding...\n")
    seed_learning_content()

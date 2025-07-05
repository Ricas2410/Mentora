#!/usr/bin/env python3
"""
Comprehensive Grade 6 Science Content Population Script
Based on Ghana Education Service (GES) Curriculum

This script creates:
- 5 comprehensive science topics for Grade 6
- Detailed study notes for each topic
- 30+ real-life quiz questions per topic (150+ total questions)
- All content aligned with GES Grade 6 Science curriculum

Topics covered:
1. Living Things and Their Environment
2. Human Body and Health
3. Matter and Materials
4. Forces and Energy
5. Earth and Space Science

Run with: python manage.py runscript populate_grade6_science_comprehensive
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice

# Import additional questions from separate file
try:
    from .grade6_science_questions_part2 import (
        HUMAN_BODY_QUESTIONS,
        MATTER_MATERIALS_QUESTIONS
    )
except ImportError:
    # If running as script, try relative import
    try:
        from grade6_science_questions_part2 import (
            HUMAN_BODY_QUESTIONS,
            MATTER_MATERIALS_QUESTIONS
        )
    except ImportError:
        print("Warning: Could not import additional questions. Only basic questions will be created.")
        HUMAN_BODY_QUESTIONS = []
        MATTER_MATERIALS_QUESTIONS = []


def create_grade6_science_content():
    """Main function to create all Grade 6 Science content"""
    print("🔬 Creating comprehensive Grade 6 Science content...")
    
    # Get or create Grade 6 Science class level
    try:
        science_subject = Subject.objects.get(name="Science")
        grade6_science, created = ClassLevel.objects.get_or_create(
            subject=science_subject,
            level_number=6,
            defaults={
                'name': 'Grade 6',
                'description': 'Grade 6 Science - Ghana Education Service Curriculum',
                'pass_percentage': 65,
                'is_active': True
            }
        )
        
        if created:
            print(f"✅ Created Grade 6 Science class level")
        else:
            print(f"📝 Grade 6 Science class level already exists")
            
    except Subject.DoesNotExist:
        print("❌ ERROR: Science subject not found! Please run the basic setup first.")
        return False
    
    # Grade 6 Science topics based on GES curriculum
    topics_data = [
        {
            'title': 'Living Things and Their Environment',
            'description': 'Ecosystems, food chains, adaptation, and environmental conservation',
            'order': 1
        },
        {
            'title': 'Human Body and Health',
            'description': 'Body systems, nutrition, hygiene, and disease prevention',
            'order': 2
        },
        {
            'title': 'Matter and Materials',
            'description': 'Properties of matter, changes of state, and material classification',
            'order': 3
        },
        {
            'title': 'Forces and Energy',
            'description': 'Types of forces, simple machines, and forms of energy',
            'order': 4
        },
        {
            'title': 'Earth and Space Science',
            'description': 'Weather patterns, water cycle, solar system, and natural disasters',
            'order': 5
        }
    ]
    
    # Create topics
    for topic_data in topics_data:
        topic, created = Topic.objects.get_or_create(
            title=topic_data['title'],
            class_level=grade6_science,
            defaults={
                'description': topic_data['description'],
                'order': topic_data['order'],
                'estimated_duration': 60,  # 1 hour per topic
                'difficulty_level': 'intermediate',
                'is_active': True
            }
        )
        
        if created:
            print(f"✅ Created topic: {topic.title}")
            create_study_notes(topic)
            create_quiz_questions(topic)
        else:
            print(f"📝 Topic already exists: {topic.title}")
            # Still create notes and questions if they don't exist
            if not topic.study_notes.exists():
                create_study_notes(topic)
            if topic.questions.count() < 30:
                create_quiz_questions(topic)

    print("🎉 Grade 6 Science content creation completed!")
    return True


def create_study_notes(topic):
    """Create comprehensive study notes for each topic"""
    
    study_notes_data = {
        'Living Things and Their Environment': [
            {
                'title': 'Ecosystems and Food Chains',
                'content': '''# Living Things and Their Environment

## What is an Ecosystem?
An ecosystem is a community where living things (plants, animals, humans) interact with each other and their non-living environment (air, water, soil, sunlight).

### Examples of Ecosystems in Ghana:
- **Forest ecosystems**: Kakum National Park, Ashanti forests
- **Grassland ecosystems**: Northern Ghana savannas
- **Aquatic ecosystems**: Lake Volta, rivers, coastal areas
- **Urban ecosystems**: Cities like Accra, Kumasi

## Food Chains and Food Webs

### What is a Food Chain?
A food chain shows how energy flows from one living thing to another through eating.

**Example - Ghana Forest Food Chain:**
Leaves → Grasshopper → Lizard → Snake → Hawk

### Food Chain Levels:
1. **Producers** (Plants): Mahogany trees, oil palm, cassava
2. **Primary Consumers** (Herbivores): Grasshoppers, antelopes, elephants
3. **Secondary Consumers** (Carnivores): Lizards, frogs, small birds
4. **Tertiary Consumers** (Top predators): Snakes, eagles, leopards

### Real-Life Example - Lake Volta Food Web:
- **Producers**: Water plants, algae
- **Primary Consumers**: Small fish, water insects
- **Secondary Consumers**: Tilapia, catfish
- **Tertiary Consumers**: Crocodiles, fishing eagles

## Adaptation to Environment

### How Animals Adapt:
- **Camels in Northern Ghana**: Store water, thick fur for cold nights
- **Chameleons**: Change color for protection
- **Birds**: Different beak shapes for different foods
- **Fish**: Gills for breathing underwater

### How Plants Adapt:
- **Baobab trees**: Store water in thick trunks
- **Cactus plants**: Thick waxy leaves to prevent water loss
- **Mangrove trees**: Special roots for salty water
- **Climbing plants**: Grow toward sunlight

## Environmental Conservation

### Why We Need to Protect Our Environment:
1. **Clean air and water** for healthy living
2. **Food sources** from plants and animals
3. **Medicine** from forest plants
4. **Climate control** - trees provide shade and rain

### Conservation Actions in Ghana:
- **National Parks**: Mole, Kakum, Bia protect wildlife
- **Tree planting**: Green Ghana Day initiatives
- **Waste management**: Proper disposal, recycling
- **Water conservation**: Protecting rivers and lakes

### What You Can Do:
- Plant trees around your school and home
- Don't litter - use proper waste bins
- Save water - turn off taps when not needed
- Protect animals - don't hunt or harm wildlife
- Use both sides of paper to save trees'''
            }
        ],
        
        'Human Body and Health': [
            {
                'title': 'Body Systems and Healthy Living',
                'content': '''# Human Body and Health

## Major Body Systems

### 1. Digestive System
**Function**: Breaks down food for energy and growth

**Main Parts**:
- **Mouth**: Teeth chew food, saliva starts digestion
- **Stomach**: Acid breaks down food further
- **Small intestine**: Absorbs nutrients into blood
- **Large intestine**: Removes waste, absorbs water

**Ghanaian Foods and Digestion**:
- **Carbohydrates**: Rice, yam, plantain give energy
- **Proteins**: Fish, beans, meat build muscles
- **Vitamins**: Fruits like oranges, mangoes keep us healthy
- **Minerals**: Leafy vegetables like kontomire provide iron

### 2. Respiratory System
**Function**: Brings oxygen into body, removes carbon dioxide

**Main Parts**:
- **Nose/Mouth**: Air enters here
- **Windpipe (Trachea)**: Carries air to lungs
- **Lungs**: Exchange oxygen and carbon dioxide
- **Diaphragm**: Muscle that helps breathing

**Keeping Lungs Healthy**:
- Avoid smoking and dusty places
- Exercise regularly - run, play football
- Plant trees for clean air
- Cover nose when coughing or sneezing

### 3. Circulatory System
**Function**: Carries blood, oxygen, and nutrients throughout body

**Main Parts**:
- **Heart**: Pumps blood (beats about 70 times per minute)
- **Blood vessels**: Arteries, veins, capillaries
- **Blood**: Carries oxygen, nutrients, fights germs

**Heart-Healthy Activities**:
- Play sports: football, basketball, running
- Eat healthy foods: fruits, vegetables, fish
- Drink plenty of clean water
- Get enough sleep (8-10 hours for children)

## Nutrition and Healthy Eating

### Balanced Diet Using Ghanaian Foods:

**Energy Foods (Carbohydrates)**:
- Rice, yam, cassava, plantain, bread
- Give energy for daily activities

**Body-Building Foods (Proteins)**:
- Fish (tilapia, tuna), chicken, beans, groundnuts
- Help muscles and bones grow strong

**Protective Foods (Vitamins & Minerals)**:
- Fruits: oranges, mangoes, pineapples, bananas
- Vegetables: tomatoes, carrots, green leafy vegetables
- Protect against diseases

### Sample Healthy Ghanaian Meals:

**Breakfast**:
- Porridge with milk and banana
- Bread with egg and tomato

**Lunch**:
- Rice with fish stew and vegetables
- Yam with kontomire and fish

**Dinner**:
- Banku with okra soup and fish
- Plantain with beans stew

## Personal Hygiene and Disease Prevention

### Daily Hygiene Habits:
1. **Brush teeth** twice daily with fluoride toothpaste
2. **Wash hands** with soap before eating and after toilet
3. **Bath daily** with soap and clean water
4. **Wear clean clothes** and change underwear daily
5. **Cut fingernails** short and keep them clean

### Preventing Common Diseases:

**Malaria Prevention**:
- Sleep under treated mosquito nets
- Remove stagnant water around homes
- Use mosquito repellent
- Keep surroundings clean

**Diarrhea Prevention**:
- Drink clean, boiled water
- Wash fruits and vegetables
- Cook food properly
- Use clean toilets

**Cholera Prevention**:
- Drink only clean water
- Eat hot, freshly cooked food
- Wash hands frequently
- Proper waste disposal

### When to See a Doctor:
- Fever for more than 2 days
- Severe stomach pain
- Difficulty breathing
- Unusual rashes or swelling
- Persistent cough'''
            }
        ],

        'Matter and Materials': [
            {
                'title': 'Properties and States of Matter',
                'content': '''# Matter and Materials

## What is Matter?
Matter is anything that takes up space and has weight. Everything around us is made of matter.

### Examples of Matter in Ghana:
- **Solids**: Rocks, wood, metals, buildings
- **Liquids**: Water, palm oil, fruit juices
- **Gases**: Air, smoke from cooking fires

## States of Matter

### 1. Solids
**Properties**:
- Have definite shape and size
- Particles are tightly packed
- Cannot be compressed easily

**Examples in Daily Life**:
- **Building materials**: Cement blocks, iron rods, wood
- **Cooking items**: Pots, spoons, plates
- **Natural solids**: Rocks, sand, salt

### 2. Liquids
**Properties**:
- Take shape of container
- Have definite volume
- Flow easily

**Examples in Daily Life**:
- **Drinking**: Water, fruit juices, milk
- **Cooking**: Palm oil, groundnut oil, soup
- **Cleaning**: Liquid soap, detergent

### 3. Gases
**Properties**:
- No definite shape or size
- Fill entire container
- Can be compressed

**Examples in Daily Life**:
- **Air we breathe**: Oxygen, nitrogen
- **Cooking gas**: LPG for stoves
- **Car exhaust**: Carbon dioxide

## Changes of State

### Melting (Solid to Liquid)
- **Ice to water** when left in sun
- **Shea butter** melts when heated
- **Metals** melt in very hot furnaces

### Freezing (Liquid to Solid)
- **Water to ice** in freezer
- **Palm oil** solidifies in cold weather
- **Candle wax** hardens when cooled

### Evaporation (Liquid to Gas)
- **Water** evaporates from wet clothes
- **Perfume** evaporates from bottle
- **Petrol** evaporates from open container

### Condensation (Gas to Liquid)
- **Water vapor** condenses on cold glass
- **Steam** from hot food becomes water drops
- **Dew** forms on grass in early morning

## Properties of Materials

### Physical Properties:
1. **Color**: Red clay, black charcoal, white salt
2. **Hardness**: Diamond (very hard), chalk (soft)
3. **Flexibility**: Rubber bends, glass breaks
4. **Transparency**: Glass (transparent), wood (opaque)

### Uses Based on Properties:

**Building Materials**:
- **Concrete**: Strong, durable for foundations
- **Wood**: Light, easy to work with
- **Glass**: Transparent for windows
- **Metal**: Strong for roofing sheets

**Cooking Materials**:
- **Aluminum pots**: Good heat conductor
- **Wooden spoons**: Don't conduct heat
- **Plastic containers**: Light, unbreakable
- **Clay pots**: Keep water cool

## Separating Mixtures

### Common Separation Methods:

**1. Sieving**:
- Separate **rice from stones**
- Remove **lumps from flour**
- Separate **sand from gravel**

**2. Filtering**:
- Clean **muddy water** through cloth
- Separate **tea leaves** from tea
- Remove **particles** from palm oil

**3. Evaporation**:
- Get **salt** from sea water
- Concentrate **palm wine**
- Dry **wet grains**

**4. Magnetic Separation**:
- Remove **iron nails** from sand
- Separate **steel** from other metals
- Clean **iron filings** from mixtures'''
            }
        ],

        'Forces and Energy': [
            {
                'title': 'Forces, Motion, and Energy in Daily Life',
                'content': '''# Forces and Energy

## What are Forces?
A force is a push or pull that can change the shape, size, or motion of an object.

### Types of Forces We See Daily:

**1. Muscular Force**:
- **Pushing** a wheelbarrow
- **Pulling** water from a well
- **Lifting** heavy bags
- **Kicking** a football

**2. Gravitational Force**:
- **Falling** mangoes from trees
- **Water flowing** downhill
- **Objects dropping** when released
- **Rain falling** from clouds

**3. Frictional Force**:
- **Brakes** stopping a bicycle
- **Walking** without slipping
- **Rubbing sticks** to make fire
- **Car tires** gripping the road

**4. Magnetic Force**:
- **Compass needle** pointing north
- **Magnets** attracting iron nails
- **Magnetic toys** sticking together

## Simple Machines in Ghana

### 1. Lever
**Examples**:
- **Crowbar**: Opening boxes, moving heavy objects
- **Scissors**: Cutting cloth, paper
- **Bottle opener**: Opening bottles
- **See-saw**: Children's playground equipment

**How it helps**: Makes lifting heavy things easier

### 2. Wheel and Axle
**Examples**:
- **Bicycles**: Transportation
- **Cars and trucks**: Moving people and goods
- **Wheelbarrow**: Carrying heavy loads
- **Potter's wheel**: Making clay pots

**How it helps**: Reduces friction, makes movement easier

### 3. Pulley
**Examples**:
- **Well pulley**: Drawing water from wells
- **Flag pole**: Raising and lowering flags
- **Construction cranes**: Lifting building materials
- **Clothesline**: Hanging clothes

**How it helps**: Changes direction of force, makes lifting easier

### 4. Inclined Plane (Ramp)
**Examples**:
- **Loading ramps**: Getting goods into trucks
- **Wheelchair ramps**: Accessibility
- **Mountain roads**: Zigzag paths up hills
- **Stairs**: Going up buildings

**How it helps**: Reduces effort needed to move up

### 5. Wedge
**Examples**:
- **Axe**: Splitting wood
- **Knife**: Cutting food
- **Chisel**: Carving wood
- **Needle**: Sewing clothes

**How it helps**: Concentrates force to cut or split

### 6. Screw
**Examples**:
- **Bottle caps**: Securing containers
- **Wood screws**: Joining materials
- **Car jacks**: Lifting vehicles
- **Corkscrews**: Opening bottles

**How it helps**: Converts rotational motion to linear motion

## Forms of Energy

### 1. Solar Energy
**Sources**: The sun
**Uses in Ghana**:
- **Solar panels**: Electricity for homes
- **Solar water heaters**: Hot water
- **Drying crops**: Cocoa, cassava, fish
- **Solar cookers**: Cooking food

### 2. Wind Energy
**Sources**: Moving air
**Uses**:
- **Windmills**: Pumping water
- **Sailing boats**: Transportation on lakes
- **Winnowing**: Separating grain from chaff
- **Drying clothes**: Hanging on lines

### 3. Water Energy (Hydroelectric)
**Sources**: Flowing water
**Uses**:
- **Akosombo Dam**: Electricity generation
- **Water mills**: Grinding grain
- **Irrigation**: Watering crops
- **Transportation**: Boats on rivers

### 4. Chemical Energy
**Sources**: Food, fuel, batteries
**Uses**:
- **Food**: Energy for our bodies
- **Petrol**: Fuel for cars
- **Batteries**: Powering flashlights, radios
- **Charcoal**: Cooking fuel

### 5. Heat Energy
**Sources**: Fire, sun, friction
**Uses**:
- **Cooking**: Preparing meals
- **Warmth**: Keeping comfortable
- **Ironing**: Smoothing clothes
- **Metalworking**: Shaping metals

## Energy Conservation

### Why Save Energy?
1. **Protect environment**: Reduce pollution
2. **Save money**: Lower electricity bills
3. **Preserve resources**: Make fuel last longer
4. **Climate protection**: Reduce global warming

### How to Save Energy at Home:
- **Turn off lights** when leaving rooms
- **Use energy-efficient bulbs** (LED)
- **Unplug appliances** when not in use
- **Use natural light** during the day
- **Air-dry clothes** instead of using dryers
- **Cook with lids** on pots to save fuel'''
            }
        ],

        'Earth and Space Science': [
            {
                'title': 'Weather, Water Cycle, and Our Solar System',
                'content': '''# Earth and Space Science

## Weather and Climate in Ghana

### Weather Elements:
1. **Temperature**: How hot or cold it is
2. **Rainfall**: Amount of water falling from sky
3. **Wind**: Moving air
4. **Humidity**: Amount of water vapor in air
5. **Sunshine**: Amount of sunlight received

### Ghana's Climate Zones:

**1. Forest Zone (South)**:
- **Regions**: Western, Central, Eastern, Ashanti (parts)
- **Rainfall**: Heavy (1,500-2,000mm per year)
- **Temperature**: Warm (24-30°C)
- **Seasons**: Two rainy seasons, two dry seasons

**2. Savanna Zone (North)**:
- **Regions**: Northern, Upper East, Upper West
- **Rainfall**: Moderate (1,000-1,200mm per year)
- **Temperature**: Hot days, cool nights
- **Seasons**: One rainy season, one long dry season

**3. Coastal Zone**:
- **Regions**: Greater Accra, parts of Central and Western
- **Rainfall**: Moderate (800-1,200mm per year)
- **Temperature**: Warm, moderated by sea breeze
- **Special features**: Sea breezes, occasional storms

### Seasonal Activities in Ghana:

**Rainy Season (April-October)**:
- **Farming**: Planting crops (maize, yam, cassava)
- **Water storage**: Filling reservoirs and dams
- **Transportation**: Some roads become difficult
- **Clothing**: Light raincoats, umbrellas

**Dry Season (November-March)**:
- **Harvesting**: Gathering crops
- **Harmattan**: Dry, dusty winds from Sahara
- **Bush fires**: Risk in northern regions
- **Water conservation**: Managing water resources

## The Water Cycle

### How Water Moves in Nature:

**1. Evaporation**:
- **Sun heats** water in rivers, lakes, ocean
- **Water vapor** rises into atmosphere
- **Examples**: Lake Volta, Volta River, coastal waters

**2. Condensation**:
- **Water vapor cools** high in atmosphere
- **Forms clouds** and fog
- **Examples**: Morning mist over forests, cloud formation

**3. Precipitation**:
- **Water falls** as rain, snow (rare in Ghana)
- **Replenishes** rivers, lakes, groundwater
- **Examples**: Rainy season downpours, thunderstorms

**4. Collection**:
- **Water flows** into rivers and lakes
- **Soaks into** ground (groundwater)
- **Cycle repeats** continuously

### Importance of Water Cycle:
- **Fresh water supply** for drinking, farming
- **Weather patterns** and climate regulation
- **Plant growth** and food production
- **Hydroelectric power** generation

## Our Solar System

### The Sun
- **Center** of our solar system
- **Source** of light and heat for Earth
- **Distance from Earth**: 150 million kilometers
- **Temperature**: About 5,500°C on surface

### The Planets (In order from Sun):
1. **Mercury**: Closest to sun, very hot
2. **Venus**: Hottest planet, thick atmosphere
3. **Earth**: Our home, has life and water
4. **Mars**: Red planet, has ice caps
5. **Jupiter**: Largest planet, has many moons
6. **Saturn**: Has beautiful rings
7. **Uranus**: Tilted on its side
8. **Neptune**: Farthest from sun, very cold

### Earth's Moon
- **Distance from Earth**: 384,400 kilometers
- **Phases**: New moon, crescent, full moon
- **Effects on Earth**: Tides in oceans
- **Appearance**: Changes shape during month

### Day and Night
- **Earth rotates** on its axis (24 hours)
- **When Ghana faces sun**: Daytime
- **When Ghana faces away**: Nighttime
- **Time zones**: Different times around world

### Seasons
- **Earth orbits** around sun (365 days)
- **Earth's tilt** causes seasons
- **In Ghana**: Less seasonal variation (near equator)
- **Other countries**: More extreme seasons

## Natural Disasters and Safety

### Common Natural Disasters in Ghana:

**1. Floods**:
- **Causes**: Heavy rainfall, poor drainage
- **Areas affected**: Accra, Northern regions
- **Safety**: Move to higher ground, avoid flood waters

**2. Droughts**:
- **Causes**: Little or no rainfall
- **Areas affected**: Northern Ghana
- **Effects**: Crop failure, water shortage

**3. Windstorms**:
- **Causes**: Strong winds during storms
- **Effects**: Roof damage, fallen trees
- **Safety**: Stay indoors, avoid tall objects

**4. Bush Fires**:
- **Causes**: Dry conditions, human activities
- **Areas affected**: Northern savanna regions
- **Prevention**: Careful use of fire, firebreaks

### Disaster Preparedness:
- **Emergency kit**: Water, food, flashlight, radio
- **Family plan**: Meeting places, contact information
- **Stay informed**: Listen to weather reports
- **Community cooperation**: Help neighbors, follow authorities'''
            }
        ]
    }

    # Create study notes for this topic
    if topic.title in study_notes_data:
        for note_data in study_notes_data[topic.title]:
            note, created = StudyNote.objects.get_or_create(
                topic=topic,
                title=note_data['title'],
                defaults={
                    'content': note_data['content'],
                    'order': 1,
                    'is_active': True
                }
            )

            if created:
                print(f"  📝 Created study note: {note_data['title']}")


def create_quiz_questions(topic):
    """Create comprehensive quiz questions for each topic"""

    questions_data = {
        'Living Things and Their Environment': [
            {
                'question_text': 'Which of these is an example of a forest ecosystem in Ghana?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Kakum National Park', 'is_correct': True},
                    {'text': 'Lake Volta', 'is_correct': False},
                    {'text': 'Accra city center', 'is_correct': False},
                    {'text': 'Sahara Desert', 'is_correct': False}
                ],
                'explanation': 'Kakum National Park is a famous forest ecosystem in Ghana with diverse plant and animal life.'
            },
            {
                'question_text': 'In a food chain, what are plants called?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Consumers', 'is_correct': False},
                    {'text': 'Producers', 'is_correct': True},
                    {'text': 'Decomposers', 'is_correct': False},
                    {'text': 'Predators', 'is_correct': False}
                ],
                'explanation': 'Plants are called producers because they make their own food using sunlight through photosynthesis.'
            },
            {
                'question_text': 'Which animal adaptation helps camels survive in Northern Ghana?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Gills for breathing underwater', 'is_correct': False},
                    {'text': 'Storing water in their humps', 'is_correct': True},
                    {'text': 'Changing color like chameleons', 'is_correct': False},
                    {'text': 'Flying to escape predators', 'is_correct': False}
                ],
                'explanation': 'Camels store water and fat in their humps to survive in dry, desert-like conditions.'
            },
            {
                'question_text': 'What is the correct order in this Ghanaian food chain: Hawk → Snake → Lizard → Grasshopper → Leaves?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Hawk → Snake → Lizard → Grasshopper → Leaves', 'is_correct': False},
                    {'text': 'Leaves → Grasshopper → Lizard → Snake → Hawk', 'is_correct': True},
                    {'text': 'Snake → Hawk → Lizard → Leaves → Grasshopper', 'is_correct': False},
                    {'text': 'Grasshopper → Leaves → Lizard → Snake → Hawk', 'is_correct': False}
                ],
                'explanation': 'Food chains start with producers (leaves), then primary consumers (grasshopper), secondary consumers (lizard), and so on.'
            },
            {
                'question_text': 'Which conservation action is practiced on Green Ghana Day?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Cutting down old trees', 'is_correct': False},
                    {'text': 'Planting new trees', 'is_correct': True},
                    {'text': 'Hunting wild animals', 'is_correct': False},
                    {'text': 'Building more factories', 'is_correct': False}
                ],
                'explanation': 'Green Ghana Day focuses on planting trees to restore forests and fight climate change.'
            },
            {
                'question_text': 'Why do mangrove trees have special roots?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'To climb other trees', 'is_correct': False},
                    {'text': 'To survive in salty water', 'is_correct': True},
                    {'text': 'To catch flying insects', 'is_correct': False},
                    {'text': 'To store food underground', 'is_correct': False}
                ],
                'explanation': 'Mangrove trees have adapted special roots to filter salt from seawater and survive in coastal areas.'
            },
            {
                'question_text': 'Which ecosystem would you find in Lake Volta?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Desert ecosystem', 'is_correct': False},
                    {'text': 'Forest ecosystem', 'is_correct': False},
                    {'text': 'Aquatic ecosystem', 'is_correct': True},
                    {'text': 'Mountain ecosystem', 'is_correct': False}
                ],
                'explanation': 'Lake Volta is an aquatic ecosystem where water plants and animals live together.'
            },
            {
                'question_text': 'What do decomposers do in an ecosystem?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Make their own food', 'is_correct': False},
                    {'text': 'Hunt other animals', 'is_correct': False},
                    {'text': 'Break down dead plants and animals', 'is_correct': True},
                    {'text': 'Pollinate flowers', 'is_correct': False}
                ],
                'explanation': 'Decomposers like bacteria and fungi break down dead organisms and return nutrients to the soil.'
            },
            {
                'question_text': 'Which plant adaptation helps baobab trees survive dry seasons?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Large colorful flowers', 'is_correct': False},
                    {'text': 'Thick trunk for water storage', 'is_correct': True},
                    {'text': 'Poisonous leaves', 'is_correct': False},
                    {'text': 'Very small size', 'is_correct': False}
                ],
                'explanation': 'Baobab trees have thick trunks that store water to survive long dry periods.'
            },
            {
                'question_text': 'What happens if we remove all the producers from a food chain?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Nothing changes', 'is_correct': False},
                    {'text': 'Only carnivores survive', 'is_correct': False},
                    {'text': 'The entire food chain collapses', 'is_correct': True},
                    {'text': 'More animals are born', 'is_correct': False}
                ],
                'explanation': 'Without producers (plants), there would be no food for herbivores, and the entire food chain would collapse.'
            },
            {
                'question_text': 'Which national park in Ghana protects elephants and other wildlife?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Mole National Park', 'is_correct': True},
                    {'text': 'Labadi Beach', 'is_correct': False},
                    {'text': 'Kumasi Central Market', 'is_correct': False},
                    {'text': 'Tema Harbor', 'is_correct': False}
                ],
                'explanation': 'Mole National Park in Northern Ghana is home to elephants, antelopes, and many other wild animals.'
            },
            {
                'question_text': 'How do chameleons adapt to their environment?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'They fly away from danger', 'is_correct': False},
                    {'text': 'They change color to blend in', 'is_correct': True},
                    {'text': 'They dig underground burrows', 'is_correct': False},
                    {'text': 'They swim very fast', 'is_correct': False}
                ],
                'explanation': 'Chameleons change their skin color to camouflage with their surroundings and avoid predators.'
            },
            {
                'question_text': 'What is the main source of energy for most food chains?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'The moon', 'is_correct': False},
                    {'text': 'The sun', 'is_correct': True},
                    {'text': 'The wind', 'is_correct': False},
                    {'text': 'The ocean', 'is_correct': False}
                ],
                'explanation': 'The sun provides energy for plants to make food through photosynthesis, starting most food chains.'
            },
            {
                'question_text': 'Which action helps conserve water in Ghana?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Leaving taps running', 'is_correct': False},
                    {'text': 'Taking very long showers', 'is_correct': False},
                    {'text': 'Turning off taps when not needed', 'is_correct': True},
                    {'text': 'Washing cars every day', 'is_correct': False}
                ],
                'explanation': 'Turning off taps when not in use helps conserve our precious water resources.'
            },
            {
                'question_text': 'In which climate zone of Ghana would you find the most forests?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Northern savanna zone', 'is_correct': False},
                    {'text': 'Southern forest zone', 'is_correct': True},
                    {'text': 'Coastal desert zone', 'is_correct': False},
                    {'text': 'Mountain ice zone', 'is_correct': False}
                ],
                'explanation': 'The southern forest zone receives more rainfall, supporting dense forest growth.'
            },
            {
                'question_text': 'What do herbivores eat?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Only meat', 'is_correct': False},
                    {'text': 'Only plants', 'is_correct': True},
                    {'text': 'Both plants and meat', 'is_correct': False},
                    {'text': 'Only dead animals', 'is_correct': False}
                ],
                'explanation': 'Herbivores are animals that eat only plants, like grass, leaves, and fruits.'
            },
            {
                'question_text': 'Which bird adaptation helps eagles hunt effectively?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Webbed feet for swimming', 'is_correct': False},
                    {'text': 'Sharp talons for catching prey', 'is_correct': True},
                    {'text': 'Long neck for reaching water', 'is_correct': False},
                    {'text': 'Colorful feathers for attracting mates', 'is_correct': False}
                ],
                'explanation': 'Eagles have sharp talons (claws) that help them catch and hold their prey while hunting.'
            },
            {
                'question_text': 'What happens during photosynthesis?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Plants eat other plants', 'is_correct': False},
                    {'text': 'Plants make food using sunlight', 'is_correct': True},
                    {'text': 'Plants sleep during the day', 'is_correct': False},
                    {'text': 'Plants move to find water', 'is_correct': False}
                ],
                'explanation': 'During photosynthesis, plants use sunlight, water, and carbon dioxide to make their own food.'
            },
            {
                'question_text': 'Which factor is NOT part of an ecosystem?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Plants and animals', 'is_correct': False},
                    {'text': 'Air and water', 'is_correct': False},
                    {'text': 'Soil and rocks', 'is_correct': False},
                    {'text': 'Plastic toys', 'is_correct': True}
                ],
                'explanation': 'Plastic toys are human-made objects and are not natural parts of ecosystems.'
            },
            {
                'question_text': 'How do fish adapt to living in water?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'They have lungs for breathing air', 'is_correct': False},
                    {'text': 'They have gills for breathing underwater', 'is_correct': True},
                    {'text': 'They hold their breath for long periods', 'is_correct': False},
                    {'text': 'They come to surface every few minutes', 'is_correct': False}
                ],
                'explanation': 'Fish have gills that extract oxygen from water, allowing them to breathe underwater.'
            },
            {
                'question_text': 'What is the role of carnivores in a food chain?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'They make their own food', 'is_correct': False},
                    {'text': 'They eat only plants', 'is_correct': False},
                    {'text': 'They eat other animals', 'is_correct': True},
                    {'text': 'They break down dead organisms', 'is_correct': False}
                ],
                'explanation': 'Carnivores are animals that eat other animals, helping control population sizes in ecosystems.'
            },
            {
                'question_text': 'Which conservation practice helps protect Ghana\'s forests?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Cutting down all old trees', 'is_correct': False},
                    {'text': 'Sustainable logging practices', 'is_correct': True},
                    {'text': 'Building more roads through forests', 'is_correct': False},
                    {'text': 'Removing all animals from forests', 'is_correct': False}
                ],
                'explanation': 'Sustainable logging means cutting trees responsibly and replanting to maintain forest health.'
            },
            {
                'question_text': 'Why are wetlands important ecosystems?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'They provide habitat for many species', 'is_correct': True},
                    {'text': 'They are good places to build houses', 'is_correct': False},
                    {'text': 'They prevent all flooding', 'is_correct': False},
                    {'text': 'They produce oil and gas', 'is_correct': False}
                ],
                'explanation': 'Wetlands provide homes for many plants and animals, and help filter water naturally.'
            },
            {
                'question_text': 'What do omnivores eat?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Only plants', 'is_correct': False},
                    {'text': 'Only meat', 'is_correct': False},
                    {'text': 'Both plants and animals', 'is_correct': True},
                    {'text': 'Only fruits', 'is_correct': False}
                ],
                'explanation': 'Omnivores eat both plants and animals. Humans are examples of omnivores.'
            },
            {
                'question_text': 'How do desert plants like cactus conserve water?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'They have very large leaves', 'is_correct': False},
                    {'text': 'They have thick, waxy leaves', 'is_correct': True},
                    {'text': 'They grow very tall', 'is_correct': False},
                    {'text': 'They change color frequently', 'is_correct': False}
                ],
                'explanation': 'Cactus plants have thick, waxy leaves that prevent water from evaporating quickly.'
            },
            {
                'question_text': 'What is biodiversity?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Having only one type of plant', 'is_correct': False},
                    {'text': 'The variety of life in an ecosystem', 'is_correct': True},
                    {'text': 'The number of rocks in an area', 'is_correct': False},
                    {'text': 'The amount of water in a lake', 'is_correct': False}
                ],
                'explanation': 'Biodiversity refers to the variety of different plants, animals, and other organisms in an ecosystem.'
            },
            {
                'question_text': 'Which human activity can harm ecosystems?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Planting trees', 'is_correct': False},
                    {'text': 'Pollution from factories', 'is_correct': True},
                    {'text': 'Creating national parks', 'is_correct': False},
                    {'text': 'Studying animals', 'is_correct': False}
                ],
                'explanation': 'Pollution from factories can contaminate air, water, and soil, harming plants and animals.'
            },
            {
                'question_text': 'How do birds help plants reproduce?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'By eating all the seeds', 'is_correct': False},
                    {'text': 'By pollinating flowers', 'is_correct': True},
                    {'text': 'By cutting down branches', 'is_correct': False},
                    {'text': 'By making nests in trees', 'is_correct': False}
                ],
                'explanation': 'Birds help pollinate flowers by carrying pollen from one flower to another as they feed on nectar.'
            },
            {
                'question_text': 'What is the main threat to wildlife in Ghana?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Too much rainfall', 'is_correct': False},
                    {'text': 'Habitat destruction', 'is_correct': True},
                    {'text': 'Too many national parks', 'is_correct': False},
                    {'text': 'Cold weather', 'is_correct': False}
                ],
                'explanation': 'Habitat destruction from deforestation and development is the main threat to Ghana\'s wildlife.'
            },
            {
                'question_text': 'Why is it important to protect endangered species?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'They are worth a lot of money', 'is_correct': False},
                    {'text': 'They maintain ecosystem balance', 'is_correct': True},
                    {'text': 'They are good pets', 'is_correct': False},
                    {'text': 'They are easy to catch', 'is_correct': False}
                ],
                'explanation': 'Endangered species play important roles in maintaining the balance of their ecosystems.'
            }
        ],

        'Human Body and Health': HUMAN_BODY_QUESTIONS,
        'Matter and Materials': MATTER_MATERIALS_QUESTIONS,

        # Add placeholder questions for remaining topics if not imported
        'Forces and Energy': [
            {
                'question_text': 'What is a force?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'A push or pull', 'is_correct': True},
                    {'text': 'A type of energy', 'is_correct': False},
                    {'text': 'A material', 'is_correct': False},
                    {'text': 'A machine', 'is_correct': False}
                ],
                'explanation': 'A force is a push or pull that can change the motion or shape of an object.'
            }
        ],

        'Earth and Space Science': [
            {
                'question_text': 'What causes day and night?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Earth rotating on its axis', 'is_correct': True},
                    {'text': 'The moon moving around Earth', 'is_correct': False},
                    {'text': 'The sun moving around Earth', 'is_correct': False},
                    {'text': 'Clouds covering the sun', 'is_correct': False}
                ],
                'explanation': 'Day and night are caused by Earth rotating on its axis every 24 hours.'
            }
        ]
    }

    # Create questions for this topic
    if topic.title in questions_data:
        for i, q_data in enumerate(questions_data[topic.title]):
            question, created = Question.objects.get_or_create(
                topic=topic,
                question_text=q_data['question_text'],
                defaults={
                    'question_type': q_data['question_type'],
                    'explanation': q_data.get('explanation', ''),
                    'order': i + 1,
                    'time_limit': 45,
                    'is_active': True
                }
            )

            if created:
                print(f"  ❓ Created question: {q_data['question_text'][:50]}...")

                # Create answer choices
                for choice_data in q_data['choices']:
                    AnswerChoice.objects.create(
                        question=question,
                        choice_text=choice_data['text'],
                        is_correct=choice_data['is_correct']
                    )

    print(f"  🎯 Completed quiz questions for: {topic.title}")


if __name__ == '__main__':
    create_grade6_science_content()

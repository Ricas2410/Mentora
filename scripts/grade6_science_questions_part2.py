#!/usr/bin/env python3
"""
Grade 6 Science Quiz Questions - Part 2
Contains questions for the remaining 4 topics:
- Human Body and Health
- Matter and Materials  
- Forces and Energy
- Earth and Space Science

This file contains the question data that will be imported by the main script.
"""

# Questions for Human Body and Health (30 questions)
HUMAN_BODY_QUESTIONS = [
    {
        'question_text': 'Which organ in the digestive system breaks down food with acid?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Mouth', 'is_correct': False},
            {'text': 'Stomach', 'is_correct': True},
            {'text': 'Small intestine', 'is_correct': False},
            {'text': 'Large intestine', 'is_correct': False}
        ],
        'explanation': 'The stomach produces acid that helps break down food into smaller pieces for digestion.'
    },
    {
        'question_text': 'Which Ghanaian food is rich in carbohydrates for energy?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Fish', 'is_correct': False},
            {'text': 'Yam', 'is_correct': True},
            {'text': 'Oranges', 'is_correct': False},
            {'text': 'Groundnuts', 'is_correct': False}
        ],
        'explanation': 'Yam is a starchy root vegetable that provides carbohydrates for energy.'
    },
    {
        'question_text': 'How many times does a healthy heart beat per minute?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'About 20 times', 'is_correct': False},
            {'text': 'About 70 times', 'is_correct': True},
            {'text': 'About 150 times', 'is_correct': False},
            {'text': 'About 300 times', 'is_correct': False}
        ],
        'explanation': 'A healthy heart beats about 60-80 times per minute, with 70 being average.'
    },
    {
        'question_text': 'Which body system brings oxygen into your body?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Digestive system', 'is_correct': False},
            {'text': 'Respiratory system', 'is_correct': True},
            {'text': 'Nervous system', 'is_correct': False},
            {'text': 'Skeletal system', 'is_correct': False}
        ],
        'explanation': 'The respiratory system, including lungs and airways, brings oxygen into the body.'
    },
    {
        'question_text': 'What should you do to prevent malaria in Ghana?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Drink dirty water', 'is_correct': False},
            {'text': 'Sleep under mosquito nets', 'is_correct': True},
            {'text': 'Stay outside at night', 'is_correct': False},
            {'text': 'Keep stagnant water around', 'is_correct': False}
        ],
        'explanation': 'Sleeping under treated mosquito nets prevents mosquito bites that can transmit malaria.'
    },
    {
        'question_text': 'Which Ghanaian food provides protein for building muscles?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Rice', 'is_correct': False},
            {'text': 'Cassava', 'is_correct': False},
            {'text': 'Beans', 'is_correct': True},
            {'text': 'Plantain', 'is_correct': False}
        ],
        'explanation': 'Beans are rich in protein, which helps build and repair muscles in the body.'
    },
    {
        'question_text': 'How often should you brush your teeth?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Once a week', 'is_correct': False},
            {'text': 'Once a month', 'is_correct': False},
            {'text': 'Twice a day', 'is_correct': True},
            {'text': 'Only when they hurt', 'is_correct': False}
        ],
        'explanation': 'Brushing teeth twice daily with fluoride toothpaste helps prevent tooth decay and gum disease.'
    },
    {
        'question_text': 'What happens to food in the small intestine?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'It is chewed into small pieces', 'is_correct': False},
            {'text': 'Nutrients are absorbed into blood', 'is_correct': True},
            {'text': 'Waste is formed and stored', 'is_correct': False},
            {'text': 'Acid breaks it down', 'is_correct': False}
        ],
        'explanation': 'The small intestine absorbs nutrients from digested food into the bloodstream.'
    },
    {
        'question_text': 'Which vitamin do we get from sunlight?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Vitamin A', 'is_correct': False},
            {'text': 'Vitamin B', 'is_correct': False},
            {'text': 'Vitamin C', 'is_correct': False},
            {'text': 'Vitamin D', 'is_correct': True}
        ],
        'explanation': 'Our skin makes Vitamin D when exposed to sunlight, which helps build strong bones.'
    },
    {
        'question_text': 'What is the main function of the heart?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'To digest food', 'is_correct': False},
            {'text': 'To pump blood', 'is_correct': True},
            {'text': 'To breathe air', 'is_correct': False},
            {'text': 'To think and remember', 'is_correct': False}
        ],
        'explanation': 'The heart is a muscle that pumps blood throughout the body, carrying oxygen and nutrients.'
    },
    {
        'question_text': 'Why should you wash your hands before eating?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'To make them smell good', 'is_correct': False},
            {'text': 'To remove germs and dirt', 'is_correct': True},
            {'text': 'To make them look white', 'is_correct': False},
            {'text': 'To exercise your arms', 'is_correct': False}
        ],
        'explanation': 'Washing hands removes germs and dirt that could cause illness if they enter your body through food.'
    },
    {
        'question_text': 'Which organ filters waste from your blood?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Liver', 'is_correct': False},
            {'text': 'Kidneys', 'is_correct': True},
            {'text': 'Lungs', 'is_correct': False},
            {'text': 'Brain', 'is_correct': False}
        ],
        'explanation': 'The kidneys filter waste products from blood and make urine to remove them from the body.'
    },
    {
        'question_text': 'What should you drink most of to stay healthy?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Soft drinks', 'is_correct': False},
            {'text': 'Clean water', 'is_correct': True},
            {'text': 'Coffee', 'is_correct': False},
            {'text': 'Energy drinks', 'is_correct': False}
        ],
        'explanation': 'Clean water is essential for all body functions and should be the main drink for good health.'
    },
    {
        'question_text': 'How many hours of sleep do children need each night?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': '3-4 hours', 'is_correct': False},
            {'text': '5-6 hours', 'is_correct': False},
            {'text': '8-10 hours', 'is_correct': True},
            {'text': '12-14 hours', 'is_correct': False}
        ],
        'explanation': 'Children need 8-10 hours of sleep each night for proper growth and brain development.'
    },
    {
        'question_text': 'Which food group helps protect against diseases?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Carbohydrates', 'is_correct': False},
            {'text': 'Proteins', 'is_correct': False},
            {'text': 'Vitamins and minerals', 'is_correct': True},
            {'text': 'Fats', 'is_correct': False}
        ],
        'explanation': 'Vitamins and minerals from fruits and vegetables help protect the body against diseases.'
    },
    {
        'question_text': 'What carries oxygen from lungs to other parts of the body?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Nerves', 'is_correct': False},
            {'text': 'Blood', 'is_correct': True},
            {'text': 'Bones', 'is_correct': False},
            {'text': 'Muscles', 'is_correct': False}
        ],
        'explanation': 'Blood carries oxygen from the lungs to all parts of the body through blood vessels.'
    },
    {
        'question_text': 'Which practice helps prevent diarrhea?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Eating unwashed fruits', 'is_correct': False},
            {'text': 'Drinking boiled water', 'is_correct': True},
            {'text': 'Not washing hands', 'is_correct': False},
            {'text': 'Eating spoiled food', 'is_correct': False}
        ],
        'explanation': 'Drinking boiled or treated water kills germs that can cause diarrhea and other illnesses.'
    },
    {
        'question_text': 'What is the largest organ in the human body?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Brain', 'is_correct': False},
            {'text': 'Liver', 'is_correct': False},
            {'text': 'Skin', 'is_correct': True},
            {'text': 'Heart', 'is_correct': False}
        ],
        'explanation': 'The skin is the largest organ, covering and protecting the entire body.'
    },
    {
        'question_text': 'Which nutrient gives the body the most energy?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Vitamins', 'is_correct': False},
            {'text': 'Minerals', 'is_correct': False},
            {'text': 'Carbohydrates', 'is_correct': True},
            {'text': 'Water', 'is_correct': False}
        ],
        'explanation': 'Carbohydrates are the body\'s main source of energy for daily activities.'
    },
    {
        'question_text': 'Why is exercise important for health?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'It makes you tired', 'is_correct': False},
            {'text': 'It strengthens muscles and heart', 'is_correct': True},
            {'text': 'It wastes time', 'is_correct': False},
            {'text': 'It makes you hungry', 'is_correct': False}
        ],
        'explanation': 'Exercise strengthens muscles, improves heart health, and helps maintain a healthy weight.'
    },
    {
        'question_text': 'What should you do if you have a fever?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Go swimming', 'is_correct': False},
            {'text': 'Rest and drink fluids', 'is_correct': True},
            {'text': 'Run around outside', 'is_correct': False},
            {'text': 'Eat lots of candy', 'is_correct': False}
        ],
        'explanation': 'When you have a fever, rest and drinking fluids help your body fight the illness.'
    },
    {
        'question_text': 'Which part of the respiratory system filters air?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Lungs', 'is_correct': False},
            {'text': 'Nose', 'is_correct': True},
            {'text': 'Heart', 'is_correct': False},
            {'text': 'Stomach', 'is_correct': False}
        ],
        'explanation': 'The nose has tiny hairs that filter dust and particles from the air we breathe.'
    },
    {
        'question_text': 'What happens when you don\'t get enough iron in your diet?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'You become very strong', 'is_correct': False},
            {'text': 'You may become anemic and weak', 'is_correct': True},
            {'text': 'You grow very tall', 'is_correct': False},
            {'text': 'Your teeth become white', 'is_correct': False}
        ],
        'explanation': 'Iron deficiency can cause anemia, making you feel weak and tired because your blood can\'t carry enough oxygen.'
    },
    {
        'question_text': 'Which Ghanaian leafy vegetable is rich in iron?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Kontomire (cocoyam leaves)', 'is_correct': True},
            {'text': 'Cassava', 'is_correct': False},
            {'text': 'Rice', 'is_correct': False},
            {'text': 'Bread', 'is_correct': False}
        ],
        'explanation': 'Kontomire (cocoyam leaves) is rich in iron and other important nutrients for healthy blood.'
    },
    {
        'question_text': 'What is the main function of white blood cells?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Carry oxygen', 'is_correct': False},
            {'text': 'Fight infections', 'is_correct': True},
            {'text': 'Digest food', 'is_correct': False},
            {'text': 'Make bones strong', 'is_correct': False}
        ],
        'explanation': 'White blood cells are part of the immune system and fight germs and infections in the body.'
    },
    {
        'question_text': 'Why should you cover your mouth when coughing?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'To look polite', 'is_correct': False},
            {'text': 'To prevent spreading germs', 'is_correct': True},
            {'text': 'To make less noise', 'is_correct': False},
            {'text': 'To exercise your arm', 'is_correct': False}
        ],
        'explanation': 'Covering your mouth when coughing prevents germs from spreading to other people through the air.'
    },
    {
        'question_text': 'Which organ controls all body functions?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Heart', 'is_correct': False},
            {'text': 'Brain', 'is_correct': True},
            {'text': 'Liver', 'is_correct': False},
            {'text': 'Kidneys', 'is_correct': False}
        ],
        'explanation': 'The brain controls all body functions including thinking, movement, breathing, and heartbeat.'
    },
    {
        'question_text': 'What should you do to keep your teeth healthy?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Eat lots of candy', 'is_correct': False},
            {'text': 'Brush and floss regularly', 'is_correct': True},
            {'text': 'Never visit a dentist', 'is_correct': False},
            {'text': 'Drink only soft drinks', 'is_correct': False}
        ],
        'explanation': 'Brushing and flossing regularly removes food particles and bacteria that can cause tooth decay.'
    },
    {
        'question_text': 'How does the body get rid of carbon dioxide?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Through the skin', 'is_correct': False},
            {'text': 'Through breathing out', 'is_correct': True},
            {'text': 'Through urination', 'is_correct': False},
            {'text': 'Through sweating', 'is_correct': False}
        ],
        'explanation': 'The lungs remove carbon dioxide from the blood and we breathe it out through our nose and mouth.'
    },
    {
        'question_text': 'Which food combination makes a balanced Ghanaian meal?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Only rice', 'is_correct': False},
            {'text': 'Rice, fish, and vegetables', 'is_correct': True},
            {'text': 'Only meat', 'is_correct': False},
            {'text': 'Only fruits', 'is_correct': False}
        ],
        'explanation': 'A balanced meal includes carbohydrates (rice), protein (fish), and vitamins/minerals (vegetables).'
    }
]

# Questions for Matter and Materials (30 questions)
MATTER_MATERIALS_QUESTIONS = [
    {
        'question_text': 'Which of these is an example of a solid?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Water', 'is_correct': False},
            {'text': 'Air', 'is_correct': False},
            {'text': 'Rock', 'is_correct': True},
            {'text': 'Steam', 'is_correct': False}
        ],
        'explanation': 'A rock is a solid because it has a definite shape and size that doesn\'t change.'
    },
    {
        'question_text': 'What happens to ice when it melts?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'It becomes gas', 'is_correct': False},
            {'text': 'It becomes liquid water', 'is_correct': True},
            {'text': 'It disappears completely', 'is_correct': False},
            {'text': 'It becomes harder', 'is_correct': False}
        ],
        'explanation': 'When ice melts, it changes from solid to liquid water due to heat.'
    },
    {
        'question_text': 'Which material is best for making cooking pots?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Paper', 'is_correct': False},
            {'text': 'Aluminum', 'is_correct': True},
            {'text': 'Cloth', 'is_correct': False},
            {'text': 'Wood', 'is_correct': False}
        ],
        'explanation': 'Aluminum is a good heat conductor and doesn\'t rust, making it ideal for cooking pots.'
    },
    {
        'question_text': 'What property allows us to see through glass?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Hardness', 'is_correct': False},
            {'text': 'Transparency', 'is_correct': True},
            {'text': 'Flexibility', 'is_correct': False},
            {'text': 'Magnetism', 'is_correct': False}
        ],
        'explanation': 'Transparency is the property that allows light to pass through glass so we can see through it.'
    },
    {
        'question_text': 'How can you separate rice from stones?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'By melting', 'is_correct': False},
            {'text': 'By sieving', 'is_correct': True},
            {'text': 'By adding water', 'is_correct': False},
            {'text': 'By freezing', 'is_correct': False}
        ],
        'explanation': 'Sieving uses different sizes to separate rice (smaller) from stones (larger).'
    },
    {
        'question_text': 'Which state of matter has no definite shape or size?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Solid', 'is_correct': False},
            {'text': 'Liquid', 'is_correct': False},
            {'text': 'Gas', 'is_correct': True},
            {'text': 'All of the above', 'is_correct': False}
        ],
        'explanation': 'Gases have no definite shape or size and expand to fill any container completely.'
    },
    {
        'question_text': 'What happens when you heat palm oil?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'It becomes solid', 'is_correct': False},
            {'text': 'It becomes more liquid', 'is_correct': True},
            {'text': 'It changes color to blue', 'is_correct': False},
            {'text': 'It becomes magnetic', 'is_correct': False}
        ],
        'explanation': 'Heating palm oil makes it less thick and more liquid, making it easier to pour.'
    },
    {
        'question_text': 'Which method can separate salt from salt water?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Filtering', 'is_correct': False},
            {'text': 'Evaporation', 'is_correct': True},
            {'text': 'Sieving', 'is_correct': False},
            {'text': 'Magnetic separation', 'is_correct': False}
        ],
        'explanation': 'Evaporation removes water, leaving salt crystals behind.'
    },
    {
        'question_text': 'Why do we use clay pots to keep water cool?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Clay is transparent', 'is_correct': False},
            {'text': 'Clay allows water to evaporate slowly', 'is_correct': True},
            {'text': 'Clay is magnetic', 'is_correct': False},
            {'text': 'Clay is very hard', 'is_correct': False}
        ],
        'explanation': 'Clay is porous, allowing slow evaporation that cools the remaining water.'
    },
    {
        'question_text': 'What is the process called when water vapor becomes liquid?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Evaporation', 'is_correct': False},
            {'text': 'Melting', 'is_correct': False},
            {'text': 'Condensation', 'is_correct': True},
            {'text': 'Freezing', 'is_correct': False}
        ],
        'explanation': 'Condensation is when water vapor (gas) cools and becomes liquid water.'
    },
    {
        'question_text': 'Which material is flexible?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Glass', 'is_correct': False},
            {'text': 'Rubber', 'is_correct': True},
            {'text': 'Stone', 'is_correct': False},
            {'text': 'Metal', 'is_correct': False}
        ],
        'explanation': 'Rubber is flexible because it can bend and stretch without breaking.'
    },
    {
        'question_text': 'What happens to water when it freezes?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'It becomes gas', 'is_correct': False},
            {'text': 'It becomes solid ice', 'is_correct': True},
            {'text': 'It disappears', 'is_correct': False},
            {'text': 'It becomes hot', 'is_correct': False}
        ],
        'explanation': 'When water freezes, it changes from liquid to solid ice.'
    },
    {
        'question_text': 'Which property makes iron useful for building?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'It is transparent', 'is_correct': False},
            {'text': 'It is strong and hard', 'is_correct': True},
            {'text': 'It is very light', 'is_correct': False},
            {'text': 'It floats on water', 'is_correct': False}
        ],
        'explanation': 'Iron is strong and hard, making it excellent for construction and building.'
    },
    {
        'question_text': 'How can you separate iron nails from sand?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Using a magnet', 'is_correct': True},
            {'text': 'Adding water', 'is_correct': False},
            {'text': 'Heating the mixture', 'is_correct': False},
            {'text': 'Using a sieve', 'is_correct': False}
        ],
        'explanation': 'A magnet attracts iron nails but not sand, making separation easy.'
    },
    {
        'question_text': 'What makes wood a good material for furniture?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'It conducts electricity well', 'is_correct': False},
            {'text': 'It is light and easy to shape', 'is_correct': True},
            {'text': 'It is transparent', 'is_correct': False},
            {'text': 'It is magnetic', 'is_correct': False}
        ],
        'explanation': 'Wood is relatively light, strong, and can be easily cut and shaped into furniture.'
    },
    {
        'question_text': 'Which change of state requires heat?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Freezing', 'is_correct': False},
            {'text': 'Condensation', 'is_correct': False},
            {'text': 'Melting', 'is_correct': True},
            {'text': 'All of the above', 'is_correct': False}
        ],
        'explanation': 'Melting requires heat to change a solid into a liquid.'
    },
    {
        'question_text': 'Why is plastic used for water bottles?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'It is heavy and strong', 'is_correct': False},
            {'text': 'It is light and unbreakable', 'is_correct': True},
            {'text': 'It conducts heat well', 'is_correct': False},
            {'text': 'It is magnetic', 'is_correct': False}
        ],
        'explanation': 'Plastic is light, doesn\'t break easily, and doesn\'t react with water.'
    },
    {
        'question_text': 'What happens to the size of most materials when heated?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'They shrink', 'is_correct': False},
            {'text': 'They expand', 'is_correct': True},
            {'text': 'They stay the same', 'is_correct': False},
            {'text': 'They disappear', 'is_correct': False}
        ],
        'explanation': 'Most materials expand (get bigger) when heated because particles move more and take up more space.'
    },
    {
        'question_text': 'Which material is the best conductor of heat?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Wood', 'is_correct': False},
            {'text': 'Plastic', 'is_correct': False},
            {'text': 'Metal', 'is_correct': True},
            {'text': 'Cloth', 'is_correct': False}
        ],
        'explanation': 'Metals are excellent heat conductors, which is why metal pots heat up quickly.'
    },
    {
        'question_text': 'How can you clean muddy water?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'By filtering through cloth', 'is_correct': True},
            {'text': 'By adding more mud', 'is_correct': False},
            {'text': 'By heating it', 'is_correct': False},
            {'text': 'By freezing it', 'is_correct': False}
        ],
        'explanation': 'Filtering through cloth removes mud particles, making water cleaner.'
    },
    {
        'question_text': 'What is the main difference between liquids and gases?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Liquids have definite volume, gases don\'t', 'is_correct': True},
            {'text': 'Liquids are always hot', 'is_correct': False},
            {'text': 'Gases are always cold', 'is_correct': False},
            {'text': 'There is no difference', 'is_correct': False}
        ],
        'explanation': 'Liquids have a definite volume but take the shape of their container, while gases expand to fill any space.'
    },
    {
        'question_text': 'Why do we use glass for windows?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'It is very soft', 'is_correct': False},
            {'text': 'It is transparent and hard', 'is_correct': True},
            {'text': 'It is magnetic', 'is_correct': False},
            {'text': 'It conducts electricity', 'is_correct': False}
        ],
        'explanation': 'Glass is transparent (we can see through it) and hard enough to protect us from weather.'
    },
    {
        'question_text': 'What happens when you mix oil and water?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'They mix completely', 'is_correct': False},
            {'text': 'Oil floats on top of water', 'is_correct': True},
            {'text': 'Water floats on top of oil', 'is_correct': False},
            {'text': 'They both disappear', 'is_correct': False}
        ],
        'explanation': 'Oil is less dense than water, so it floats on top and they don\'t mix.'
    },
    {
        'question_text': 'Which material would be best for making a raincoat?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Cotton cloth', 'is_correct': False},
            {'text': 'Waterproof plastic', 'is_correct': True},
            {'text': 'Paper', 'is_correct': False},
            {'text': 'Metal', 'is_correct': False}
        ],
        'explanation': 'Waterproof plastic repels water, keeping you dry in the rain.'
    },
    {
        'question_text': 'What is evaporation?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Liquid changing to gas', 'is_correct': True},
            {'text': 'Gas changing to liquid', 'is_correct': False},
            {'text': 'Solid changing to liquid', 'is_correct': False},
            {'text': 'Liquid changing to solid', 'is_correct': False}
        ],
        'explanation': 'Evaporation is when liquid changes to gas, like water becoming water vapor.'
    },
    {
        'question_text': 'Why is charcoal black?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Because it absorbs all light', 'is_correct': True},
            {'text': 'Because it reflects all light', 'is_correct': False},
            {'text': 'Because it is transparent', 'is_correct': False},
            {'text': 'Because it glows in the dark', 'is_correct': False}
        ],
        'explanation': 'Charcoal appears black because it absorbs most light instead of reflecting it back to our eyes.'
    },
    {
        'question_text': 'Which property allows a material to return to its original shape after bending?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Hardness', 'is_correct': False},
            {'text': 'Elasticity', 'is_correct': True},
            {'text': 'Transparency', 'is_correct': False},
            {'text': 'Magnetism', 'is_correct': False}
        ],
        'explanation': 'Elasticity allows materials like rubber bands to return to their original shape after stretching.'
    },
    {
        'question_text': 'How can you separate a mixture of rice and beans?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'By hand picking', 'is_correct': True},
            {'text': 'By melting', 'is_correct': False},
            {'text': 'By using a magnet', 'is_correct': False},
            {'text': 'By adding water', 'is_correct': False}
        ],
        'explanation': 'Rice and beans can be separated by hand picking because they have different sizes and colors.'
    },
    {
        'question_text': 'What makes metals good for making electrical wires?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'They are transparent', 'is_correct': False},
            {'text': 'They conduct electricity well', 'is_correct': True},
            {'text': 'They are very light', 'is_correct': False},
            {'text': 'They float on water', 'is_correct': False}
        ],
        'explanation': 'Metals conduct electricity well, allowing electric current to flow through wires easily.'
    },
    {
        'question_text': 'Which change is reversible?',
        'question_type': 'multiple_choice',
        'choices': [
            {'text': 'Burning paper', 'is_correct': False},
            {'text': 'Melting ice', 'is_correct': True},
            {'text': 'Cooking an egg', 'is_correct': False},
            {'text': 'Rusting iron', 'is_correct': False}
        ],
        'explanation': 'Melting ice is reversible because you can freeze the water back into ice.'
    }
]

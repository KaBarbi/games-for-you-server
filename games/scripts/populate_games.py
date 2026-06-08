from games.models import Game


def run():
    if Game.objects.exists():
        print("Games already exist, skipping seed.")
        return

    games = [
        {
            "title": "Hollow Knight",
            "description": "Enter the haunting underground kingdom of Hallownest and explore a vast world filled with ancient ruins, dangerous creatures, and hidden secrets. Master precise combat and platforming as you uncover the mysteries of a fallen civilization in this beautifully hand-drawn action adventure.",
            "price": 14.99,
            "stock": 15,
            "platform": "PS",
            "cover": "hollow_knight.jpg",
        },
        {
            "title": "God of War: Ragnarok",
            "description": "Join Kratos and Atreus on an epic journey across the Nine Realms as the threat of Ragnarök approaches. Face powerful Norse gods, explore breathtaking landscapes, and confront the consequences of fate in a cinematic action adventure that blends brutal combat with emotional storytelling.",
            "price": 69.99,
            "stock": 10,
            "platform": "PS",
            "cover": "god_of_war_ragnarok.jpg",
        },
        {
            "title": "Spider-Man 2",
            "description": "Swing across an expanded New York City as Peter Parker and Miles Morales in a thrilling superhero adventure. Use new abilities, face legendary villains, and protect the city from escalating threats. Experience fast-paced combat, fluid traversal, and a powerful story about responsibility and sacrifice.",
            "price": 69.99,
            "stock": 8,
            "platform": "PS",
            "cover": "spider_man_2.jpg",
        },
        {
            "title": "Halo Infinite",
            "description": "Step into the armor of Master Chief and return to humanity’s greatest battle. Explore the vast world of Zeta Halo, confront the ruthless Banished, and fight to restore hope to the galaxy. Experience classic Halo combat evolved with a larger battlefield and dynamic freedom.",
            "price": 59.99,
            "stock": 12,
            "platform": "XB",
            "cover": "halo_infinite.jpg",
        },
        {
            "title": "Forza Horizon 5",
            "description": "Explore the vibrant landscapes of Mexico in the ultimate open-world racing festival. Drive hundreds of the world’s greatest cars through jungles, deserts, cities, and volcanoes. Join friends and players online as you compete, explore, and create unforgettable moments in a constantly evolving world of speed.",
            "price": 59.99,
            "stock": 10,
            "platform": "XB",
            "cover": "forza_horizon_5.jpg",
        },
        {
            "title": "Starfield",
            "description": "Journey among the stars in a massive space-faring role-playing adventure. Create your character, pilot your own ship, and explore distant planets across a vast galaxy. Discover ancient mysteries, join powerful factions, and forge your own path as humanity reaches beyond the limits of known space.",
            "price": 69.99,
            "stock": 7,
            "platform": "XB",
            "cover": "starfield.jpg",
        },
        {
            "title": "Zelda: Tears of the Kingdom",
            "description": "Return to Hyrule in a vast adventure that stretches across the land and the skies above. Use powerful new abilities to explore, build, and solve puzzles in a world filled with mystery. As ancient forces awaken, Link must rise once again to protect the kingdom.",
            "price": 69.99,
            "stock": 10,
            "platform": "NS",
            "cover": "zelda_totk.jpg",
        },
        {
            "title": "Metroid Dread",
            "description": "Guide legendary bounty hunter Samus Aran on a dangerous mission to a mysterious alien planet. Explore interconnected environments, discover powerful upgrades, and survive relentless robotic hunters. Combining classic side-scrolling exploration with tense encounters, Metroid Dread delivers a thrilling fight for survival and discovery.",
            "price": 59.99,
            "stock": 9,
            "platform": "NS",
            "cover": "metroid_dread.jpg",
        },
        {
            "title": "Hollow Knight: Silksong",
            "description": "Play as Hornet in a brand-new adventure set in a mysterious kingdom far from Hallownest. Leap through dangerous environments, battle deadly foes, and master new acrobatic abilities. Climb toward a shining citadel while uncovering secrets, completing quests, and facing powerful enemies along the journey.",
            "price": 29.99,
            "stock": 20,
            "platform": "NS",
            "cover": "silksong.jpg",
        },
        {
            "title": "Gears 5",
            "description": "Continue the Gears saga as Kait Diaz searches for the truth behind her mysterious connection to the enemy. Travel across vast environments, battle terrifying creatures, and fight alongside your squad in intense third-person combat. Experience a gripping campaign and explosive multiplayer battles.",
            "price": 29.99,
            "stock": 20,
            "platform": "XB",
            "cover": "gears_5.jpg",
        },
        {
            "title": "The Last of Us Part II",
            "description": "Five years after their dangerous journey across the United States, Ellie and Joel settle into life in Jackson. But when a violent event shatters their peace, Ellie embarks on a relentless quest for justice. Experience an emotionally powerful story set in a brutal, beautifully realized world.",
            "price": 39.99,
            "stock": 18,
            "platform": "PS",
            "cover": "the_last_of_us_2.jpg",
        },
        {
            "title": "Super Mario Odyssey",
            "description": "Join Mario on a globe-trotting adventure across imaginative kingdoms to stop Bowser’s wedding plans. Explore vibrant worlds, collect Power Moons, and use Mario’s new companion Cappy to capture enemies and objects. Discover secrets, solve puzzles, and experience a creative platforming adventure full of surprises.",
            "price": 49.99,
            "stock": 25,
            "platform": "NS",
            "cover": "super_mario_odyssey.jpg",
        },

    ]

    for g in games:
        Game.objects.create(**g)

    print("✔️ Games seeded successfully!")

import requests

# Function to get card details from Scryfall API
def get_commander_details(commander_name):
    # Define the Scryfall API URL
    scryfall_url = f"https://api.scryfall.com/cards/named?fuzzy={commander_name}"

    try:
        # Send a GET request to the Scryfall API
        response = requests.get(scryfall_url)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract relevant information
            color_identity = ''.join(data.get('color_identity', []))
            mana_cost = data.get('mana_cost', '')
            price = data.get('prices', {}).get('usd', 'N/A')
            card_text = data.get('oracle_text', 'N/A')
            card_type = data.get('type_line', 'N/A')

            return color_identity, mana_cost, price, card_text, card_type

        else:
            print(f"Failed to fetch data for {commander_name}. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

# Function to check if keywords are present in the card text
def has_keywords(card_text, keywords):
    card_text = card_text.lower()
    return any(keyword.lower() in card_text for keyword in keywords)

# Function to search for cards of a specific type and color identity
def search_cards(commander_color_identity, card_type, keywords):
    # Define the Scryfall API URL for card search
    scryfall_url = "https://api.scryfall.com/cards/search"

    # Build the query string for the search
    query = f"type:{card_type} color<=WUBRG id:{commander_color_identity}"

    try:
        # Send a GET request to the Scryfall API with the query
        response = requests.get(scryfall_url, params={"q": query})

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract and print the card names and card text that match the query and keywords
            matching_cards = [card for card in data.get('data', []) if has_keywords(card.get('oracle_text', ''), keywords)]
            if matching_cards:
                print(f"Matching cards of type '{card_type}' with keywords:")
                for card in matching_cards:
                    card_name = card['name']
                    card_mana_cost = card['mana_cost']
                    card_oracle_text = card['oracle_text']
                    print(f" - {card_name} ({card_mana_cost})\n   Card Text: {card_oracle_text}\n")

                # Ask the user if they want to add any cards to the deck
                add_to_deck = input("Do you want to add any cards to the deck? (Enter card names separated by commas or 'no'): ")
                if add_to_deck.lower() != 'no':
                    deck.extend(add_to_deck.split(','))

                # Ask the user if they want to continue searching for more cards
                continue_search = input(f"Do you want to continue searching for more cards? (yes/no): ")
                if continue_search.lower() == 'yes':
                    return True

            else:
                print(f"No matching cards found for type '{card_type}' with keywords.")
            
        else:
            print(f"Failed to fetch card data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

    return False

# Input the commander's name
commander_name = input("Enter the commander's name: ")

# Get commander details
details = get_commander_details(commander_name)

if details:
    color_identity, mana_cost, price, card_text, card_type = details
    print(f"Commander: {commander_name}")
    print(f"Color Identity: {color_identity}")
    print(f"Mana Cost: {mana_cost}")
    print(f"Price: {price}")
    print(f"Card Text: {card_text}")
    print(f"Card Type: {card_type}")

    # Define keywords to search for
    keywords = [
        "Deathtouch", "Defender", "Double strike", "Enchant", "Equip",
        "First strike", "Flash", "Flying", "Haste", "Hexproof",
        "Indestructible", "Lifelink", "Menace", "Protection", "Prowess",
        "Reach", "Trample", "Vigilance"
    ]

    # Initialize the deck as an empty list
    deck = []

    # Continue searching for cards
    while len(deck) < 100:
        # Prompt the user to select a card type to search for
        card_type = input("Enter the card type to search for (e.g., Instant, Sorcery, Artifact, or 'done' to finish building the deck): ")
        
        if card_type.lower() == 'done':
            break  # Exit the loop if the user is done building the deck
        
        # Search for cards of the specified type with matching keywords and add them to the deck
        if search_cards(color_identity, card_type, keywords):
            continue

        # Check if the deck has reached 65 cards and prompt the user to add lands
        if len(deck) == 65:
            add_lands_prompt = input("You have 65 cards in the deck. Do you want to fill the remaining deck with lands? (yes/no): ")
            if add_lands_prompt.lower() == 'yes':
                # You can add your code here to add lands to the deck
                # For example, you can add basic lands or any specific land cards you prefer
                print("Filling the remaining deck with lands...")
                deck.extend(['Forest'] * (100 - len(deck)))

    # Ensure the deck has exactly 100 cards
    while len(deck) < 100:
        print("Your deck does not have enough cards. Please add more cards.")
        add_to_deck = input("Add cards to the deck (enter card names separated by commas): ")
        deck.extend(add_to_deck.split(','))

    # Display the final deck
    print("Your deck is complete with the following cards:")
    for card in deck:
        print(f"- {card}")

    print("Deck building is complete!")

else:
    print("Failed to retrieve commander details.")

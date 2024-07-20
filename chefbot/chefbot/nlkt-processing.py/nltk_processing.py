import json
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import nltk

# Download NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('wordnet')

# Load general.json data
with open('general.json', 'r', encoding='utf-8') as f:
    general_data = json.load(f)

# Function to tokenize text
def tokenize(text):
    return word_tokenize(text)

# Function to find synonyms of a word using WordNet
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

# Function to generate response based on user input
def generate_response(user_input):
    tokens = tokenize(user_input.lower())
    
    for intent in general_data['intents']:
        if 'patterns' in intent:
            for pattern in intent['patterns']:
                pattern_tokens = tokenize(pattern.lower())
                if all(token in tokens for token in pattern_tokens):
                    return random.choice(intent['responses'])

    # Check for recipe related queries
    if any(word in tokens for word in ['recipe', 'cook', 'make']):
        return "What ingredients do you have in mind?"

    # Check for ingredients provided by the user
    user_ingredients = []
    for token in tokens:
        if token in general_data['ingredients']:
            user_ingredients.append(token)

    if user_ingredients:
        matched_recipes = []
        for recipe in general_data['recipes']:
            recipe_ingredients = recipe['ingredients']
            matched_count = sum(1 for ingredient in recipe_ingredients if ingredient in user_ingredients)
            if matched_count >= len(user_ingredients) * 0.7: 
                matched_recipes.append(recipe)

        if matched_recipes:
            random_recipe = random.choice(matched_recipes)
            response = f"Here is a recipe you can make with the available ingredients: {random_recipe['title']} "
            response += f"Ingredients: {', '.join(random_recipe['ingredients'])}\n "
            response += f"Instructions: \n{'\n'.join(random_recipe['instructions'])}\n"
            return response
        else:
            return "Sorry, I couldn't find a recipe matching the available ingredients. Please try different ingredients."

    return "I'm sorry, I didn't understand that. Please rephrase."

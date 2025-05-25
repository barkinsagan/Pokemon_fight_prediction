import streamlit as st
import pandas as pd
import joblib
import random
import requests
import altair as alt
from predict import predict_battle_from_base_stats

# Load the model
best_model = joblib.load('best_model_exp2.pkl')

# Load the Pokémon data
pokemon_data = pd.read_csv('pokemon.csv')

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Arena", "Catalogue"])

def get_pokemon_image_and_data(pokemon_name):
    """Fetch Pokémon image and data from PokeAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data['name'],
            "sprite": data['sprites']['front_default']
        }
    else:
        return None

if page == "Arena":
    # Title of the app
    st.title('Pokémon Battle Predictor')

    # Instructions
    st.write("Select two Pokémon to predict the winner of their battle.")

    # Dropdowns for Pokémon selection
    pokemon_names = pokemon_data['Name'].tolist()
    pokemon1 = st.selectbox('Select the first Pokémon:', pokemon_names)
    pokemon2 = st.selectbox('Select the second Pokémon:', pokemon_names)

    # Display images and stats side by side
    if pokemon1 and pokemon2:
        col1, col2 = st.columns(2)

        with col1:
            poke_info1 = get_pokemon_image_and_data(pokemon1)
            if poke_info1:
                st.image(poke_info1['sprite'], width=200)
                st.write(f"**Name:** {pokemon1}")
                poke_stats1 = pokemon_data[pokemon_data['Name'] == pokemon1].iloc[0]
                
                # Prepare data for bar chart
                stats1 = {
                    "Stat": ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"],
                    "Value": [
                        poke_stats1['HP'],
                        poke_stats1['Attack'],
                        poke_stats1['Defense'],
                        poke_stats1['Sp. Atk'],
                        poke_stats1['Sp. Def'],
                        poke_stats1['Speed']
                    ]
                }
                stats_df1 = pd.DataFrame(stats1)

                # Create a bar chart
                chart1 = alt.Chart(stats_df1).mark_bar().encode(
                    x=alt.X('Stat', sort=None),
                    y='Value',
                    color='Stat'
                ).properties(
                    width=300,
                    height=200
                )

                st.altair_chart(chart1, use_container_width=True)

        with col2:
            poke_info2 = get_pokemon_image_and_data(pokemon2)
            if poke_info2:
                st.image(poke_info2['sprite'], width=200)
                st.write(f"**Name:** {pokemon2}")
                poke_stats2 = pokemon_data[pokemon_data['Name'] == pokemon2].iloc[0]
                
                # Prepare data for bar chart
                stats2 = {
                    "Stat": ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"],
                    "Value": [
                        poke_stats2['HP'],
                        poke_stats2['Attack'],
                        poke_stats2['Defense'],
                        poke_stats2['Sp. Atk'],
                        poke_stats2['Sp. Def'],
                        poke_stats2['Speed']
                    ]
                }
                stats_df2 = pd.DataFrame(stats2)

                # Create a bar chart
                chart2 = alt.Chart(stats_df2).mark_bar().encode(
                    x=alt.X('Stat', sort=None),
                    y='Value',
                    color='Stat'
                ).properties(
                    width=300,
                    height=200
                )

                st.altair_chart(chart2, use_container_width=True)

    # Button to make prediction
    if st.button('Predict Winner'):
        try:
            # Use the imported function to predict the winner
            result = predict_battle_from_base_stats(pokemon1, pokemon2, best_model, 'pokemon.csv')
            
            # Display the winner's image and name
            if result == 1:
                winner_info = poke_info1
                winner_name = pokemon1
            else:
                winner_info = poke_info2
                winner_name = pokemon2

            st.markdown("<hr>", unsafe_allow_html=True)
            st.write("### Winner")
            st.markdown(
                f"<div style='text-align: center;'><img src='{winner_info['sprite']}' width='200'></div>",
                unsafe_allow_html=True
            )
            st.markdown(f"<div style='text-align: center;'><strong>{winner_name}</strong> is predicted to win!</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")

elif page == "Catalogue":
    st.title("Pokémon Showcase")
    st.write("Here is a random selection of 5 Pokémon with their images, stats, and categorical values.")

    # Search bar for selecting the first Pokémon
    selected_pokemon_name = st.selectbox('Select a Pokémon:', ['Random'] + pokemon_data['Name'].tolist())

    # Ensure we have 5 Pokémon with images
    selected_pokemon = []
    if selected_pokemon_name != 'Random':
        selected_pokemon.append(selected_pokemon_name)

    while len(selected_pokemon) < 5:
        random_pokemon = random.sample(pokemon_data['Name'].tolist(), 5 - len(selected_pokemon))
        for pokemon_name in random_pokemon:
            if pokemon_name not in selected_pokemon:
                poke_info = get_pokemon_image_and_data(pokemon_name)
                if poke_info and poke_info['sprite']:
                    selected_pokemon.append(pokemon_name)
            if len(selected_pokemon) == 5:
                break

    # Display Pokémon details
    for pokemon_name in selected_pokemon:
        poke_stats = pokemon_data[pokemon_data['Name'] == pokemon_name].iloc[0]
        poke_info = get_pokemon_image_and_data(pokemon_name)

        # Create three columns for layout
        col1, col2, col3 = st.columns([1, 4, 4])

        with col1:
            if poke_info:
                st.image(poke_info['sprite'], width=900)

        with col2:
            # Prepare data for bar chart
            stats = {
                "Stat": ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"],
                "Value": [
                    poke_stats['HP'],
                    poke_stats['Attack'],
                    poke_stats['Defense'],
                    poke_stats['Sp. Atk'],
                    poke_stats['Sp. Def'],
                    poke_stats['Speed']
                ]
            }
            stats_df = pd.DataFrame(stats)

            # Create a bar chart
            chart = alt.Chart(stats_df).mark_bar().encode(
                x=alt.X('Stat', sort=None),
                y='Value',
                color='Stat'
            ).properties(
                width=400,
                height=250
            )

            st.altair_chart(chart, use_container_width=True)

        with col3:
            # Display categorical values
            st.write(f"**Name:** {poke_stats['Name']}")
            st.write(f"**Type 1:** {poke_stats['Type 1']}")
            st.write(f"**Type 2:** {poke_stats['Type 2']}")
            st.write(f"**Generation:** {poke_stats['Generation']}")
            st.write(f"**Legendary:** {'Yes' if poke_stats['Legendary'] else 'No'}")

        # Add spacing between rows
        st.markdown("<br>", unsafe_allow_html=True) 
import pandas as pd
import numpy as np
import joblib

def predict_battle_from_base_stats(pokemon1, pokemon2, best_model, pokemon_csv_path='pokemon.csv'):
    """
    Predicts the winner between two Pokémon using base stats from pokemon.csv and the trained model.
    
    Parameters:
        pokemon1 (str): Name of the first Pokémon.
        pokemon2 (str): Name of the second Pokémon.
        best_model: Trained XGBoost model.
        pokemon_csv_path (str): Path to the pokemon.csv file.

    Returns:
        int: 1 if first Pokémon wins, 0 if second Pokémon wins.
    """
    # --- Load base data ---
    df_base = pd.read_csv(pokemon_csv_path)

    # Ensure consistent naming
    pokemon1 = pokemon1.strip()
    pokemon2 = pokemon2.strip()

    # Get the rows for the Pokémon
    poke1 = df_base[df_base['Name'] == pokemon1]
    poke2 = df_base[df_base['Name'] == pokemon2]

    if poke1.empty or poke2.empty:
        raise ValueError("One or both Pokémon names not found in the CSV.")

    poke1 = poke1.iloc[0]
    poke2 = poke2.iloc[0]

    # --- Compute Features ---
    row = {
        'First_Generation': poke1['Generation'],
        'Second_Generation': poke2['Generation'],
        'First_Legendary': int(poke1['Legendary']),
        'Second_Legendary': int(poke2['Legendary']),
        'First_Type 1': poke1['Type 1'],
        'Second_Type 1': poke2['Type 1'],
        'HP_Diff': poke1['HP'] - poke2['HP'],
        'Attack_Diff': poke1['Attack'] - poke2['Attack'],
        'Defense_Diff': poke1['Defense'] - poke2['Defense'],
        'SpAtk_Diff': poke1['Sp. Atk'] - poke2['Sp. Atk'],
        'SpDef_Diff': poke1['Sp. Def'] - poke2['Sp. Def'],
        'Speed_Diff': poke1['Speed'] - poke2['Speed']
        
    }

    df_input = pd.DataFrame([row])

    # One-hot encode type columns
    df_input = pd.get_dummies(df_input, columns=['First_Type 1', 'Second_Type 1'], drop_first=True)

    # Align with model features
    model_features = best_model.get_booster().feature_names
    for col in model_features:
        if col not in df_input.columns:
            df_input[col] = 0  # Add missing dummy columns

    df_input = df_input[model_features]  # Ensure correct order

    # --- Predict ---
    prediction = best_model.predict(df_input)[0]
    return prediction  # 1 = First Pokémon wins, 0 = Second Pokémon wins

if __name__ == "__main__":
    # Example usage
    try:
        # Load the model
        best_model = joblib.load('best_model_exp2.pkl')
        
        # Example Pokémon names
        pokemon1 = "Pikachu"
        pokemon2 = "Charizard"
        
        # Predict the winner
        result = predict_battle_from_base_stats(pokemon1, pokemon2, best_model)
        
        # Output the result
        if result == 1:
            print(f"{pokemon1} is predicted to win against {pokemon2}.")
        else:
            print(f"{pokemon2} is predicted to win against {pokemon1}.")
    except Exception as e:
        print(f"An error occurred: {e}")

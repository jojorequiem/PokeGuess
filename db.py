import sqlite3

# Function that select a random pokemon from the DATABASE 
def info_pokemon():
    conn = sqlite3.connect("database/pokemons.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT types.libelle
        FROM pokemons
        JOIN est_type ON pokemons.id = est_type.pokemon_id
        JOIN types ON est_type.type_id = types.id
        JOIN evolue_en ON pokemons.id = evolue_en.pokemon_base_id
        WHERE evolue_en.pokemon_evol_id != -1
        ORDER BY RANDOM() LIMIT 1
    """)
    type_pokemon = cursor.fetchone()[0]

    cursor.execute("""
        SELECT pokemons.id, pokemons.nom, evo.nom
        FROM pokemons
        JOIN est_type ON pokemons.id = est_type.pokemon_id
        JOIN types ON est_type.type_id = types.id
        LEFT JOIN evolue_en ON pokemons.id = evolue_en.pokemon_base_id
        LEFT JOIN pokemons evo ON evolue_en.pokemon_evol_id = evo.id
        WHERE types.libelle = ? AND (evolue_en.pokemon_evol_id IS NULL OR evolue_en.pokemon_evol_id != -1)
        ORDER BY RANDOM() LIMIT 1
    """, (type_pokemon,))
    pokemon_id, pokemon, evolution = cursor.fetchone()

    cursor.execute("""
        SELECT poids, taille
        FROM taille_et_poids
        WHERE pokemon_id = (
            SELECT id
            FROM pokemons
            WHERE nom = ?
        )
    """, (pokemon,))
    weight, height = cursor.fetchone()

    cursor.execute("""
        SELECT attaques.libelle
        FROM attaques
        JOIN types ON attaques.type_id = types.id
        WHERE types.libelle = ?
        ORDER BY RANDOM() LIMIT 1
    """, (type_pokemon,))
    attack = cursor.fetchone()[0]

    cursor.execute("""
        SELECT types.libelle
        FROM pokemons
        JOIN est_type ON pokemons.id = est_type.pokemon_id
        JOIN types ON est_type.type_id = types.id
        WHERE pokemons.nom = ?
    """, (pokemon,))
    pokemon_types = cursor.fetchall()
    pokemon_types_str = " & ".join([t[0] for t in pokemon_types])

    if evolution: #If the selected Pokemon has no evolution => return None
        evolution = evolution
    else :
        evolution = None

    conn.close()

    return pokemon, evolution, pokemon_types_str, weight, height, attack, pokemon_id

# Function that enables auto-completion of the player's input
def get_autocomplete_results(text):
    conn = sqlite3.connect("database/pokemons.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nom
        FROM pokemons
        WHERE nom LIKE ?
        ORDER BY nom
    """, (text + "%",))

    result = cursor.fetchall()

    return [row[0] for row in result]
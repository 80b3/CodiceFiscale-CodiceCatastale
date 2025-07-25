import re
import json
import os
import logging
from datetime import datetime

# Configura il logging per una migliore segnalazione degli errori
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calculate_check_digit(cf_first_15: str) -> str:
    """
    Calcola il carattere di controllo per un Codice Fiscale italiano basandosi sui primi 15 caratteri.

    Args:
        cf_first_15: I primi 15 caratteri del Codice Fiscale.

    Returns:
        Il carattere di controllo calcolato (una singola lettera maiuscola).
    """
    # Tabella di conversione per posizioni dispari (contando da 1)
    odd_chars = {
        '0': 1, '1': 0, '2': 5, '3': 7, '4': 9, '5': 13, '6': 15, '7': 17, '8': 19, '9': 21,
        'A': 1, 'B': 0, 'C': 5, 'D': 7, 'E': 9, 'F': 13, 'G': 15, 'H': 17, 'I': 19, 'J': 21,
        'K': 2, 'L': 4, 'M': 18, 'N': 20, 'O': 11, 'P': 3, 'Q': 6, 'R': 8, 'S': 12, 'T': 14,
        'U': 16, 'V': 10, 'W': 22, 'X': 25, 'Y': 24, 'Z': 23
    }

    # Tabella di conversione per posizioni pari (contando da 1)
    even_chars = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
        'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18,
        'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25
    }

    # Tabella di mappatura del carattere di controllo
    remainder_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    total = 0
    # Itera sui primi 15 caratteri per calcolare la somma di controllo
    for i in range(15):
        char = cf_first_15[i]
        # Le posizioni dispari (contando da 1) corrispondono agli indici pari (contando da 0)
        if (i + 1) % 2 != 0:  # Posizione dispari
            total += odd_chars.get(char, 0) # Usa .get con default per gestire caratteri potenzialmente mancanti
        else:  # Posizione pari
            total += even_chars.get(char, 0) # Usa .get con default per gestire caratteri potenzialmente mancanti

    # Calcola il resto e ottieni il carattere di controllo
    remainder = total % 26
    return remainder_chars[remainder]

def load_location_codes(file_path: str) -> dict | None:
    """
    Carica i codici di località da un file JSON.

    Args:
        file_path: Il percorso del file location_codes.json.

    Returns:
        Un dizionario contenente i codici di località se l'operazione ha successo, None altrimenti.
    """
    if not os.path.exists(file_path):
        logger.error(f'File dei codici di località non trovato: {file_path}')
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            locations = json.load(f)
            if not isinstance(locations, dict) or not all(k in locations for k in ('Comune', 'Estero')):
                logger.error('Formato del file dei codici di località errato: non è un oggetto JSON valido o mancano i raggruppamenti di tipo necessari')
                return None
            return locations
    except json.JSONDecodeError as e:
        logger.error(f'Errore di parsing del file dei codici di località: {str(e)}')
        return None
    except Exception as e:
        logger.error(f'Errore durante la lettura delle informazioni sulla località: {str(e)}')
        return None

def validate_codice_fiscale(cf: str) -> tuple[bool, dict | str]:
    """
    Valida un Codice Fiscale italiano ed estrae le informazioni pertinenti.

    Args:
        cf: La stringa del Codice Fiscale da validare.

    Returns:
        Una tupla: (True, dict) se valido, dove il dict contiene le informazioni estratte.
                 (False, str) se non valido, dove la stringa è un messaggio di errore.
    """
    # Converti in maiuscolo per una validazione coerente
    cf = cf.upper()

    # 1. Controlla la lunghezza
    if len(cf) != 16:
        return False, "Il Codice Fiscale deve essere lungo 16 caratteri."

    # 2. Controlla il formato di base usando le espressioni regolari
    # Pattern: 6 lettere, 2 cifre, 1 lettera specifica (A-EHLMPRST per il mese),
    # 2 cifre, 1 lettera, 3 cifre, 1 lettera (carattere di controllo)
    if not re.match(r'^[A-Z]{6}\d{2}[A-EHLMPRST]\d{2}[A-Z]\d{3}[A-Z]$', cf):
        return False, "Il formato del Codice Fiscale non è corretto. Si prega di controllare le regole."

    # 3. Valida il carattere di controllo
    expected_check_digit = calculate_check_digit(cf[:15])
    if cf[15] != expected_check_digit:
        return False, f"Carattere di controllo errato. Previsto: {expected_check_digit}, Attuale: {cf[15]}."

    # 4. Estrai l'anno di nascita
    year_two_digits = int(cf[6:8])
    current_year_suffix = datetime.now().year % 100
    if year_two_digits > current_year_suffix:
        year = 1900 + year_two_digits
    else:
        year = 2000 + year_two_digits

    # 5. Estrai il mese
    months_map = 'ABCDEHLMPRST' # A=Gen, B=Feb, C=Mar, D=Apr, E=Mag, H=Giu, L=Lug, M=Ago, P=Set, R=Ott, S=Nov, T=Dic
    month_char = cf[8]
    try:
        month = months_map.index(month_char) + 1
    except ValueError:
        return False, "Codice del mese di nascita non valido."

    # 6. Estrai il giorno e determina il sesso
    day_raw = int(cf[9:11])
    if day_raw > 40:
        gender = 'F' # Femmina
        day = day_raw - 40
    else:
        gender = 'M' # Maschio
        day = day_raw

    # 7. Valida la data di nascita
    try:
        birth_date = datetime(year, month, day)
        birth_date_str = birth_date.strftime('%Y-%m-%d')
    except ValueError:
        return False, "Data di nascita non valida."

    # 8. Calcola l'età
    today = datetime.now()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    # 9. Estrai il codice del luogo di nascita e recupera le informazioni
    birth_place_code = cf[11:15]
    
    # Determina il percorso assoluto del file location_codes.json
    script_dir = os.path.dirname(__file__)
    location_file_path = os.path.join(script_dir, 'location_codes.json')

    locations = load_location_codes(location_file_path)
    if locations is None:
        return False, "Impossibile caricare il file dei codici di località. Assicurati che 'location_codes.json' esista e sia formattato correttamente."

    birth_place_info = None
    # Cerca in 'Comune' (Comuni italiani)
    for item in locations.get('Comune', []):
        if item.get('code') == birth_place_code:
            birth_place_info = {'name': item.get('name', 'Località sconosciuta'), 'type': 'Comune'}
            break
    
    # Se non trovato in 'Comune', cerca in 'Estero' (Paesi stranieri)
    if not birth_place_info:
        for item in locations.get('Estero', []):
            if item.get('code') == birth_place_code:
                birth_place_info = {'name': item.get('name', 'Località sconosciuta'), 'type': 'Estero'}
                break
    
    # Se ancora non trovato, imposta come sconosciuto
    if not birth_place_info:
        logger.warning(f'Nessun codice di località corrispondente trovato per: {birth_place_code}')
        birth_place_info = {'name': 'Località sconosciuta', 'type': 'unknown'}

    result = {
        'valid': True,
        'gender': gender,
        'birth_date': birth_date_str,
        'age': age,
        'birth_place_code': birth_place_code,
        'birth_place': birth_place_info['name'],
        'birth_place_type': birth_place_info['type']
    }
    
    return True, result

if __name__ == '__main__':
    # Esempio di utilizzo:
    print("--- Esempi di Validazione del Codice Fiscale ---")

    # Esempio 1: Codice Fiscale valido (sostituisci con uno reale per i test)
    # Formato: 6 lettere, 2 cifre (anno), 1 lettera (mese), 2 cifre (giorno), 1 lettera (codice provincia/estero), 3 cifre (sequenziale), 1 lettera (carattere di controllo)
    # Esempio per un uomo nato a Roma il 15/01/1980 (codice fittizio)
    cf_valid_male = "RSSMRA80A15H501Z"
    valid, info = validate_codice_fiscale(cf_valid_male)
    if valid:
        print(f"\nCodice Fiscale: {cf_valid_male}")
        print(f"Codice Fiscale valido!")
        print(f"Sesso: {'Femmina' if info['gender'] == 'F' else 'Maschio'}")
        print(f"Età: {info['age']} anni")
        print(f"Data di Nascita: {info['birth_date']}")
        print(f"Luogo di Nascita: {info['birth_place_code']} ({info['birth_place_type']}) - {info['birth_place']}")
    else:
        print(f"\nCodice Fiscale: {cf_valid_male}")
        print(f"Codice Fiscale non valido! Errore: {info}")

    # Esempio 2: Codice Fiscale valido per una donna nata all'estero (codice fittizio)
    cf_valid_female_foreign = "MRCRSS75T55Z100X" # Fittizio: Mese T, Giorno 15+40=55, Codice estero Z100
    valid, info = validate_codice_fiscale(cf_valid_female_foreign)
    if valid:
        print(f"\nCodice Fiscale: {cf_valid_female_foreign}")
        print(f"Codice Fiscale valido!")
        print(f"Sesso: {'Femmina' if info['gender'] == 'F' else 'Maschio'}")
        print(f"Età: {info['age']} anni")
        print(f"Data di Nascita: {info['birth_date']}")
        print(f"Luogo di Nascita: {info['birth_place_code']} ({info['birth_place_type']}) - {info['birth_place']}")
    else:
        print(f"\nCodice Fiscale: {cf_valid_female_foreign}")
        print(f"Codice Fiscale non valido! Errore: {info}")

    # Esempio 3: Lunghezza non valida
    cf_invalid_length = "ABCDEF12A34B567C" # 16 caratteri
    valid, info = validate_codice_fiscale(cf_invalid_length)
    if valid:
        print(f"\nCodice Fiscale: {cf_invalid_length}")
        print(f"Codice Fiscale valido!")
    else:
        print(f"\nCodice Fiscale: {cf_invalid_length}")
        print(f"Codice Fiscale non valido! Errore: {info}")

    # Esempio 4: Formato non valido (non lettera nei primi 6)
    cf_invalid_format = "ABCDE112A34B567C"
    valid, info = validate_codice_fiscale(cf_invalid_format)
    if valid:
        print(f"\nCodice Fiscale: {cf_invalid_format}")
        print(f"Codice Fiscale valido!")
    else:
        print(f"\nCodice Fiscale: {cf_invalid_format}")
        print(f"Codice Fiscale non valido! Errore: {info}")

    # Esempio 5: Carattere di controllo non valido (fittizio)
    cf_invalid_check_digit = "RSSMRA80A15H501Y" # Il carattere finale corretto dovrebbe essere Z, non Y
    valid, info = validate_codice_fiscale(cf_invalid_check_digit)
    if valid:
        print(f"\nCodice Fiscale: {cf_invalid_check_digit}")
        print(f"Codice Fiscale valido!")
    else:
        print(f"\nCodice Fiscale: {cf_invalid_check_digit}")
        print(f"Codice Fiscale non valido! Errore: {info}")

    # Esempio 6: Data di nascita non valida (es. 30 febbraio)
    cf_invalid_date = "RSSMRA80B30H501Z" # Fittizio, 30 febbraio
    valid, info = validate_codice_fiscale(cf_invalid_date)
    if valid:
        print(f"\nCodice Fiscale: {cf_invalid_date}")
        print(f"Codice Fiscale valido!")
    else:
        print(f"\nCodice Fiscale: {cf_invalid_date}")
        print(f"Codice Fiscale non valido! Errore: {info}")

    # Esempio 7: Codice di località sconosciuto (fittizio)
    cf_unknown_location = "RSSMRA80A15XXXXZ" # Fittizio, XXXX non è in location_codes.json
    valid, info = validate_codice_fiscale(cf_unknown_location)
    if valid:
        print(f"\nCodice Fiscale: {cf_unknown_location}")
        print(f"Codice Fiscale valido!")
        print(f"Luogo di Nascita: {info['birth_place_code']} ({info['birth_place_type']}) - {info['birth_place']}")
    else:
        print(f"\nCodice Fiscale: {cf_unknown_location}")
        print(f"Codice Fiscale non valido! Errore: {info}")

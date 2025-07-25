CodiceFiscale-Validator
Questo repository fornisce uno script Python per convalidare il Codice Fiscale italiano ed estrarre informazioni personali pertinenti come sesso, data di nascita, età e luogo di nascita.

🌟 Funzionalità
Validazione Completa: Controlla la lunghezza, il formato e la correttezza del carattere di controllo.

Estrazione Informazioni: Estrae automaticamente sesso, data di nascita completa, età e dettagli del luogo di nascita da un Codice Fiscale valido.

Integrazione Dati di Località: Utilizza un file location_codes.json per mappare i codici del luogo di nascita ai nomi effettivi di città/paesi.

Messaggi di Errore Chiari: Fornisce messaggi di errore descrittivi sia in italiano che in cinese per input di Codice Fiscale non validi.

🚀 Per Iniziare
Prerequisiti
Python 3.6 o superiore

Installazione
Clona il repository:

git clone https://github.com/your-username/CodiceFiscale-Validator.git
cd CodiceFiscale-Validator


Assicurati che location_codes.json sia presente:
Assicurati che il file location_codes.json si trovi nella stessa directory di codice_fiscale_validator.py. Un file di esempio è fornito in questo repository. Per i codici di località ufficiali e aggiornati, fai riferimento alle fonti menzionate nella sezione "Fonte" di seguito.

💡 Utilizzo
Puoi utilizzare la funzione validate_codice_fiscale nei tuoi progetti Python.

from codice_fiscale_validator import validate_codice_fiscale

# Esempio: Codice Fiscale valido
cf = "RSSMRA80A15H501Z" # Sostituisci con un Codice Fiscale reale per test effettivi

valido, info = validate_codice_fiscale(cf)

if valido:
    print("Codice Fiscale è valido!")
    print(f"Sesso: {'Femmina' if info['gender'] == 'F' else 'Maschio'}")
    print(f"Età: {info['age']} anni")
    print(f"Data di Nascita: {info['birth_date']}")
    print(f"Luogo di Nascita: {info['birth_place_code']} ({info['birth_place_type']}) - {info['birth_place']}")
else:
    print(f"Codice Fiscale non valido! Errore: {info}")

# Esempio: Codice Fiscale non valido (lunghezza errata)
cf_invalid = "ABCDEF123456789"
valido, info = validate_codice_fiscale(cf_invalid)
if not valido:
    print(f"\nCF non valido: {cf_invalid}, Errore: {info}")


Puoi anche eseguire lo script direttamente per vedere gli esempi:

python codice_fiscale_validator.py


📚 Fonte (Fonti per i Codici di Località)
Il file location_codes.json è fondamentale per mappare i codici del luogo di nascita. Puoi trovare elenchi ufficiali e aggiornati dall'Agenzia delle Entrate italiana e da altre fonti ufficiali.

CodiceFiscale-Validator
Questo repository fornisce uno script Python per convalidare il Codice Fiscale italiano ed estrarre informazioni personali pertinenti come sesso, data di nascita, età e luogo di nascita.

🌟 Funzionalità
Validazione Completa: Controlla la lunghezza, il formato e la correttezza del carattere di controllo.

Estrazione Informazioni: Estrae automaticamente sesso, data di nascita completa, età e dettagli del luogo di nascita da un Codice Fiscale valido.

Integrazione Dati di Località: Utilizza un file location_codes.json per mappare i codici del luogo di nascita ai nomi effettivi di città/paesi.

Messaggi di Errore Chiari: Fornisce messaggi di errore descrittivi sia in italiano che in cinese per input di Codice Fiscale non validi.

🚀 Per Iniziare
Prerequisiti
Python 3.6 o superiore

Installazione
Clona il repository:

git clone https://github.com/your-username/CodiceFiscale-Validator.git
cd CodiceFiscale-Validator


Assicurati che location_codes.json sia presente:
Assicurati che il file location_codes.json si trovi nella stessa directory di codice_fiscale_validator.py. Un file di esempio è fornito in questo repository. Per i codici di località ufficiali e aggiornati, fai riferimento alle fonti menzionate nella sezione "Fonte" di seguito.

💡 Utilizzo
Puoi utilizzare la funzione validate_codice_fiscale nei tuoi progetti Python.

from codice_fiscale_validator import validate_codice_fiscale

# Esempio: Codice Fiscale valido
cf = "RSSMRA80A15H501Z" # Sostituisci con un Codice Fiscale reale per test effettivi

valido, info = validate_codice_fiscale(cf)

if valido:
    print("Codice Fiscale è valido!")
    print(f"Sesso: {'Femmina' if info['gender'] == 'F' else 'Maschio'}")
    print(f"Età: {info['age']} anni")
    print(f"Data di Nascita: {info['birth_date']}")
    print(f"Luogo di Nascita: {info['birth_place_code']} ({info['birth_place_type']}) - {info['birth_place']}")
else:
    print(f"Codice Fiscale non valido! Errore: {info}")

# Esempio: Codice Fiscale non valido (lunghezza errata)
cf_invalid = "ABCDEF123456789"
valido, info = validate_codice_fiscale(cf_invalid)
if not valido:
    print(f"\nCF non valido: {cf_invalid}, Errore: {info}")


Puoi anche eseguire lo script direttamente per vedere gli esempi:

python codice_fiscale_validator.py


📚 Fonte (Fonti per i Codici di Località)
Il file location_codes.json è fondamentale per mappare i codici del luogo di nascita. Puoi trovare elenchi ufficiali e aggiornati dall'Agenzia delle Entrate italiana e da altre fonti ufficiali.

Comuni Italiani:

Tabella dei Codici Catastali dei Comuni - Agenzia Entrate (Questo è un PDF, dovrai estrarne i dati o trovare una versione leggibile da macchina.)

Stati Esteri:

Studio K SRL help.studiok.it/etri/codicefiscaledegliestieri (Questo potrebbe richiedere estrazione o analisi manuale.)

Nota: Il location_codes.json fornito in questo repository è un esempio e potrebbe non essere esaustivo o perfettamente aggiornato. Si consiglia di aggiornare periodicamente questo file da fonti ufficiali se i dati precisi sulla località sono critici per la tua applicazione.

🤝 Contribuisci
I contributi sono benvenuti! Se hai suggerimenti per miglioramenti, correzioni di bug o nuove funzionalità, apri un'issue o invia una pull request.

📄 Licenza
Questo progetto è concesso in licenza con la Licenza MIT - vedi il file LICENSE per i dettagli (potresti voler aggiungere un file LICENSE al tuo repository).

🤝 Contribuisci
I contributi sono benvenuti! Se hai suggerimenti per miglioramenti, correzioni di bug o nuove funzionalità, apri un'issue o invia una pull request.

📄 Licenza
Questo progetto è concesso in licenza con la Licenza MIT - vedi il file LICENSE per i dettagli (potresti voler aggiungere un file LICENSE al tuo repository).

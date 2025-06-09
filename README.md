# Guida Aviation Weather MCP Server 🛩️

## Cos'è l'Aviation Weather MCP?

L'**Aviation Weather MCP** è un server che ti permette di accedere facilmente a dati meteorologici per l'aviazione direttamente da VS Code. È come avere un meteorologo per piloti sempre a portata di mano!

### A cosa serve?

Se sei interessato all'aviazione, sia come pilota, appassionato di volo, o semplicemente curioso del meteo negli aeroporti, questo strumento ti permette di:

- 🌦️ **Controllare il meteo attuale** negli aeroporti di tutto il mondo
- 📊 **Leggere le previsioni** per pianificare voli
- ✈️ **Vedere i rapporti dei piloti** su turbolenze e condizioni di volo
- 🚨 **Ricevere avvisi meteorologici** importanti per la sicurezza del volo
- 🗺️ **Ottenere informazioni** su aeroporti, radioassistenze e punti di navigazione

## Come funziona?

Il server si collega al sito ufficiale **aviationweather.gov** (gestito dalla NOAA - Agenzia Meteorologica USA) e ti fornisce dati in tempo reale in un formato facile da leggere.

## Principali Tipi di Dati Disponibili

### 1. **METAR** - Osservazioni Meteorologiche Attuali
I METAR sono rapporti meteorologici che vengono aggiornati ogni ora (o più frequentemente se necessario) e contengono:
- Temperatura e punto di rugiada
- Velocità e direzione del vento
- Visibilità
- Copertura nuvolosa e altezza delle nuvole
- Precipitazioni in corso
- Pressione atmosferica

### 2. **TAF** - Previsioni Meteorologiche
I TAF sono previsioni dettagliate per 24-30 ore che includono:
- Cambiamenti previsti nelle condizioni meteorologiche
- Orari specifici dei cambiamenti
- Condizioni di vento, visibilità e nuvole previste

### 3. **PIREP** - Rapporti dei Piloti
Rapporti diretti dai piloti in volo che segnalano:
- Turbolenze
- Formazione di ghiaccio
- Visibilità in volo
- Altezza delle nuvole effettiva

### 4. **SIGMET e AIRMET** - Avvisi Meteorologici
Avvisi ufficiali per condizioni meteorologiche pericolose come:
- Temporali severi
- Turbolenze intense
- Formazione di ghiaccio
- Visibilità ridotta

## Come Usare il Server

### 🎯 Prompt di Contesto per Forzare l'Uso dell'MCP

Se l'AI non utilizza automaticamente il server aviation-weather MCP, usa questo **prompt di contesto** all'inizio della tua conversazione:

```
Sei un AI che usa MCP server. In particolare usa aviation-weather che è running. 
Voglio sapere il meteo di [INSERISCI QUI LA TUA RICHIESTA]
```

**Esempi pratici:**
```
Sei un AI che usa MCP server. In particolare usa aviation-weather che è running. 
Voglio sapere il meteo di Roma Fiumicino

Sei un AI che usa MCP server. In particolare usa aviation-weather che è running. 
Voglio sapere il meteo di Milano Malpensa e le previsioni per domani

Sei un AI che usa MCP server. In particolare usa aviation-weather che è running. 
Voglio sapere se ci sono turbolenze sulla rotta Roma-Londra
```

### Esempi di Prompt Semplici

Ecco alcuni esempi di richieste che puoi fare:

#### 🌍 **Controllare il Meteo negli Aeroporti**
```
"Mostrami il meteo attuale per Roma Fiumicino (LIRF)"
"Che tempo c'è ora a Milano Malpensa (LIMC)?"
"Dammi i METAR per New York JFK (KJFK) e Los Angeles (KLAX)"
```

#### 📊 **Leggere le Previsioni**
```
"Mostrami le previsioni TAF per Londra Heathrow (EGLL)"
"Che tempo è previsto per domani a Parigi Charles de Gaulle (LFPG)?"
"Dammi le previsioni per Miami (KMIA) per le prossime 24 ore"
```

#### ✈️ **Informazioni sugli Aeroporti**
```
"Dimmi tutto sull'aeroporto di Tokyo Narita (RJAA)"
"Che informazioni hai su Barcellona El Prat (LEBL)?"
"Mostrami i dettagli dell'aeroporto di Dubai (OMDB)"
```

#### 🚨 **Controllare Avvisi Meteorologici**
```
"Ci sono SIGMET attivi negli Stati Uniti?"
"Mostrami gli avvisi meteorologici per l'Europa"
"Ci sono avvisi per turbolenze nel Regno Unito?"
```

#### 🗺️ **Cercare per Area Geografica**
```
"Mostrami tutti gli aeroporti nella zona di Milano"
"Che tempo c'è negli aeroporti della Florida?"
"Dammi i METAR per tutti gli aeroporti in un raggio di 100 miglia da Chicago"
```

### Esempio Completo di Conversazione

**Tu:** "Ciao! Sto pianificando un volo da Roma a Londra domani. Puoi aiutarmi a controllare le condizioni meteorologiche?"

**AI con Aviation Weather MCP:** 
- Controllerò prima i METAR attuali per Roma Fiumicino (LIRF) e Londra Heathrow (EGLL)
- Poi vedrò le previsioni TAF per domani
- Infine controllerò se ci sono SIGMET o avvisi particolari sulla rotta

**Tu:** "Perfetto! E puoi anche dirmi se ci sono rapporti di turbolenze?"

**AI:** Certo! Controllo subito i PIREP per la zona...

## Codici Aeroporto (ICAO)

Gli aeroporti sono identificati da codici di 4 lettere chiamati **codici ICAO**. Ecco alcuni esempi:

### Italia 🇮🇹
- **LIRF** - Roma Fiumicino
- **LIMC** - Milano Malpensa
- **LIPZ** - Venezia Marco Polo
- **LIRN** - Napoli
- **LICC** - Catania

### Europa 🇪🇺
- **EGLL** - Londra Heathrow
- **LFPG** - Parigi Charles de Gaulle
- **EDDF** - Francoforte
- **LEMD** - Madrid Barajas
- **EHAM** - Amsterdam Schiphol

### Stati Uniti 🇺🇸
- **KJFK** - New York JFK
- **KLAX** - Los Angeles
- **KORD** - Chicago O'Hare
- **KMIA** - Miami
- **KSFO** - San Francisco

### Resto del Mondo 🌍
- **RJAA** - Tokyo Narita
- **VHHH** - Hong Kong
- **OMDB** - Dubai
- **FAOR** - Johannesburg
- **YSSY** - Sydney

## Strumenti Disponibili

Il server mette a disposizione 12 strumenti diversi:

1. **get_metar** - Osservazioni meteorologiche attuali
2. **get_taf** - Previsioni aeroportuali
3. **get_pirep** - Rapporti piloti
4. **get_sigmet** - Avvisi meteorologici nazionali
5. **get_isigmet** - Avvisi meteorologici internazionali
6. **get_gairmet** - Avvisi grafici meteo
7. **get_cwa** - Avvisi centri meteorologici
8. **get_wind_temp** - Dati vento e temperatura in quota
9. **get_station_info** - Informazioni stazioni meteorologiche
10. **get_airport_info** - Informazioni aeroporti
11. **get_navaid_info** - Informazioni radioassistenze
12. **get_fix_info** - Punti di navigazione

## Vantaggi di Questo Sistema

- 📡 **Dati in tempo reale** direttamente dalla fonte ufficiale
- 🌍 **Copertura globale** di migliaia di aeroporti
- 🤖 **Integrato in VS Code** - non devi cambiare applicazione
- 📝 **Facile da usare** - basta chiedere in linguaggio naturale
- 🔄 **Sempre aggiornato** - collegato direttamente ai server NOAA

## Configurazione VS Code

### Passo 1: Configurare il file settings.json

Per utilizzare l'Aviation Weather MCP in VS Code, devi aggiungere la configurazione nel file `settings.json`. 

1. **Apri il file settings.json di VS Code:**
   - Premi `Ctrl+Shift+P` (o `Cmd+Shift+P` su Mac)
   - Digita "Preferences: Open User Settings (JSON)"
   - Premi Invio

2. **Aggiungi questa configurazione** nella sezione `"mcp"` → `"servers"`:

```json
{
    "mcp": {
        "servers": {
            "aviation-weather": {
                "url": "http://localhost:8003/sse"
            }
        }
    }
}
```

### Esempio di configurazione completa:

Se il tuo `settings.json` è vuoto o non ha ancora una sezione MCP, ecco un esempio completo:

```json
{
    "mcp": {
        "servers": {
            "aviation-weather": {
                "url": "http://localhost:8003/sse"
            }
        }
    },
    "chat.mcp.discovery.enabled": true
}
```

### Se hai già altri server MCP configurati:

Se hai già altri server MCP (come Excel, Postgres, ecc.), aggiungi semplicemente la configurazione aviation-weather:

```json
{
    "mcp": {
        "servers": {
            "my-mcp-server-postgres": {
                "type": "stdio",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-postgres", "..."]
            },
            "excel": {
                "url": "http://localhost:8000/sse",
                "env": {
                    "EXCEL_FILES_PATH": "/workspace/db-ready"
                }
            },
            "aviation-weather": {
                "url": "http://localhost:8003/sse"
            }
        }
    },
    "chat.mcp.discovery.enabled": true
}
```

### Passo 2: Avviare il Server

Prima di usare VS Code, assicurati che il server Aviation Weather sia avviato:

1. **Apri un terminale** in VS Code (`Ctrl+`` o dal menu Terminal)

2. **Naviga nella cartella del server:**
   ```bash
   cd /workspace/db-ready/aviation-weather-mcp-server
   ```

3. **Avvia il server:**
   ```bash
   ./start.sh
   ```

4. **Verifica che sia in esecuzione** - dovresti vedere:
   ```
   Aviation Weather MCP Server - SSE mode
   --------------------------------------
   Server will start on localhost:8003
   Press Ctrl+C to exit
   INFO:     Uvicorn running on http://127.0.0.1:8003 (Press CTRL+C to quit)
   ```

### Passo 3: Testare la Configurazione

1. **Riavvia VS Code** dopo aver modificato settings.json
2. **Apri la chat di VS Code** 
3. **Fai un test semplice:**
   ```
   "Mostrami il meteo attuale per Milano Malpensa (LIMC)"
   ```

Se tutto funziona, dovresti ricevere dati meteorologici in tempo reale!

## Risoluzione Problemi

### ❌ Errore: "Server exited before responding"
- **Causa:** Il server non è avviato
- **Soluzione:** Esegui `./start.sh` nella cartella aviation-weather-mcp-server

### ❌ Errore: "Connection failed"
- **Causa:** Porta sbagliata nel settings.json
- **Soluzione:** Verifica che l'URL sia `http://localhost:8003/sse`

### ❌ Il server si avvia ma VS Code non lo vede
- **Causa:** settings.json non aggiornato correttamente
- **Soluzione:** Controlla la sintassi JSON e riavvia VS Code

## Come Iniziare

Dopo aver completato la configurazione:

1. **✅ Server avviato** con `./start.sh`
2. **✅ settings.json configurato** con aviation-weather
3. **✅ VS Code riavviato**
4. **🚀 Pronto per volare!** - Fai le tue domande meteorologiche

---

*Nota: Questo server è perfetto per scopi educativi, hobby, e pianificazione generale. Per operazioni di volo reali, consulta sempre le fonti ufficiali e segui le procedure appropriate.*

## Link Utili

- 🌐 [aviationweather.gov](https://aviationweather.gov) - Sito ufficiale
- 📚 [Guida ai METAR](https://aviationweather.gov/metar/help) - Come leggere i dati METAR
- 📖 [Guida ai TAF](https://aviationweather.gov/taf/help) - Come interpretare le previsioni

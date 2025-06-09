# Come Funziona il Server MCP Aviation Weather

## Introduzione

Questo documento spiega in dettaglio come funziona il server MCP (Model Context Protocol) per i dati meteorologici dell'aviazione. Il server permette di accedere alle API di aviationweather.gov attraverso un'interfaccia standardizzata MCP.

## Architettura del Sistema

### 1. Struttura dei File

```
src/aviation_weather_mcp/
├── __main__.py      # Entry point dell'applicazione
├── server.py        # Server MCP con tutte le funzioni/tool
├── client.py        # Client HTTP per le API aviationweather.gov
└── exceptions.py    # Classi per la gestione degli errori
```

### 2. Componenti Principali

#### FastMCP
Il sistema utilizza **FastMCP**, una libreria Python che implementa il protocollo MCP. MCP è uno standard che permette ai modelli di AI di comunicare con server esterni per ottenere dati o eseguire azioni.

#### HTTP Client
Il client HTTP asincrono (basato su `httpx`) gestisce tutte le comunicazioni con le API di aviationweather.gov.

## Analisi del Codice

### 1. Entry Point (`__main__.py`)

```python
import asyncio
import typer
import os

from .server import run_sse, run_stdio

app = typer.Typer(help="Aviation Weather MCP Server")
```

Questo file usa **Typer** per creare un'interfaccia a linea di comando. Offre due modalità:

- **SSE Mode** (Server-Sent Events): Per VS Code e client web
- **STDIO Mode**: Per comunicazioni dirette via standard input/output

**Come funziona:**
1. L'utente esegue il comando con modalità desiderata
2. Il sistema configura le variabili d'ambiente per host/porta
3. Avvia il server nella modalità scelta

### 2. Server MCP (`server.py`)

Il cuore del sistema è il server MCP che espone 14 "tool" (funzioni) diverse:

```python
from mcp.server.fastmcp import FastMCP
app = FastMCP("Aviation Weather MCP Server")
```

#### Pattern dei Tool

Ogni tool segue questo pattern:

```python
@app.tool()
async def get_metar(
    ids: str = "",
    format: str = "json",
    # ... altri parametri
) -> str:
    """Documentazione del tool"""
    try:
        client = await get_client()
        result = await client.get_metar(parametri...)
        return json.dumps(result) if isinstance(result, (dict, list)) else str(result)
    except Exception as e:
        logger.error(f"Error getting METAR: {e}")
        raise AviationWeatherError(f"Failed to get METAR data: {e}")
```

**Spiegazione del Pattern:**

1. **Decoratore `@app.tool()`**: Registra la funzione come tool MCP
2. **Parametri tipizzati**: Python usa type hints per validazione
3. **Gestione asincrona**: `async/await` per non bloccare il server
4. **Client singleton**: Un'unica istanza del client HTTP riutilizzata
5. **Gestione errori**: Try/catch con logging e eccezioni custom
6. **Serializzazione**: Converte oggetti Python in stringhe JSON

#### Tool Disponibili

1. **get_metar**: Osservazioni meteorologiche correnti
2. **get_taf**: Previsioni aeroportuali
3. **get_pirep**: Rapporti piloti
4. **get_sigmet/get_isigmet**: Avvisi meteorologici significativi
5. **get_gairmet**: Avvisi grafici
6. **get_cwa**: Avvisi centri meteorologici
7. **get_wind_temp**: Dati vento e temperatura in quota
8. **get_station_info**: Informazioni stazioni meteorologiche
9. **get_airport_info**: Informazioni aeroporti
10. **get_navaid_info**: Informazioni aiuti alla navigazione
11. **get_fix_info**: Informazioni punti di navigazione

### 3. Client HTTP (`client.py`)

Il client gestisce tutte le comunicazioni con l'API esterna:

```python
class AviationWeatherClient:
    BASE_URL = "https://aviationweather.gov/api/data"
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
```

#### Metodo Core: `_make_request`

```python
async def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Any:
    url = f"{self.BASE_URL}/{endpoint}"
    
    # Rimuove parametri None
    clean_params = {k: v for k, v in params.items() if v is not None}
    
    try:
        response = await self.client.get(url, params=clean_params)
        response.raise_for_status()
        
        # Restituisce JSON o testo basato su content-type
        content_type = response.headers.get('content-type', '')
        if 'application/json' in content_type:
            return response.json()
        else:
            return response.text
    except httpx.TimeoutException:
        raise NetworkError(f"Request to {url} timed out")
    # ... altri catch
```

**Cosa fa questo metodo:**

1. **Costruisce URL**: Combina base URL con endpoint specifico
2. **Pulisce parametri**: Rimuove valori None per non inviare parametri vuoti
3. **Fa richiesta HTTP**: GET asincrona con timeout di 30 secondi
4. **Gestisce risposta**: Auto-parsing JSON o ritorna testo grezzo
5. **Gestisce errori**: Converte eccezioni HTTP in eccezioni custom

#### Metodi Specifici

Ogni API endpoint ha il suo metodo:

```python
async def get_metar(self, ids=None, format="json", taf=False, ...):
    params = {"ids": ids, "format": format, "taf": taf, ...}
    return await self._make_request("metar", params)
```

Questo pattern evita duplicazione di codice e centralizza la logica HTTP.

### 4. Gestione Errori (`exceptions.py`)

Sistema gerarchico di eccezioni:

```python
class AviationWeatherError(Exception):
    """Base exception per tutte le operazioni"""

class APIError(AviationWeatherError):
    """Errori dalle API aviationweather.gov"""

class ValidationError(AviationWeatherError):
    """Errori di validazione parametri"""

class NetworkError(AviationWeatherError):
    """Errori di rete/connessione"""
```

Questo permette di:
- Catturare errori specifici per tipo
- Fornire messaggi d'errore informativi
- Gestire diversi tipi di fallimento appropriatamente

## Flusso di Esecuzione

### Scenario Tipico: Richiesta METAR

1. **Client MCP** (es. VS Code) invia richiesta tool "get_metar"
2. **Server MCP** riceve richiesta e valida parametri
3. **Server** chiama `get_client()` per ottenere istanza HTTP client
4. **Client HTTP** costruisce URL e parametri per API aviationweather.gov
5. **Client HTTP** fa richiesta GET asincrona
6. **API Externa** risponde con dati METAR
7. **Client HTTP** parsea risposta (JSON/testo)
8. **Server MCP** serializza risultato in stringa
9. **Client MCP** riceve risposta finale

### Diagramma del Flusso

```
[Client MCP] → [Server MCP] → [HTTP Client] → [aviationweather.gov]
     ↑                                              ↓
     └── [Risposta JSON] ← [Serializzazione] ← [Parsing JSON]
```

## Configurazione e Deployment

### Variabili d'Ambiente

- `FASTMCP_HOST`: Host del server (default: 127.0.0.1)
- `FASTMCP_PORT`: Porta del server (default: 8003)

### Modalità di Esecuzione

#### SSE Mode (Raccomandato per VS Code)
```bash
aviation-weather-mcp-server sse --port 9000
```

#### STDIO Mode (Per integrazione diretta)
```bash
aviation-weather-mcp-server stdio
```

## Punti di Forza del Design

### 1. Separazione delle Responsabilità
- **Server**: Gestisce protocollo MCP e orchestrazione
- **Client**: Gestisce comunicazioni HTTP
- **Exceptions**: Centralizza gestione errori

### 2. Programmazione Asincrona
- Non blocca su richieste HTTP lunghe
- Può gestire multiple richieste concorrenti
- Performance migliori per I/O bound operations

### 3. Gestione Robusta degli Errori
- Timeout configurabili
- Retry logic implicita
- Logging dettagliato per debugging

### 4. Configurabilità
- Parametri via command line o environment
- Format di output multipli (JSON, XML, raw)
- Filtri geografici e temporali

## Possibili Miglioramenti

1. **Cache**: Implementare cache per richieste frequenti
2. **Rate Limiting**: Protezione contro troppe richieste
3. **Configurazione**: File di configurazione per settings avanzate
4. **Monitoring**: Metriche su performance e utilizzo
5. **Authentication**: Se necessaria per API future

## Debugging e Troubleshooting

### Log Files
Il server scrive log in `aviation-weather-mcp.log` con:
- Timestamp delle richieste
- URL e parametri chiamati
- Errori e stack traces
- Informazioni di startup/shutdown

### Errori Comuni

1. **Timeout**: API aviationweather.gov lenta/irraggiungibile
2. **404**: Endpoint API cambiato
3. **400**: Parametri non validi
4. **Rate limiting**: Troppe richieste simultanee

### Testing
Il file `test_client.py` fornisce esempi di utilizzo per testare ogni endpoint.

## Conclusione

Questo server MCP è un esempio eccellente di come creare un bridge tra API esterne e l'ecosistema MCP. Il design modulare, la gestione degli errori robusta e l'approccio asincrono lo rendono scalabile e maintainabile.

La separazione tra logica MCP (server.py) e logica HTTP (client.py) permette facile testing e modifiche future, mentre il sistema di eccezioni custom facilita il debugging in produzione.

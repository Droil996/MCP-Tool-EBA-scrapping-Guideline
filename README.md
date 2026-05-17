# EBA MCP Simple

---

## Obiettivo del progetto

Server MCP didattico in Python per il monitoraggio delle pubblicazioni regolamentari da parte dell'EBA (European Banking Authority). Il need funzionale dietro la soluzione è di dotare gli utenti di un intermediario finanziario di uno strumento di Generative capace di :

1. Collegarsi direttamente alle pubblicazioni recenti dell'EBA;
2. Permettere un download diretto delle ultime pubblicazioni;
3. Ricevere un first-Look Assessment della GL pubblicata, con uno scoring in Rosso, Giallo, Verde della rilevanza per l'intermediario.
4. Storicizzare le valutazioni svolte dall'agent.

Sotto il profilo tehc, La soluzione è basata sull'impieto del protocollo MCP e dell'Agent di Antigravity, a cui è espesto un paniere di primitive bucketizzabili in:

- **Tools**: azioni operative invocabili dal modello o dal client MCP;
- **Resources**: dati contestuali disponibili per l'analisi;
- **Prompts**: template controllati dall'utente per guidare l'Agent/LLM.



## Architettura

```text
MCP Client / Agent
        ↓
FastMCP Server
        ↓
Tools / Resources / Prompts
        ↓
EBA website + repository locale
```

Struttura principale:

```text
eba_mcp_simple/
├── __init__.py
├── __main__.py
├── server.py
├── mcp_instance.py
├── mcp_tools.py
├── mcp_resources.py
├── mcp_prompt.py
├── models.py
├── utils.py
└── config.py

repository/
├── metadata/
│   ├── eba_publications.json
│   └── assessments.json
└── pdf/
```

---

## Primitive MCP esposte

### Tools

|       Tool                  | Descrizione                                               |
| `fetch_eba_publications`    | Recupera le pubblicazioni EBA e salva i metadata locali   |
| `download_eba_pdfs`         | Scarica i PDF associati alle pubblicazioni già recuperate |
| `extract_pdf_preview`       | Estrae una preview testuale dai PDF scaricati             |
| `save_guideline_assessment` | Salva un assessment prodotto dall'Agent/LLM               |
| `get_guideline_assessments` | Restituisce gli assessment salvati                        |

---

### Resources

| Resource                     | Descrizione                                              |

| `eba://taxonomy`             | Tassonomia regolamentare semplificata                    |
| `eba://classification/rules` | Regole di classificazione semplificate Alto/Medio/Basso  |

---

### Prompts

| Prompt                       | Descrizione                                                              |
| `analizza_guideline`         | Prompt per analizzare una guideline EBA partendo da titolo e preview PDF |
| `spiega_impatto`             | Prompt per spiegare in modo semplice una classificazione di impatto                  |

---

## Classificazione dell'impatto

Il progetto usa tre livelli:

| Impatto | Colore | Significato                                                                          |
| Alto    | Rosso  | Possibili obblighi regolamentari, impatti operativi, reporting, capitale, compliance |
| Medio   | Giallo | Documento da monitorare o valutare internamente                                      |
| Basso   | Verde  | Materiale prevalentemente informativo                                                |

La classificazione viene generata dall'Agent/LLM usando:

- preview del PDF;
- risorsa `eba://classification/rules`;
- risorsa `eba://taxonomy`;
- prompt `analizza_guideline`.

---

## Installazione


Con `uv`:

```bash
uv sync
```

## Avvio server

```bash
uv run eba-mcp-simple --port 8001
```

Oppure:

```bash
python -m eba_mcp_simple --port 8001
```

Endpoint MCP:

```text
http://localhost:8001/mcp/
```

Health check:

```text
http://localhost:8001/health
```

---

## Esempio di flusso operativo

1. Il client MCP chiama:

```text
fetch_eba_publications
```

2. Il client MCP chiama:

```text
download_eba_pdfs
```

3. Il client MCP chiama:

```text
extract_pdf_preview
```

4. L'Agent usa il prompt:

```text
analizza_guideline
```

insieme alle resources:

```text
eba://classification/rules
eba://taxonomy
```

5. L'Agent produce un JSON compatibile con `GuidelineAssessment`.

6. Il client MCP salva l'output con:

```text
save_guideline_assessment
```

7. Gli assessment salvati possono essere riletti con:

```text
get_guideline_assessments
```

---


## DEMO

Ai fini di una demo, si consiglia di procedere nel seguente modo:

1. Richiesta recupero ultime Guideline (documenti tecnici dell'EBA)
2. Richiesta download ultimi PDF (documenti tecnici dell'EBA) recuperati al punto 1
3. Richiesta di valutazione delle GL in acccordo a Prompt e REsourse già disponibili
4. Possibilita di salvare gli assessment prodotti dall'Agent/LLM
5. Possibilita di rileggere gli assessment salvati. 
6. Possibilità di explain dell'assessment scelto.

## Persistenza locale

Il server usa una cartella locale `repository/`.

I metadata vengono salvati in:

```text
repository/metadata/eba_publications.json
```

Gli assessment vengono salvati in:

```text
repository/metadata/assessments.json
```

I PDF vengono salvati in:

```text
repository/pdf/
```

---

## Limiti noti

- Lo scraping dipende dalla struttura HTML della pagina EBA.
- L'analisi completa dei PDF non viene eseguita automaticamente.
- La preview è limitata alle prime pagine del documento.
- La classificazione dipende dall'Agent/LLM che invoca il prompt MCP.
---

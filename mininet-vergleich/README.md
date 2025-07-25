# Mininet Vergleich Projekt

Dieses Projekt führt Netzwerkexperimente mit Mininet durch, um den Durchsatz, die Latenz und den Paketverlust von TCP- und UDP-Datenströmen zu messen. Es vergleicht auch die Leistung von TCP mit DCTCP (Data Center TCP).

## Projektstruktur

- `src/experiments.py`: Hauptskript zur Durchführung von Experimenten in Mininet. Implementiert die Logik zur Messung von Durchsatz, Latenz und Paketverlust für TCP- und UDP-Datenströme. Ergebnisse werden über iperf erfasst.
  
- `src/dctcp_experiments.py`: Führt Experimente durch, die den Vergleich zwischen TCP und DCTCP beinhalten. Misst ebenfalls Durchsatz, Latenz und Paketverlust und verwendet iperf zur Datenerfassung.

- `src/topologies/basic_topology.py`: Definiert die Topologie für das Mininet-Setup. Erstellt eine Netzwerktopologie mit vier Servern und einem Router, die für die Experimente benötigt wird.

- `src/types/index.py`: Enthält Typdefinitionen und möglicherweise benutzerdefinierte Datentypen, die in den Experimenten verwendet werden. Könnte Klassen oder Funktionen zur Handhabung von Ergebnissen oder zur Konfiguration der Experimente exportieren.

- `requirements.txt`: Listet die Python-Abhängigkeiten auf, die für das Projekt benötigt werden, einschließlich Mininet und iperf.

## Installation

Um das Projekt auszuführen, stellen Sie sicher, dass Sie die erforderlichen Abhängigkeiten installiert haben. Führen Sie den folgenden Befehl aus:

```
pip install -r requirements.txt
```

## Ausführung der Experimente

Um die Experimente durchzuführen, verwenden Sie die folgenden Befehle:

- Für TCP- und UDP-Experimente:
  ```
  python src/experiments.py
  ```

- Für DCTCP-Experimente:
  ```
  python src/dctcp_experiments.py
  ```

## Automatisierte Experimente und Plotten

Um für verschiedene UDP-Bandbreiten die Latenz und den Durchsatz von TCP und DCTCP zu messen und zu vergleichen, gehen Sie wie folgt vor:

1. Führen Sie die Experimente für alle gewünschten UDP-Bandbreiten durch:
   ```
   python src/experiments.py --all
   python src/dctcp_experiments.py --all
   ```

   *(Die Option `--all` sorgt dafür, dass für eine feste Menge an UDP-Bandbreiten die Messungen automatisiert durchgeführt werden. Passen Sie dies ggf. an Ihre Implementierung an.)*

2. Plotten Sie die Ergebnisse:
   ```
   python src/plot_results.py
   ```

   *(Das Skript `plot_results.py` liest die gespeicherten Messdaten und erstellt Vergleichsplots für Latenz und Durchsatz von TCP und DCTCP in Abhängigkeit von der UDP-Bandbreite.)*

Die Plots werden im Ordner `plots/` gespeichert.

## Ergebnisse

Die Ergebnisse der Experimente werden in den entsprechenden Verzeichnissen gespeichert. Sie können die Ergebnisse analysieren, um die Leistung von TCP und DCTCP zu vergleichen und die Auswirkungen von Latenz und Paketverlust zu verstehen.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.
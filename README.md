# Scheduler für Stundenplanbenachrichtigungen
Dieses Projekt ermöglicht es, den Stundenplan ander Universität Leipzig abzurufen und Benachrichtigungen über Telegram zu erhalten. Jeden Sonntag sendet der Telegram-Bot den Stundenplan der nächsten Woche um 12 Uhr

## Inhaltsverzeichnis
1. [Einleitung](#einleitung)
2. [Funktionsweise](#funktionsweise)
3. [Verwendung](#verwendung)
4. [Konfiguration](#konfiguration)
5. [Installation](#installation)
6. [Beitragen](#beitragen)
7. [Lizenz](#lizenz)

## Einleitung
Falls man sich - wie ich - nicht merken kann, wann und wo man Unterricht hat, kann es nützlich sein, den Stundenplan regelmäßig zugesendet zu bekommen. Dieses Scheduler-Tool wurde entwickelt, damit ich meine schöne Lebenszeit nicht damit verbringen muss, jeden Tag AlmaWeb zu öffnen. 

## Funktionsweise
Das System verwendet einen Flask-Server als Proxy, um zwischen dem Skript und der AlmaWeb-Plattform zu vermitteln. Dies ermöglicht es, das von AlmaWeb erzwungene CORS zu umgehen und eine reibungslose Kommunikation zu gewährleisten. Der Ablauf des Systems ist wie folgt:

Authentifizierung und Anfrage: Das Skript führt jeden Sonntag eine Authentifizierung auf der AlmaWeb-Plattform durch und fragt den Wochenplans für den folgenden Tag ab.
Datenverarbeitung: Die empfangenen Daten werden analysiert und die relevanten Informationen extrahiert. Dazu gehört die Aufbereitung des Stundenplans für eine benutzerfreundliche Darstellung.
Benachrichtigung: Die aufbereiteten Daten werden dann per Bot an einen benutzerdefinierten Chat gesendet. Dies ermöglicht es den Benutzern, den Wochenplan bequem und zeitnah zu erhalten.
Durch diese Prozesse bietet das System eine effiziente und zuverlässige Möglichkeit, den Stundenplan abzurufen und Benachrichtigungen über Telegram zu erhalten.

## Verwendung
Um den Scheduler zu verwenden, müssen Sie die Konfiguration entsprechend anpassen und das Hauptskript ausführen. Der Scheduler ruft den Stundenplan automatisch ab und sendet Benachrichtigungen über Telegram.

## Konfiguration
Die Konfiguration erfolgt über Umgebungsvariablen, die in einer .env-Datei bereitgestellt werden. Folgende Variablen müssen konfiguriert werden:

ALMAWEB_USERNAME: Benutzername für den Zugriff auf die AlmaWeb-Plattform.
ALMAWEB_PASSWORD: Passwort für den Zugriff auf die AlmaWeb-Plattform.
TELEGRAM_BOT_TOKEN: Token für den Zugriff auf den Telegram-Bot.
TELEGRAM_CHAT_ID: Chat-ID des Telegram-Chats, an den Benachrichtigungen gesendet werden sollen.

## Installation
Um das Projekt lokal auszuführen, müssen Sie die folgenden Schritte ausführen:

Klonen Sie das Repository: git clone https://github.com/MrMxffin/uni_leipzig_scheduler.git
Wechseln Sie in das Verzeichnis: cd uni_leipzig_scheduler
Installieren Sie die Abhängigkeiten: pip install -r requirements.txt
Erstellen Sie eine .env-Datei und konfigurieren Sie die erforderlichen Umgebungsvariablen.
Führen Sie das Hauptskript aus: python main.py

## Beitragen
Beiträge sind immer willkommen! Wenn Sie Verbesserungen vornehmen möchten, öffnen Sie bitte ein Issue oder senden Sie eine Pull-Anfrage.

## Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Informationen finden Sie in der [Lizenzdatei](./LICENSE).

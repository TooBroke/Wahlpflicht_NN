Inhalt:
0. Erklärung der Dateien
1. Das Spiel
2. Verwendung des GUI
3. Dependencies des Neuronalen Netzwerks
4. Trainieren des Neuronalen Netzwerks
5. Anweisung zum Testen des Neuronalen Netzwerks
6. Anmerkung

0. Erklärung der Dateien
- GAMELOGIC.py:
- GAMEMODEL.py:
- NN_GENETIC.py: Trainingsprogramm zum Trainieren der Gewichtungen des Neuronalen Netzwerks.
- NN_GENETIC_FOR_GUI.py:
- population.pkl: Pickle-Datei, welche die aktuelle Population beinhaltet.
- best_individual.pkl: Pickle-Datei, welche die besten Gewichtungen des Neuronalen Netzwerks beinhaltet.

1. Das Spiel

2. Verwendung des GUI

3. Dependencies des Neuronalen Netzwerks:
- wxPython 4.0.0a2: https://wxpython.org/
- Numpy 1.11.3+mkl cp27: http://www.lfd.uci.edu/~gohlke/pythonlibs/
- Scipy 0.19.0 cp27: http://www.lfd.uci.edu/~gohlke/pythonlibs/
- Pybrain 0.3: https://github.com/pybrain/pybrain/wiki/installation

4. Trainieren des Neuronalen Netzwerks
4.1 Training starten
Um das Trainieren des Neuronalen Netzwerks zu starten muss das Trainingsprogramm "NN_GENETIC.py" ausgeführt werden.
Zuerst sucht das Programm nach einer vorhandenen Population (population.pkl). Wenn keine Population vorhanden ist
wird eine neue generiert. Nachdem eine Population ausgewählt wurde, wird der Benutzer nach der Eingabe einer Anzahl
der zu trainierenden Generationen gefragt. Danach trainiert das Programm die vorhandene Population und speichert diese
nach jeder neuen Generation in der Pickle-Datei "population.pkl". Daraufhin wird überprüft ob die neue Population ein
Individuum enthält, welches einen besseren Fitnesswert als das in der Pickle-Datei "best_individual.pkl" gespeicherte
Individuum aufweist. Ist dies der Fall wird das Individuum gespeichert.

4.2 Neue Popopulation generieren
Beim starten des Trainingsprogramms "NN_GENETIC.py" wird nach einer bereits vorhandenen Population gesucht.
Wenn keine Population vorhanden ist, also keine "population.pkl" Datei gefunden wird, generiert das Programm
eine neue Population und speichert diese in einer Datei "population.pkl". Um eine neue Population zu generieren
muss also die vorhandene "population.pkl" Datei entweder umbenannt oder gelöscht werden.

5. Anweisung zum Testen des Neuronalen Netzwerks


6. Anmerkung
<ANDERE AUSPROBIERT>
Das Trainieren des Neuronalen Netzwerks funktioniert, jedoch ist es aufgrund der Fitnessfunktion sehr langsam. Um die
Fitness eines Individuums zu berechnen muss das Spiel sehr oft gespielt werden. Das Netzwerk haben wir mit 50
Spieldurchläufen pro Individuum trainiert, aufgrund der Zufälligkeit des Spiels sind selbst 50 zu wenig.
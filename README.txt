##############################################################################################
Inhalt
##############################################################################################
0. Erklärung der Dateien
1. Das Spiel
2. Verwendung des GUI
3. Dependencies des Neuronalen Netzwerks
4. Trainieren des Neuronalen Netzwerks
5. Anweisung zum Testen des Neuronalen Netzwerks
6. Vorgehen
7. Anmerkung

##############################################################################################
0. Erklärung der Dateien
##############################################################################################
GAMELOGIC.py                Die Logik des Spiels.

GAMEMODEL.py                Modellklassen und Datentypen für das Spiel.

NN_GENETIC.py               Trainingsprogramm zum Trainieren der Gewichtungen 
                            des Neuronalen Netzwerks.

NN_GENETIC_FOR_GUI.py       Funktionen aus NN_GENETIC.py, um das Netzwerk in dem 
                            GUI spielen zu lassen.

GUI.py                      Eine grafishe Oberfläche und KI-Optionen für das Spiel.

population.pkl              Pickle-Datei, welche die aktuelle Population beinhaltet.

best_individual.pkl         Pickle-Datei, welche die besten Gewichtungen des 
                            Neuronalen Netzwerks beinhaltet.

best_individual_gui.pkl     Pickle-Datei, welche vortrainierte Gewichtungen enthält.

##############################################################################################
1. Das Spiel
##############################################################################################
2048 ist ein rundenbasiertes Highscorespiel. Das Spielfeld startet mit zwei Zahlen und pro 
Runde kann eine Richtung gewählt werden. Alle Elemente des Spielfeldes bewegen sich dann in 
diese Richtung und sollten dabei 2 gleiche Zahlen aufeinander treffen, werden diese addiert.

Alle Zahlen auf dem Spielfeld sind 2er Potenzen, da jede Runde eine neue Zahl zufällig 
erscheint, die eine 2 oder eine 4 sein kann. Ziel ist es den höchstmöglichen Score zu 
erreichen, welcher bei dem Addieren zweier Zahlen erhöht wird. Die Zahl 2048 zu erreichen 
ist meist nicht einfach und somit das sekundäre Ziel neben dem Highscore. Es ist dennoch 
möglich größere Zahlen zu kombinieren mit einem theoretischen Maximum von 131072.

##############################################################################################
2. Verwendung des GUI
##############################################################################################
Das GUI kann benutzt werden, um selbst zu spielen, eine vordefinierte AI oder 
ein Neuronales Netz spielen zu lassen.
----------------------------------------------------------------------------------------------
Steuerung (Tastatur)
----------------------------------------------------------------------------------------------
    W - Spielfeld nach oben bewegen
    A - Spielfeld nach links bewegen
    S - Spielfeld nach unten bewegen
    D - Spielfeld nach rechts bewegen
    R - Spiel neustarten
----------------------------------------------------------------------------------------------
Erklärung der Buttons
----------------------------------------------------------------------------------------------
    Scorefeld:  Anzeige des Scores, der Fehler (ein Fehler ist ein Spielzug in eine Richtung, 
                in der sich das Spielfeld nicht ändert) und ob das Spiel gerade läuft. 
                Zusätzlich wenn eine KI spielt werden noch die Anzahl der Spiele ausgegeben 
                und der durchschnittliche Score.
    
    AiSpeed:    Zeit in ms, die die KI zwischen ihren Zügen warten soll
    
    AI:         Auswahlfeld der KIs. (testAI : nimmt immer die untere Richtung, 
                                      randomAI : nimmt eine zufällige Richtung,
                                      simpleAI : ein simpler Greedy-Algorithmus,
                                      geneticNN : Ein neuronales Netz, dessen Gewichtungen 
                                      in der Datei "best_individual_gui.pkl" gespeichert sind)
    
    Runs:       Anzahl an Spielen, die die KI spielen soll (0 = unendlich)
    
    Run AI:     Startet die KI mit den momentanen Einstellungen
    
    Stop AI:    Stoppt die KI, wenn gerade eine läuft
    
    Restart:    Beginnt ein neues Spiel. Stoppt die KI, wenn gerade eine läuft                        

##############################################################################################
3. Dependencies des Neuronalen Netzwerks und des GUI
##############################################################################################
Python 2.7              https://www.python.org/downloads/

wxPython 4.0.0a2        https://wxpython.org/download.php#msw

Numpy 1.11.3+mkl cp27   http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

Scipy 0.19.0 cp27       http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy

Pybrain 0.3             https://github.com/pybrain/pybrain

##############################################################################################
4. Trainieren des Neuronalen Netzwerks
##############################################################################################
4.1 Training starten
----------------------------------------------------------------------------------------------
Um das Trainieren des Neuronalen Netzwerks zu starten muss das Trainingsprogramm 
"NN_GENETIC.py" ausgeführt werden. Zuerst sucht das Programm nach einer vorhandenen Population 
(population.pkl). Wenn keine Population vorhanden ist, wird eine neue generiert. Nachdem eine 
Population ausgewählt wurde, wird der Benutzer nach der Eingabe einer Anzahl der zu 
trainierenden Generationen gefragt. Danach trainiert das Programm die vorhandene Population 
und speichert diese nach jeder neuen Generation in der Pickle-Datei "population.pkl". 
Daraufhin wird überprüft ob die neue Population ein Individuum enthält, welches einen besseren 
Fitnesswert als das in der Pickle-Datei "best_individual.pkl" gespeicherte Individuum aufweist. 
Ist dies der Fall wird das Individuum gespeichert.
----------------------------------------------------------------------------------------------
4.2 Neue Popopulation generieren
----------------------------------------------------------------------------------------------
Beim starten des Trainingsprogramms "NN_GENETIC.py" wird nach einer bereits vorhandenen 
Population gesucht. Wenn keine Population vorhanden ist, also keine "population.pkl" Datei 
gefunden wird, generiert das Programm eine neue Population und speichert diese in einer Datei 
"population.pkl". Um eine neue Population zu generieren muss also die vorhandene 
"population.pkl" Datei entweder umbenannt oder gelöscht werden.

##############################################################################################
5. Anweisung zum Testen des Neuronalen Netzwerks
##############################################################################################
Um ein trainiertes Netz zu testen, muss man die Datei "best_individual.pkl", die
beim trainieren erzeugt wurde und die besten Gewichtungen enthält in "best_individual_gui.pkl"
umbenennen. Startet man nun das GUI, wählt als AI "geneticNN" aus und drückt auf "Run AI", 
werden die Gewichtungen automatisch geladen und ohne weitere Einstellungen werden 
unendlich Spiele mit dem neuronalen Netz gespielt und oben rechts ist der average score
zu sehen.

##############################################################################################
6. Vorgehen
##############################################################################################
Für die Lösung des Problems haben wir mehrere Trainingsmethoden für Neuronale Netze probiert.

Backpropagation             Wurde zunächst verworfen, da es unter den Bereich Supervised 
                            Learning fällt und es bei einem Highscorespiel mit viel Zufall 
                            schwer ist den besten möglichen Zug ermitteln. Später wurde eine 
                            Variante versucht, bei der Wert für den bestmöglichen Zug durch 
                            den Errorwert der Temporal Difference ersetzt wurde. Dies führte 
                            zu keinem Erfolg.
                    
Reinforcement Learning      Reinforcement Learning sollte sich eigentlich ganz gut für 2048 
                            eignen. Da es Probleme mit PyBrain für die Nutzung von RL gab, 
                            haben wir versucht ein eigenes Netz zu schreiben und dies zu 
                            trainieren. Das Training beruhte zunächst darauf, dass das Netz 
                            für Score in einem Zug belohnt wurde und für Fehler (ein Zug bei 
                            dem das Spiefeld sich nicht ändert) bestraft. Dies führte jedoch 
                            zu keinem ersichtlichen Erfolg, was sowohl am Training als auch 
                            an dem implementierten Netz gelegen haben könnte.
                        
Genetischer  Algorithmus    Beim Genetischen Algorithmus zum Trainieren des Netzes haben wir 
(Evolutionärer)             PyBrain genutzt, um das Netz zu konstruieren. Dies besteht aus 
                            einem linearen InputLayer mit 16 Knoten, 2 hidden SigmoidLayer mit 
                            20 Knoten und einem SigmoidLayer für den Output. Die beiden Output-
                            neuronen werden durch eine rectify Methode in 0 oder 1 gewandelt. 
                            Diese können zusammen als Binärzahl interpretiert werden und stel-
                            len somit die 4 Richtungen des Spiels dar. Als Input wird das 
                            Spielfeld als eindimensionales Array übergeben.
                            Beim Trainieren des Netzes haben wir eine Population von 50 
                            gewählt und die Fitness eines Netzes wird durch den Durchschnitts-
                            score nach 50 Spielen ermittelt. Beim Trainieren erkennt man, 
                            dass die Population sehr langsam besser wird. Um wirklich gute 
                            Ergebnisse zu erzielen, müssten in der Fitnessfunktion ca. 1000 
                            Spiele gespielt werden und eine Population von 100.000+ wäre 
                            bestimmt auch besser. Zeitlich war es uns aber nicht möglich das 
                            zu testen.
                            
##############################################################################################
7. Anmerkungen
##############################################################################################
Die Datei "best_individual_gui.pkl" enthält vortrainierte Gewichtungen nach ca. 1800 
Generationen. Das Trainieren hat ca. 17 Stunden gedauert und das Netz kommt mit den 
Gewichtungen auf einen Durchschnittsscore von ca. 220. 
Dies kann auch direkt in dem GUI getestet werden.

Github Repo: https://github.com/TooBroke/Wahlpflicht_NN



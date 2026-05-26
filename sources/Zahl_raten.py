geheime_zahl= 40
moegliche_versuche = 3

while moegliche_versuche > 0:
    # Regel 1 + 2
    print('Errate die Zahl zwischen 1 und 100 \nDu hast ', str(moegliche_versuche) + ' Versuche')
    eingabe = input('Deine Eingabe:')

    try:
        geratene_zahl = int(eingabe)
        # Regel 1
        if geratene_zahl > 100:
            print('Die Zahl liegt doch unter 100!')
            continue
        # Regel 3
        if geratene_zahl > geheime_zahl:
            print('Zu hoch! Versuch\'s nochmal!')
            moegliche_versuche-=1
        # Regel 4
        elif geratene_zahl < geheime_zahl:
             print('Zu niedrig! Versuch\'s nochmal!')
             moegliche_versuche-=1
        # Regel 5
        else:
            print('Richtig geraten!')
    # Regel 7
    except ValueError:
        print('Ganz vergessen.. nur gerade Zahlen bitte!')
        moegliche_versuche-=1
# Regel 6
print('Du hattest drei Versuche und hast die Zahl leider nicht erraten :( Die gesuchte Zahl war', geheime_zahl)
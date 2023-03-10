# Systemy wspomagania decyzji

## Moduł 1:

Zaimplementuj (system będzie modułowy - kolejne moduły na kolejnych zajęciach):

- wczytywanie danych w formacie tekstowym (dane oddzielone spacją, tabulatorem, średnikiem; w pliku same dane bez liczby wierszy lub kolumn; dane mogą być tekstowe lub numeryczne), mogą posiadać wiersz nagłówkowy z nazwami kolumn; każdą linię zaczynającą się od znaku # należy zignorować (komentarz);
    - zadeklarować w sprawozdaniu czym rozdzielamy
    - dane wyświetlamy w tabeli i umożliwiamy edycję
    - można narzucić jaki format daty (ogólnie można narzucać różne rzeczy, byle w sprawozdaniu było opisane)
- dla chętnych wczytywanie danych z Excela lub bezpośrednie przeklejanie danych z Excela do arkusza z danymi w programie;
- zamiana danych tekstowych na numeryczne (np. klasa1, klasa2, klasa3 zmieniane na kolejne liczby całkowite 1,2,3 - np. wg kolejności alfabetycznej lub kolejności wystąpienia);
- dyskretyzacja zmiennych rzeczywistych na określoną liczbę przedziałów;
    - od nas zależy jak domykamy przedziały czy z lewej czy prawej - w sytuacji brzegowej, później algorytmy budujące drzewa mogą to inaczej przypisać
- standaryzacja zmiennych rzeczywistych ( (wartość-średnia)/odchylenie_standardowe);
- zmiana przedziału wartości z oryginalnego <min; max> na przedział, którego zakres wartości poda użytkownik <a; b>
- wyświetlenie/zaznaczenie określonego przez użytkownika procentu najmniejszych i największych wartości zmiennych
- wykres 2D (rozproszeń dwuwymiarowy) - zależność dwóch zmiennych, z możliwością wybrania opcji o zastosowaniu kolorów/znaczników do klas
    - użytkownik wprowadza jaka wartość ma być na osi X i Y
    - jeżeli użytkownik poda klasę, to można za pomocą symbolu oznaczyć jako 3 parametr
    - kolory nie monochromatyczne, unikać żółtego
    - pierwsze pięć kolorów ustawić na stałe (później ma się przydać jak na postawie koloru mamy wziąc klasę)
- wykres 3D
- histogram (zmienna dyskretna, zmienna ciągła - podanie liczby przedziałów)
    - przy rysowaniu histogramu albo narzucamy ile słupków albo użytkownik wprowadza (a my proponujemy)
- dodać zapis i odczyt danych

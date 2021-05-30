# Automat Biletowy MPK

## Ogólne działanie projektu
Po uruchomieniu aplikacji pojawia nam się okienko w którym
dokonujemy wyboru ilości bieltów (wzorowane na to jakie 
znajduje się w MPK tj. bilet i klikamy plusikiem, lub minusem),
gdy wybierzemy conajmniej jeden bilet możemy poprzez przycisk "KUPUJĘ",
przejść do okna płatności.

W tym oknie mamy kolejno monety/banknoty które możemy użyć do zapłacenia za
nasze bilety. W każdym wierszu widzimy:
```
MB   < IWA >   [-]  Ilosc  [+]
```
Jak na przykładzie MB (jaka moneta/banknot), następnie w <> IWA (ilość
w automacie danego MB), przycisk wycofania wrzuconego MB, potem
ilość wrzuconych MB i ostatni przycisk do dorzucenia danego MB.

Mamy tutaj też pole do wprowadzania ilości biletów, które nie pozwala wprowadzać 
znaków innych niż cyfry, w przypadku liczby mniejszej niż 1 liczba 
wprowadzanych biletow jest równa 1 oraz gdy jest wieksza od 999
liczba ta jest ograniczana do 999.

Jeśli po dorzuceniu danej monety kwota płatności jest większa lub równa, 
kosztowi biletów automat odrazu próbuje dokonać płatności i ew. zwrotu MB.

Na samej górze istnieje przycisk do powrotu do okienka z wyborem biletów,
oczywiście po ponownym powrocie do płatności jeśli koszt sumaryczny naszych 
biletów zmniejszył się będzie on odrazu w tym okienku próbował nam wydać resztę.

## Uruchamianie testow
Testy są dokonywane przy pomocy biblioteki **unittest**.

Aby je uruchomić należy w głównym katalogu projektu wykonać następujące polecenie:

```shell
python -m unittest discover -s automat_biletowy_mpk -p *_tests.py
```

Testy które w projekcie zostały zawarte w paragrafie testy znajdują się w pliku tests/automat_biletowy_mpk/main_tests.py

Reszta testów testuje poszczególne pomniejsze działania modułów.

## Odniesienie do pkt 4 
### 4.a Udokumentowanie przypadków użycia zawartych w opisie zadania
#### Brak reszty/moze wydać wyskakuje okienko z informacja o zakupach, wydaje resztę (dolicza wrzucone monety jako reszta), wraca do wyboru biletow
W głównym okienku wybieram bilet ulgowy 60 minutowy za 3,50 zł klikam przycisk KUPUJĘ i wybieram po jednej z kolejno wymienionych
monet: 2 zł, 1 zł, 0.5 zł. Następnie pojawia się okienko które informuje nas o braku reszty.
Wybierając bilet np. za 3.5 zł zobaczymy że doliczyło wpłacone monety do reszty.
#### Nie może wydać: wyskakuje okienko z napisem "Tylko odliczona kwota" oraz zwraca włożone monety
Wybieramy ponownie bilet za 3.5 zł, klikamy KUPUJĘ i tym razem płacimy za 50zł, automat powie nam że nie ma jak wydać danej kwoty.

### 4.b Sprawdzanie danych
Dane wprowadzane są poprzez przyciski, a w punkcie gdzie mamy wprowadzac ilosc biletów jest ograniczenie tylko 
do wprowadzania znaków, a sama liczba jest ograniczona miedzy 1 a 999 nawet jesli wybierzemy 10000.

## Odniesienie do pkt 5
### 5.1 Co sprawiło problemy
Testy dziwnie się importują, na jakimś sstarym poradniku wyczytałem iż powinny znajdować się w tak samo nazwanym katalogu /tests a potem 
w odpowiednio nazwanych katalogach odpowiadającym modułom. Następnie odpowiednią komendą powinny być uruchamiane z głównego katalogu.
Uruchamianie testu pojedynczo nie działa z danego katalogu testowego, gdyż ma problem z powiązaniem importu.

Niektóre testy jednostkowe miały być sprawdzone poprzez "wyskakujące okienko", na konsultacjach ustaliliśmy, że wystarczy łapanie
Exeptiona po którym w kodzie wyświetlamy takie okienko.

Tkinter ma jakiś osobny kanał przechwytywania exeptionów i przez co wyłapywanie błędów w handlerach np. przycisków nie działa w
tradycyjny sposób try/catch trzeba nadpisać metodę w głównym okienku aplikacji. Jest to dla mnie conajmniej dziwne podejście, gdyż 
lambda komendy(w której chciałem łapać error) powinna wykonać się wcześniej niż np. obłożona nią jakaś lambda wewnątrz biblioteki, lub jak to w pythonie działa...

### 5.2 Linki do fragmentów w kodzie
#### Lambdy (3)
- [Przyklad 1](https://github.com/paweldabrowa1/automat_biletowy_mpk/blob/675ae319d6ce6e47bd38ba014674715a790c7539/automat_biletowy_mpk/ticket_machine/ticket_machine_ui.py#L214)
- [Przyklad 2](https://github.com/paweldabrowa1/automat_biletowy_mpk/blob/675ae319d6ce6e47bd38ba014674715a790c7539/automat_biletowy_mpk/ticket_machine/ticket_machine_ui.py#L221)
- [Przyklad 3](https://github.com/paweldabrowa1/automat_biletowy_mpk/blob/2643cff3d2e244a7c619360dd79428d1b867a0e9/automat_biletowy_mpk/runner.py#L23)
#### List comprehension (3)
- [Przyklad 1](https://github.com/paweldabrowa1/automat_biletowy_mpk/blob/2643cff3d2e244a7c619360dd79428d1b867a0e9/automat_biletowy_mpk/runner.py#L23)
- [Przyklad 2](https://github.com/paweldabrowa1/automat_biletowy_mpk/blob/2643cff3d2e244a7c619360dd79428d1b867a0e9/automat_biletowy_mpk/coins/coins.py#L2)
- [Przyklad 3](https://github.com/paweldabrowa1/automat_biletowy_mpk/blob/2643cff3d2e244a7c619360dd79428d1b867a0e9/automat_biletowy_mpk/tests/automat_biletowy_mpk/main_tests.py#L46)
#### Klasy (4)
- [Przyklad 1](https://github.com/paweldabrowa1/automat_biletowy_mpk/blob/2643cff3d2e244a7c619360dd79428d1b867a0e9/automat_biletowy_mpk/coins/coins.py#L5)
- [Przyklad 2](https://github.com/paweldabrowa1/automat_biletowy_mpk/blob/2643cff3d2e244a7c619360dd79428d1b867a0e9/automat_biletowy_mpk/coins/coins_holder.py#L12)
- [Przyklad 3](https://github.com/paweldabrowa1/automat_biletowy_mpk/blob/2643cff3d2e244a7c619360dd79428d1b867a0e9/automat_biletowy_mpk/ticket_machine/ticket.py#L1)
- [Dziedziczenie 1](https://github.com/paweldabrowa1/automat_biletowy_mpk/blob/2643cff3d2e244a7c619360dd79428d1b867a0e9/automat_biletowy_mpk/ticket_machine/ticket_machine.py#L14)
- [Dziedziczenie 2](https://github.com/paweldabrowa1/automat_biletowy_mpk/blob/2643cff3d2e244a7c619360dd79428d1b867a0e9/automat_biletowy_mpk/ticket_machine/ticket_machine.py#L48)
#### Wyjątki (Definicja i rzucanie)
- [Definicja](https://github.com/paweldabrowa1/automat_biletowy_mpk/blob/2643cff3d2e244a7c619360dd79428d1b867a0e9/automat_biletowy_mpk/coins/coins_holder.py#L8)
- [Wyrzucenie](https://github.com/paweldabrowa1/automat_biletowy_mpk/blob/2643cff3d2e244a7c619360dd79428d1b867a0e9/automat_biletowy_mpk/coins/coins_holder.py#L26)
- [Łapanie](https://github.com/paweldabrowa1/automat_biletowy_mpk/blob/2643cff3d2e244a7c619360dd79428d1b867a0e9/automat_biletowy_mpk/tests/automat_biletowy_mpk/main_tests.py#L71)
#### Moduły
- Logika - każdy plik poza plikiem od tkintera
- [UI](https://github.com/paweldabrowa1/automat_biletowy_mpk/blob/2643cff3d2e244a7c619360dd79428d1b867a0e9/automat_biletowy_mpk/ticket_machine/ticket_machine_ui.py#L23)

class Teater:
    """Beskriver en teater, har attributen namn, antal platser, vuxenpris, pensionärspris, barnpris, intäkt, sålda platser och belägg"""

    def __init__(self, namn, platser, vuxen, pensionär, barn, prisintäkt = 0, sålda_platser = 0, belägg = 0):
        """Konstruktorn som anropas när vi skapar en ny teater
        Parametrar: namn, antal platser, vuxenpris, pensionärspris, barnpris, intäkt, sålda platser, belägg
        """
        self.namn = namn
        self.platser = platser
        self.vuxen = vuxen
        self.pensionär = pensionär
        self.barn = barn
        self.prisintäkt = prisintäkt
        self.sålda_platser = sålda_platser
        self.belägg = belägg
    
    def __lt__(self, other):
        """För jämförelser mellan teatrar (används vid sortering). """
        if self.belägg < other.belägg:
            return True
        else:
            return False
          

    def ändra_intäkt(self, platser, prisgrupp, föreställning):
        """adderar intäkten i attributet prisintäkkter
        Parametrar: self, platser, prisgrupp, föreställning
        Returnerar: inget """

        if prisgrupp == "vuxen":
            self.prisintäkt += platser * self.vuxen 
        elif prisgrupp == "pensionär":
            self.prisintäkt += platser * self.pensionär
        elif prisgrupp == "barn":
            self.prisintäkt += platser * self.barn
        else:
            print("Du skrev fel prisgrupp, prova igen")
            föreställning.hantera_sålda_platser()
    

    def ändrar_sålda_platser(self, platser, föreställning):
        """ändrar attributet antal sålda platser
        Parametrar: self, platser, föreställning
        Returnerar: inget"""

        self.sålda_platser += platser

        if self.sålda_platser > self.platser:
            print("Du har skrivit för många platser, prova igen")
            self.sålda_platser -= platser
            föreställning.hantera_sålda_platser()
            

    def beräkna_belägg(self):
        """Beräknar belägg och ändrar attributet belägg
        Parametrar: self
        Returnerar: inget"""

        self.belägg = float(self.sålda_platser) / float(self.platser) *100
    
    
def hitta_siffror(rad):
    """Hittar siffror från raden
    Parametrar: rad
    Returnerar: siffrorna (int)"""

    tal = ""
    for i in rad:
        if i.isdigit():
            tal += i
    if not tal.isdigit():
        tal = "0"
    return int(tal)


class Föreställning:
    """Beskriver en föreställning"""

    def __init__(self):
        """ Skapar en tom lista där teatrarna ska läggas in """
        self.teatrar = []    

    def las_teatrar(self):
        """ Läser teatrar från filen till attributet teatrar.
        Parametrar: self
        Returnerar: inget """
        
        with open("fil.txt", encoding = 'utf8') as textfil:
            fil = textfil.readlines()
            for i in range(0, len(fil), 6):
                namn = fil[i].strip()
                antal_platser = hitta_siffror(fil[i+1])
                vuxen_pris = hitta_siffror(fil[i+2])
                pensionär_pris = hitta_siffror(fil[i+3])
                barn_pris = hitta_siffror(fil[i+4])
                
                ny_teater = Teater(namn, antal_platser, vuxen_pris, pensionär_pris, barn_pris)
                self.teatrar.append(ny_teater)
                
                for i in namn:
                    if i.isdigit():
                        print("Filen är felaktig, ändra teaternamnen")
                        input()

                if not antal_platser or not vuxen_pris or not pensionär_pris or not barn_pris:
                    print("Filen är felaktig, lägg till siffervärdern")
                    input()
                elif barn_pris >= (vuxen_pris or pensionär_pris) or pensionär_pris >= vuxen_pris:
                    print("Filen är felaktig, ändra biljettpriserna")
                    input()
                

    def statistik(self):
        """ Skriver ut statistiken om alla teatrar per föreställning
        Parametrar: self
        Returnerar: inget """
       
        for teater in self.teatrar:
            teater.beräkna_belägg()
       
        print("Detta är statistiken för föreställningen, sorterade efter belägg:")
        self.teatrar.sort(reverse=True)
        for teater in self.teatrar:
            print(f"{teater.namn} har tjänat {teater.prisintäkt} och sålt {round(teater.belägg)}% av sina platser")
    
    
    def visa_alla(self):
        """ Skriver ut information om alla teatrars bijettpriser per föreställning
        Parametrar: self
        Returnerar: inget """
        
        print("\nDu har valt att bestäma sålda platser, här är alla teatrar:")
        for teater in self.teatrar:
            print(f"{teater.namn} har {teater.platser} platser och biljettpriserna är:")
            print(f"Vuxen: {teater.vuxen} kr")
            print(f"Pensionär: {teater.pensionär} kr")
            print(f"Barn: {teater.barn} kr")
            print("---------------------------------")


    def hantera_sålda_platser(self):
        """ Hanterar antal sålda platser av varje prigrupp
        Parametrar: self
        Returnerar: Inget"""

        val_namn = input("\nVälj teater, skriv namnet: ")
        val_prisgrupp = input("Prisgrupp: ").lower()
        while True:
            try:
                val_platser = int(input("Hur många platser såldes? "))
                break
            except ValueError:
                print("Du skrev fel, skriv endast siffror")
                continue
        hittat_namn = False
        for teater in self.teatrar:
            if teater.namn == val_namn:
                hittat_namn = True
                teater.ändrar_sålda_platser(val_platser, self)
                teater.ändra_intäkt(val_platser, val_prisgrupp, self)
                
        if not hittat_namn:
            print("Du skrev fel namn på teatern, prova igen")
            self.hantera_sålda_platser()
    

    def beräkna_biljettförsäljning(self):
        """ Beräknar antalet sålda biljetter av varje prisklass utifrån prisintäkterna 
        Parametrar: self
        Returnerar: Inget"""

        for teater in self.teatrar:
            print("---------------------------------")
            print(f"För {teater.namn} kan: ")
            for i in range(round(teater.prisintäkt/teater.vuxen) + 1):
                for j in range(round(teater.prisintäkt/teater.pensionär) + 1):
                    for k in range(round(teater.prisintäkt/teater.barn) + 1):
                        if teater.vuxen * i + teater.pensionär * j + teater.barn * k == teater.prisintäkt:
                            print(f"{i} vuxenbiljetter, {j} pensionärsbiljetter och {k} barnbiljetter kan ha sålts")
        
        
def menyval():
    """Skriver ut menyn, läser in och returnerar användarens val
    Parametrar: inget
    Returnerar: val"""

    print("\nVad vill du göra?")
    print("1. Bestäm sålda platser")
    print("2. Se statistik")
    print("3. Beräkna biljettförsäljning")
    print("4. Avsluta")
    val = input()
    if (val != "1") and (val != "2") and (val != "3") and (val != "4"):
        print("Du valde ett felaktigt alternativ prova igen")
        menyval()
    return val


def main():
    """Huvudprogrammet, som skapar föreställning-objektet, läser in från fil
      anropar menyn och hanterar inmatningen som gjorts.
      Parametrar: inga
      Returnerar: inget"""
    
    print("Välkommen till Teaterprogrammet")
    print("---------------------------------")
    föreställning = Föreställning()
    föreställning.las_teatrar()
    val = menyval()
    while val != "4":
        if val == "1":
            föreställning.visa_alla()
            föreställning.hantera_sålda_platser()
        elif val == "2":
            föreställning.statistik()
        elif val == "3":
            föreställning.beräkna_biljettförsäljning()
        val = menyval()
    print("Tack för besöket, välkommen åter!")

if __name__ == "__main__":
    main()
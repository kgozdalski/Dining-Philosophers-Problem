from threading import Thread, Lock
import random
import time

liczbaFilozofow = 5

class Filozof(Thread):
    uruchomiony = True

    def __init__(self,nr,lewyWidelec,prawyWidelec):
        self.nr = nr
        self.lewyWidelec = lewyWidelec
        self.prawyWidelec = prawyWidelec
        super().__init__()

    def run(self):
        while(self.uruchomiony):
            time.sleep(random.uniform(1,5)) #Przerwa miedzy jedzeniem
            print("Filozof #{} jest glodny".format(self.nr))
            self.jedz()
    
    def jedz(self):
        zamienione = False #Ktory widelec filozof wybiera jako pierwszy; False - lewy, True - prawy
        w1, w2 = self.lewyWidelec, self.prawyWidelec
        while True:
            czyZablokowanyw1 = w1.acquire(True,timeout=random.uniform(1,3)) 
            if czyZablokowanyw1 == True:
                if zamienione == False:
                    print("Filozof #{} podnosi lewy widelec".format(self.nr))
                else:
                    print("Filozof #{} podnosi prawy widelec".format(self.nr))
                czyZablokowanyw2 = w2.acquire(False) #Jeżeli nie może podniesc widelca zwraca False; jeżeli może - True i blokuje
                if czyZablokowanyw2:
                    if zamienione == False:
                        print("Filozof #{} podnosi prawy widelec".format(self.nr))
                    else:
                        print("Filozof #{} podnosi lewy widelec".format(self.nr))
                    break
                w1.release() #Jeżeli nie może podniesc drugiego widelca odklada pierwszy
                if zamienione == False:
                    print("Filozof #{} odklada lewy widelec".format(self.nr))
                else:
                    print("Filozof #{} odklada prawy widelec".format(self.nr))

            print("Filozof #{} zamienia widelce".format(self.nr))
            w1, w2 = w2, w1 #Zmiana kolejnosci podnoszenia widelcow
            zamienione = not zamienione
        
        self.jedzenie()
        try:
            w1.release()
            w2.release()
        except RuntimeError:
            pass

    def jedzenie(self):
        print("Filozof #{} zaczyna jesc ####################".format(self.nr))
        time.sleep(random.uniform(3,5))
        print("Filozof #{} kończy jesc --------------------".format(self.nr))
    
def main():
    if int(liczbaFilozofow) < 2:
        exit()
    widelce = [Lock() for i in range(liczbaFilozofow)]

    filozofowie = [Filozof(i,widelce[(i)%liczbaFilozofow],widelce[(i+1)%liczbaFilozofow]) for i in range(liczbaFilozofow)]

    Filozof.uruchomiony = True
    for f in filozofowie:
        f.start()
    time.sleep(10) #Ustawienie czasu dzialania programu (kiedy filozofowie moga stac sie glodni)
    Filozof.uruchomiony = False
    print("Koniec dzialania")

main()


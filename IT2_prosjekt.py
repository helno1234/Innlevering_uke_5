# Importerer nødvendige biblioteker
import pygame
import random

# Konstanter
BREDDE = 700
HØYDE = 500

SONE_BREDDE = 450
SONE_HØYDE = HØYDE

# Størrelsen til vinduet
STØRRELSE = (BREDDE,HØYDE)

# Frames Per Second (bilder per sekund)
FPS = 120

# Farger (RGB)
HVITT = (255, 255, 255)
SVART = (0, 0, 0)
GRÅTT = (200,200,200)
SPØKELSE_GRÅTT = (100,100,100)
GRØNT = (140, 250, 140)
MENNESKE_FARGE = (200,130,50)

# Antall poeng
poeng = 0

# Lager en overflate (surface) vi kan tegne på
overflate = pygame.display.set_mode(STØRRELSE)

# Lager en klokke
klokke = pygame.time.Clock()

# Objekt-bredde og -høyde
objekt_bredde, objekt_høyde = 40, 40

# Superklasse for spillobjektene
class SpillObjekt:
    """
    Klasse til spill-objekter
    
    Attributter:
        yPosisjon (int): y-posisjonen til objektet
    """
    def __init__(self):
        self.yPosisjon = random.randint(objekt_høyde, HØYDE-objekt_høyde)
        
    def plassering(self):
        # Oppdaterer x- og y-verdiene til rect
        self.rect.x = self.xPosisjon
        self.rect.y = self.yPosisjon
        
# Subklasse: sauobjekt  
class Sau(SpillObjekt):
    """
    Subklasse til superklassen spill-objekter
    
    Attributter:
        xPosisjon (int): x-posisjonen til sau-objektet
        rect (list): Rektangelet (sauen) sin x- og y-posisjon, samt bredden og høyden til objektet
    """
    def __init__(self):
        super().__init__()
        self.xPosisjon = random.randint(BREDDE-((BREDDE-SONE_BREDDE)/2), BREDDE-objekt_bredde)
        self.rect = pygame.Rect(self.xPosisjon, self.yPosisjon, objekt_bredde, objekt_bredde)
        
# Subklasse: hindringsobjekt  
class Hindring(SpillObjekt):
    """
    Subklasse til superklassen spill-objekter
    
    Attributter:
        xPosisjon (int): x-posisjonen til hindringsobjektet
        rect (list): Rektangelet (hindringen) sin x- og y-posisjon, samt bredden og høyden til objektet
    """
    def __init__(self):
        super().__init__()
        self.xPosisjon = random.randint((BREDDE-SONE_BREDDE)/2, (BREDDE-((BREDDE-SONE_BREDDE)/2))-objekt_bredde)
        self.rect = pygame.Rect(self.xPosisjon, self.yPosisjon, objekt_bredde, objekt_bredde) 
        
# Subklasse: menneskesobjekt
class Menneske(SpillObjekt):
    """
    Subklasse til superklassen spill-objekter
    
    Attributter:
        xPosisjon (int): x-posisjonen til menneske-objektet
        rect (list): Rektangelet (mennesket) sin x- og y-posisjon, samt bredden og høyden til objektet
        vx (int): farten til mennesket i x-retning
        vy (int): farten til mennesket i y-retning
    """
    def __init__(self):
        super().__init__()
        self.xPosisjon = random.randint(0, ((BREDDE-SONE_BREDDE)/2-objekt_bredde))
        self.rect = pygame.Rect(self.xPosisjon, self.yPosisjon, objekt_bredde, objekt_bredde)
        self.vx = 0
        self.vy = 0
        
    def plassering(self, fart):
        super().plassering()
        self.xPosisjon += self.vx
        self.yPosisjon += self.vy
        
        # Henter knappene fra tastaturet som trykkes på
        keys = pygame.key.get_pressed()
    
        # Sjekker om ulike taster trykkes på for å bevege menneskeobjekt
        if keys[pygame.K_LEFT] and menneske.xPosisjon > 0:
            menneske.vx = -fart
        elif keys[pygame.K_RIGHT] and menneske.xPosisjon < BREDDE-objekt_bredde:
            menneske.vx = fart
        else:
            menneske.vx = 0 
        if keys[pygame.K_UP] and menneske.yPosisjon > 0:
            menneske.vy = -fart
        elif keys[pygame.K_DOWN] and menneske.yPosisjon < HØYDE-objekt_høyde:
            menneske.vy = fart
        else:
            menneske.vy = 0
    
# Subklasse: spøkelsessobjekt
class Spøkelse(SpillObjekt):
    """
    Subklasse til superklassen spill-objekter
    
    Attributter:
        xPosisjon (int): x-posisjonen til spøkelses-objektet
        rect (list): Rektangelet (spøkelset) sin x- og y-posisjon, samt bredden og høyden til objektet
        vx (int): farten til spøkelset i x-retning
        vy (int): farten til spøkelset i y-retning
    """
    def __init__(self):
        super().__init__()
        self.xPosisjon = random.randint((BREDDE-SONE_BREDDE)/2, (BREDDE-((BREDDE-SONE_BREDDE)/2))-objekt_bredde) 
        self.rect = pygame.Rect(self.xPosisjon, self.yPosisjon, objekt_bredde, objekt_bredde)
        self.vx = -1
        self.vy = 1
    
    def plassering(self): 
        super().plassering() 
        self.xPosisjon += self.vx
        self.yPosisjon += self.vy
        
    def endreRetning(self):
        # Sjekker om spøkelset går ut av det grønne området
        if spøkelse.xPosisjon+objekt_bredde >= SONE_BREDDE+(BREDDE-SONE_BREDDE)/2:
            self.vx *= -1
        if spøkelse.xPosisjon <= (BREDDE-SONE_BREDDE)/2:
            self.vx *= -1
        if spøkelse.yPosisjon+objekt_høyde >= HØYDE:
            self.vy *= -1
        if spøkelse.yPosisjon<=0:
            self.vy *= -1    

# Lager funksjoner for å legge til objekter i objekt_listene
def legger_til_sau():
    sau = Sau()
    sauer.append(sau)
    
def legger_til_hindring():
    hindring = Hindring()
    hindringer.append(hindring)

def legger_til_spøkelse():
    spøkelse = Spøkelse()
    spøkelser.append(spøkelse)

menneske = Menneske() # Lager et menneskeobjekt

menneske_med_sau = False # Mennesket har ikke med en sau

# Definerer tomme lister for sau-, spøkelses- og hindringsobjektene
sauer = []
hindringer = []
spøkelser = []

# Legger til 3 saueobjekter og hindringsobjekter
for i in range(3):
    legger_til_sau()
    legger_til_hindring()
    i += 1

legger_til_spøkelse() # Legger kun til 1 spøkelse

pygame.init() # Initiere pygame

kjør_program = True # Variabel som styrer om spillet skal kjøres

# Spill-løkken
while kjør_program:
    klokke.tick(FPS) # Sørger for at løkken kjører i korrekt hastighet
    
    overflate.fill(GRÅTT) # OVerflaten skal være grå

    pygame.draw.rect(overflate, GRØNT, [(BREDDE-SONE_BREDDE)/2, 0, SONE_BREDDE, SONE_HØYDE]) # Tegner grønt spillbrett (ikke frisonene)

    pygame.draw.rect(overflate, MENNESKE_FARGE, [menneske.xPosisjon, menneske.yPosisjon, objekt_bredde, objekt_høyde]) # Tegner mennesket

    # Tegner hindringer
    for hindring in hindringer:
        # For-løkke som sjekker om eventuelt overlapping mellom hindringer som skal tegnes
        for annen_hindring in hindringer:
            if hindring != annen_hindring:
                if hindring.rect.colliderect(annen_hindring.rect):
                    
                    # Oppdaterer x- og y-posisjon til hindringene ikke ligger oppå hverandre
                    while sau.rect.colliderect(annen_sau.rect):
                        hindring.xPosisjon = random.randint((BREDDE-SONE_BREDDE)/2, (BREDDE-((BREDDE-SONE_BREDDE)/2))-objekt_bredde)
                        hindring.yPosisjon = random.randint(objekt_høyde, HØYDE-objekt_høyde)
                        hindring.plassering()
                    
        # Sjekker om menneske kolliderer med hindring         
        if (menneske.rect.colliderect(hindring.rect)):
            if menneske.xPosisjon < hindring.xPosisjon:
                menneske.xPosisjon -= 2
            elif menneske.xPosisjon > hindring.xPosisjon:
                menneske.xPosisjon += 2
            elif menneske.yPosisjon > hindring.yPosisjon:
                menneske.yPosisjon += 2
            elif menneske.yPosisjon < hindring.yPosisjon:
                menneske.yPosisjon -= 2
                
        # Tegner hindring
        pygame.draw.rect(overflate, SVART, [hindring.xPosisjon, hindring.yPosisjon, objekt_bredde, objekt_høyde])    
        
    # Tegner spøkelser
    for spøkelse in spøkelser:
        # For-løkke som sjekker om eventuelt overlapping mellom spøkelser som skal tegnes
        for annet_spøkelse in spøkelser:
            if spøkelse != annet_spøkelse:
                if spøkelse.rect.colliderect(annet_spøkelse.rect):
                    # Oppdaterer x- og y-posisjon til spøkelsene ikke kolliderer
                    while not spøkelse.rect.colliderect(annet_spøkelse.rect):
                        spøkelse.xPosisjon = random.randint((BREDDE-SONE_BREDDE)/2, (BREDDE-((BREDDE-SONE_BREDDE)/2))-objekt_bredde)
                        spøkelse.yPosisjon = random.randint(objekt_høyde, HØYDE-objekt_høyde)
                        
        # Tegner spøkelse
        pygame.draw.rect(overflate, SPØKELSE_GRÅTT, [spøkelse.xPosisjon, spøkelse.yPosisjon, objekt_bredde, objekt_høyde])
        
        # Gir spøkelsene en plassering og sjekker eventuelle kollisjoner med "veggene"
        spøkelse.plassering()
        spøkelse.endreRetning()    
    
    
    # Tegner sauer
    for sau in sauer:
        # For-løkke som sjekker om eventuelt overlapping mellom sauer som skal tegnes
        for annen_sau in sauer:
            if sau != annen_sau:
                if sau.rect.colliderect(annen_sau.rect):
                    # Oppdaterer x- og y-posisjon til sauene ikke ligger oppå hverandre
                    while sau.rect.colliderect(annen_sau.rect):
                        sau.xPosisjon = random.randint(BREDDE-((BREDDE-SONE_BREDDE)/2), BREDDE-objekt_bredde)
                        sau.yPosisjon = random.randint(objekt_høyde, HØYDE-objekt_høyde)
                        sau.plassering()
        
        # Tegner sau
        pygame.draw.rect(overflate, HVITT, [sau.xPosisjon, sau.yPosisjon, objekt_bredde, objekt_høyde])
        
        # Sjekker om sau kolliderer med menneske
        if sau.rect.colliderect(menneske.rect):
            # Sjekker om mennesket allerede har en sau
            if menneske_med_sau:
                kjør_program = False
            else:
                sauer.remove(sau)
                MENNESKE_FARGE = HVITT # Menneskets farge blir hvit, for å vise at mennesket har en sau
                menneske_med_sau = True

    if menneske_med_sau:
        # Hvis mennesket har sau, og er i venstre frisone
        if menneske.xPosisjon <= ((BREDDE-SONE_BREDDE)/2)-objekt_bredde:
            poeng += 1
            legger_til_spøkelse()
            legger_til_sau()
            legger_til_hindring()
            MENNESKE_FARGE = (200,130,50) # Endrer mennesket sin farge tilbake
            menneske_med_sau = False
    
    for spøkelse in spøkelser:
        if spøkelse.rect.colliderect(menneske.rect): # Sjekker kollisjon mellom spøkelsesobjekt og menneskeobjekt
            kjør_program = False # Avslutter spillet
    
    if menneske_med_sau:
        menneske.plassering(0.7) # Sakker ned farten til mennesket
    else:
        menneske.plassering(1.2) # Oppdaterer posisjonen til mennesket (med normal fart)
             
    # Går gjennom hendelser 
    for hendelser in pygame.event.get():
        # Sjekker om vi ønsker å lukke vinduet
        if hendelser.type == pygame.QUIT:
            kjør_program = False # Spillet skal avsluttes
             
    pygame.display.flip() # "Flipper" displayet for å vise hva vi har tegnet

pygame.quit() # Avslutter pygame

print(f"Du fikk {poeng} poeng") # Viser hvor mange poeng du fikk, etter spillet er ferdig
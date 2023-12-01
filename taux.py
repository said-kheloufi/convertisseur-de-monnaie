import json
from forex_python.converter import CurrencyRates

#partie historique
def charger_historique():
    try:
        with open("historique_conversions.json", "r") as fichier:
            return json.load(fichier)
    except FileNotFoundError:
        return []

def sauvegarder_historique(historique):
    with open("historique_conversions.json", "w") as fichier:
        json.dump(historique, fichier, indent=2)

#partir taux et conversion
def obtenir_taux_de_change(devis_source, devis_cible):
    c = CurrencyRates()
    return c.get_rate(devis_source, devis_cible)

def convertir_devise(montant, devis_source, devis_cible):
    taux_de_change = obtenir_taux_de_change(devis_source, devis_cible)
    if taux_de_change is None:
        return None
    else:
        montant_converti = montant * taux_de_change
        return montant_converti

#partie affichage de l'historique
def afficher_historique(historique):
    print("\n--- Historique des Conversions ---")
    for conversion in historique:
        print(f"{conversion['montant']} {conversion['devis_source']} = {conversion['montant_converti']} {conversion['devis_cible']}")
    print("---------------------------------\n")

#
def main():
    historique_conversions = charger_historique()

    while True:
        try:
            montant = float(input("Entrez le montant à convertir : "))
            devis_source = input("Entrez la devise source (ex: USD) : ").upper()
            devis_cible = input("Entrez la devise cible (ex: EUR) : ").upper()

            montant_converti = convertir_devise(montant, devis_source, devis_cible)

            if montant_converti is not None:
                print(f"\n{montant} {devis_source} = {montant_converti} {devis_cible}\n")
                historique_conversions.append({
                    'montant': montant,
                    'devis_source': devis_source,
                    'montant_converti': montant_converti,
                    'devis_cible': devis_cible
                })
                sauvegarder_historique(historique_conversions)
            else:
                print("\nConversion impossible. Vérifiez les devises saisies.\n")

            afficher_historique(historique_conversions)

            continuer = input("Voulez-vous effectuer une autre conversion ? (Oui/Non) : ").lower()
            if continuer != 'oui':
                break

        except ValueError:
            print("\nErreur : Veuillez entrer un montant numérique.\n")

if __name__ == "__main__":
    main()

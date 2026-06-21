import flet as ft
import time
import random
import threading

def main(page: ft.Page):
    page.title = "we Depanne"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#EEF2F7"

    # ----- PALETTE -----
    BLEU = "#3B82F6"
    BLEU_FONCE = "#1D4ED8"
    NOIR = "#0B1220"
    GRIS_CHAMP = "#EFF1F4"
    GRIS_TXT = "#6B7280"
    VERT = "#22A45D"

    phone_body = ft.Column(expand=True, scroll="auto", spacing=0)
    bottom_container = ft.Container()

    service_selectionne = {"nom": "", "emoji": ""}
    etat = {"conv": 0}
    utilisateur = {"nom": "", "photo": ""}  # nom saisi + chemin de la photo de profil choisie

    # ----- LOGO -----
    # ----- IMAGES (version APK : tout est dans le dossier assets/) -----
    # Dans un APK, les images sont chargées par leur nom depuis assets/.
    # Toutes les images existent (placeholders fournis), donc pas de test d'existence.

    def logo(size=22, with_text=True):
        return ft.Image(src="logo.png", height=size + 16)

    def grand_logo(hauteur=150):
        return ft.Image(src="logo.png", height=hauteur)

    # ----- IMAGES DE CATÉGORIES -----
    CAT_FICHIERS = {
        "Mécanicien auto": "cat_depannage.png",
        "Mécanicien moto": "cat_mecanique.png",
        "Électricien": "cat_electricite.png",
        "Plombier": "cat_plomberie.png",
        "Peintre": "cat_peinture.png",
        "Coiffeur": "cat_coiffure.png",
        "Vulcanisateur": "cat_vulcanisation.png",
        "Menuisier": "cat_menuiserie.png",
        "Vitrier": "cat_vitrerie.png",
        "Chauffeur": "cat_chauffeur.png",
        "Agent de nettoyage": "cat_nettoyage.png",
        "Livreur": "cat_livraison.png",
        "Technicien froid": "cat_frigoriste.png",
    }

    def icone_categorie(service, emoji, taille=26):
        fichier = CAT_FICHIERS.get(service)
        if fichier:
            return ft.Image(src=fichier, width=taille + 6, height=taille + 6)
        return ft.Text(emoji, size=taille)

    def img_ou_emoji(fichier, emoji, largeur, hauteur=None, taille_emoji=None):
        if fichier:
            return ft.Image(src=fichier, width=largeur, height=hauteur or largeur)
        return ft.Text(emoji, size=taille_emoji or largeur)

    # Avatar rond : photo importée par l'utilisateur > profil.png par défaut.
    def avatar(diametre=40):
        source = utilisateur["photo"] if utilisateur["photo"] else "profil.png"
        return ft.Container(
            content=ft.Image(src=source, width=diametre, height=diametre),
            width=diametre, height=diametre, border_radius=diametre,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, bgcolor=GRIS_CHAMP)


    # ----- BOUTONS -----
    def btn_noir(texte, on_click, width=330):
        return ft.ElevatedButton(
            content=ft.Text(texte, color="white", weight=ft.FontWeight.BOLD, size=15),
            on_click=on_click, width=width, height=54,
            style=ft.ButtonStyle(bgcolor=NOIR, color="white",
                                 shape=ft.RoundedRectangleBorder(radius=27), elevation=0),
        )

    def btn_gris(texte, on_click, width=330):
        return ft.ElevatedButton(
            content=ft.Text(texte, color=NOIR, weight=ft.FontWeight.BOLD, size=15),
            on_click=on_click, width=width, height=54,
            style=ft.ButtonStyle(bgcolor=GRIS_CHAMP, color=NOIR,
                                 shape=ft.RoundedRectangleBorder(radius=27), elevation=0),
        )

    def btn_social(emoji, texte, on_click, width=330, logo_fichier=None):
        icone = img_ou_emoji(logo_fichier, emoji, 18, 18, 16) if logo_fichier else ft.Text(emoji, size=16)
        return ft.ElevatedButton(
            content=ft.Row([icone,
                            ft.Text(texte, color=NOIR, weight=ft.FontWeight.BOLD, size=14)],
                           alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            on_click=on_click, width=width, height=52,
            style=ft.ButtonStyle(bgcolor="white", color=NOIR,
                                 shape=ft.RoundedRectangleBorder(radius=26),
                                 side=ft.BorderSide(1, "#E2E8F0"), elevation=0),
        )

    def btn_bleu(texte, on_click, width=330):
        # Utilisé pour WhatsApp : on garde le vert WhatsApp officiel.
        return ft.ElevatedButton(
            content=ft.Text(texte, color="white", weight=ft.FontWeight.BOLD, size=15),
            on_click=on_click, width=width, height=54,
            style=ft.ButtonStyle(bgcolor="#25D366", color="white",
                                 shape=ft.RoundedRectangleBorder(radius=27), elevation=0),
        )

    def btn_lien(texte, on_click, color=NOIR):
        return ft.TextButton(content=ft.Text(texte, color=color, weight=ft.FontWeight.BOLD, size=13),
                             on_click=on_click)

    def btn_retour(on_click):
        return ft.TextButton(content=ft.Text("←", size=22, weight=ft.FontWeight.BOLD, color=NOIR),
                             on_click=on_click)

    def champ(label, hint, password=False, ref=None):
        tf = ft.TextField(hint_text=hint, password=password, can_reveal_password=password,
                          width=330, height=48, border_radius=14, filled=True, bgcolor=GRIS_CHAMP,
                          border_color="transparent", content_padding=ft.padding.only(left=16, top=0, right=16, bottom=0))
        if ref is not None:
            ref["field"] = tf
        return ft.Column([
            ft.Text(label, size=13, weight=ft.FontWeight.BOLD, color=NOIR),
            tf,
        ], spacing=4)

    # ----- DONNÉES -----
    toutes_categories = [
        ("🪚", "Menuisier"), ("🚗", "Mécanicien auto"), ("🏍️", "Mécanicien moto"),
        ("⚡", "Électricien"), ("🚰", "Plombier"), ("🎨", "Peintre"),
        ("💈", "Coiffeur"), ("🛞", "Vulcanisateur"), ("🪟", "Vitrier"),
        ("🚖", "Chauffeur"), ("🧹", "Agent de nettoyage"), ("📦", "Livreur"),
        ("❄️", "Technicien froid"),
    ]
    maitres_db = {
        "Menuisier": [{"nom": "Cyrille A.", "note": 4.6, "distance": "1.8 km", "tarif": "9 000 F", "tel": "+22996001122"}],
        "Mécanicien auto": [
            {"nom": "Florent A.", "note": 4.8, "distance": "1.2 km", "tarif": "10 000 F", "tel": "+22997001122"},
            {"nom": "Romuald K.", "note": 4.6, "distance": "2.0 km", "tarif": "8 500 F", "tel": "+22996223344"}],
        "Mécanicien moto": [{"nom": "Patrice D.", "note": 4.9, "distance": "0.8 km", "tarif": "12 000 F", "tel": "+22995334455"}],
        "Électricien": [{"nom": "Serge H.", "note": 4.7, "distance": "1.5 km", "tarif": "7 000 F", "tel": "+22994445566"}],
        "Plombier": [{"nom": "Casimir B.", "note": 4.5, "distance": "2.4 km", "tarif": "6 500 F", "tel": "+22993556677"}],
        "Peintre": [{"nom": "Yves T.", "note": 4.6, "distance": "3.1 km", "tarif": "15 000 F", "tel": "+22992667788"}],
        "Coiffeur": [{"nom": "Estelle M.", "note": 4.9, "distance": "0.5 km", "tarif": "3 000 F", "tel": "+22991778899"}],
        "Vulcanisateur": [{"nom": "Bruno L.", "note": 4.4, "distance": "1.9 km", "tarif": "2 500 F", "tel": "+22990889900"}],
        "Vitrier": [{"nom": "Hervé N.", "note": 4.5, "distance": "2.2 km", "tarif": "8 000 F", "tel": "+22989990011"}],
        "Chauffeur": [{"nom": "Aurel S.", "note": 4.8, "distance": "0.9 km", "tarif": "5 000 F", "tel": "+22988001122"}],
        "Agent de nettoyage": [{"nom": "ProClean", "note": 4.7, "distance": "1.6 km", "tarif": "11 000 F", "tel": "+22987112233"}],
        "Livreur": [{"nom": "Ulrich M.", "note": 4.6, "distance": "1.1 km", "tarif": "1 500 F", "tel": "+22986223344"}],
        "Technicien froid": [{"nom": "Désiré K.", "note": 4.7, "distance": "1.4 km", "tarif": "13 000 F", "tel": "+22985334455"}],
    }
    maitre_defaut = {"nom": "Expert we Depanne", "note": 4.7, "distance": "1.5 km", "tarif": "Sur devis", "tel": "+22900000000"}

    conversations = [{
        "nom": "Florent A.", "service": "Mécanicien auto", "tel": "+22997001122",
        "messages": [{"de": "maitre", "texte": "Bonjour ! Je suis tout proche, j'arrive dans 5 minutes 🚗"},
                     {"de": "moi", "texte": "Oui parfait, je vous attends !"}]}]
    historique = [
        {"service": "Mécanicien moto", "maitre": "Patrice D.", "date": "18 juin 2026", "statut": "Terminé"},
        {"service": "Plombier", "maitre": "Casimir B.", "date": "12 juin 2026", "statut": "Terminé"},
        {"service": "Électricien", "maitre": "Serge H.", "date": "5 juin 2026", "statut": "Annulé"}]

    # ----- NAVIGATION -----
    def go(ecran):
        phone_body.controls.clear()
        bottom_container.content = None
        page.bgcolor = "#EEF2F7"
        ecrans.get(ecran, ec_splash)()
        page.update()

    # ----- MENU DU BAS -----
    NAV_FICHIERS = {
        "Accueil": "nav_accueil.png",
        "Services": "nav_services.png",
        "Messages": "nav_messages.png",
        "Profil": "nav_profil.png",
    }

    def nav_item(emoji, label, ecran, actif_label):
        actif = (label == actif_label)
        couleur = BLEU if actif else "#9AA3AF"
        icone = img_ou_emoji(NAV_FICHIERS.get(label, ""), emoji, 22, 22, 17)
        return ft.ElevatedButton(
            content=ft.Column([icone,
                               ft.Text(label, size=9, color=couleur,
                                       weight=ft.FontWeight.BOLD if actif else ft.FontWeight.NORMAL)],
                              alignment=ft.MainAxisAlignment.CENTER,
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            on_click=lambda _: go(ecran), expand=True, height=60,
            style=ft.ButtonStyle(bgcolor="white", elevation=0, shape=ft.RoundedRectangleBorder(radius=0)))

    def menu_bas(actif):
        return ft.Container(
            content=ft.Row([nav_item("🏠", "Accueil", "accueil", actif),
                            nav_item("📋", "Services", "commandes", actif),
                            nav_item("💬", "Messages", "messages", actif),
                            nav_item("👤", "Profil", "profil", actif)], spacing=0),
            bgcolor="white", border=ft.border.only(top=ft.BorderSide(1, "#EAECEF")))

    def lancer(nom, emoji):
        def h(e):
            if nom is None:
                go("commandes"); return
            service_selectionne["nom"] = nom
            service_selectionne["emoji"] = emoji
            go("localisation")
        return h

    # ====== ÉCRANS ======

    # SPLASH (image de démarrage plein écran)
    def ec_splash():
        page.bgcolor = "#FFFFFF"
        contenu = ft.Container(
            expand=True, bgcolor="#FFFFFF",
            content=ft.Column([
                ft.Image(src="demarrage.png", width=384, height=680),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
               alignment=ft.MainAxisAlignment.CENTER),
        )
        phone_body.controls.append(contenu)
        def worker():
            time.sleep(2.2)
            go("onboarding")
        threading.Thread(target=worker, daemon=True).start()

    # ONBOARDING
    def ec_onboarding():
        haut = [ft.Container(height=30)]
        phone_body.controls.append(ft.Column(haut + [
            ft.Container(height=20), grand_logo(170),
            ft.Container(height=20),
            ft.Text("Bienvenue sur", size=22, weight=ft.FontWeight.BOLD, color=NOIR,
                    text_align=ft.TextAlign.CENTER),
            ft.Row([ft.Text("we ", size=28, weight=ft.FontWeight.BOLD, color=NOIR),
                    ft.Text("Depanne", size=28, weight=ft.FontWeight.BOLD, color=BLEU_FONCE)],
                   alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            ft.Container(height=12),
            ft.Text("Un expert chez vous, en un clic.\nDisponible partout, à tout moment.",
                    size=14, color=GRIS_TXT, text_align=ft.TextAlign.CENTER),
            ft.Container(height=30),
            btn_noir("S'inscrire", lambda _: go("inscription")),
            btn_gris("J'ai déjà un compte", lambda _: go("connexion")),
            ft.Container(height=14),
            ft.Container(content=ft.Text("En créant un compte, vous acceptez nos Conditions Générales et notre Politique de Confidentialité.",
                                         size=10, color="#9AA3AF", text_align=ft.TextAlign.CENTER),
                         padding=ft.padding.only(left=30, top=0, right=30, bottom=0)),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8))

    # INSCRIPTION DÉTAILLÉE
    def ec_inscription():
        ref_nom = {}
        type_compte = ft.Dropdown(
            options=[ft.dropdown.Option("Client"), ft.dropdown.Option("Artisan")],
            value="Client", width=330, border_radius=14, filled=True, bgcolor=GRIS_CHAMP,
            border_color="transparent")
        cgu = ft.Checkbox(label="", value=False)

        def inscrire(e):
            champ_nom = ref_nom.get("field")
            if champ_nom and champ_nom.value:
                utilisateur["nom"] = champ_nom.value
            if type_compte.value == "Artisan":
                go("inscription_maitre")
            else:
                go("accueil")

        entete = ft.Row([
            btn_retour(lambda _: go("onboarding")),
            logo(18),
            ft.Container(width=40),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        phone_body.controls.append(ft.Column([
            ft.Container(height=10), entete, ft.Container(height=6),
            ft.Container(content=ft.Column([
                ft.Text("Créer un compte", size=26, weight=ft.FontWeight.BOLD, color=NOIR),
                ft.Text("Remplissez vos informations pour commencer.", size=13, color=GRIS_TXT),
            ], spacing=2), padding=ft.padding.only(left=24, top=0, right=24, bottom=0)),
            ft.Container(height=14),
            champ("Nom complet", "Jean Dupont", ref=ref_nom),
            champ("Numéro de téléphone", "+229 XX XX XX XX"),
            champ("Adresse e-mail", "votre.email@exemple.com"),
            ft.Column([ft.Text("Je suis un :", size=13, weight=ft.FontWeight.BOLD, color=NOIR), type_compte], spacing=4),
            champ("Mot de passe", "••••••••", password=True),
            champ("Confirmer le mot de passe", "••••••••", password=True),
            ft.Row([cgu, ft.Container(content=ft.Text("J'accepte les Conditions Générales et la Politique de Confidentialité.",
                                                      size=11, color=GRIS_TXT), width=290)],
                   spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=6),
            btn_noir("S'INSCRIRE", inscrire),
            ft.Container(content=ft.Text("— Ou —", size=12, color="#9AA3AF"), margin=ft.margin.only(left=0, top=8, right=0, bottom=8)),
            btn_social("🟢", "Continuer avec Google", lambda _: go("accueil"), logo_fichier="google.png"),
            btn_social("", "Continuer avec Apple", lambda _: go("accueil"), logo_fichier="apple.png"),
            ft.Row([ft.Text("Vous avez déjà un compte ?", size=12, color=GRIS_TXT),
                    btn_lien("Se connecter", lambda _: go("connexion"))],
                   alignment=ft.MainAxisAlignment.CENTER, spacing=2),
            ft.Container(height=20),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12))

    # CONNEXION
    def ec_connexion():
        entete = ft.Row([
            btn_retour(lambda _: go("onboarding")),
            logo(18), ft.Container(width=40),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        phone_body.controls.append(ft.Column([
            ft.Container(height=10), entete, ft.Container(height=10),
            ft.Container(content=ft.Column([
                ft.Text("Bon retour 👋", size=26, weight=ft.FontWeight.BOLD, color=NOIR),
                ft.Text("Connectez-vous pour continuer.", size=13, color=GRIS_TXT),
            ], spacing=2), padding=ft.padding.only(left=24, top=0, right=24, bottom=0)),
            ft.Container(height=18),
            champ("Adresse e-mail ou téléphone", "votre.email@exemple.com"),
            champ("Mot de passe", "••••••••", password=True),
            ft.Row([btn_lien("Mot de passe oublié ?", lambda _: go("connexion"), color=BLEU_FONCE)],
                   alignment=ft.MainAxisAlignment.END),
            btn_noir("SE CONNECTER", lambda _: go("accueil")),
            ft.Container(content=ft.Text("— Ou —", size=12, color="#9AA3AF"), margin=ft.margin.only(left=0, top=8, right=0, bottom=8)),
            btn_social("🟢", "Continuer avec Google", lambda _: go("accueil"), logo_fichier="google.png"),
            btn_social("", "Continuer avec Apple", lambda _: go("accueil"), logo_fichier="apple.png"),
            ft.Row([ft.Text("Pas encore de compte ?", size=12, color=GRIS_TXT),
                    btn_lien("S'inscrire", lambda _: go("inscription"))],
                   alignment=ft.MainAxisAlignment.CENTER, spacing=2),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12))

    # INSCRIPTION MAÎTRE
    def ec_inscription_maitre():
        txt_cni = ft.Text("📷 Photo CNI / Passeport", color=BLEU_FONCE, weight=ft.FontWeight.BOLD)
        txt_dip = ft.Text("📄 Photo Diplôme / Attestation", color=BLEU_FONCE, weight=ft.FontWeight.BOLD)

        def up_cni(e):
            txt_cni.value = "✅ CNI enregistrée !"; txt_cni.color = VERT; page.update()

        def up_dip(e):
            txt_dip.value = "✅ Diplôme enregistré !"; txt_dip.color = VERT; page.update()

        b_cni = ft.ElevatedButton(content=txt_cni, on_click=up_cni, width=330, height=50,
                                  style=ft.ButtonStyle(bgcolor=GRIS_CHAMP, elevation=0,
                                                       shape=ft.RoundedRectangleBorder(radius=14)))
        b_dip = ft.ElevatedButton(content=txt_dip, on_click=up_dip, width=330, height=50,
                                  style=ft.ButtonStyle(bgcolor="#E7F6EC", elevation=0,
                                                       shape=ft.RoundedRectangleBorder(radius=14)))
        phone_body.controls.append(ft.Column([
            ft.Container(height=10),
            ft.Row([btn_retour(lambda _: go("inscription"))],
                   alignment=ft.MainAxisAlignment.START),
            ft.Container(content=ft.Column([
                ft.Text("Dossier Artisan", size=24, weight=ft.FontWeight.BOLD, color=NOIR),
                ft.Text("Rejoignez le réseau d'experts certifiés.", size=13, color=GRIS_TXT)], spacing=2),
                padding=ft.padding.only(left=24, top=0, right=24, bottom=0)),
            ft.Container(height=10),
            champ("Métier", "ex : Électricien, Mécanicien…"),
            champ("Zone de déplacement", "ex : Cotonou, Calavi…"),
            champ("Tarif indicatif", "ex : dès 5 000 F"),
            ft.Text("Certifications obligatoires :", size=12, weight=ft.FontWeight.BOLD, color=NOIR),
            b_cni, b_dip, ft.Container(height=8),
            btn_noir("Soumettre mon dossier 🔒", lambda _: go("attente")),
            ft.Container(height=20),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12))

    def ec_attente():
        phone_body.controls.append(ft.Column([
            ft.Container(content=ft.Text("⏳", size=64), margin=ft.margin.only(left=0, top=70, right=0, bottom=20)),
            ft.Text("Dossier en cours d'analyse", size=20, weight=ft.FontWeight.BOLD, color=NOIR,
                    text_align=ft.TextAlign.CENTER),
            ft.Container(content=ft.Text("Nous vérifions vos documents sous 24h pour vous attribuer le badge Certifié 🌟.",
                                         size=13, color=GRIS_TXT, text_align=ft.TextAlign.CENTER),
                         padding=ft.padding.only(left=34, top=12, right=34, bottom=36)),
            btn_noir("Découvrir l'application", lambda _: go("accueil")),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER))

    # ACCUEIL
    def ec_accueil():
        prenom = utilisateur["nom"].strip().split(" ")[0] if utilisateur["nom"].strip() else ""
        salutation = f"Bonjour, {prenom} 👋" if prenom else "Bonjour 👋"
        header = ft.Container(content=ft.Row([
            avatar(46),
            ft.Column([
                ft.Text(salutation, size=20, weight=ft.FontWeight.BOLD, color=NOIR),
                ft.Text("Comment pouvons-nous vous aider ?", size=13, color=GRIS_TXT),
            ], spacing=2, expand=True),
        ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.only(left=22, top=22, right=22, bottom=0))

        search = ft.Container(
            content=ft.Row([ft.Text("Rechercher un service...", color="#9AA3AF", size=14, expand=True),
                            ft.Text("🔍", size=15)]),
            bgcolor=GRIS_CHAMP, padding=ft.padding.only(left=16, top=14, right=16, bottom=14), border_radius=16,
            margin=ft.margin.only(left=22, top=16, right=22, bottom=16))

        banner = ft.Container(
            content=ft.Image(src="banniere.png", width=336),
            border_radius=18, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            margin=ft.margin.only(left=22, top=0, right=22, bottom=22))

        titre = ft.Container(content=ft.Row([
            ft.Text("Catégories de Service", size=18, weight=ft.FontWeight.BOLD, color=NOIR),
            ft.TextButton(content=ft.Text("Voir tout", size=13, color=NOIR, weight=ft.FontWeight.BOLD),
                          on_click=lambda _: go("commandes"))],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN), padding=ft.padding.only(left=22, top=0, right=22, bottom=4))

        # Carte ronde : cercle cliquable (image) + nom du métier EN DESSOUS
        def carte(emoji, label, service, bg, texte_blanc=False):
            fichier = CAT_FICHIERS.get(service)
            if fichier:
                contenu = ft.Container(
                    content=ft.Image(src=fichier, width=64, height=64),
                    width=64, height=64, border_radius=32,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS)
            else:
                # cercle de couleur avec emoji centré
                contenu = ft.Container(
                    content=ft.Text(emoji, size=26),
                    width=64, height=64, border_radius=32, bgcolor=bg,
                    alignment=ft.alignment.center)
            cercle = ft.ElevatedButton(
                content=contenu, on_click=lancer(service, emoji),
                width=64, height=64,
                style=ft.ButtonStyle(bgcolor=bg, elevation=0,
                                     padding=ft.padding.only(left=0, top=0, right=0, bottom=0),
                                     shape=ft.RoundedRectangleBorder(radius=32)))
            return ft.Column([
                cercle,
                ft.Text(label, size=10, weight=ft.FontWeight.BOLD,
                        color="white" if texte_blanc else NOIR,
                        text_align=ft.TextAlign.CENTER, max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS, width=80),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6, width=80)

        l1 = ft.Row([carte("🚗", "Méca. auto", "Mécanicien auto", "#FDE7E7"),
                     carte("🏍️", "Méca. moto", "Mécanicien moto", "#E7F6EC"),
                     carte("⚡", "Électricien", "Électricien", "#FFF6DA"),
                     carte("🚰", "Plombier", "Plombier", "#E6F0FF")],
                    alignment=ft.MainAxisAlignment.CENTER, spacing=8)
        l2 = ft.Row([carte("🎨", "Peintre", "Peintre", "#F3E8FF"),
                     carte("💈", "Coiffeur", "Coiffeur", "#FFE9F1"),
                     carte("❄️", "Tech. froid", "Technicien froid", "#E6F7FF"),
                     carte("➕", "Plus", None, NOIR)],
                    alignment=ft.MainAxisAlignment.CENTER, spacing=8)
        # bouton "Plus" : image ronde plus.png si dispo, sinon rond noir avec +
        plus_cercle = ft.ElevatedButton(
            content=ft.Container(content=ft.Image(src="plus.png", width=64, height=64),
                                 width=64, height=64, border_radius=32,
                                 clip_behavior=ft.ClipBehavior.ANTI_ALIAS),
            on_click=lambda _: go("commandes"), width=64, height=64,
            style=ft.ButtonStyle(bgcolor="white", elevation=0,
                                 padding=ft.padding.only(left=0, top=0, right=0, bottom=0),
                                 shape=ft.RoundedRectangleBorder(radius=32)))
        l2.controls[3] = ft.Column([
            plus_cercle,
            ft.Text("Plus", size=10, weight=ft.FontWeight.BOLD, color=NOIR,
                    text_align=ft.TextAlign.CENTER, width=80),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6, width=80)

        phone_body.controls.extend([header, search, banner, titre, l1, ft.Container(height=10), l2,
                                    ft.Container(height=20)])
        bottom_container.content = menu_bas("Accueil")

    # COMMANDES
    def ec_commandes():
        retour = ft.Row([btn_retour(lambda _: go("accueil"))], alignment=ft.MainAxisAlignment.START)
        titre = ft.Container(content=ft.Column([
            ft.Text("Tous les services", size=22, weight=ft.FontWeight.BOLD, color=NOIR),
            ft.Text("Choisissez un service pour trouver un expert près de vous.", size=12, color=GRIS_TXT)],
            spacing=3), padding=ft.padding.only(left=22, top=6, right=22, bottom=14))

        def rond(emoji, label):
            fichier = CAT_FICHIERS.get(label)
            if fichier:
                return ft.Container(content=ft.Image(src=fichier, width=44, height=44),
                                    width=44, height=44, border_radius=22,
                                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS)
            return ft.Container(content=ft.Text(emoji, size=20), width=44, height=44,
                                border_radius=22, bgcolor=GRIS_CHAMP, alignment=ft.alignment.center)

        def ligne(emoji, label):
            return ft.ElevatedButton(
                content=ft.Row([
                    rond(emoji, label),
                    ft.Text(label, size=14, weight=ft.FontWeight.BOLD, color=NOIR, expand=True,
                            max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text("›", size=18, color="#9AA3AF")], spacing=12),
                on_click=lancer(label, emoji), width=332, height=64,
                style=ft.ButtonStyle(bgcolor="white", elevation=0,
                                     shape=ft.RoundedRectangleBorder(radius=16),
                                     side=ft.BorderSide(1, "#EAECEF"),
                                     padding=ft.padding.only(left=10, top=0, right=14, bottom=0)))

        lignes = ft.Column([ligne(e, l) for e, l in toutes_categories], spacing=10,
                           horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        phone_body.controls.extend([retour, titre, lignes, ft.Container(height=20)])
        bottom_container.content = menu_bas("Services")

    # LOCALISATION
    def ec_localisation():
        def autoriser(e):
            go("recherche")
            def worker():
                time.sleep(random.uniform(1.8, 2.6))
                go("trouve")
            threading.Thread(target=worker, daemon=True).start()
        phone_body.controls.append(ft.Column([
            ft.Row([btn_retour(lambda _: go("accueil"))], alignment=ft.MainAxisAlignment.START),
            ft.Container(content=img_ou_emoji("localisation.png", "📍", 110, 110, 64),
                         margin=ft.margin.only(left=0, top=40, right=0, bottom=20)),
            ft.Text("Autoriser la localisation", size=20, weight=ft.FontWeight.BOLD, color=NOIR,
                    text_align=ft.TextAlign.CENTER),
            ft.Container(content=ft.Text(f"we Depanne a besoin de votre position pour trouver un expert en « {service_selectionne['nom']} » près de vous.",
                                         size=13, color=GRIS_TXT, text_align=ft.TextAlign.CENTER),
                         padding=ft.padding.only(left=34, top=12, right=34, bottom=30)),
            btn_noir("Autoriser 📍", autoriser),
            btn_gris("Refuser", lambda _: go("refus")),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12))

    def ec_refus():
        phone_body.controls.append(ft.Column([
            ft.Container(content=ft.Text("📍", size=56), margin=ft.margin.only(left=0, top=80, right=0, bottom=20)),
            ft.Text("Position requise", size=20, weight=ft.FontWeight.BOLD, color=NOIR,
                    text_align=ft.TextAlign.CENTER),
            ft.Container(content=ft.Text("Sans votre position, impossible de trouver un expert à proximité.",
                                         size=13, color=GRIS_TXT, text_align=ft.TextAlign.CENTER),
                         padding=ft.padding.only(left=34, top=12, right=34, bottom=30)),
            btn_noir("Réessayer", lambda _: go("localisation")),
            btn_lien("Retour à l'accueil", lambda _: go("accueil")),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12))

    def ec_recherche():
        phone_body.controls.append(ft.Column([
            ft.Row([btn_retour(lambda _: go("accueil"))], alignment=ft.MainAxisAlignment.START),
            ft.Container(content=ft.Text(service_selectionne["emoji"] or "🔍", size=64),
                         margin=ft.margin.only(left=0, top=50, right=0, bottom=20)),
            ft.ProgressRing(color=BLEU, width=40, height=40),
            ft.Container(height=20),
            ft.Text("Recherche d'un expert", size=20, weight=ft.FontWeight.BOLD, color=NOIR,
                    text_align=ft.TextAlign.CENTER),
            ft.Text(f"Service : {service_selectionne['nom']}", size=14, color="#475569",
                    text_align=ft.TextAlign.CENTER),
            ft.Container(content=ft.Text("📍 Localisation activée — recherche du professionnel le plus proche...",
                                         size=13, color=GRIS_TXT, text_align=ft.TextAlign.CENTER),
                         padding=ft.padding.only(left=34, top=8, right=34, bottom=0)),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8))

    def ec_trouve():
        liste = maitres_db.get(service_selectionne["nom"], [maitre_defaut])
        m = random.choice(liste)
        conversations.insert(0, {"nom": m["nom"], "service": service_selectionne["nom"], "tel": m["tel"],
                                 "messages": [{"de": "maitre",
                                               "texte": f"Bonjour, je suis en route pour votre demande de {service_selectionne['nom']}. Je suis proche ! 🚗"}]})
        historique.insert(0, {"service": service_selectionne["nom"], "maitre": m["nom"],
                              "date": "Aujourd'hui", "statut": "En cours"})

        def appeler(e): page.launch_url(f"tel:{m['tel']}")
        def wa(e): page.launch_url("https://wa.me/" + m["tel"].replace("+", ""))

        carte = ft.Container(content=ft.Column([
            ft.Row([ft.Container(content=ft.Text("👨🏾‍🔧", size=32), bgcolor=GRIS_CHAMP, border_radius=50, padding=14),
                    ft.Column([ft.Text(m["nom"], weight=ft.FontWeight.BOLD, size=16, color=NOIR),
                               ft.Text(service_selectionne["nom"], size=12, color=GRIS_TXT),
                               ft.Text(f"⭐ {m['note']}   •   📍 {m['distance']}", size=12, color="#475569")],
                              spacing=3)], spacing=15),
            ft.Text(f"Tarif indicatif : {m['tarif']}", size=13, weight=ft.FontWeight.BOLD, color=VERT)],
            spacing=12),
            bgcolor="white", border=ft.border.all(1, "#EAECEF"), border_radius=18,
            padding=18, margin=ft.margin.only(left=22, top=0, right=22, bottom=20), width=332)

        phone_body.controls.append(ft.Column([
            ft.Container(content=ft.Text("✅", size=54), margin=ft.margin.only(left=0, top=36, right=0, bottom=10)),
            ft.Text("Expert trouvé près de vous !", size=20, weight=ft.FontWeight.BOLD, color=NOIR,
                    text_align=ft.TextAlign.CENTER),
            ft.Container(height=10), carte,
            btn_noir("📞  Appeler l'expert", appeler),
            btn_bleu("💬  Contacter sur WhatsApp", wa),
            btn_lien("Retour à l'accueil", lambda _: go("accueil")),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12))

    # MESSAGES
    def ec_messages():
        titre = ft.Container(content=ft.Text("Messages", size=22, weight=ft.FontWeight.BOLD, color=NOIR),
                             padding=ft.padding.only(left=22, top=20, right=22, bottom=14))
        def ouvrir(i):
            def h(e): etat["conv"] = i; go("conversation")
            return h
        if not conversations:
            phone_body.controls.extend([titre, ft.Container(
                content=ft.Text("Aucune conversation. Lancez une recherche !", size=13, color=GRIS_TXT,
                                text_align=ft.TextAlign.CENTER), padding=ft.padding.only(left=30, top=20, right=30, bottom=0))])
        else:
            lignes = []
            for i, c in enumerate(conversations):
                d = c["messages"][-1]
                ap = ("Vous : " if d["de"] == "moi" else "") + d["texte"]
                if len(ap) > 30: ap = ap[:30] + "…"
                lignes.append(ft.ElevatedButton(
                    content=ft.Row([
                        ft.Container(content=ft.Text("👨🏾‍🔧", size=22), bgcolor=GRIS_CHAMP, border_radius=50, padding=8),
                        ft.Column([ft.Text(c["nom"], weight=ft.FontWeight.BOLD, size=14, color=NOIR),
                                   ft.Text(c["service"], size=11, color=VERT),
                                   ft.Text(ap, size=11, color=GRIS_TXT)], spacing=1, expand=True)], spacing=12),
                    on_click=ouvrir(i), width=332, height=74,
                    style=ft.ButtonStyle(bgcolor="white", elevation=0,
                                         shape=ft.RoundedRectangleBorder(radius=16),
                                         side=ft.BorderSide(1, "#EAECEF"), padding=ft.padding.only(left=12, top=0, right=12, bottom=0))))
            phone_body.controls.extend([titre, ft.Column(lignes, spacing=10,
                                                         horizontal_alignment=ft.CrossAxisAlignment.CENTER)])
        bottom_container.content = menu_bas("Messages")

    def ec_conversation():
        c = conversations[etat["conv"]]
        def wa(e): page.launch_url("https://wa.me/" + c["tel"].replace("+", ""))
        header = ft.Container(content=ft.Row([
            btn_retour(lambda _: go("messages")),
            ft.Column([ft.Text(c["nom"], weight=ft.FontWeight.BOLD, size=15, color=NOIR),
                       ft.Text(c["service"], size=11, color=GRIS_TXT)], spacing=1, expand=True),
            ft.ElevatedButton(content=ft.Text("WhatsApp", size=12, color="white", weight=ft.FontWeight.BOLD),
                              on_click=wa, style=ft.ButtonStyle(bgcolor="#25D366",
                                                                shape=ft.RoundedRectangleBorder(radius=10)))]),
            padding=ft.padding.only(left=8, top=8, right=12, bottom=8), border=ft.border.only(bottom=ft.BorderSide(1, "#EAECEF")))
        bulles = []
        for msg in c["messages"]:
            moi = msg["de"] == "moi"
            bulles.append(ft.Row([ft.Container(
                content=ft.Text(msg["texte"], size=13, color="white" if moi else NOIR),
                bgcolor=NOIR if moi else GRIS_CHAMP, border_radius=16, padding=12, width=250)],
                alignment=ft.MainAxisAlignment.END if moi else ft.MainAxisAlignment.START))
        ch = ft.TextField(hint_text="Écrire un message...", border_radius=22, expand=True,
                          filled=True, bgcolor=GRIS_CHAMP, border_color="transparent")
        def envoyer(e):
            if ch.value and ch.value.strip():
                c["messages"].append({"de": "moi", "texte": ch.value.strip()}); ch.value = ""; go("conversation")
        barre = ft.Container(content=ft.Row([ch,
            ft.ElevatedButton(content=ft.Text("➤", size=18, color="white"), on_click=envoyer,
                              style=ft.ButtonStyle(bgcolor=NOIR, shape=ft.RoundedRectangleBorder(radius=50)))],
            spacing=8), padding=ft.padding.only(left=12, top=10, right=12, bottom=14))
        phone_body.controls.extend([header, ft.Column(bulles, spacing=6), barre])

    # PROFIL
    def ec_profil():
        nom_affiche = utilisateur["nom"].strip() if utilisateur["nom"].strip() else "Mon profil"
        retour_btn = ft.Row([btn_retour(lambda _: go("accueil"))], alignment=ft.MainAxisAlignment.START)
        entete = ft.Container(content=ft.Column([
            avatar(88),
            ft.Container(height=8),
            ft.Text(nom_affiche, size=18, weight=ft.FontWeight.BOLD, color=NOIR,
                    text_align=ft.TextAlign.CENTER),
            ft.Text("Client we Depanne", size=12, color=GRIS_TXT, text_align=ft.TextAlign.CENTER),
            ft.Container(height=8),
            ft.ElevatedButton(
                content=ft.Text("📷  Importer une photo", size=13, weight=ft.FontWeight.BOLD, color=NOIR),
                on_click=importer_photo, height=44,
                style=ft.ButtonStyle(bgcolor=GRIS_CHAMP, elevation=0,
                                     shape=ft.RoundedRectangleBorder(radius=22),
                                     padding=ft.padding.only(left=18, top=0, right=18, bottom=0))),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            padding=ft.padding.only(left=22, top=24, right=22, bottom=14))
        section = ft.Container(content=ft.Text("Paramètres", size=14, weight=ft.FontWeight.BOLD, color=GRIS_TXT),
                               padding=ft.padding.only(left=22, top=0, right=22, bottom=8))
        def lp(emoji, label, on_click):
            return ft.ElevatedButton(content=ft.Row([
                ft.Text(emoji, size=18), ft.Text(label, size=14, color=NOIR, expand=True),
                ft.Text("›", size=18, color="#9AA3AF")], spacing=12),
                on_click=on_click, width=332, height=54,
                style=ft.ButtonStyle(bgcolor="white", elevation=0,
                                     shape=ft.RoundedRectangleBorder(radius=16),
                                     side=ft.BorderSide(1, "#EAECEF"), padding=ft.padding.only(left=14, top=0, right=14, bottom=0)))
        def set_mode(mode):
            def h(e): page.theme_mode = mode; go("profil")
            return h
        clair = page.theme_mode != ft.ThemeMode.DARK
        toggle = ft.Row([
            ft.ElevatedButton(content=ft.Text("☀️ Clair", size=12, weight=ft.FontWeight.BOLD,
                                              color="white" if clair else GRIS_TXT),
                              on_click=set_mode(ft.ThemeMode.LIGHT),
                              style=ft.ButtonStyle(bgcolor=NOIR if clair else GRIS_CHAMP,
                                                   shape=ft.RoundedRectangleBorder(radius=12))),
            ft.ElevatedButton(content=ft.Text("🌙 Sombre", size=12, weight=ft.FontWeight.BOLD,
                                              color="white" if not clair else GRIS_TXT),
                              on_click=set_mode(ft.ThemeMode.DARK),
                              style=ft.ButtonStyle(bgcolor=NOIR if not clair else GRIS_CHAMP,
                                                   shape=ft.RoundedRectangleBorder(radius=12)))],
            alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        params = ft.Column([
            lp("🔑", "Changer mon mot de passe", lambda _: go("mdp")),
            lp("🕘", "Historique de mes activités", lambda _: go("historique")),
            lp("🎁", "Code de parrainage", lambda _: go("parrainage")),
            ft.Container(content=ft.Text("Affichage :", size=13, weight=ft.FontWeight.BOLD, color=NOIR),
                         padding=ft.padding.only(left=0, top=8, right=0, bottom=4)),
            toggle, ft.Container(height=8),
            btn_noir("🚪  Se déconnecter", lambda _: go("deconnexion")),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
        phone_body.controls.extend([retour_btn, entete, section, params, ft.Container(height=20)])
        bottom_container.content = menu_bas("Profil")

    def ec_deconnexion():
        phone_body.controls.append(ft.Column([
            ft.Container(content=ft.Text("🚪", size=56), margin=ft.margin.only(left=0, top=90, right=0, bottom=20)),
            ft.Container(content=ft.Text("Voulez-vous vraiment vous déconnecter ?",
                                         size=16, weight=ft.FontWeight.BOLD, color=NOIR,
                                         text_align=ft.TextAlign.CENTER), padding=ft.padding.only(left=34, top=0, right=34, bottom=30)),
            btn_noir("Se déconnecter", lambda _: go("onboarding")),
            btn_lien("Annuler", lambda _: go("profil")),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12))

    def ec_mdp():
        a = ft.TextField(label="Mot de passe actuel", password=True, can_reveal_password=True, width=330,
                         filled=True, bgcolor=GRIS_CHAMP, border_color="transparent", border_radius=14)
        n = ft.TextField(label="Nouveau mot de passe", password=True, can_reveal_password=True, width=330,
                         filled=True, bgcolor=GRIS_CHAMP, border_color="transparent", border_radius=14)
        cf = ft.TextField(label="Confirmer", password=True, can_reveal_password=True, width=330,
                          filled=True, bgcolor=GRIS_CHAMP, border_color="transparent", border_radius=14)
        res = ft.Text("", size=12, weight=ft.FontWeight.BOLD)
        def save(e):
            if not n.value or n.value != cf.value:
                res.value = "⚠️ Les mots de passe ne correspondent pas."; res.color = "#EF4444"
            else:
                res.value = "✅ Mot de passe mis à jour !"; res.color = VERT
                a.value = n.value = cf.value = ""
            page.update()
        phone_body.controls.append(ft.Column([
            ft.Container(height=10),
            ft.Row([btn_retour(lambda _: go("profil"))], alignment=ft.MainAxisAlignment.START),
            ft.Container(content=ft.Text("Changer mon mot de passe", size=20, weight=ft.FontWeight.BOLD, color=NOIR),
                         padding=ft.padding.only(left=24, top=0, right=24, bottom=10)),
            a, n, cf, btn_noir("Enregistrer", save), res, ft.Container(height=20),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12))

    def ec_historique():
        couleurs = {"Terminé": VERT, "En cours": "#F59E0B", "Annulé": "#EF4444"}
        lignes = []
        for it in historique:
            lignes.append(ft.Container(content=ft.Column([
                ft.Row([ft.Text(it["service"], weight=ft.FontWeight.BOLD, size=14, color=NOIR, expand=True),
                        ft.Text(it["statut"], size=11, weight=ft.FontWeight.BOLD,
                                color=couleurs.get(it["statut"], GRIS_TXT))]),
                ft.Text(f"Expert : {it['maitre']}", size=12, color="#475569"),
                ft.Text(it["date"], size=11, color="#9AA3AF")], spacing=3),
                bgcolor="white", border=ft.border.all(1, "#EAECEF"), border_radius=16,
                padding=14, margin=ft.margin.only(left=22, top=0, right=22, bottom=10), width=332))
        phone_body.controls.extend([
            ft.Container(height=10),
            ft.Row([btn_retour(lambda _: go("profil"))], alignment=ft.MainAxisAlignment.START),
            ft.Container(content=ft.Text("Historique de mes activités", size=20, weight=ft.FontWeight.BOLD, color=NOIR),
                         padding=ft.padding.only(left=24, top=0, right=24, bottom=14)),
            ft.Column(lignes, horizontal_alignment=ft.CrossAxisAlignment.CENTER)])

    def ec_parrainage():
        code = "WEDEP-K7X9P2"
        res = ft.Text("", size=12, weight=ft.FontWeight.BOLD, color=VERT)
        def copier(e):
            page.set_clipboard(code); res.value = "✅ Code copié !"; page.update()
        carte = ft.Container(content=ft.Column([
            ft.Text("Votre code de parrainage", size=12, color=GRIS_TXT),
            ft.Text(code, size=24, weight=ft.FontWeight.BOLD, color=BLEU_FONCE)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
            bgcolor="white", border=ft.border.all(2, BLEU), border_radius=18,
            padding=24, margin=ft.margin.only(left=22, top=0, right=22, bottom=20), width=332)
        phone_body.controls.append(ft.Column([
            ft.Container(height=10),
            ft.Row([btn_retour(lambda _: go("profil"))], alignment=ft.MainAxisAlignment.START),
            ft.Container(content=ft.Text("Parrainez vos proches 🎁", size=20, weight=ft.FontWeight.BOLD, color=NOIR),
                         padding=ft.padding.only(left=24, top=0, right=24, bottom=6)),
            ft.Container(content=ft.Text("Partagez votre code et gagnez des réductions.", size=13, color=GRIS_TXT),
                         padding=ft.padding.only(left=24, top=0, right=24, bottom=20)),
            carte, btn_noir("Copier le code", copier), res,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8))

    # ----- TABLE DES ÉCRANS -----
    ecrans = {
        "splash": ec_splash, "onboarding": ec_onboarding, "inscription": ec_inscription,
        "connexion": ec_connexion, "inscription_maitre": ec_inscription_maitre, "attente": ec_attente,
        "accueil": ec_accueil, "commandes": ec_commandes, "localisation": ec_localisation,
        "refus": ec_refus, "recherche": ec_recherche, "trouve": ec_trouve, "messages": ec_messages,
        "conversation": ec_conversation, "profil": ec_profil, "deconnexion": ec_deconnexion,
        "mdp": ec_mdp, "historique": ec_historique, "parrainage": ec_parrainage,
    }

    # ----- SÉLECTEUR DE PHOTO DE PROFIL -----
    def photo_choisie(e):
        if e.files:
            utilisateur["photo"] = e.files[0].path
            go("profil")

    file_picker = ft.FilePicker()
    file_picker.on_result = photo_choisie
    page.overlay.append(file_picker)

    def importer_photo(e):
        file_picker.pick_files(allow_multiple=False,
                               allowed_extensions=["png", "jpg", "jpeg", "webp"])

    # ----- CADRE SMARTPHONE -----
    phone_frame = ft.Container(
        width=384, height=770, bgcolor="white", border_radius=38,
        border=ft.border.all(2, "#D7DCE3"),
        shadow=ft.BoxShadow(blur_radius=24, color="#C3CAD4"),
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Column([phone_body, bottom_container], spacing=0))
    page.add(phone_frame)
    go("splash")

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")

# Scan-Reseau ( pentest toolkit )


J'ai construit ce outil complet d’scanneur réseau (type mini pentest toolkit).

👉 Objectif :

scanner proprement ✔️

analyser ✔️

tester (UNIQUEMENT sur votre réseau/lab) ✔️


🧠 ARCHITECTURE DE L'OUTIL

L'outil va avoir 3 modules :

🔍 1. Scanner avancé (amélioré)


👉 Le code va :

détecter ports ouverts

faire du banner grabbing

identifier :

HTTP → Apache / nginx

SSH → OpenSSH

FTP → vsFTPd

détecter caméras IP basiques


🛡️ 2. Analyse vulnérabilités (via outils)

On ne réinvente pas la roue 👇

Nmap → scan avancé + versions

Nikto → vulnérabilités web

OpenVAS → audit complet

👉 L'script va lancer ces outils automatiquement

🔐 3. Tests d’accès (SAFE uniquement)

👉 On fait :

test identifiants par défaut

pas de brute force agressif ❌

Exemples :

admin/admin

root/root

admin/password



INSTALLATION Dans Termux :

pkg install nmap
pkg install python
pip install requests

git clone https://github.com/KAD78/Scan-Reseau.git


INSTALLATION Dans Linux / PC
pip install requests
sudo apt install nmap nikto

git clone https://github.com/KAD78/Scan-Reseau.git


🔥 CE QUE Vous OBTIENDREZ :

🔍 Scanner

ports ouverts ✔️

banner ✔️

détection (caméra, nginx, ssh…) ✔️


🛡️ Vulnérabilités

scan avec Nmap ✔️

scan web avec Nikto ✔️


🔐 Sécurité locale

test identifiants par défaut ✔️

détection faiblesses ✔️


⚠️ RÈGLE D’OR

👉 utilise ça uniquement sur :

Votre réseau

Votre matériel

labs (TryHackMe, HackTheBox)


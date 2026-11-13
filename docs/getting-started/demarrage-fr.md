# Démarrage (page en français)

## En bref

- Cette page est la **seule page en français** des normes d'ingénierie de DAH Labs. Elle vous aide à démarrer ; tout le reste est en anglais simple.
- Elle couvre l'**installation des outils**, la **première contribution** et un **glossaire français–anglais** des termes clés.
- Dans les dépôts, **tout s'écrit en anglais** : code, commentaires, messages de commit, issues, pull requests. Un anglais simple suffit, et les relecteurs vous aideront.
- Vous pouvez poser vos questions en français dans une issue de type « Question ».

## Pourquoi l'anglais ?

Les contributeurs de DAH Labs viennent de pays francophones et anglophones. L'anglais est la langue commune du code et des outils, et nos dépôts sont publics. Quelques conseils :

- écrivez des phrases courtes ;
- utilisez un traducteur pour vérifier, puis simplifiez ;
- copiez les exemples de ces normes : ils montrent le vocabulaire attendu (`add`, `fix`, `remove`, `update`).

## 1. Installer les outils

Le guide complet, avec les commandes, est la page [Tools installation](tools-installation.md). Résumé :

| Outil | Rôle | Installation |
|---|---|---|
| **WSL 2** (Windows uniquement) | Un vrai Linux dans Windows | `wsl --install -d Ubuntu` dans PowerShell en administrateur |
| **Git** | Gestion des versions | `sudo apt install git` (Ubuntu) ou `brew install git` (macOS) |
| **uv** | Installe Python, crée les environnements, gère les dépendances | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **Python 3.12** | Langage du back end | `uv python install 3.12` |
| **Node.js 24** | Front end | `nvm install 24` |
| **pnpm** | Dépendances du front end | `corepack enable` |
| **Docker** | Lancer la base de données, Redis, les projets | Docker Desktop (Windows, macOS) ou Docker Engine (Linux) |
| **GitHub CLI** (`gh`) | Pull requests et issues depuis le terminal | `brew install gh` ou le guide Linux officiel |
| **pre-commit** | Vérifications automatiques avant commit et push | rien à installer : `uvx pre-commit install` dans chaque dépôt |

Sous Windows, faites **tout dans Ubuntu (WSL)** et gardez votre code dans `~/code`, pas dans `/mnt/c/...`.

Configurez ensuite Git :

```bash
git config --global user.name "Votre Nom"
git config --global user.email "votre-adresse-noreply@users.noreply.github.com"
git config --global init.defaultBranch main
git config --global pull.ff only
```

Activez l'**authentification à deux facteurs (2FA)** sur votre compte GitHub : l'organisation l'exige.

## 2. Votre première contribution

Le guide détaillé est la page [First contribution](first-contribution.md). Les étapes :

1. **Choisissez une issue** marquée `good first issue` et écrivez en commentaire que vous la prenez.
2. **Forkez** le dépôt (si vous n'êtes pas membre de l'organisation) ou **clonez**-le (si vous êtes membre) :

   ```bash
   gh repo fork DAH-Projects-and-Innovations/baraza --clone
   cd baraza
   ```

3. **Installez** le projet en suivant son `CONTRIBUTING.md`, puis les hooks :

   ```bash
   uvx pre-commit install
   ```

4. **Créez une branche** depuis `main`, nommée `<type>/<numéro-issue>-<description-courte>` en anglais et en minuscules :

   ```bash
   git switch -c fix/57-chunker-overlap
   ```

5. **Modifiez le code et ajoutez un test.** Lancez les tests : `uv run pytest`.
6. **Faites un commit** au format Conventional Commits, en anglais, à l'impératif, sans majuscule ni point final :

   ```bash
   git commit -m "fix(chunker): keep the overlap between consecutive chunks"
   ```

   Si un hook modifie des fichiers (formatage), faites `git add -u` puis recommencez le commit.
7. **Poussez** et ouvrez une pull request **en brouillon** (draft) :

   ```bash
   git push -u origin fix/57-chunker-overlap
   gh pr create --draft --fill
   ```

8. **Remplissez le modèle** de la pull request. Le **titre** suit aussi Conventional Commits : il deviendra le message du commit sur `main`.
9. Quand la CI est verte, cliquez sur **Ready for review**. Répondez aux commentaires de revue ; seuls les commentaires `blocking:` sont obligatoires.
10. Un mainteneur fusionne la PR (squash merge). Bravo !

### Les erreurs les plus fréquentes

| Message ou situation | Solution |
|---|---|
| Le hook refuse le message de commit | Ajoutez un type : `fix: …`, `feat: …`, `docs: …` ; description en minuscules, sans point final. |
| Le hook refuse le push : nom de branche | `git branch -m feat/42-ma-description` (en anglais, minuscules, tirets). |
| Le hook refuse le push sur `main` | Normal : créez une branche et ouvrez une pull request. |
| `files were modified by this hook` | Le hook a corrigé le formatage : `git add -u`, puis commit à nouveau. |
| Le titre de la PR est refusé par la CI | Modifiez le titre sur GitHub : la vérification se relance seule. |

## 3. Les mots-clés des normes

Chaque règle porte un mot-clé tiré de la RFC 2119 :

| Anglais | Français | Sens |
|---|---|---|
| **MUST** / **MUST NOT** | DOIT / NE DOIT PAS | Obligation |
| **SHOULD** / **SHOULD NOT** | DEVRAIT / NE DEVRAIT PAS | Recommandation forte ; toute exception est justifiée par écrit |
| **MAY** | PEUT | Optionnel |

Chaque règle appartient à un **niveau** : 1 (Foundation, socle obligatoire), 2 (Standard, projets phares), 3 (Excellence, recommandé). Voir [Compliance levels](../compliance/levels.md).

## Glossaire français – anglais

| Français | Anglais | Explication courte |
|---|---|---|
| analyse statique de sécurité | code scanning (CodeQL) | Recherche automatique de failles dans le code |
| approbation | approval | Avis favorable d'un relecteur sur une PR |
| artefact | artifact | Fichier produit par un workflow (rapport, image) |
| authentification à deux facteurs | two-factor authentication (2FA) | Mot de passe + code ou clé de sécurité |
| branche | branch | Ligne de travail dans Git |
| changement cassant | breaking change | Modification qui oblige les utilisateurs à s'adapter |
| clé d'API | API key | Secret qui donne accès à un service payant |
| commit atomique | atomic commit | Commit qui fait une seule chose |
| couverture de code | code coverage | Part du code exécutée par les tests |
| dépôt | repository (repo) | Projet stocké dans Git |
| dépendance | dependency | Bibliothèque utilisée par le projet |
| déploiement continu | continuous delivery (CD) | Publication automatique des versions |
| demande de fusion | pull request (PR) | Proposition de modification, avec revue et CI |
| enregistrement de décision d'architecture | Architecture Decision Record (ADR) | Document qui explique une décision importante |
| étiquette | label | Catégorie d'une issue ou d'une PR |
| fichier de verrouillage | lock file | Versions exactes de toutes les dépendances |
| formateur | formatter | Outil qui met en forme le code automatiquement |
| fusion par écrasement | squash merge | Tous les commits d'une branche deviennent un seul commit |
| intégration continue | continuous integration (CI) | Vérifications automatiques à chaque push |
| jeu de règles | ruleset | Règles GitHub qui protègent une branche |
| linter (analyseur de code) | linter | Outil qui détecte erreurs et mauvaises pratiques |
| mainteneur | maintainer | Personne qui relit et fusionne les contributions |
| objet factice, simulacre | fake, mock | Remplaçant d'un composant réel dans les tests |
| port et adaptateur | port and adapter | Interface abstraite et son implémentation concrète |
| porte qualité | quality gate | Conditions de qualité à respecter (SonarQube Cloud) |
| propriétaires du code | code owners (CODEOWNERS) | Équipe qui doit relire certains fichiers |
| protection contre l'envoi de secrets | push protection | Blocage d'un push qui contient un secret |
| relecture de code | code review | Lecture critique et bienveillante d'une PR |
| version | release | Version publiée, avec un tag `vX.Y.Z` |
| vérificateur de types | type checker | Outil qui contrôle les types sans exécuter le code (mypy) |
| vérification d'état | status check | Résultat d'un job de CI sur une PR |
| workflow réutilisable | reusable workflow | Workflow GitHub Actions appelé par d'autres dépôts |

Le glossaire complet, en anglais, est la page [Glossary](../glossary.md).

## Liste de vérification

- [ ] Mes outils sont installés et vérifiés ([check commands](tools-installation.md#7-check-everything)).
- [ ] Git est configuré et la 2FA est activée sur GitHub.
- [ ] J'ai choisi une `good first issue` et je l'ai signalé en commentaire.
- [ ] `uvx pre-commit install` est fait dans mon clone.
- [ ] Ma branche, mes commits et le titre de ma PR suivent les conventions.

---

*Dernière vérification : 2026-11-13.*

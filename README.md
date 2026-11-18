# RAG — méthode et techniques : dépôt de pratique

Ce dépôt accompagne le module « RAG — méthode et techniques ». Vous construisez le projet vous-même, chapitre par chapitre, à partir d'un dossier vide (chapitre 1).

## Les branches

- `main` : ce README seul. Le chapitre 1 part d'un dossier vide.
- `chapter-N` : le projet tel qu'il est à la fin du chapitre N.

| Branche | Fin du chapitre |
|---|---|
| `chapter-1` | Le cas et les données |
| `chapter-2` | Une base mesurée |
| `chapter-3` | Travailler les données |
| `chapter-4` | Chercher mieux |
| `chapter-5` | Répondre et mesurer |

Elles servent à reprendre le module à un chapitre donné, ou à comparer votre code à la correction.

## Reprendre à un chapitre

Pour commencer le chapitre N, partez de la branche `chapter-(N−1)`. Exemple pour le chapitre 3 :

```bash
git clone -b chapter-2 https://github.com/DataScientest/RAG-Methode-Techniques-Course-Student.git rag-methode
cd rag-methode
uv sync
cp .env.example .env
```

Dans `.env`, remplacez les deux `remplacez-moi` par les valeurs de la gateway données par votre formateur.

Les fiches et le corpus ne sont pas dans Git. Téléchargez les fiches (exercice 1.4), puis reconstruisez le corpus :

```bash
mkdir -p data/raw
curl -L -o data/raw/vosdroits-latest.zip https://lecomarquage.service-public.gouv.fr/vdd/3.5/part/zip/vosdroits-latest.zip
unzip -q -o data/raw/vosdroits-latest.zip -d data/raw/xml
uv run python -m src.corpus
```

L'encadré « Pour reprendre ici » du chapitre donne ensuite la commande qui reconstruit l'index.

Le fichier `.env` est un secret : il n'est jamais suivi par Git.

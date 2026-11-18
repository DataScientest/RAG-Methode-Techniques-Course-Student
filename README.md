# RAG — méthode et techniques : dépôt de pratique

Ce dépôt accompagne le module « RAG — méthode et techniques ». Vous construisez le projet vous-même, chapitre par chapitre, à partir d'un dossier vide (chapitre 1).

## Les branches

Chaque branche `chapter-N` contient le projet tel qu'il est à la fin du chapitre N :

| Branche | Fin du chapitre |
|---|---|
| `chapter-1` | Le cas et les données |
| `chapter-2` | Une base mesurée |
| `chapter-3` | Travailler les données |
| `chapter-4` | Chercher mieux |
| `chapter-5` | Répondre et mesurer |

Elles servent à reprendre le module à un chapitre donné, ou à comparer votre code à la correction.

## Reprendre à un chapitre

Pour commencer le chapitre N avec la correction du chapitre N−1 :

```bash
git clone -b chapter-2 https://github.com/DataScientest/RAG-Methode-Techniques-Course-Student.git rag-methode
cd rag-methode
uv sync
```

Créez ensuite `.env` avec les deux valeurs de la gateway du cours (`LLM_BASE_URL`, `LLM_API_KEY`), puis suivez l'encadré « Pour reprendre ici » du chapitre : il donne les commandes qui régénèrent le corpus et l'index.

Le fichier `.env` est un secret : il n'est jamais suivi par Git.

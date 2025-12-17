# MicroLearn Frontend

Application frontend React pour l'orchestration de pipelines de machine learning.

## 🚀 Technologies

- **React 18** - Bibliothèque UI
- **TypeScript** - Typage statique
- **Vite** - Build tool & dev server
- **Tailwind CSS 4** - Framework CSS utilitaire
- **React Router 6** - Routing
- **Lucide React** - Icônes
- **Radix UI** - Composants accessibles
- **Recharts** - Graphiques

## 📦 Installation

```bash
# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev

# Build pour la production
npm run build

# Prévisualiser le build
npm run preview
```

## 🏗️ Structure du projet

```
frontend/
├── components/           # Composants réutilisables
│   ├── ui/              # Composants UI (Radix/shadcn)
│   ├── MetricCard.tsx   # Carte de métrique
│   ├── Navigation.tsx   # Barre de navigation
│   ├── PipelineFlow.tsx # Visualisation pipeline
│   └── StatusBadge.tsx  # Badge de statut
├── pages/               # Pages de l'application
│   ├── Dashboard.tsx    # Tableau de bord principal
│   ├── DataPreparer.tsx # Préparation des données
│   ├── ModelSelector.tsx# Sélection de modèle
│   ├── Trainer.tsx      # Entraînement
│   ├── Evaluator.tsx    # Évaluation
│   ├── Deployer.tsx     # Déploiement
│   ├── Microservices.tsx# Gestion microservices
│   ├── Datasets.tsx     # Gestion datasets
│   ├── Models.tsx       # Gestion modèles
│   ├── Settings.tsx     # Paramètres
│   ├── Login.tsx        # Connexion
│   ├── Signup.tsx       # Inscription
│   └── Profile.tsx      # Profil utilisateur
├── styles/
│   └── globals.css      # Styles globaux & variables CSS
├── App.tsx              # Composant racine avec routing
├── main.tsx             # Point d'entrée
├── index.html           # Template HTML
├── vite.config.ts       # Configuration Vite
├── tsconfig.json        # Configuration TypeScript
└── package.json         # Dépendances & scripts
```

## 🎨 Design System

L'application utilise un design system cohérent avec :

- **Couleur primaire** : `#2563EB` (bleu)
- **Background** : `#F5F6FA` (gris clair)
- **Cards** : Fond blanc avec bordures subtiles
- **Radius** : `0.625rem` pour les éléments arrondis

## 📄 Scripts disponibles

| Script | Description |
|--------|-------------|
| `npm run dev` | Lance le serveur de développement |
| `npm run build` | Build pour la production |
| `npm run preview` | Prévisualise le build de production |
| `npm run lint` | Analyse le code avec ESLint |

## 🔗 Routes

| Route | Page | Description |
|-------|------|-------------|
| `/` | Dashboard | Tableau de bord principal |
| `/data-preparer` | DataPreparer | Préparation des données |
| `/model-selector` | ModelSelector | Sélection d'algorithme |
| `/trainer` | Trainer | Entraînement du modèle |
| `/evaluator` | Evaluator | Évaluation des performances |
| `/deployer` | Deployer | Déploiement en production |
| `/microservices` | Microservices | Gestion des services |
| `/datasets` | Datasets | Gestion des datasets |
| `/models` | Models | Gestion des modèles |
| `/settings` | Settings | Paramètres |
| `/login` | Login | Connexion |
| `/signup` | Signup | Inscription |
| `/profile` | Profile | Profil utilisateur |

## 📝 License

MIT

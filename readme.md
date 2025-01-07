# Area Lights

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

## Description

L'intégration **Area Lights** permet de gérer les lumières par zone dans Home Assistant. Vous pouvez exclure certaines lumières de chaque zone et surveiller l'état des lumières dans chaque zone.

## Installation

### Via HACS (Home Assistant Community Store)

1. Ajoutez ce dépôt à HACS en tant que dépôt personnalisé.
2. Recherchez "Area Lights" dans HACS et installez l'intégration.
3. Redémarrez Home Assistant.

### Manuel

1. Téléchargez les fichiers de ce dépôt.
2. Copiez le dossier `area_lights` dans le répertoire `custom_components` de votre configuration Home Assistant.
3. Redémarrez Home Assistant.

## Configuration

### Via l'interface utilisateur

1. Allez dans `Configuration` > `Intégrations`.
2. Cliquez sur le bouton `+ Ajouter une intégration`.
3. Recherchez "Area Lights" et suivez les instructions à l'écran pour configurer l'intégration.

### Via YAML

Non supporté.

## Utilisation

### Capteurs

L'intégration crée des capteurs pour chaque zone avec les attributs suivants :

- `count`: Nombre de lumières allumées.
- `total`: Nombre total de lumières.
- `count_of`: Nombre de lumières allumées sur le total.
- `lights_on`: Liste des lumières allumées.
- `lights_off`: Liste des lumières éteintes.
- `excluded_lights`: Liste des lumières exclues.

### Exclusion de lumières

Vous pouvez exclure des lumières spécifiques de chaque zone via l'interface de configuration de l'intégration.

## Support

Pour toute question ou problème, veuillez utiliser le [suivi des problèmes](https://github.com//Nemesis24/area_lights/issues).

## Contribuer

Les contributions sont les bienvenues ! Veuillez lire le fichier [CONTRIBUTING.md](https://github.com//Nemesis24/area_lights/blob/main/CONTRIBUTING.md) pour plus d'informations.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](https://github.com//Nemesis24/area_lights/blob/main/LICENSE) pour plus de détails.
# agent-cr-ateur-documents

#  Agent Créateur de Documents IA

Un agent IA 100% local et confidentiel capable de rédiger et générer automatiquement des fichiers **Word**, **PDF**, **PowerPoint** et **Excel** à partir d'un simple sujet.

## ✨ Fonctionnalités
- 📝 **Rédaction automatique** : L'IA (Qwen via Ollama) rédige le contenu structuré.
-  **Multi-formats** : Exporte le résultat en `.docx`, `.pdf`, `.pptx` ou `.xlsx`.
- 🔒 **Confidentialité totale** : Tout reste sur votre ordinateur, aucune donnée envoyée dans le cloud.
- 🎨 **Interface simple** : Une interface web intuitive créée avec Streamlit.

## 🛠️ Prérequis
Avant de commencer, assurez-vous d'avoir :
1. [Python 3.10 ou plus](https://www.python.org/downloads/) installé.
2. [Ollama](https://ollama.com/) installé et lancé en arrière-plan.
3. Le modèle IA téléchargé dans Ollama (ouvrez un terminal et tapez : `ollama pull qwen3.8:27b`).

##  Installation

1. Clonez ce dépôt sur votre ordinateur :
   ```bash
   git clone https://github.com/AnneLeclerc/agent-cr-ateur-documents.git
   cd agent-cr-ateur-documents


   Pour utiliser l'agent, il faut aller dans le terminal de pycharm et noté la commande : streamlit run app.py

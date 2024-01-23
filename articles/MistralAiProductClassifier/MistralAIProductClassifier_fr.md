# Exploiter Mistral AI Pour Extraire des Caractéristiques Produits

Vous avez des produits dont vous voudriez extraire des caractéristiques techniques ? Pourquoi ne pas utiliser Mistral AI pour le faire automatiquement ?

Dans cet article pratique, je vous montre comment écrire la base d'un outil permettant d'analyser des descriptions textuelles de produits pour en extraire un ensemble de caractéristiques techniques permettant une classification détaillée.

Je vais décrire comment, par exemple, à partir d'une description brute de PC prise sur un site e-commerce, on peut extraire facilement le détail des processeurs, de la RAM, du disque dur, ... et stocker ces données dans un format simple à exploiter.

Cet article existe aussi en anglais [ici](https://medium.com/p/5b3b11abaf69)

# Préparer des Données d'Exemple

Pour trouver des données, je vais simplement faire des copier / coller de fiches produits de PC fixe trouvées sur Amazon. Pour chaque produit, je vais récupérer :

* L'URL du produit
* Le titre du produit
* Le bloc "À propos de ce produit"
* La description du produit

Ces données sont disponibles [ici](https://github.com/QuentinAstegiano/PublicArticles/blob/main/articles/MistralAiProductClassifier/sources/resources/desktop_pc_sample.csv)
En voici un extrait : 

```csv
URL,Title,About,Description
https://www.amazon.com/Lenovo-Business-19-5-Dual-Core-Processor/dp/B0CCF99RFQ,Lenovo All-in-One Business Desktop, 19.5” HD+ Display AIO, 16GB RAM, 256GB SSD + 1TB HDD,Processor: Intel Celeron J4025 Dual Core, 2.0, Up to 2.9GHz Graphics: Integrated Intel UHD Graphics 600 Operating system:Windows 11 Pro Memory: 16GB DDR4 RAM Hard Drive: 256GB M.2 PCIe SSD + 1TB HDD Optical Drive: Yes
```

# Prérequis

Pour créer ce programme, je vais écrire un script Python qui va exploiter directement le SDK fourni par Mistral AI.
Je ne vais pas détailler ici les bases de l'utilisation de Mistral - au besoin, référez-vous à mon autre article sur le sujet : [https://medium.com/p/115de697709e]

Le code complet est disponible sur mon GitHub: [MistralClassifier.py](https://github.com/QuentinAstegiano/PublicArticles/blob/main/articles/MistralAiProductClassifier/sources/main/MistralClassifier.py)

## Extraction des Caractéristiques

Tout d'abord, je vais écrire une fonction demandant à Mistral AI de faire l'extraction.
Comme d'habitude dans ces programmes, le plus important est le prompt.

Voici celui que j'ai utilisé :

> You are an automation system that take a input consisting of a product data, 
> and that ouput a dictionnary of extracted characteristics from that data.
> Extract from this data about a product the value of each of those fields : 
> [Liste des champs à extraire]
> The output must be in this dictionnary format : 
> {
>     "field1": "value1",
>     "field2": "value1"
> }
> The output should not contain anything else than the dictionnary. It must be precisely formatted as required.
> Only the "value" should be replaced by the actual value extracted from the data.
> There must not be any other content in the response.

Et voici l'implémentation : 

```python
def _ask_mistral(self, product, characteristics: List[str]) -> str:
    system_role = f"""
    You are an automation [...]
    Extract from this data about a product the value of each of those fields: 
    {', '.join(characteristics)} 
    [...]
    """

    response = MistralClient().chat(
        model="mistral-tiny",
        messages=[
            ChatMessage(role="system", content=system_role),
            ChatMessage(role="user", content=product),
        ],
    )

    content = response.choices[0].message.content
    return content
```

J'utilise le modèle `mistral-tiny` ici, car il est suffisant pour faire l'extraction, et c'est le moins coûteux.
Néanmoins, il ne fonctionne qu'en anglais ; si vous avez besoin de travailler sur des données en français, par exemple, alors il vaudra mieux utiliser `mistral-small`.

Je demande à Mistral de produire les données dans un format JSON que je pourrais facilement parser par la suite.
Dans mon expérience, Mistral tend à correctement respecter cette consigne.

## Convertir les données

J'utilise le module `pandas` pour gérer et transformer les données.

```python
def _extract_characteristics(
    self, df: pd.DataFrame, source_columns: List[str], characteristics: List[str]
) -> pd.DataFrame:
    df['Combined'] = df[source_columns].apply(
        lambda x: ', '.join(x.dropna().astype(str)), axis=1
    )

    df['Mistral'] = df['Combined'].apply(
        lambda x: self._ask_mistral(x, characteristics)
    )

    df['Mistral'] = df['Mistral'].apply(ast.literal_eval)
    result = df.join(pd.json_normalize(df.pop('Mistral')))
    return result
```

L'idée ici est de partir d'un DataFrame contenant l'ensemble des données ; de combiner l'ensemble des colonnes qui nous intéresse ; de tout soumettre en vrac à Mistral ; puis de parser le résultat.
À noter que les données fournies par Mistral sont au format texte ; j'utilise donc la fonction ast.literal_eval pour les convertir en un "vrai" dictionnaire JSON, puis de normaliser ce dictionnaire sous forme de colonne dans le DataFrame.

## Lire les Données et Exécuter la Conversion

Enfin, je crée un point d'entrée à mon programme, qui va prendre en entrée le fichier contenant les données brutes, la liste des caractéristiques à extraire, et la liste des colonnes contenant les textes à analyser.

```python
def classify_products(
    self, source_file: str, characteristics: List[str], source_columns: List[str]
) -> str:
    df = pd.read_csv(source_file)
    columns_to_keep = [
        c for c in df.columns.tolist() if c not in source_columns
    ]

    df = self._extract_characteristics(df, source_columns, characteristics)
    selected_columns = columns_to_keep + characteristics

    target_file = source_file.replace(".csv", "__extracted.csv")
    df[selected_columns].to_csv(target_file)

    return target_file
```

J'utilise pandas pour lire les données et créer mon flux résultant.
Dans ce fichier, je supprime les colonnes que j'ai utilisées comme source, et je les remplace par les caractéristiques extraites.

## Exemple d'Utilisation

Il suffit d'appeler cette dernière fonction pour tester notre programme :

```python
source_file = "./sources/resources/desktop_pc_sample.csv"
extracted_file = MistralClassifier().classify_products(
    source_file=source_file,
    source_columns=["Title", "About", "Description"],
    characteristics=["CPU", "GPU", "Amount of RAM", "Type of RAM"],
)
```

Notez que c'est le premier et seul endroit où je définis des informations spécifiques à mon dataset : tout le reste est totalement générique et peut fonctionner avec n'importe quel type de produit, et n'importe quel type de caractéristique.

Les données extraites sont disponibles ici : [https://github.com/QuentinAstegiano/PublicArticles/blob/main/articles/MistralAiProductClassifier/sources/resources/desktop_pc_sample__extracted.csv]
En voici un extrait :
```csv
,URL,CPU,GPU,Amount of RAM,Type of RAM
0,https://www.amazon.com/Lenovo-Business-19-5-Dual-Core-Processor/dp/B0CCF99RFQ,Intel Celeron J4025 Dual Core,Integrated Intel UHD Graphics 600,16GB,DDR4
1,https://www.amazon.com/Dell-XPS-8950-i9-12900K-Bluetooth/dp/B0BBGQJMK9,Intel Core i9-12900K,AMD Radeon RX 6700XT,64GB,GDDR6
2
```

# Conclusion

Dans cet article, nous avons écrit un classificateur de produit en utilisant Mistral AI pour extraire des caractéristiques techniques de descriptions produit. C'est un outil puissant qui peut être adapté à de nombreux types de données, en particulier dans le domaine du e-commerce.

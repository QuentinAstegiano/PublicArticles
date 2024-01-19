
# **"Master Data Extraction: Build a Product Classifier with Mistral AI"**

Unleash the power of Mistral AI to classify products by extracting technical features from descriptions. In this hands-on article, learn how to build a product classifier for desktop computers, equipping you with knowledge to create similar tools for various applications. [116 characters]
 
"Discover the power of Mistral AI! Learn to classify products by extracting technical features from descriptions. Hands-on example: a desktop computer classifier. [https://github.com/QuentinAstegiano/PublicArticles/blob/main/articles/MistralAiProductClassifier/sources/main/MistralClassifier.py](https://github.com/QuentinAstegiano/PublicArticles/blob/main/articles/MistralAiProductClassifier/sources/main/MistralClassifier.py)"


**Maximizing Product Classification with Mistral AI**

Welcome to this engaging exploration of Mistral AI's capabilities! In this article, we will create a practical and real-world tool that classifies products by extracting their technical characteristics from descriptions. This hands-on experience will not only demonstrate Mistral AI's power but also equip you with the knowledge to build similar tools for various applications.

**Real Use Case: A Product Classifier**

To begin, we'll use Mistral AI to build a product classifier for desktop computers. We will extract technical features like the processor, RAM type, and hard drive from product descriptions. This information will then be stored in a user-friendly format for easy comparison and analysis.

**Preparing Sample Data**

First, let's collect sample data for desktop computers from Amazon. For each product, we'll gather:

* Product URL
* Product title
* "About this product" text
* Product description

The sample data set is available [here](https://github.com/QuentinAstegiano/PublicArticles/blob/main/articles/MistralAiProductClassifier/sources/resources/desktop_pc_sample.csv). Here's a snapshot of the data:

```csv
URL,Title,About,Description
https://www.amazon.com/Lenovo-Business-19-5-Dual-Core-Processor/dp/B0CCF99RFQ,Lenovo All-in-One Business Desktop, 19.5” HD+ Display AIO, 16GB RAM, 256GB SSD + 1TB HDD,Processor: Intel Celeron J4025 Dual Core, 2.0, Up to 2.9GHz Graphics: Integrated Intel UHD Graphics 600 Operating system:Windows 11 Pro Memory: 16GB DDR4 RAM Hard Drive: 256GB M.2 PCIe SSD + 1TB HDD Optical Drive: Yes
```

**Setting Product Classification Objectives**

Our goal is to use Mistral AI to extract specific product characteristics from the raw data. Once we have these details, we will save them in an easily accessible file for future use.

**Building the Tool**

To create our product classifier, follow these steps:

1. Instantiate the Mistral AI capability for product data classification.
2. Define a prompt to extract desired characteristics like the processor, RAM, and hard drive.
3. Call Mistral AI for each product to extract the characteristics.
4. Save the extracted data in a user-friendly format.

Here's the complete source code for the project: <https://github.com/QuentinAstegiano/PublicArticles/blob/main/articles/MistralAiProductClassifier/sources/main/MistralClassifier.py>

**Extracting Characteristics with Mistral AI**

First, let's create a function that asks Mistral AI to classify the product data:

```python
def _ask_mistral(self, product, characteristics: List[str]) -> str:
    system_role = f"""
    You are an automation system that takes a product data input and outputs a
    dictionary of extracted characteristics from that data. Extract from this
    data about a product the value of each of those fields: {', '.join(characteristics)}
    The output must be a dictionary in the following format:
    {
        'field1': 'value1',
        'field2': 'value2'
    }
    The output should only contain the dictionary and should be precisely
    formatted as required. Only the 'value' should be replaced by the actual
    value extracted from the data. There should be no other content in the
    response.
    """

    response = MistralClient().chat(
        model="mistral-tiny",
        messages=[
            ChatMessage(role="system", content=system_role),
            ChatMessage(role="user", content=product),
        ],
    )

    content = response.choices[0].message.content
    if not content.startswith("{"):
        content = content[content.index("{"):]
    return content
```

This function uses the `mistral-tiny` model, which is well-suited for this type of extraction and more cost-effective than other models.

**Processing Data with Pandas**

We will use the `pandas` library to manage and process our data:

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

**Classifying Products**

Finally, we will create a `classify_products` function to classify the products and save the data:

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

**Example of Usage**

To use the product classifier, simply call the `classify_products` function:

```python
source_file = "./sources/resources/desktop_pc_sample.csv"
extracted_file = MistralClassifier().classify_products(
    source_file=source_file,
    source_columns=["Title", "About", "Description"],
    characteristics=["CPU", "GPU", "Amount of RAM", "Type of RAM"],
)
```

**Conclusion**

In this article, we've built a product classifier using Mistral AI to extract technical characteristics from product descriptions. This powerful tool can be applied to various products and data sources, making it a valuable resource for e-commerce, supply chain management, and more. Explore Mistral AI's capabilities and create your own unique tools for data extraction and classification!


# Conclusion

In this article, we have taken a deep dive into the world of product classification using Mistral AI. We began with a real-world use case, creating a product classifier for desktop computers that extracts technical features from product descriptions. By preparing sample data, setting classification objectives, and building the tool step-by-step, we equipped you with the knowledge to construct similar tools for various applications.

Through the use of Mistral AI's powerful language models, we demonstrated how to extract specific product characteristics from raw data, saving them in a user-friendly format for easy comparison and analysis. The `mistral-tiny` model, in particular, proved to be an effective and cost-efficient solution for this type of extraction.

By leveraging the `pandas` library for data management and processing, we were able to combine product data and extract the desired characteristics with ease. The `classify_products` function served as a practical example of how to utilize these techniques for efficient product classification.

Now that you have a solid understanding of Mistral AI's capabilities for product classification, consider exploring its potential in other domains. The applications for Mistral AI's data extraction and classification features are vast, from e-commerce and supply chain management to customer support and content moderation. By harnessing the power of Mistral AI, you can unlock new possibilities in data analysis and automation, driving efficiency and innovation across various industries.

To continue your journey with Mistral AI, visit the [official documentation](https://docs.mistral.ai/) for more information on available models, features, and best practices. Don't hesitate to share your experiences and discoveries, as the Mistral AI community is constantly growing and eager to learn from one another. Together, we can shape the future of AI-powered data extraction and classification.
                
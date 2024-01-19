# Mistral AI Real Use Case : A Product Classifier

After building some toy project with Mistral AI, let's build an real tool with real world application.
To achieve a project I'm working on, I need to be able to extract technical characteristics from a product description, in order to classify and compare them.

# Sample data

As an example, I'm going to pull some desktop computers data from Amazon.
For each product, I'll collect : 
* the product url
* the product title
* the "about this product" text
* the product description

The sample data is available here, in a CSV file : [https://github.com/QuentinAstegiano/PublicArticles/blob/main/articles/MistralAiProductClassifier/sources/resources/desktop_pc_sample.csv]
Here's an exerpt from it (truncated for clarity): 
```csv
"URL","Title","About","Description"
"https://www.amazon.com/Lenovo-Business-19-5-Dual-Core-Processor/dp/B0CCF99RFQ","Lenovo All-in-One Business Desktop, 19.5” HD+ Display AIO, 16GB RAM, 256GB SSD + 1TB HDD","     【Storage and RAM】This system boasts a generous storage and RAM configuration, including a 256GB M.2 PCIe SSD coupled with a 1TB HDD. Additionally, it is equipped with 16GB of DDR4 RAM, ensuring","Processor: Intel Celeron J4025 Dual Core, 2.0, Up to 2.9GHz Graphics: Integrated Intel UHD Graphics 600 Operating system:Windows 11 Pro Memory: 16GB DDR4 RAM Hard Drive: 256GB M.2 PCIe SSD + 1TB HDD Optical Drive: Yes"
```

# Product objectives

The idea here is to feed that data to Mistral AI, and, for each product, to ask it to extract some specifics characteristics of the products : in our example, the processor, the amount and type of RAM, the hard drive, ...
We'll then store that data in a easily accessible file.

# Building the tool

The complete source code for this project is available on my (GitHub)[https://github.com/QuentinAstegiano/PublicArticles/blob/main/articles/MistralAiProductClassifier/sources/main/MistralClassifier.py]

I won't cover the basics of using Mistral AI in this article. You can refer to my other article for reference : (Forget about ChatGPT, Discover Mistral AI : the forefront of the AI revolution)[https://medium.com/p/115de697709e]

The first thing to do is to create the capability to ask Mistral AI to classify the data.
As usual, the most important thing here is the prompt. Here's what I've come up with:

> You are an automation system that take a input consisting of a product data, 
> and that ouput a dictionnary of extracted characteristics from that data.
> Extract from this data about a product the value of each of those fields : 
> [List of the fields to extract]
> The output must be in this dictionnary format : 
> {
>     "field1": "value1",
>     "field2": "value1"
> }
> The output should not contain anything else than the dictionnary. It must be precisely formatted as required.
> Only the "value" should be replaced by the actual value extracted from the data.
> There must not be any other content in the response.

Here's the actual function (with a truncated prompt, for brevity):
```python
    def _ask_mistral(self, product, characteristics: list):
        system_role = f"""
            You are an automation system that take a input consisting of a product data, 
            [..]
            Extract from this data about a product the value of each of those fields : 
            {", ".join(characteristics)}
            [..]
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
            content = content[content.index("{") :]
        return content
```

Nothing fancy here : it's a very standard Mistral AI function, with the definition of a role for the LLM with the prompt seen earlier, and a `user` message containing the product data.

I'm using *mistral-tiny* here, because I've found it to work well enough for that kind of extraction. Given that it's cheaper than the other models, I see no reason to do otherwise.

Now that we can extract characteristics from the raw data, all we need to do is to call Mistral AI for each of our product.
I'm using `pandas` to manage data, because, well, it's quite suited for anything data related. 
Some other library would work here too, or even using simple pythons types ; it's not that relevent to the tool we're creating.

```python
    def _extract_characteristics(
        self, df: pd.DataFrame, source_columns: list, characteristics: list
    ) -> pd.DataFrame:
        df["Combined"] = df[source_columns].apply(
            lambda x: ", ".join(x.dropna().astype(str)), axis=1
        )
        df["Mistral"] = df["Combined"].apply(
            lambda x: self._ask_mistral(x, characteristics)
        )
        df["Mistral"] = df["Mistral"].apply(literal_eval)
        result = df.join(pd.json_normalize(df.pop("Mistral")))
        return result
```

That method take a Pandas DataFrame as an input, along with the list of the columns to use as source, and the list of characteristics to extract from the data.

This whole system is completly independant from the kind of data we're processing : I've made an example with some computer, but it is usable as is on nearly anything you want to extract some characteristics of.

The last thing to do is to load our data, add the extracted characteristics, and output a result.

```python
    def classify_products(
        self, source_file: str, characteristics: list, source_columns: list
    ) -> str:
        df = pd.read_csv(source_file)
        columns_to_keep = [c for c in df.columns.tolist() if c not in source_columns]
        df = self._extract_characteristics(df, source_columns, characteristics)

        selected_columns = columns_to_keep + characteristics
        target_file = source_file.replace(".csv", "__extracted.csv")

        df[selected_columns].to_csv(target_file)

        return target_file
```

When saving the data I'm removing the columns I used to extract the characteristics, in order to have a simpler resulting data set.

Calling the function is easy : 
```python
source_file = "./sources/resources/desktop_pc_sample.csv"
extracted_file = MistralClassifier().classify_products(
    source_file=source_file,
    source_columns=["Title", "About", "Description"],
    characteristics=["CPU", "GPU", "Amount of RAM", "Type of RAM"],
)
```

Here is the only point where I'm inputing something specific to my use case - and it's only listing the columns to use and the characteristics to extract.

The complete output on the sample data is available here : [https://github.com/QuentinAstegiano/PublicArticles/blob/main/articles/MistralAiProductClassifier/sources/resources/desktop_pc_sample__extracted.csv]
Here's an exerpt of it : 
```csv
,URL,CPU,GPU,Amount of RAM,Type of RAM
0,https://www.amazon.com/Lenovo-Business-19-5-Dual-Core-Processor/dp/B0CCF99RFQ,Intel Celeron J4025 Dual Core,Integrated Intel UHD Graphics 600,16GB,DDR4
1,https://www.amazon.com/Dell-XPS-8950-i9-12900K-Bluetooth/dp/B0BBGQJMK9,Intel Core i9-12900K,AMD Radeon RX 6700XT,64GB,GDDR6
2
```

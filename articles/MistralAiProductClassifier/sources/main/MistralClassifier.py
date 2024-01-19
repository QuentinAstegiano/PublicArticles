import pandas as pd
from dotenv import load_dotenv
from mistralai.models.chat_completion import ChatMessage
from ast import literal_eval

load_dotenv()

from mistralai.client import MistralClient


class MistralClassifier:
    def _get_sample_dict(self, characteristics: list) -> str:
        sample = "{"
        for c in characteristics:
            sample += f'"{c}" : "value",'
        sample += "}"
        return sample

    def _ask_mistral(self, product, characteristics: list):
        system_role = f"""
            You are an automation system that take a input consisting of a product data, 
            and that ouput a dictionnary of extracted characteristics from that data.

            Extract from this data about a product the value of each of those fields : 

            {", ".join(characteristics)}

            The output must be in this dictionnary format : 
            
            {self._get_sample_dict(characteristics)}

            The output should not contain anything else than the dictionnary. It must be precisely formatted as required.
            Only the "value" should be replaced by the actual value extracted from the data.
            There must not be any other content in the response.
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


source_file = "./sources/resources/desktop_pc_sample.csv"
extracted_file = MistralClassifier().classify_products(
    source_file=source_file,
    source_columns=["Title", "About", "Description"],
    characteristics=["CPU", "GPU", "Amount of RAM", "Type of RAM"],
)
print("Extracted data from", source_file, "to", extracted_file)

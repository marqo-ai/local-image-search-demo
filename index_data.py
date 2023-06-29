import pandas as pd
from tqdm import tqdm
import marqo
import colorama
import os
from typing import Dict
import random
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")

marqo.set_log_level("WARN")

N = os.getenv("N_DOCUMENTS", None)
DEVICE = os.getenv("MARQO_DEVICE", "cpu")
CLIENT = marqo.Client()
INDEX_NAME = os.getenv("MARQO_INDEX_NAME", None)
REQUEST_CHUNK_SIZE = 16
CLIENT_BATCH_SIZE = 16


def print_banner(message: str) -> None:
    horizontal_line = "#" * (len(message) + 4)
    empty_line = "#" + " " * (len(message) + 2) + "#"
    print(colorama.Fore.BLUE + horizontal_line + colorama.Style.RESET_ALL)
    print(colorama.Fore.BLUE + empty_line + colorama.Style.RESET_ALL)
    print(
        colorama.Fore.BLUE
        + "# "
        + colorama.Fore.GREEN
        + message
        + colorama.Fore.BLUE
        + " #"
        + colorama.Style.RESET_ALL
    )
    print(colorama.Fore.BLUE + empty_line + colorama.Style.RESET_ALL)
    print(colorama.Fore.BLUE + horizontal_line + colorama.Style.RESET_ALL)
    print(
        "\nThe application will now undergo some first time setup, please wait while your local "
        + colorama.Fore.GREEN
        + "Marqo"
        + colorama.Style.RESET_ALL
        + " index is constructed."
    )
    print()
    print(f"Your index will have {N if N is not None else 'all available'} images.")
    print(
        f"{'' if N is None else 'To use more images set N_DOCUMENTS in .env.local, to use all images, comment out N_DOCUMENTS'}\n"
    )


def create_index() -> None:
    """
    This function has a lot of extra checks to make it pretty hard to shoot yourself in the foot
    """
    settings = {
        "index_defaults": {
            "treat_urls_and_pointers_as_images": True,
            "model": "ViT-L/14",
            "normalize_embeddings": True,
        },
    }
    try:
        CLIENT.create_index(INDEX_NAME, settings_dict=settings)
        print("Finished creating index...")
    except Exception as e:
        print(colorama.Fore.RED + "Exception occured:" + colorama.Style.RESET_ALL)
        print(e)
        choice = None
        while choice not in {"y", "n"}:
            choice = input(
                "Would you like to reset the index if it exists? (y/n): "
            ).strip()
        if choice == "y":
            try:
                CLIENT.delete_index(INDEX_NAME)
                CLIENT.create_index(INDEX_NAME, settings_dict=settings)
                print("Finished creating index...")
            except Exception as e:
                print(
                    colorama.Fore.RED + "Exception occured:" + colorama.Style.RESET_ALL
                )
                print(e)


def get_data() -> Dict[str, str]:
    """
    Fetch the dataset from S3
    """
    filename = "https://marqo-overall-demo-assets.s3.us-west-2.amazonaws.com/ecommerce_meta_data.csv"
    data = pd.read_csv(filename, nrows=int(N) if N is not None else None)
    data["image"] = data["s3_http"]
    documents = data[["image"]].to_dict(orient="records")
    for i in range(len(documents)):
        documents[i]["_id"] = documents[i]["image"].split("/")[-1]

    random.shuffle(documents)
    print("Data fetched.\n")
    return documents


def index_data(documents: Dict[str, str]) -> None:
    """
    Index the data into Marqo
    """
    print(f"Indexing data with requests of {REQUEST_CHUNK_SIZE} documents...")
    if DEVICE == "cpu":
        print("You are using a CPU so indexing may be time consuming.")
    for i in tqdm(range(0, len(documents), REQUEST_CHUNK_SIZE), desc="Indexing data"):
        chunk = documents[i : i + REQUEST_CHUNK_SIZE]

        CLIENT.index(INDEX_NAME).add_documents(
            chunk, client_batch_size=CLIENT_BATCH_SIZE, device=DEVICE
        )

    print(
        colorama.Fore.GREEN + "\nFinished indexing data!\n" + colorama.Style.RESET_ALL
    )


def setup_application() -> None:
    """
    Driver function to do all the set up.
    """
    # Initialize colorama
    colorama.init()
    banner_message = "Application First-time Setup"
    print_banner(banner_message)

    print("Fetching data from AWS S3...")
    documents = get_data()

    create_index()

    index_data(documents)

    # Reset colorama on program exit
    colorama.deinit()

    print("Done.")


if __name__ == "__main__":
    setup_application()

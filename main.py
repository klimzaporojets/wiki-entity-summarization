import os
import pickle

from dotenv import load_dotenv
import networkx as nx
from top_visited_collector.tvwpc import fetch_top_visited_wikipedia_pages
from wikipedia_abstract_processor.wpap import construct_wikipedia_abstract_graph
from graph_builder.esgb import construct_entity_summarization_graph


def get_path(graph_path):
    path = os.getenv(graph_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


if __name__ == '__main__':
    load_dotenv(".env")
    os.makedirs(os.path.dirname(os.getenv("OUTPUT_VOLUME_PATH")), exist_ok=True)

    app = os.getenv("APP_MODULE")

    # Top Visited Wikipedia Pages Collector
    if app == "TVWPC":
        load_dotenv("configs/tvwpc.env")
        fetch_top_visited_wikipedia_pages(
            top_n=int(os.getenv("TOP_N")),
            output_csv_path=get_path("TOP_VISITED_CSV_PATH"),
            to_year=int(os.getenv("TO_YEAR")),
            to_month=int(os.getenv("TO_MONTH")),
            from_year=int(os.getenv("FROM_YEAR")),
            from_month=int(os.getenv("FROM_MONTH"))
        )

    # Wikipedia Abstract Processor
    elif app == "WPAP":
        load_dotenv("configs/wpap.env")
        wpg_path = get_path("WPG_PICKLE_PATH")

        wpag = construct_wikipedia_abstract_graph(os.getenv("WIKIPEDIA_DUMPS_PATH"))
        with open(os.getenv("WPG_PICKLE_PATH"), 'wb') as f:
            pickle.dump(wpag, f)

    # Entity Summarization Graph Builder
    elif app == "ESGB":
        load_dotenv("configs/wpap.env")
        load_dotenv("configs/esgb.env")
        wpg_path = os.getenv("WPG_PICKLE_PATH")

        if not os.path.exists(wpg_path):
            raise FileNotFoundError(f"`{wpg_path}` does not exist! Please run `WPAP` first!")

        esg_path = get_path("ESG_PICKLE_PATH")

        with open(wpg_path, 'rb') as f:
            wpag = pickle.load(f)

        esg = construct_entity_summarization_graph(wpag)
        with open(esg_path, 'wb') as f:
            pickle.dump(esg, f)

    # Entity Summarization Graph Extender
    elif app == "ESGE":
        load_dotenv("configs/esge.env")
        pass

    # Entity Summarization Graph Edge Refiner
    elif app == "ESGER":
        load_dotenv("configs/esger.env")
        pass
    else:
        raise ValueError(
            f'Invalid app module should be one of the following:'
            f'"TVWPC" Top-visited Wiki Pages Collector | "WPAP" Wikipedia Abstract Processor |'
            f' "ESGB" Entity Summarization Graph Builder | "ESGE" Entity Summarization Graph Expander |'
            f' "ESGER" Entity Summarization Graph Edge Refiner'
        )
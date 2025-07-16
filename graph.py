from langgraph.graph import StateGraph, END

from nodes.validate_bank import validate_bank_node, has_error
from nodes.search_articles import search_articles_node
from nodes.sentiment_analysis import sentiment_node
from nodes.format_output import format_node
from nodes.validate_bank_serper_api import is_real_bank_serper_and_llm
from schemas import State


def build_graph():
    builder = StateGraph(State)

    builder.add_node("validate_bank", validate_bank_node)
    builder.add_node("search_articles", search_articles_node)
    builder.add_node("sentiment_analysis", sentiment_node)
    builder.add_node("format_output", format_node)

    # Entry point
    builder.set_entry_point("validate_bank")

    # Conditional branching based on presence of error
    builder.add_conditional_edges("validate_bank", has_error, {
        "error": END,
        "success": "search_articles"
    })

    # Linear flow for the rest
    builder.add_edge("search_articles", "sentiment_analysis")
    builder.add_edge("sentiment_analysis", "format_output")
    builder.add_edge("format_output", END)

    return builder.compile()


def build_graph_serper_api():
    builder = StateGraph(State)

    builder.add_node("validate_bank", is_real_bank_serper_and_llm)
    builder.add_node("search_articles", search_articles_node)
    builder.add_node("sentiment_analysis", sentiment_node)
    builder.add_node("format_output", format_node)

    # Entry point
    builder.set_entry_point("validate_bank")

    # Conditional branching based on presence of error
    builder.add_conditional_edges("validate_bank", has_error, {
        "error": END,
        "success": "search_articles"
    })

    # Linear flow for the rest
    builder.add_edge("search_articles", "sentiment_analysis")
    builder.add_edge("sentiment_analysis", "format_output")
    builder.add_edge("format_output", END)

    return builder.compile()

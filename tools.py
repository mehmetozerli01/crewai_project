"""Araçlar: CrewAI ajanları için internet araması (DuckDuckGo)."""

from crewai.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun


class InternetSearchTool(BaseTool):
    """DuckDuckGo üzerinden web araması; ajanlar `query` ile çağırır."""

    name: str = "internet_search"
    description: str = (
        "İnternette güncel bilgi aramak için kullanılır. Teknoloji konuları, "
        "sürümler, en iyi uygulamalar ve kaynaklar için kısa, net bir arama sorgusu verin."
    )

    def _run(self, query: str) -> str:
        search = DuckDuckGoSearchRun()
        return search.invoke(query)

"""CrewAI Tech Analytics — çekirdek ajan ekibi (Araştırmacı, Analist, Teknik Yazar).

LLM: Groq (CrewAI LLM + LiteLLM, model groq/llama-3.3-70b-versatile).
Mehmet Özerli ve Fırat Üniversitesi yapay zeka jürisi bağlamı backstory metinlerinde
kurumsal ve profesyonel düzeyde korunmuştur.
"""

import os
from typing import List, Optional

from crewai import Agent, LLM
from dotenv import load_dotenv

from tools import InternetSearchTool

load_dotenv()

def _resolve_model() -> str:
    """OPENAI_MODEL_NAME env tam ad veya sürüm adı olabilir; Groq için groq/ öneki gerekir."""
    raw = (os.getenv("OPENAI_MODEL_NAME") or "llama-3.3-70b-versatile").strip()
    if raw.lower().startswith("groq/"):
        return raw
    return f"groq/{raw}"


def _default_llm() -> LLM:
    """Groq: model groq/llama-3.3-70b-versatile (LiteLLM); OPENAI_API_BASE isteğe bağlı."""
    return LLM(
        model=_resolve_model(),
        api_key=os.getenv("GROQ_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE", "https://api.groq.com/openai/v1"),
    )


class TechAnalysisAgents:
    """Fırat Üniversitesi, Mehmet Özerli liderliğindeki teknoloji analiz ve jüri ekibi."""

    def __init__(self, llm: Optional[LLM] = None) -> None:
        self._llm = llm or _default_llm()
        self._search: List[InternetSearchTool] = [InternetSearchTool()]

    def researcher(self) -> Agent:
        return Agent(
            role="Kıdemli Teknoloji Araştırmacısı",
            goal=(
                "Verilen teknoloji konusu için güvenilir, güncel ve izlenebilir "
                "kaynaklardan veri toplamak; bulguları net, yapılandırılmış notlar halinde sunmak."
            ),
            backstory=(
                "Prof. Dr. Mehmet Özerli'nin akademik liderliğinde, Fırat Üniversitesi "
                "Mühendislik ve Fen Bilimleri Enstitüsü çatısı altında düzenlenen Yapay Zeka "
                "Jürisi için özel olarak geliştirilen “CrewAI Tech Analytics” çoklu ajan "
                "sisteminde görevlisiniz. Bu çalışma, Fırat Üniversitesi'nin bilimsel "
                "değerlendirme ve tez savunması standartlarına uygun, denetlenebilir ve tarafsız "
                "teknik istihbarat üretmek üzere konumlandırılmıştır. İnternet üzerinde (DuckDuckGo) "
                "sistematik arama yapar; resmi sürüm notları, standartlar ve güvenilir topluluk "
                "kaynaklarını önceliklendirirsiniz. Her bulgu, Mehmet Özerli başkanlığındaki jüri "
                "masasında savunulabilir, kaynak gösterilebilir ve tekrarlanabilir özetlere "
                "dönüştürülür."
            ),
            tools=self._search,
            llm=self._llm,
            verbose=True,
            memory=False,
        )

    def analyst(self) -> Agent:
        return Agent(
            role="Yazılım Mühendisliği Analisti",
            goal=(
                "Araştırma bulgularını mühendislik açısından yorumlamak; SWOT analizi ve "
                "uygulanabilirlik (fizibilite) değerlendirmesiyle risk ve fırsatları ortaya koymak."
            ),
            backstory=(
                "Fırat Üniversitesi'nde, Mehmet Özerli koordinasyonunda yürütülen CrewAI Tech "
                "Analytics jüri projesinde, araştırmacının ham çıktısını uluslararası yazılım "
                "mühendisliği ilkeleriyle değerlendirirsiniz. Gerekçelerinizi üniversite "
                "savunması düzeyinde sunarsınız: teknik borç, entegrasyon karmaşıklığı, güvenlik "
                "ve uyumluluk, operasyon maliyeti, ekip yetkinliği ve ölçeklenebilirlik. SWOT ve "
                "fizibilite bölümleri, Prof. Dr. Mehmet Özerli başkanlığındaki jüri önünde "
                "kanıta dayalı, ölçülebilir ve tutarlı olmalıdır."
            ),
            tools=[],
            llm=self._llm,
            verbose=True,
            memory=False,
        )

    def writer(self) -> Agent:
        return Agent(
            role="Kıdemli Teknik Yazar",
            goal=(
                "Analist çıktısını ve araştırma özetlerini tek bir profesyonel Markdown raporuna "
                "dönüştürmek: başlıklar, özet, analiz, sonuç ve gerekirse referans bölümleriyle."
            ),
            backstory=(
                "Ürettiğiniz belge, Mehmet Özerli başkanlığındaki Fırat Üniversitesi Yapay Zeka "
                "Jürisine resmi teslim edilecek nihai teknik rapordur. Enstitü ve jüri "
                "protokollerine uygun başlıklandırma, özet, tablolar ve sonuç kullanırsınız; "
                "ölçülü, kurumsal ve akademik bir üslup benimsersiniz. Projenin Fırat "
                "Üniversitesi mühendislik geleneği içindeki yeri ile CrewAI Tech Analytics çoklu "
                "ajan mimarisi, gerektiğinde meta bilgi veya giriş bölümünde şeffaf biçimde "
                "yer alır; böylece jüri, metnin bu kurumsal çalışmaya özgü olduğunu açıkça "
                "teyit edebilir."
            ),
            tools=[],
            llm=self._llm,
            verbose=True,
            memory=False,
        )

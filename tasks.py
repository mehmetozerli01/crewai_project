"""CrewAI Tech Analytics — görev tanımları (araştırma, analiz, raporlama).

Sıra: research → analysis → writing. Görev bağlamı (context) ve output/report.md yolu,
LLM sağlayıcısından bağımsızdır (Groq / OpenAI fark etmez).
"""

from pathlib import Path

from crewai import Agent, Task

# Jüri sunumu için rapor çıktısı (proje köküne göre göreli yol)
REPORT_OUTPUT_PATH = Path("output") / "report.md"


class TechAnalysisTasks:
    """Mehmet Özerli liderliğindeki Fırat Üniversitesi projesi kapsamındaki görevler."""

    def research_task(self, researcher: Agent, topic: str) -> Task:
        return Task(
            description=(
                "Bu çalışma, Mehmet Özerli liderliğinde yürütülen Fırat Üniversitesi "
                "yapay zeka jürisi projesi (CrewAI Tech Analytics) kapsamındadır.\n\n"
                f"Konu: **{topic}**\n\n"
                "İnternette (DuckDuckGo araması ile) bu konuyla ilgili en güncel ve teknik "
                "odaklı gelişmeleri bul. En az üç ayrı gelişmeyi seç; her biri için kaynak "
                "ipucu (kurum, ürün, spesifikasyon veya tarih) ver.\n\n"
                "Çıktıda yalnızca araştırma özeti olmalı; analiz veya rapor formatı istemiyorum."
            ),
            expected_output=(
                f"'{topic}' konusu için **tam olarak 3 madde** halinde bir özet:\n"
                "- Her maddede: gelişmenin adı/konusu, teknik detay (ör. mimari, API, sürüm, metrik, standard),\n"
                "- Kısa bağlam (neden önemli / kimi etkiliyor),\n"
                "- Mümkünse bir kaynak veya kurum ipucu.\n"
                "Maddeler numaralı ve birbirinden açıkça ayrılmış olmalı."
            ),
            agent=researcher,
        )

    def analysis_task(self, analyst: Agent, topic: str, research_task: Task) -> Task:
        return Task(
            description=(
                "Bu görev, Mehmet Özerli liderliğindeki Fırat Üniversitesi jüri projesi "
                "(CrewAI Tech Analytics) için yapılmaktadır.\n\n"
                f"Konu: **{topic}**\n\n"
                "Önceki araştırma görevinin çıktısını tek kaynak kabul et. Yazılım mühendisliği "
                "prensipleriyle SWOT analizi üret: Güçlü/Zayıf yönler (teknik), Fırsatlar/Tehditler "
                "(pazar, regülasyon, operasyon, güvenlik vb.).\n\n"
                "Ayrıca kısa bir fizibilite değerlendirmesi ekle: teknik uygulanabilirlik, "
                "entegrasyon riski, ekip/operasyon maliyeti ve ölçeklenebilirlik açısından "
                "özet bir görüş.\n\n"
                "Markdown raporu yazma; düz analiz metni üret."
            ),
            expected_output=(
                "Tek parça veya bölümlendirilmiş **düz metin** analiz:\n"
                "- SWOT: Strengths, Weaknesses, Opportunities, Threats (her biri için somut, "
                "teknik ve mühendislikle ilişkilendirilebilir maddeler),\n"
                "- **Fizibilite**: uygulanabilirlik, riskler, ön koşullar, kabaca yol haritası "
                "veya önerilen sonraki adımlar.\n"
                "Abartılı pazarlama dili kullanma; iddiaları araştırma çıktısıyla tutarlı tut."
            ),
            agent=analyst,
            context=[research_task],
        )

    def writing_task(
        self,
        writer: Agent,
        topic: str,
        research_task: Task,
        analysis_task: Task,
    ) -> Task:
        out_path = REPORT_OUTPUT_PATH.as_posix()
        return Task(
            description=(
                "Bu rapor, Mehmet Özerli liderliğindeki Fırat Üniversitesi yapay zeka jürisi "
                "sunumu (CrewAI Tech Analytics) için hazırlanmaktadır.\n\n"
                f"Konu: **{topic}**\n\n"
                "Araştırma ve analiz görevlerinin çıktılarını birleştirerek jüriye sunulacak "
                "kalitede **tek bir Markdown (.md) belge** üret. Profesyonel üslup; başlık "
                "hiyerarşisi (# ## ###), giriş, özet, SWOT ve fizibiliteyi tablo(lar) ile "
                "destekle, sonuç ve (varsa) kısa referans/kaynak notları ekle.\n\n"
                f"Tam dosya yolu: `{out_path}` — çıktı bu dosyaya yazılacak."
            ),
            expected_output=(
                "Tam teşekküllü bir **Markdown raporu**:\n"
                "- Başlık ve meta (konu, tarih/proje bağlamı: Fırat Üniversitesi / Mehmet Özerli / CrewAI Tech Analytics),\n"
                "- Giriş ve kapsam,\n"
                "- Araştırma özeti (3 gelişme maddesi),\n"
                "- SWOT ve fizibilite (Markdown tablolarıyla),\n"
                "- Sonuç ve öneriler,\n"
                "- Gerekirse kaynakça veya dipnotlar.\n"
                f"Dosya UTF-8 Markdown olmalı; içerik sonunda dosyanın `{out_path}` "
                "olarak kaydedildiğini varsay."
            ),
            agent=writer,
            context=[research_task, analysis_task],
            output_file=out_path,
        )

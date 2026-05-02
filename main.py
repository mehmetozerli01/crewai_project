"""
CrewAI Tech Analytics — proje giriş noktası.

Mehmet Özerli liderliğinde yürütülen Fırat Üniversitesi yapay zeka jürisi
çalışması kapsamında: çoklu ajan (araştırma → analiz → rapor) akışını başlatır.
"""

from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv

# Proje modülleri: ajan ve görev fabrikaları
from agents import TechAnalysisAgents
from tasks import TechAnalysisTasks, REPORT_OUTPUT_PATH

# CrewAI: sıralı işlemde ekip orkestrasyonu
from crewai import Crew, Process

# .env: GROQ_API_KEY, OPENAI_MODEL_NAME (Groq Llama — Fırat Üniversitesi jüri yapılandırması)
load_dotenv()

# Çıktı kökü — jüri sunumunda raporun toplanacağı klasör
OUTPUT_DIR = Path("output")


def ensure_output_dir() -> None:
    """output/ yoksa oluştur; rapor (report.md) yazılırken IO hatalarını önler."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def prompt_topic() -> str:
    """
    Kullanıcı (Mehmet Özerli / jüri oturumu) için terminalde okunaklı konu girişi.
    Fırat Üniversitesi CrewAI Tech Analytics demolarında net bir başlangıç verir.
    """
    line = "─" * 58
    banner = f"""
{line}
  CrewAI Tech Analytics
  Fırat Üniversitesi  ·  Yapay Zeka Jürisi  ·  Mehmet Özerli
{line}
  Bu oturumda ajanlar vereceğiniz teknoloji konusunu
  internette araştırıp analiz eder ve {REPORT_OUTPUT_PATH.as_posix()} raporunu üretir.
{line}
"""
    print(banner)
    while True:
        try:
            raw = input("Araştırma konusu (topic) > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nİptal edildi.")
            sys.exit(0)
        if raw:
            return raw
        print("Lütfen boş olmayan bir konu girin (ör. 'CrewAI ve çoklu ajan sistemleri').")


def main() -> None:
    # Fırat Üniversitesi jüri demosu: rapor dizini her çalıştırmada hazır olsun
    ensure_output_dir()

    topic = prompt_topic()

    # Ajan ve görev sınıfları — Mehmet Özerli proje akışı (agents.py, tasks.py).
    # Groq ile memory=False (agents.py): jüri sunumunda bellek katmanında takılma riskini azaltır.
    agent_factory = TechAnalysisAgents()
    task_factory = TechAnalysisTasks()

    researcher = agent_factory.researcher()
    analyst = agent_factory.analyst()
    writer = agent_factory.writer()

    research = task_factory.research_task(researcher, topic)
    analysis = task_factory.analysis_task(analyst, topic, research)
    # Not: tasks.py içinde metot adı writing_task (kullanıcı spesinde write_task ile aynı rol)
    writing = task_factory.writing_task(writer, topic, research, analysis)

    # Ekip: sıralı süreç, verbose açık (sunumda ajan diyaloglarının izlenmesi için)
    crew = Crew(
        agents=[researcher, analyst, writer],
        tasks=[research, analysis, writing],
        process=Process.sequential,
        verbose=True,
    )

    # --- Kickoff: Fırat Üniversitesi jüri senaryosu tam döngü ---
    result = crew.kickoff()

    print("\n" + "═" * 60)
    print("Crew tamamlandı — özet çıktı:")
    print("═" * 60)
    print(result)
    print("\nRapor dosyası:", REPORT_OUTPUT_PATH.resolve())


if __name__ == "__main__":
    main()

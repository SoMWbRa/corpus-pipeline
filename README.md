# Ukrainian Text Corpus Pipeline

## English Below

Система автоматизованого формування текстових корпусів (САФТК) для української мови з покращеними методами нормалізації та токенізації. Розроблена в рамках кваліфікаційної роботи магістра в Харківському національному університеті радіоелектроніки.

Система реалізує повний конвеєр обробки тексту: отримання даних з вебджерел, парсинг HTML зі збереженням структури, нормалізація форматування, оцінка якості тексту, виправлення помилок та семантична токенізація. Кожен етап зберігає проміжні результати в структурованому форматі з метаданими та діагностичною інформацією.

Система вирішує проблеми непослідовності форматування в українських новинних текстах: стандартизує телефонні номери, нормалізує апострофи та лапки згідно з правописом, забезпечує семантично коректну токенізацію. Модульна архітектура дозволяє легко адаптувати систему для різних джерел даних та завдань корпусної лінгвістики.

Поточна реалізація має наступні обмеження:
- реалізовано компоненти лише для роботи з джерелом «Суспільне»;
- компонент виправлення тексту не реалізовано, використовується заглушка;
- немає підтримки відслідкування прогресу;
- компонент перевірки тексту LanguageTool суттєво уповільнює обробку.

В межах роботи зроблена публікація щодо нормалізації тексту на прикладі UberText 2.0. Деталі доступні за посиланням: https://github.com/SoMWbRa/ukrainian-text-normalization/tree/main

Детальна записка до роботи та відео демонстрації доступні в окремій гілці: https://github.com/SoMWbRa/corpus-pipeline/tree/university

**Автор**: Данило Горєлов  
**Керівник**: Олександр В. Вечур  
**Університет**: Харківський національний університет радіоелектроніки, 2025

---

Automated Text Corpus Formation System for Ukrainian language with enhanced normalization and tokenization methods. Developed as part of Master's thesis research at Kharkiv National University of Radio Electronics.

The system implements a complete text processing pipeline: data acquisition from web sources, HTML parsing with structure preservation, format normalization, text quality assessment, error correction, and semantic tokenization. Each stage saves intermediate results in structured format with metadata and diagnostic information.

The system addresses formatting inconsistencies in Ukrainian news texts: standardizes phone numbers, normalizes apostrophes and quotation marks according to orthographic rules, provides semantically correct tokenization. Modular architecture allows easy adaptation for different data sources and corpus linguistics tasks.

Current implementation has the following limitations:
- components are implemented only for "Suspilne" news source;
- text correction component is not implemented, using placeholder;
- no progress tracking support;
- LanguageTool text evaluation component significantly slows down processing.

A publication on text normalization using UberText 2.0 as a case study was prepared as part of this research. Details available at: https://github.com/SoMWbRa/ukrainian-text-normalization/tree/main

Detailed thesis documentation and demonstration videos are available in a separate branch: https://github.com/SoMWbRa/corpus-pipeline/tree/university

**Author**: Danylo Horielov  
**Supervisor**: Oleksander V. Vechur  
**University**: Kharkiv National University of Radio Electronics, 2025

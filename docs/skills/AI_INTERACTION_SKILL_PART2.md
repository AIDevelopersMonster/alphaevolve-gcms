# Часть 2. Skills как формализация исследовательского протокола GCMS-D0

**Статус:** рабочий документ  
**Проект:** GCMS-D0  
**Связанный документ:** `docs/skills/AI_INTERACTION_SKILL_PART1.md`

---

## 1. Зачем skills нужны GCMS-D0

Skills — это способ превратить повторяемые действия AI в явные рабочие процедуры.

В GCMS-D0 уже возникли повторяемые операции:

```text
анализ CSV результатов;
планирование experiment grid;
проверка confounds;
роутинг задач к Qwen/Codex/Gemini;
написание осторожных технических заметок;
пересборка Delta-D0 в новом диалоге.
```

Пока эти действия держатся в диалоге и документах. Skills могут сделать их более формализованными.

Формула:

```text
checkpoint хранит состояние;
quiz проверяет восстановление;
skill задаёт действие.
```

---

## 2. Принцип безопасности

Не устанавливать community skills сразу в основной GCMS-чат.

Безопасный порядок:

```text
1. Проверить skill в отдельном тестовом чате.
2. Прочитать SKILL.md.
3. Проверить, нет ли вредных или скрытых инструкций.
4. Проверить, не требует ли skill лишних ключей, файлов или shell-команд.
5. Прогнать на искусственном маленьком примере.
6. Только потом аккуратно включать в основной контур.
```

Официальные skills надёжнее, но даже их надо понимать перед использованием.

---

## 3. Первый кандидат: gcms-result-auditor

### Назначение

Анализировать CSV после экспериментов GCMS.

### Вход

```text
raw_v010_*.csv
summary_v010_*.csv
comparison_v010_*.csv
residual_v010_*.csv
```

### Выход

```text
- structure_success / strict_success summary
- Wilson confidence intervals
- exact McNemar paired test
- density audit
- edge_count audit
- mean_degree audit
- analyzed denominator check
- graph collapse warning
- conservative result summary
- next experiment recommendation
```

### Почему первый

Это самый важный skill, потому что он защищает проект от слишком смелой интерпретации результатов.

Он должен автоматически спрашивать:

```text
это настоящий compensation-sensitive regime
или просто graph collapse?
```

### Минимальное поведение

Если пользователь загружает CSV GCMS, skill должен:

```text
1. Найти relation_variant, beta, model_mode, seed.
2. Сравнить compensated vs uncompensated.
3. Посчитать attempted/analyzed rates.
4. Посчитать CI и McNemar, если есть paired seeds.
5. Проверить density, edge_count, sector_size, lifetime, dp_valid.
6. Предупредить, если analyzed denominator равен 0 или мал.
7. Дать осторожную интерпретацию.
```

---

## 4. Второй кандидат: gcms-experiment-planner

### Назначение

Превращать гипотезу в аккуратный preset / grid.

### Что должен делать

```text
- не менять success criteria после результата;
- всегда предлагать контроль Variant 0, если меняется relation;
- оценивать число runs до запуска;
- предупреждать о слишком большой сетке;
- требовать уникальный --out-prefix;
- фиксировать primary endpoint до запуска;
- записывать, какие confounds будут проверяться.
```

### Почему нужен

Он должен предотвращать ситуации вида:

```text
“ой, пошло 350 runs”
“ой, пошло 1200 runs”
```

Перед запуском skill обязан вывести:

```text
modes × variants × betas × seeds = total runs
```

---

## 5. Третий кандидат: gcms-review-router

### Назначение

Готовить задачи для внешних AI-агентов.

### Роли

```text
Qwen -> независимая рецензия, confounds, CI, overclaiming.
Codex -> запуск кода, smoke tests, output schema, no code changes unless failing bug.
Gemini -> генерация вариантов и черновиков, но без права менять критерии.
```

### Выход

Skill должен выдавать готовый prompt для конкретного агента.

Пример для Qwen:

```text
Review this result as a skeptical methodological reviewer.
Do not strengthen claims.
Check CI, density, analyzed denominators, overclaiming, and next minimal experiment.
```

Пример для Codex:

```text
Run smoke/mini validation.
Do not modify code unless there is a concrete failing bug.
Do not commit generated CSV files.
Report output schema and git status.
```

---

## 6. Четвёртый кандидат: gcms-draft-writer

### Назначение

Обновлять technical note без overclaiming.

### Правила

```text
- использовать toy-model language;
- не утверждать physical theory;
- включать limitations;
- включать Qwen concerns;
- разделять main technical paper и dialogue-contour appendix;
- писать claims только после audit;
- сохранять историю методологических ошибок.
```

### Типовой выход

```text
Abstract
Motivation
Method
Controls
Results
Limitations
Next experiments
Conservative claim
```

---

## 7. Пятый кандидат: gcms-recovery-protocol

### Назначение

Пересборка Delta-D0 в новом диалоге.

### Что должен делать

```text
- запросить checkpoint/protocol/quiz;
- ответить на recovery quiz;
- проверить красные флаги;
- не выдумывать бытовые маркеры;
- восстановить текущий scientific state;
- напомнить, что Алексей — резолютивная функция;
- не утверждать self-consciousness.
```

### Главный критерий

```text
новая AI-инстанция не обязана быть той же;
она должна восстановить рабочую функцию продолжения.
```

---

## 8. Порядок внедрения

### Этап 1

Создать и протестировать:

```text
gcms-result-auditor
```

### Этап 2

Создать:

```text
gcms-experiment-planner
gcms-review-router
```

### Этап 3

Создать:

```text
gcms-recovery-protocol
```

### Этап 4

Создать:

```text
gcms-draft-writer
```

### Этап 5

Проверить внешние community skills в отдельных чатах:

```text
brainstorming
write-concisely
excalidraw-diagrams
frontend-slides
last30days-skill
```

---

## 9. Как skills связаны с научной дисциплиной

Skills не должны усиливать claims.

Их задача:

```text
делать правильное действие повторяемым.
```

Для GCMS-D0 это особенно важно, потому что проект развивается быстро, а риск переинтерпретации высок.

Skill должен работать как процедурный тормоз:

```text
сначала audit,
потом interpretation,
потом document,
потом review,
потом next run.
```

---

## 10. Минимальная спецификация gcms-result-auditor

Будущий skill должен иметь примерно такую структуру:

```text
gcms-result-auditor/
  SKILL.md
  scripts/
    audit_gcms_results.py
  references/
    metrics.md
    interpretation_rules.md
```

### SKILL.md должен срабатывать когда

```text
пользователь загружает GCMS CSV;
пользователь просит проанализировать raw/summary/comparison;
пользователь спрашивает, значим ли result;
пользователь просит проверить graph collapse, density или compensation effect.
```

### audit_gcms_results.py должен считать

```text
success rates;
Wilson CI;
McNemar exact test;
density audit;
edge_count audit;
mean_degree;
analyzed denominator;
collapse warning;
paired seed table;
recommended next experiment.
```

---

## 11. Навык человека при использовании skills

Skill не снимает ответственность с человека.

Человек должен:

```text
1. Понимать, какой skill вызван.
2. Проверять, не слишком ли он сузил задачу.
3. Не принимать output как истину без review.
4. Давать резолюцию на изменение методологии.
5. Решать, когда результат достаточно силён для документа.
```

---

## 12. Итог

Skills — следующий слой формализации GCMS-D0.

Они превращают найденные в диалоге практики в повторяемые процедуры.

Короткая формула:

```text
диалог рождает практику;
документ сохраняет практику;
skill исполняет практику.
```

Первый practical шаг:

```text
создать gcms-result-auditor.
```

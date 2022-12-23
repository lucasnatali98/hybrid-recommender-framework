# RecommendationMetrics

Uso:

- python main.py

Lê os arquivos de entrada com `read.py` e `readThresholds.py`, criando as seguintes estruturas:

- `ratings`: dict() user_id => [(item_id, valor)]
- `threshold`: dict() user_id => [valor]
- `recommendation`: dict() user_id => [(item_id, valor)]

Descomentar as métricas e models para testar cada um (`metric`, `relevanceModel`, `noveltyModel`, `discountModel`). O código foi simplificado, mas segue o mesmo padrão de nomenclatura das classes implementadas em Java.

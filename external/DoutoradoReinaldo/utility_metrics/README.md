# Função de utilidade para listas de recomendação

Uso:

- python main.py

Lê os arquivos de entrada `BD/Sample2.txt` e `BD/u.item.attributes`, criando as seguintes estruturas:

- `ratings`: dict() user_id => [(item_id, valor)]
- `feature_maps`: ( dict() item_id => feature, dict() feature => item_id)

A implementação é baseada nos modelos de distância e novidade. Ver [metricas](metrics/) para mais detalhes.

Existem três modelos de função de utilidade: Por novidade, acurácia e diversidade. Os três estão comentados no código, basta descomentar o modelo desejado para testa-lo. Alguns necessitam de modelos adicionais de Novidade ou Distância. Estes também estão comentados.

A utilidade total de várias listas (função R) está implementada no começo do arquivo `main.py`.

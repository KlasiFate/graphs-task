## Install and activate virtual environment
IMPORTANT: this package needs python version 3.10 and numpy
- Using poetry on linux and windows
    ```bash
    poetry install
    poetry shell
    ```
    If poetry can't find python 3.10, you may specify it to poetry by
    ```bash
    poetry env use <path-to-python3.10-executable>
    ```
- Using pip and venv on linux
    ```bash
    python3 -m venv venv
    chmod +x ./venv/bin/activate
    ./venv/bin/activate
    pip3 install -r requirements.txt
    ```
- Using pip and venv on windows
    ```cmd
    python -m venv venv
    venv\bin\activate
    pip install -r requirements.txt
    ```
- Using pip without venv on linux
    ```bash
    pip3 install -r requirements.txt
    ```
- Using pip without venv on windows
    ```cmd
    pip install -r requirements.txt
    ```

## Examples of running
- linux
    ```bash
    python3 -m graphs building-tree -v 0 -f test-graphs/1.txt
    python3 -m graphs building-tree -v 0 -f test-graphs/2.txt --input-format edge-set --output-format edge-set
    python3 -m graphs building-tree --input-format edge-set
    python3 -m graphs building-tree --output-format edge-set
    ```
- windows
    ```bash
    python -m graphs building-tree -v 0 -f test-graphs/1.txt
    python -m graphs building-tree -v 0 -f test-graphs/2.txt --input-format edge-set --output-format edge-set
    python -m graphs building-tree --input-format edge-set
    python -m graphs building-tree --output-format edge-set
    ```

## Для препода
Задача данного алгоритма - построить дерево на основе переданного графа. Его работа основывается на обходе графа в глубину (DFS) с проверкой на уже пройденные вершины. Фактическая его сложность есть O(n^2) так, как каждую вершину мы посещаем 1 раз и в каждой вершине мы ищем соседей среди n вершин в цикле. Для большего понимания как работать с программой смотрите примеры и команду ниже
```bash
python -m graphs building-tree --help
```
# Detecção de invasão de espaço no carro (parte de vídeo)

Protótipo que usa o **MediaPipe Pose** para detectar quando alguém dentro do carro põe a mão no espaço de outra pessoa por tempo prolongado. Funciona nos dois sentidos: motorista → passageiro e passageiro → motorista.

## Como funciona

1. A câmera fica fixa (ex.: no para-brisa, olhando para dentro do carro).
2. Cada banco é um retângulo fixo na imagem, a **zona** (`ZONES` no `config.py`).
3. Em cada frame, o MediaPipe encontra as pessoas e os pontos do corpo delas.
4. Cada pessoa pertence ao banco onde está o **meio dos seus ombros**.
5. Se uma **mão** dela (pulso ou ponta do indicador) entra na zona de **outro banco ocupado**, começa a contar o tempo.
6. Se isso dura mais que `INVASION_SECONDS` (padrão: 1,5 s), aparece um **ALERTA** na tela e no terminal.

Mão no próprio banco, ou num banco vazio (ex.: pegar uma bolsa), não conta. Uma falha de detecção em 1 frame não zera a contagem: o tempo sobe enquanto a invasão acontece e desce no mesmo ritmo quando ela para.

## Arquivos (`app/`)

| Arquivo | O que faz |
|---|---|
| `config.py` | Todos os parâmetros: vídeo, modelo, confianças, zonas, tempo do alerta |
| `zones.py` | A regra: em qual banco cada pessoa está, quem está invadindo quem e o contador de tempo |
| `main.py` | Abre o vídeo ou a webcam, roda a detecção, desenha na tela e imprime os alertas |
| `calibrate.py` | Gera as zonas (automático ou com o mouse) e grava o bloco `ZONES` no `config.py` |

## Instalação

```bash
pip install mediapipe opencv-python
```

O modelo usado é `pose_landmarker_full.task`, na raiz do projeto.

## Como rodar

Sempre de dentro da pasta `app`:

```bash
cd app
python main.py                    # vídeo definido em config.py (uber.mp4)
python main.py falso_assedio.mp4  # outro vídeo
python main.py 0                  # webcam
```

Teclas: **ESPAÇO** pausa e continua, **ESC** sai.

Na tela:
- retângulos cinza são as zonas (ficam vermelhos quando alguém invade);
- o ponto amarelo e o nome indicam o banco de cada pessoa (`fora das zonas` se ela não estiver em nenhuma);
- os pontos verdes são os pontos da mão considerados (pulsos e pontas dos indicadores);
- no topo: `atencao` (contando tempo) ou `ALERTA` (passou do limite).

No terminal:

```
[   12.3s] ALERTA: motorista -> passageiro_frente
[   15.0s] fim:    motorista -> passageiro_frente
```

## Calibração das zonas (uma vez por posição de câmera)

Numa instalação real, a câmera não se mexe, então cada banco aparece sempre no mesmo lugar da imagem. Por isso as zonas são marcadas **uma única vez**, quando a câmera é instalada, e depois valem para todo o vídeo contínuo. Só é preciso recalibrar se a câmera mudar de lugar ou de carro.

Nos testes com vídeos da internet, cada vídeo tem um ângulo diferente, então cada um precisa da sua calibração.

### Automática (padrão)

```bash
python calibrate.py                          # vídeo do config.py
python calibrate.py ia_tocando_coxa.mp4      # outro vídeo
python calibrate.py uber.mp4 --inicio 60     # analisa a partir do segundo 60
python calibrate.py 0                        # webcam
```

O script roda o MediaPipe nos primeiros segundos (`--segundos`, padrão 3) e:

1. cria uma zona em volta do corpo de cada pessoa (da cabeça aos joelhos, com uma folga);
2. divide ao meio o espaço entre duas pessoas vizinhas, para as zonas não se sobreporem;
3. chama de `motorista` a pessoa mais à direita da imagem; as outras viram `passageiro_frente` ou `banco_tras` (ombros bem menores que os do motorista = mais longe = banco de trás). O nome é só um rótulo, a regra de invasão não depende dele;
4. grava o bloco `ZONES` no `config.py` e mostra uma janela com as zonas desenhadas (aperte qualquer tecla para fechar).

Para funcionar bem, **todos precisam estar sentados normalmente no trecho analisado**, e a câmera não pode se mexer nem ter cortes. Banco vazio não ganha zona (e banco vazio já não conta como invasão). Se o resultado ficar estranho, escolha outro trecho com `--inicio` ou use o modo manual.

### Manual

```bash
python calibrate.py uber.mp4 --manual --inicio 10
```

Para cada banco (`motorista`, `passageiro_frente`, `banco_tras`): arraste um retângulo e aperte **ENTER**. Para pular um banco, aperte ENTER sem desenhar. O resultado também é gravado no `config.py`. Se duas zonas se sobrepõem, vale a que aparece primeiro na lista.

## Teste rápido com a webcam

É o jeito mais fácil de ver o alerta disparar:

1. Duas pessoas sentadas lado a lado em frente à webcam.
2. `python calibrate.py 0`, com as duas pessoas paradas nos primeiros segundos. As zonas são gravadas no `config.py`.
3. `python main.py 0`.
4. Uma pessoa coloca a mão na zona da outra e segura por 2 segundos. Deve aparecer `ALERTA` em vermelho.

## Ajustes no `config.py`

| Parâmetro | Para que serve |
|---|---|
| `INVASION_SECONDS` | Tempo até virar alerta. Menor = mais sensível, mais alarmes falsos |
| `MIN_VISIBILITY` | Visibilidade mínima de um ponto da mão para contar |
| `MIN_*_CONFIDENCE` | Quanto o MediaPipe aceita de detecções duvidosas. Valores baixos geram esqueletos "fantasma" |
| `MAX_POSES` | Máximo de pessoas procuradas |
| `MODEL_PATH` | `lite` (rápido), `full` (padrão) ou `heavy` (mais preciso, mais lento) |

## Limitações conhecidas

- **Sem profundidade:** a análise é 2D. Uma mão *na frente* de outra pessoa (ex.: na marcha) pode parecer uma invasão. Um filtro com profundidade estimada (ex.: Depth Anything V2) é uma melhoria possível.
- **Câmera fixa:** em vídeos com a câmera se mexendo (celular na mão), as zonas fixas ficam desalinhadas.
- **Corpo parcial:** o MediaPipe às vezes não acha quem está no banco de trás, ou no escuro.
- A regra indica **invasão de espaço prolongada**, que é um sinal de risco, e não uma prova de assédio.

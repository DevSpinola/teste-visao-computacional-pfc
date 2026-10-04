# zones.py
# Regra: a pessoa pertence ao banco (zona) onde está o meio dos seus ombros.
# Invasão: um pulso dela entra na zona de OUTRO banco que está ocupado.
# Funciona nos dois sentidos (motorista -> passageiro e passageiro -> motorista).

LEFT_SHOULDER, RIGHT_SHOULDER = 11, 12
LEFT_WRIST, RIGHT_WRIST = 15, 16


def zone_at(x, y, zones):
    """Nome da primeira zona que contém o ponto (x, y), ou None."""
    for name, (x1, y1, x2, y2) in zones.items():
        if x1 <= x <= x2 and y1 <= y <= y2:
            return name
    return None


def seat_of(pose, zones):
    """Banco da pessoa = zona onde fica o ponto médio entre os ombros."""
    left, right = pose[LEFT_SHOULDER], pose[RIGHT_SHOULDER]
    return zone_at((left.x + right.x) / 2, (left.y + right.y) / 2, zones)


def find_invasions(poses, zones, min_visibility):
    """
    Retorna (seats, invasions):
      seats: banco de cada pessoa detectada (ou None se estiver fora das zonas)
      invasions: conjunto de pares (invasor, vitima), ex.: {('motorista', 'banco_tras')}
    """
    seats = [seat_of(pose, zones) for pose in poses]
    occupied = {seat for seat in seats if seat}

    invasions = set()
    for pose, seat in zip(poses, seats):
        if seat is None:
            continue
        for wrist_idx in (LEFT_WRIST, RIGHT_WRIST):
            wrist = pose[wrist_idx]
            if wrist.visibility < min_visibility:
                continue
            target = zone_at(wrist.x, wrist.y, zones)
            # Mão no próprio banco ou em banco vazio (ex.: pegar a bolsa) não conta
            if target and target != seat and target in occupied:
                invasions.add((seat, target))
    return seats, invasions


class InvasionTimer:
    """
    Acumula quanto tempo cada par (invasor, vitima) está em invasão.
    Sobe enquanto a invasão acontece e desce no mesmo ritmo quando para,
    assim uma falha de 1 frame na detecção não zera a contagem.
    """

    def __init__(self, seconds_to_alert):
        self.seconds_to_alert = seconds_to_alert
        self.elapsed = {}

    def update(self, invasions, dt):
        for pair in set(self.elapsed) | invasions:
            t = self.elapsed.get(pair, 0.0)
            t = t + dt if pair in invasions else max(0.0, t - dt)
            self.elapsed[pair] = min(t, self.seconds_to_alert * 2)

    def alerts(self):
        return [pair for pair, t in self.elapsed.items() if t >= self.seconds_to_alert]

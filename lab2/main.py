import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import random

# Tworzymy wejscia (antecedent) i wyjscia (consequent)
# Gaz 0..1 co 0.1
gas = ctrl.Antecedent(np.arange(0, 1.1, 0.1), "gas")
# Obroty 0..6000 co 100
rpm = ctrl.Antecedent(np.arange(0, 6100, 100), "rpm")
# Przyspieszenie w m/s -3..3 co 0.2
acc = ctrl.Antecedent(np.arange(-3, 3.2, 0.2), "acc")
# Co zrobic z biegiem 0..1 co 0.1
result = ctrl.Consequent(np.arange(0, 1.1, 0.1), "result")

# Tworzymy przynaleznosci
gas["braking"] = fuzz.trimf(gas.universe, [0, 0, 0.2])
gas["maintaining_speed"] = fuzz.trimf(gas.universe, [0.1, 0.2, 0.4])
gas["accelerating"] = fuzz.trimf(gas.universe, [0.2, 0.5, 1])
gas["fast_accelerating"] = fuzz.trimf(gas.universe, [0.6, 1, 1])

rpm["off"] = fuzz.trimf(rpm.universe, [0, 0, 500])
rpm["very_low"] = fuzz.trimf(rpm.universe, [200, 400, 600])
rpm["low"] = fuzz.trimf(rpm.universe, [500, 800, 1500])
rpm["optimal"] = fuzz.trimf(rpm.universe, [1000, 1600, 2500])
rpm["high"] = fuzz.trimf(rpm.universe, [1500, 3200, 5000])
rpm["too_high"] = fuzz.trimf(rpm.universe, [3000, 6000, 6000])

acc["fast_braking"] = fuzz.trimf(acc.universe, [-3, -3, -1])
acc["braking"] = fuzz.trimf(acc.universe, [-3, -1.5, 0])
acc["idle"] = fuzz.trimf(acc.universe, [-0.5, 0, 0.5])
acc["accelerating"] = fuzz.trimf(acc.universe, [0, 1.5, 3])
acc["fast_accelerating"] = fuzz.trimf(acc.universe, [1, 3, 3])

result["idle"] = fuzz.trimf(result.universe, [0, 0, 0.5])
result["shift_down"] = fuzz.trimf(result.universe, [0.25, 0.5, 0.75])
result["stay"] = fuzz.trimf(result.universe, [0.5, 0.75, 1])
result["shift_up"] = fuzz.trimf(result.universe, [0.75, 1, 1])

# Tworzymy zasady
# Tablica zasad:

#  Pedal gazu  |  Obroty  |  Przysp.  |  Wynik
# ==================================================
#    ------    |   off    |   ----    |  idle          < Grozba zgaszenia silnika - skrzynia na luz
#    ------    | very_low |   ----    | shift_down     < Obroty niskie - zrzuc na poprzedni bieg niezaleznie od tego co sie dzieje
#    ------    |   low    |   ----    |  stay          < Domyslnie - nie zmieniaj biegu
#    ------    | optimal  |   ----    |  stay          < Domyslnie - nie zmieniaj biegu
#    ------    |  high    |   ----    |  stay          < Domyslnie - nie zmieniaj biegu
#    ------    | too_high |   ----    | shift_up       < Obroty wysokie - ucieknij na wyzszy bieg niezaleznie od czegokolwiek
#   braking    |   low    |   ----    | shift_down     < Zwalniamy - zrzuc bieg na nizszych obrotach
#   braking    | optimal  | fast_brak | shift_down     < Zrzuc bieg szybciej jesli mocno hamujemy
#  maintaining | optimal  |  braking  | shift_down     < Jezeli jedziemy pod gore to zrzuc bieg troche szybciej
# accelerating |   low    |   ----    | shift_down     < Chcemy przyspieszyc - zrzuc bieg na nizszych obrotach
# accelerating | optimal  |  braking  | shift_down     < Jezeli jedziemy pod gore to zrzuc bieg troche szybciej
# accelerating | optimal  |  acceler  | shift_up       < W miare szybko wrzuc kolejny bieg jesli przyspieszamy
# fast_acceler |   low    |   ----    | shift_down     < Chcemy bardzo przyspieszyc - zrzuc bieg na nizszych obrotach
# fast_acceler | optimal  |   ----    | shift_down     < Chcemy bardzo przyspieszyc - zrzuc bieg rowniez na nieco wyzszych obrotach!
# fast_acceler |  high    |  acceler  | shift_up       < Przeciagnij bieg dluzej jesli chcemy przyspieszac szybciej

# Zalozenia dla aplikacji rzeczywistej:
# - Logika ta pauzuje na chwile przy zmianie biegu
# - Logika ta nie dziala na biegu jalowym

gear_ctrl = ctrl.ControlSystem([
    ctrl.Rule(rpm["off"],                                                      result["idle"]),
    ctrl.Rule(rpm["very_low"],                                                 result["shift_down"]),
    ctrl.Rule(rpm["low"] | rpm["optimal"] | rpm["high"],                       result["stay"]),
    ctrl.Rule(rpm["too_high"],                                                 result["shift_up"]),
    ctrl.Rule(gas["braking"]           & rpm["low"],                           result["shift_down"]),
    ctrl.Rule(gas["braking"]           & rpm["optimal"] & acc["fast_braking"], result["shift_down"]),
    ctrl.Rule(gas["maintaining_speed"] & rpm["optimal"] & acc["braking"],      result["shift_down"]),
    ctrl.Rule(gas["accelerating"]      & rpm["low"],                           result["shift_down"]),
    ctrl.Rule(gas["accelerating"]      & rpm["optimal"] & acc["braking"],      result["shift_down"]),
    ctrl.Rule(gas["accelerating"]      & rpm["optimal"] & acc["accelerating"], result["shift_up"]),
    ctrl.Rule(gas["fast_accelerating"] & rpm["low"],                           result["shift_down"]),
    ctrl.Rule(gas["fast_accelerating"] & rpm["optimal"],                       result["shift_down"]),
    ctrl.Rule(gas["fast_accelerating"] & rpm["high"]    & acc["accelerating"], result["shift_up"]),
])

# Przeprowadzenie symulacji na losowych danych

for i in range(10):
    # Tworzymy symulacje
    gear_sim = ctrl.ControlSystemSimulation(gear_ctrl)
    # Generujemy parametry
    _gas = random.randint(0, 100) / 100
    _rpm = random.randint(0, 6000)
    _acc = random.randint(-100, 100) / 100
    gear_sim.input["gas"] = _gas
    gear_sim.input["rpm"] = _rpm
    gear_sim.input["acc"] = _acc
    # Generacja wyniku
    gear_sim.compute()
    # Sprawdzenie gdzie najbardziej przynalezy wynik
    max_memb = 0
    max_memb_term = ""
    for category, term in result.terms.items():
        memb = fuzz.interp_membership(result.universe, term.mf, gear_sim.output["result"])
        if memb >= max_memb:
            max_memb = memb
            max_memb_term = category
    # Wypisanie wyniku
    print()
    print("Symulacja " + str(i + 1))
    print(" - Pedal gazu: " + str(_gas))
    print(" - Obroty [rpm]: " + str(_rpm))
    print(" - Przysp. [m/s^2]: " + str(_acc))
    print("Wynik: " + str(gear_sim.output["result"]) + " -> " + max_memb_term)

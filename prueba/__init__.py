import random
import json


class Equipo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntos = 0
        self.goles_a_favor = 0
        self.goles_en_contra = 0
        self.partidos_jugados = 0

    def actualizar_estadisticas(self, goles_a_favor, goles_en_contra):
        self.goles_a_favor += goles_a_favor
        self.goles_en_contra += goles_en_contra
        self.partidos_jugados += 1
        if goles_a_favor > goles_en_contra:
            self.puntos += 3
        elif goles_a_favor == goles_en_contra:
            self.puntos += 1


class Partido:
    def __init__(self, equipo_local, equipo_visitante):
        self.equipo_local = equipo_local
        self.equipo_visitante = equipo_visitante
        self.goles_local = random.randint(0, 5)
        self.goles_visitante = random.randint(0, 5)

    def simular(self):
        self.equipo_local.actualizar_estadisticas(self.goles_local, self.goles_visitante)
        self.equipo_visitante.actualizar_estadisticas(self.goles_visitante, self.goles_local)
        return self.goles_local, self.goles_visitante


class Torneo:
    def __init__(self, nombre, equipos):
        self.nombre = nombre
        self.equipos = equipos
        self.partidos = []

    def simular_torneo(self):
        for i in range(len(self.equipos)):
            for j in range(i + 1, len(self.equipos)):
                partido = Partido(self.equipos[i], self.equipos[j])
                self.partidos.append(partido.simular())

    def generar_tabla_posiciones(self):
        self.equipos = sorted(self.equipos, key=lambda equipo: (
            equipo.puntos,
            equipo.goles_a_favor - equipo.goles_en_contra,
            equipo.goles_a_favor
        ), reverse=True)

    def obtener_campeon(self):
        self.generar_tabla_posiciones()
        return self.equipos[0]


class Liga:
    def __init__(self, equipos):
        self.equipos = equipos
        self.torneo_apertura = Torneo("Apertura", equipos)
        self.torneo_clausura = Torneo("Clausura", equipos)

    def simular_liga(self):
        print("Simulando Torneo Apertura...")
        self.torneo_apertura.simular_torneo()
        campeon_apertura = self.torneo_apertura.obtener_campeon()
        print(f"Campeón del Torneo Apertura: {campeon_apertura.nombre}")

        print("Simulando Torneo Clausura...")
        self.torneo_clausura.simular_torneo()
        campeon_clausura = self.torneo_clausura.obtener_campeon()
        print(f"Campeón del Torneo Clausura: {campeon_clausura.nombre}")

    def calcular_promedios_descenso(self):
        promedios = {}
        for equipo in self.equipos:
            if equipo.partidos_jugados > 0:
                promedio = equipo.puntos / equipo.partidos_jugados
            else:
                promedio = 0
            promedios[equipo.nombre] = promedio

        equipos_ordenados = list(promedios.items())
        for i in range(len(equipos_ordenados) - 1):
            for j in range(i + 1, len(equipos_ordenados)):
                if equipos_ordenados[i][1] > equipos_ordenados[j][1]:
                    equipos_ordenados[i], equipos_ordenados[j] = equipos_ordenados[j], equipos_ordenados[i]

        return equipos_ordenados

    def mostrar_resultados_finales(self):
        print("\n--- Resumen Final de la Temporada ---")
        print("Campeón del Torneo Apertura:", self.torneo_apertura.obtener_campeon().nombre)
        print("Campeón del Torneo Clausura:", self.torneo_clausura.obtener_campeon().nombre)

        print("\nTabla Final del Torneo Apertura:")
        self.torneo_apertura.generar_tabla_posiciones()
        for equipo in self.torneo_apertura.equipos:
            print(f"{equipo.nombre} - Puntos: {equipo.puntos}, Goles a Favor: {equipo.goles_a_favor}, Goles en Contra: {equipo.goles_en_contra}")

        print("\nTabla Final del Torneo Clausura:")
        self.torneo_clausura.generar_tabla_posiciones()
        for equipo in self.torneo_clausura.equipos:
            print(f"{equipo.nombre} - Puntos: {equipo.puntos}, Goles a Favor: {equipo.goles_a_favor}, Goles en Contra: {equipo.goles_en_contra}")

        print("\nEquipos descendidos por promedio:")
        equipos_descendidos = self.calcular_promedios_descenso()[:2]
        for equipo, promedio in equipos_descendidos:
            print(f"{equipo} - Promedio: {promedio:.2f}")

    def guardar_resultados(self, archivo="resultados_liga.json"):
        datos = {
            "apertura": [{"equipo": equipo.nombre, "puntos": equipo.puntos, "goles_a_favor": equipo.goles_a_favor,
                          "goles_en_contra": equipo.goles_en_contra} for equipo in self.torneo_apertura.equipos],
            "clausura": [{"equipo": equipo.nombre, "puntos": equipo.puntos, "goles_a_favor": equipo.goles_a_favor,
                          "goles_en_contra": equipo.goles_en_contra} for equipo in self.torneo_clausura.equipos],
            "descendidos": self.calcular_promedios_descenso()[:2]
        }
        with open(archivo, "w") as f:
            json.dump(datos, f)
        print(f"Resultados guardados en {archivo}")


equipos = [Equipo("Equipo A"), Equipo("Equipo B"), Equipo("Equipo C"), Equipo("Equipo D")]
liga = Liga(equipos)

liga.simular_liga()

liga.mostrar_resultados_finales()

liga.guardar_resultados()



import random
import numpy as npy
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def create_custom_colormap(cmap_name = 'viridis'):
    """
    Crea un mapa de colores personalizado con blanco para -1 y una escala para otros valores.

    Parameters:
        cmap_name (str): Nombre del mapa de colores base a utilizar.

    Returns:
        LinearSegmentedColormap: Mapa de colores personalizado.
    """

    # Obtiene el mapa de colores base especificado por cmap_name
    cmap = plt.get_cmap(cmap_name)

    # Crea una lista de colores utilizando el mapa de colores base
    cmap_list = [cmap(i) for i in range(cmap.N)]

    # Establece el color blanco para el valor -1 en la lista de colores
    cmap_list[0] = (1, 1, 1, 1)  # Blanco: (R, G, B, A)

    # Crea un mapa de colores lineal segmentado personalizado a partir de la lista de colores
    custom_cmap = LinearSegmentedColormap.from_list('custom_colormap', cmap_list, cmap.N)

    return custom_cmap

def initialize_road(length, density, max_speed):
    """
    Inicializa la carretera con vehículos.

    Parameters:
        length (int): Longitud de la carretera.
        density (float): Densidad de vehículos en la carretera.
        max_speed (int): Velocidad máxima de los vehículos.

    Returns:
        list: Lista que representa el estado inicial de la carretera.
    """

    road = [-1 if random.random() > density else random.randint(0, max_speed) for _ in range(length)]

    return road

def update(road, max_speed, p_slow):
    """
    Actualiza el estado de la carretera en un paso de simulación.

    Parameters:
        road (list): Lista que representa el estado actual de la carretera.
        max_speed (int): Velocidad máxima de los vehículos.
        p_slow (float): Probabilidad de reducir la velocidad.

    Returns:
        list: Lista que representa el estado actualizado de la carretera.
    """

    new_road = [-1] * len(road)

    for i in range(len(road)):
        if road[i] == -1:
            continue
        else:
            distance = 1
            while road[(i + distance) % len(road)] == -1:
                distance += 1
            if road[i] < max_speed and distance > road[i]:
                road[i] += 1
            if road[i] > 0 and random.random() < p_slow:
                road[i] -= 1
            new_position = min(i + road[i], len(road) - 1)
            new_road[new_position] = road[i]

    return new_road

def simulate_traffic(length, density, max_speed, p_slow, num_steps):
    """
    Simula el tráfico vehicular y muestra un heatmap de la carretera en cada paso de tiempo.

    Parameters:
        length (int): Longitud de la carretera.
        density (float): Densidad de vehículos en la carretera.
        max_speed (int): Velocidad máxima de los vehículos.
        p_slow (float): Probabilidad de reducir la velocidad.
        num_steps (int): Número de pasos de simulación.
    """

    road = initialize_road(length, density, max_speed)
    heatmap = []

    for step in range(num_steps):
        heatmap.append(road.copy())
        road = update(road, max_speed, p_slow)

    heatmap = npy.array(heatmap)

    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (length/(5*3), num_steps/3))

    heatmap = ax.imshow(heatmap,
                        cmap = create_custom_colormap(cmap_name = 'brg'),
                        origin = 'upper',
                        aspect = 'auto',
                        vmin = -0.5)
    ax.set_xlabel("Posición")
    ax.set_ylabel("Tiempo")
    ax.set_yticks(range(num_steps + 1))
    ax.set_title("Simulación de Tráfico")
    fig.colorbar(heatmap,
                 label = "Velocidad del vehículo",
                 ax = ax)


if __name__ == "__main__":

    ROAD_LENGTH = 900  # Longitud de la carretera
    VEHICLE_DENSITY = 0.5  # Densidad de vehículos en la carretera
    MAX_VEHICLE_SPEED = 10  # Velocidad máxima de los vehículos
    SLOWDOWN_PROBABILITY = 0.3  # Probabilidad de reducir la velocidad
    SIMULATION_STEPS = 40  # Número de pasos de simulación

    simulate_traffic(ROAD_LENGTH,
                     VEHICLE_DENSITY,
                     MAX_VEHICLE_SPEED,
                     SLOWDOWN_PROBABILITY,
                     SIMULATION_STEPS)

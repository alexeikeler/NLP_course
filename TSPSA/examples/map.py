import pandas as pd
import geopandas as gpd
import plotly_express as px
import networkx as nx
import osmnx as ox
import folium

from tabulate import tabulate
from shapely.geometry import Point, LineString
from matplotlib import pyplot as plt
from collections import defaultdict

mcdonalds_crds = {
    '1':(46.46017852906863, 30.74971815202219),
    '2':(46.43770354539548, 30.746456117114306),
    '3':(46.43050142005451, 30.72908567280626)
}
ox.config(use_cache=True, log_console=True)


def create_graph(loc, dist, transport_mode, loc_type='address') -> nx.MultiDiGraph | None:
    """

    :param loc:
    :param dist:
    :param transport_mode: walk, bile, drive, drive_service, all
    :param loc_type:
    :return:
    """
    graph = None
    if loc_type == 'address':
        graph = ox.graph_from_address(loc, dist=dist, network_type=transport_mode)

    elif loc_type == 'points':
        graph = ox.graph_from_point(loc, dist=dist, network_type=transport_mode)

    return graph


def folium_test():
    ox.config(log_console=True, use_cache=True)
    g_walk = ox.graph_from_place('Odessa', network_type='walk')
    routes = []
    #latlon = [ (51.249443914705175, -0.13878830247011467), (51.249443914705175, -0.13878830247011467), (51.249768239976866, -2.8610415615063034)]
    mapit = folium.Map( location=[46.467321113604406, 30.73313785866247], zoom_start=15)
    
    for coord in mcdonalds_crds.values():
        folium.Marker( location=[ coord[0], coord[1] ], fill_color='#43d9de', radius=8 ).add_to( mapit )

    for from_ in mcdonalds_crds.values():
        for to_ in mcdonalds_crds.values():
            start = ox.get_nearest_node(g_walk, from_)
            end = ox.get_nearest_node(g_walk, to_)
            route = nx.shortest_path(g_walk, start, end, weight='length')
            routes.append(route)
    
    route_map = ox.plot_graph_routes(g_walk, routes)
    plt.plot(route_map)
    plt.show()

    mapit.save('odessa_macdonalds.html')






def ox_test():
    place_name = "Odessa" 
    
    graph = ox.graph_from_place(place_name)
    
    area = ox.geocode_to_gdf(place_name)
    
    buildings = ox.geometries_from_place(place_name, tags={'buildings':True})
    restaurants = ox.geometries_from_place(place_name, tags={'amenity':'restaurant'})
    restaurants[:10] = restaurants
    nodes, edges = ox.graph_to_gdfs(graph)
    
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot the footprint
    area.plot(ax=ax, facecolor='black')

    # Plot street edges
    edges.plot(ax=ax, linewidth=1, edgecolor='#FFFFFF')

    # Plot buildings
    buildings.plot(ax=ax, facecolor='khaki', alpha=0.7)

    # Plot restaurants
    restaurants.plot(ax=ax, color='red', alpha=1, markersize=15)
    plt.tight_layout()
    
    plt.show()


def main():
    folium_test()
    

if __name__ == '__main__':
    main()

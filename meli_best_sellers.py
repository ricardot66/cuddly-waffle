import concurrent.futures
from scraper_api import ScraperAPIClient
from datetime import date
from bs4 import BeautifulSoup
import requests
import math
import time
import csv
import re


start = time.perf_counter()
today = date.today()

cats = [
    'MLM1368', 'MLM1384', 'MLM1246', 'MLM1039', 'MLM1051', 'MLM1648', 'MLM1144', 'MLM1276', 'MLM1575', 'MLM1000',
    'MLM186863', 'MLM1574', 'MLM1499', 'MLM1182', 'MLM3937', 'MLM1132', 'MLM3025', 'MLM1168', 'MLM1430',
    'MLM187772', 'MLM1367'
]

cat_names = {
    'MLM1368': 'Arte, Papelería y Mercería',
    'MLM1384': 'Bebés',
    'MLM1246': 'Belleza y Cuidado Personal',
    'MLM1039': 'Cámaras y Accesorios',
    'MLM1051': 'Celulares y Telefonía',
    'MLM1648': 'Computación',
    'MLM1144': 'Consolas y Videojuegos',
    'MLM1276': 'Deportes y Fitness',
    'MLM1575': 'Electrodomésticos',
    'MLM1000': 'Electrónica, Audio y Video',
    'MLM186863': 'Herramientas y Construcción',
    'MLM1574': 'Hogar, Muebles y Jardín',
    'MLM1499': 'Industrias y Oficinas',
    'MLM1182': 'Instrumentos Musicales',
    'MLM3937': 'Joyas y Relojes',
    'MLM1132': 'Juegos y Juguetes',
    'MLM3025': 'Libros, Revistas y Comics',
    'MLM1168': 'Música, Películas y Series',
    'MLM1430': 'Ropa, Bolsas y Calzado',
    'MLM187772': 'Salud y Equipamiento Médico',
    'MLM1367': 'Antigüedades y Colecciones'
    }

cat_map = {
    'Arte': 'MLM1368',
    'Espejos Venecitas': 'MLM1368',
    'Insumos para Hacer Velas': 'MLM1368',
    'Mercería': 'MLM1368',
    'Moldes para Jabones': 'MLM1368',
    'Papelería': 'MLM1368',
    'Piezas para Llaveros': 'MLM1368',
    'Otros': 'MLM1367',
    'Andaderas y Correpasillos': 'MLM1384',
    'Artículos de Bebés para Baño': 'MLM1384',
    'Artículos de Maternidad': 'MLM1384',
    'Chupones y Mordederas': 'MLM1384',
    'Comida para Bebés': 'MLM1384',
    'Corrales para Bebés': 'MLM1384',
    'Higiene y Cuidado del Bebé': 'MLM1384',
    'Juegos y Juguetes para Bebés': 'MLM1384',
    'Lactancia y Alimentación': 'MLM1384',
    'Paseo del Bebé': 'MLM1384',
    'Recámara de Bebés': 'MLM1384',
    'Ropa y Calzado para Bebés': 'MLM1384',
    'Salud del Bebé': 'MLM1384',
    'Seguridad para Bebés': 'MLM1384',
    'Artículos de Peluquería': 'MLM1246',
    'Barbería': 'MLM1246',
    'Cuidado de la Piel': 'MLM1246',
    'Cuidado del Cabello': 'MLM1246',
    'Depilación': 'MLM1246',
    'Electrodomésticos de Belleza': 'MLM1246',
    'Farmacia': 'MLM1246',
    'Higiene Personal': 'MLM1246',
    'Manicure y Pedicure': 'MLM1246',
    'Maquillajes': 'MLM1246',
    'Perfumes y Fragancias': 'MLM1246',
    'Tratamientos de Belleza': 'MLM1246',
    'Accesorios para Cámaras': 'MLM1039',
    'Álbumes y Portarretratos': 'MLM1039',
    'Cables': 'MLM1000',
    'Cámaras': 'MLM1039',
    'Cámaras de Video': 'MLM1039',
    'Drones y Accesorios': 'MLM1000',
    'Instrumentos Ópticos': 'MLM1039',
    'Laboratorios y Mini Labs': 'MLM1039',
    'Lentes y Filtros': 'MLM1039',
    'Repuestos para Cámaras': 'MLM1039',
    'Accesorios para Celulares': 'MLM1051',
    'Celulares y Smartphones': 'MLM1051',
    'Equipos de Radiofrecuencia': 'MLM1051',
    'Lentes de Realidad Virtual': 'MLM1051',
    'Repuestos para Celulares': 'MLM1051',
    'Smartwatches y Accesorios': 'MLM1051',
    'Tarificadores y Casetas': 'MLM1051',
    'Telefonía Fija e Inalámbrica': 'MLM1051',
    'Telefonía IP': 'MLM1051',
    'Accesorios de Antiestática': 'MLM1648',
    'Accesorios para PC Gaming': 'MLM1144',
    'Almacenamiento': 'MLM1648',
    'Cables y Conectores': 'MLM1648',
    'Componentes de PC': 'MLM1648',
    'Conectividad y Redes': 'MLM1648',
    'Estuches, Cajas y Sobres': 'MLM1648',
    'Impresión': 'MLM1648',
    'Laptops y Accesorios': 'MLM1648',
    'Lectores y Scanners': 'MLM1648',
    'Limpieza y Cuidado de PCs': 'MLM1648',
    'Monitores y Accesorios': 'MLM1648',
    'Palms y Pocket PCs': 'MLM1648',
    'PC de Escritorio': 'MLM1648',
    'Periféricos de PC': 'MLM1648',
    'Proyectores y Pantallas': 'MLM1000',
    'Reguladores y No Breaks': 'MLM1648',
    'Software': 'MLM1648',
    'Tablets y Accesorios': 'MLM1648',
    'Accesorios para Consolas': 'MLM1144',
    'Consolas': 'MLM1144',
    'Maquinitas': 'MLM1144',
    'Repuestos para Consolas': 'MLM1144',
    'Videojuegos': 'MLM1144',
    'Alpinismo y Escalada': 'MLM1276',
    'Artes Marciales y Box': 'MLM1276',
    'Bádminton': 'MLM1276',
    'Básquetbol': 'MLM1276',
    'Bicicletas y Ciclismo': 'MLM1276',
    'Buceo': 'MLM1276',
    'Camping, Caza y Pesca': 'MLM1276',
    'Canoas, Kayaks e Inflables': 'MLM1276',
    'Equitación y Polo': 'MLM1276',
    'Esgrima': 'MLM1276',
    'Esqui y Snowboard': 'MLM1276',
    'Fitness y Musculación': 'MLM1276',
    'Fútbol ': 'MLM1276',
    'Fútbol Americano': 'MLM1276',
    'Golf': 'MLM1276',
    'Handball': 'MLM1276',
    'Hockey': 'MLM1276',
    'Juegos de Salón': 'MLM1132',
    'Kitesurf': 'MLM1276',
    'Monopatines y Scooters': 'MLM1276',
    'Natación': 'MLM1276',
    'Paintball': 'MLM1276',
    'Parapente': 'MLM1276',
    'Patín, Gimnasia y Danza': 'MLM1276',
    'Pilates y Yoga': 'MLM1276',
    'Pulsómetros y Cronómetros': 'MLM3937',
    'Ropa Deportiva': 'MLM1430',
    'Rugby': 'MLM1276',
    'Skateboard y Sandboard': 'MLM1276',
    'Slackline': 'MLM1276',
    'Softball y Béisbol': 'MLM1276',
    'Suplementos y Shakers': 'MLM1276',
    'Surf y Bodyboard': 'MLM1276',
    'Tenis': 'MLM1276',
    'Tenis, Paddle y Squash': 'MLM1276',
    'Tiro Deportivo': 'MLM1276',
    'Volleyball': 'MLM1276',
    'Wakeboard': 'MLM1276',
    'Windsurf': 'MLM1276',
    'Artefactos de Cuidado Personal': 'MLM1575',
    'Climatización': 'MLM1575',
    'Cocción': 'MLM1575',
    'Filtros y Purificadores': 'MLM1575',
    'Lavado': 'MLM1575',
    'Pequeños Electrodomésticos': 'MLM1575',
    'Refrigeración': 'MLM1575',
    'Accesorios para Audio y Video': 'MLM1000',
    'Accesorios para TV': 'MLM1000',
    'Audio': 'MLM1000',
    'Componentes Electrónicos': 'MLM1000',
    'Controles Remotos': 'MLM1000',
    'DVD Players y Video': 'MLM1000',
    'Fundas y Bolsos': 'MLM1000',
    'Media Streaming': 'MLM1000',
    'Pilas y Cargadores': 'MLM1000',
    'Repuestos para Audio y Video': 'MLM1000',
    'Televisores': 'MLM1000',
    'Otros Electrónicos': 'MLM1000',
    'Aberturas': 'MLM186863',
    'Componentes Eléctricos': 'MLM186863',
    'Construcción': 'MLM186863',
    'Herramientas': 'MLM186863',
    'Mobiliario para Baños': 'MLM186863',
    'Mobiliario para Cocinas': 'MLM186863',
    'Pinturería': 'MLM186863',
    'Pisos, Paredes y Aberturas': 'MLM186863',
    'Plomería': 'MLM186863',
    'Adornos y Decoración del Hogar': 'MLM1574',
    'Baños': 'MLM1574',
    'Camas, Colchones y Accesorios': 'MLM1574',
    'Cocina': 'MLM1574',
    'Cuidado del Hogar y Lavanderia': 'MLM1574',
    'Iluminación para el Hogar': 'MLM1574',
    'Jardines y Exteriores': 'MLM1574',
    'Muebles para el Hogar': 'MLM1574',
    'Organización para el Hogar': 'MLM1574',
    'Seguridad para el Hogar': 'MLM1574',
    'Textiles de Hogar y Decoración': 'MLM1574',
    'Arquitectura y Diseño': 'MLM1499',
    'Embalaje y Logística': 'MLM1499',
    'Equipamiento Médico': 'MLM187772',
    'Equipamiento para Comercios': 'MLM1499',
    'Equipamiento para Oficinas': 'MLM1499',
    'Gastronomía y Hotelería': 'MLM1499',
    'Gráfica e Impresión': 'MLM1499',
    'Herramientas Industriales': 'MLM1499',
    'Publicidad y Promoción': 'MLM1499',
    'Seguridad Laboral': 'MLM1499',
    'Textil y Calzado': 'MLM1499',
    'Uniformes': 'MLM1430',
    'Baterías y Percusión': 'MLM1182',
    'Equipos de DJ y Accesorios': 'MLM1182',
    'Estudio de Grabación': 'MLM1182',
    'Instrumentos de Cuerdas': 'MLM1182',
    'Instrumentos de Viento': 'MLM1182',
    'Metrónomos': 'MLM1182',
    'Micrófonos y Amplificadores': 'MLM1182',
    'Parlantes y Bafles': 'MLM1182',
    'Partituras y Letras': 'MLM1182',
    'Pedales y Accesorios': 'MLM1182',
    'Teclados y Pianos': 'MLM1182',
    'Exhibidores y Alhajeros': 'MLM3937',
    'Insumos para Joyería': 'MLM3937',
    'Joyería': 'MLM3937',
    'Piedras Preciosas': 'MLM3937',
    'Piercings': 'MLM3937',
    'Plumas y Bolígrafos': 'MLM3937',
    'Relojes': 'MLM3937',
    'Repuestos para Relojes': 'MLM3937',
    'Smartwatch': 'MLM3937',
    'Bloques y Construcción': 'MLM1132',
    'Casas y Tiendas para Niños': 'MLM1132',
    'Dibujo, Pintura y Manualidades': 'MLM1132',
    'Electrónicos para Niños': 'MLM1132',
    'Estampas, Álbumes y Cromos': 'MLM1132',
    'Hobbies': 'MLM1132',
    'Instrumentos Musicales': 'MLM1132',
    'Juegos de Agua y Playa': 'MLM1132',
    'Juegos de Mesa y Cartas': 'MLM1132',
    'Juegos de Plaza y Aire Libre': 'MLM1132',
    'Juguetes Antiestrés e Ingenio': 'MLM1132',
    'Juguetes de Bromas': 'MLM1132',
    'Juguetes de Oficios': 'MLM1132',
    'Juguetes para Bebés': 'MLM1132',
    'Lanzadores de Juguete': 'MLM1132',
    'Mesas y Sillas': 'MLM1132',
    'Montables para Niños': 'MLM1132',
    'Muñecos y Muñecas': 'MLM1132',
    'Patines y Patinetas': 'MLM1132',
    'Peloteros y Brincolines': 'MLM1132',
    'Peluches': 'MLM1132',
    'Títeres y Marionetas': 'MLM1132',
    'Vehículos de Juguete': 'MLM1132',
    'Catálogos': 'MLM3025',
    'Comics': 'MLM3025',
    'Libros': 'MLM3025',
    'Manga': 'MLM3025',
    'Revistas': 'MLM3025',
    'Cursos': 'MLM1168',
    'Música': 'MLM1168',
    'Películas': 'MLM1168',
    'Series de TV': 'MLM1168',
    'Accesorios de Moda': 'MLM1430',
    'Bermudas y Shorts': 'MLM1430',
    'Blusas': 'MLM1430',
    'Calzado': 'MLM1430',
    'Camisas': 'MLM1430',
    'Chamarras': 'MLM1430',
    'Equipaje y Bolsas': 'MLM1430',
    'Faldas': 'MLM1430',
    'Jumpsuits y Overoles': 'MLM1430',
    'Leggings': 'MLM1430',
    'Lotes de Ropa': 'MLM1430',
    'Pantalones y Jeans': 'MLM1430',
    'Playeras': 'MLM1430',
    'Ropa de Danza y Patín': 'MLM1430',
    'Ropa Interior y de Dormir': 'MLM1430',
    'Ropa para Bebés': 'MLM1430',
    'Saquitos, Sweaters y Chalecos': 'MLM1430',
    'Sudaderas y Hoodies': 'MLM1430',
    'Trajes': 'MLM1430',
    'Trajes de Baño': 'MLM1430',
    'Vestidos': 'MLM1430',
    'Cuidado de la Salud': 'MLM187772',
    'Masajes': 'MLM187772',
    'Movilidad': 'MLM187772',
    'Ortopedia': 'MLM187772',
    'Suplementos Alimenticios': 'MLM187772',
    'Terapias Alternativas': 'MLM187772',
    'Antigüedades': 'MLM1367',
    'Coleccionables de Deportes': 'MLM1367',
    'Esculturas': 'MLM1367',
    'Filatelia': 'MLM1367',
    'Militaria y Afines': 'MLM1367',
    'Monedas y Billetes': 'MLM1367',
    'Posters': 'MLM1367'
}

cat_dict = {
    'Arte': 'https://listado.mercadolibre.com.mx/arte/#CATEGORY_ID=MLM1945&S=hc_arte-papeleria-y-merceria',
    'Espejos Venecitas': 'https://listado.mercadolibre.com.mx/espejos-venecitas/#CATEGORY_ID=MLM381266&S=hc_arte-papeleria-y-merceria',
    'Insumos para Hacer Velas': 'https://listado.mercadolibre.com.mx/insumos-hacer-velas/#CATEGORY_ID=MLM436793&S=hc_arte-papeleria-y-merceria',
    'Mercería': 'https://listado.mercadolibre.com.mx/merceria/#CATEGORY_ID=MLM5166&S=hc_arte-papeleria-y-merceria',
    'Moldes para Jabones': 'https://listado.mercadolibre.com.mx/moldes-jabones/#CATEGORY_ID=MLM432924&S=hc_arte-papeleria-y-merceria',
    'Papelería': 'https://listado.mercadolibre.com.mx/papeleria/#CATEGORY_ID=MLM2136&S=hc_arte-papeleria-y-merceria',
    'Piezas para Llaveros': 'https://listado.mercadolibre.com.mx/piezas-llaveros/#CATEGORY_ID=MLM437077&S=hc_arte-papeleria-y-merceria',
    'Otros': 'https://listado.mercadolibre.com.mx/arte-antiguedades/otros/#CATEGORY_ID=MLM1885&S=hc_antiguedades-y-colecciones',
    'Andaderas y Correpasillos': 'https://listado.mercadolibre.com.mx/bebes/andaderas-correpasillos/#CATEGORY_ID=MLM423151&S=hc_bebes',
    'Artículos de Bebés para Baño': 'https://listado.mercadolibre.com.mx/bebes/bano/#CATEGORY_ID=MLM5702&S=hc_bebes',
    'Artículos de Maternidad': 'https://listado.mercadolibre.com.mx/bebes/maternidad/#CATEGORY_ID=MLM429651&S=hc_bebes',
    'Chupones y Mordederas': 'https://listado.mercadolibre.com.mx/bebes/chupones-mordederas/#CATEGORY_ID=MLM421311&S=hc_bebes',
    'Comida para Bebés': 'https://listado.mercadolibre.com.mx/bebes/comida/#CATEGORY_ID=MLM39965&S=hc_bebes',
    'Corrales para Bebés': 'https://listado.mercadolibre.com.mx/corrales-bebes/#CATEGORY_ID=MLM40393&S=hc_bebes',
    'Higiene y Cuidado del Bebé': 'https://listado.mercadolibre.com.mx/bebes/higiene-cuidado/#CATEGORY_ID=MLM187792&S=hc_bebes',
    'Juegos y Juguetes para Bebés': 'https://listado.mercadolibre.com.mx/juegos-juguetes-bebes/#CATEGORY_ID=MLM1392&S=hc_bebes',
    'Lactancia y Alimentación': 'https://listado.mercadolibre.com.mx/lactancia-alimentacion/#CATEGORY_ID=MLM5360&S=hc_bebes',
    'Paseo del Bebé': 'https://listado.mercadolibre.com.mx/bebes/paseo/#CATEGORY_ID=MLM429683&S=hc_bebes',
    'Recámara de Bebés': 'https://listado.mercadolibre.com.mx/bebes/recamara/#CATEGORY_ID=MLM5362&S=hc_bebes',
    'Ropa y Calzado para Bebés': 'https://listado.mercadolibre.com.mx/bebes/ropa-calzado/#CATEGORY_ID=MLM1396&S=hc_bebes',
    'Salud del Bebé': 'https://listado.mercadolibre.com.mx/bebes/salud/#CATEGORY_ID=MLM429704&S=hc_bebes',
    'Seguridad para Bebés': 'https://listado.mercadolibre.com.mx/bebes/seguridad/#CATEGORY_ID=MLM1385&S=hc_bebes',
    'Artículos de Peluquería': 'https://listado.mercadolibre.com.mx/cuidado-personal/articulos-de-peluqueria/#CATEGORY_ID=MLM187817&S=hc_belleza-y-cuidado-personal',
    'Barbería': 'https://listado.mercadolibre.com.mx/barberia/#CATEGORY_ID=MLM194072&S=hc_belleza-y-cuidado-personal',
    'Cuidado de la Piel': 'https://listado.mercadolibre.com.mx/cuidado-personal/cuidado-de-la-piel/#CATEGORY_ID=MLM1253&S=hc_belleza-y-cuidado-personal',
    'Cuidado del Cabello': 'https://listado.mercadolibre.com.mx/cuidado-personal/cuidado-del-cabello/#CATEGORY_ID=MLM1263&S=hc_belleza-y-cuidado-personal',
    'Depilación': 'https://listado.mercadolibre.com.mx/cuidado-personal/depilacion/#CATEGORY_ID=MLM43673&S=hc_belleza-y-cuidado-personal',
    'Electrodomésticos de Belleza': 'https://listado.mercadolibre.com.mx/cuidado-personal/electrodomesticos-de-belleza/#CATEGORY_ID=MLM187814&S=hc_belleza-y-cuidado-personal',
    'Farmacia': 'https://listado.mercadolibre.com.mx/farmacia/#CATEGORY_ID=MLM194452&S=hc_belleza-y-cuidado-personal',
    'Higiene Personal': 'https://listado.mercadolibre.com.mx/cuidado-personal/higiene-personal/#CATEGORY_ID=MLM187663&S=hc_belleza-y-cuidado-personal',
    'Manicure y Pedicure': 'https://listado.mercadolibre.com.mx/cuidado-personal/manicure-pedicure/#CATEGORY_ID=MLM126070&S=hc_belleza-y-cuidado-personal',
    'Maquillajes': 'https://listado.mercadolibre.com.mx/maquillajes/#CATEGORY_ID=MLM1248&S=hc_belleza-y-cuidado-personal',
    'Perfumes y Fragancias': 'https://listado.mercadolibre.com.mx/perfumes-fragancias/#CATEGORY_ID=MLM454712&S=hc_belleza-y-cuidado-personal',
    'Tratamientos de Belleza': 'https://listado.mercadolibre.com.mx/tratamientos-belleza/#CATEGORY_ID=MLM194417&S=hc_belleza-y-cuidado-personal',
    'Accesorios para Cámaras': 'https://fotografia.mercadolibre.com.mx/accesorios-camaras/#CATEGORY_ID=MLM1049&S=hc_camaras-y-accesorios',
    'Álbumes y Portarretratos': 'https://fotografia.mercadolibre.com.mx/albumes-portarretratos/#CATEGORY_ID=MLM1041&S=hc_camaras-y-accesorios',
    'Cables': 'https://electronica.mercadolibre.com.mx/cables/#CATEGORY_ID=MLM432164&S=hc_electronica-audio-y-video',
    'Cámaras': 'https://fotografia.mercadolibre.com.mx/camaras/#CATEGORY_ID=MLM168281&S=hc_camaras-y-accesorios',
    'Cámaras de Video': 'https://fotografia.mercadolibre.com.mx/camaras-video/#CATEGORY_ID=MLM174554&S=hc_camaras-y-accesorios',
    'Drones y Accesorios': 'https://electronica.mercadolibre.com.mx/drones-accesorios/#CATEGORY_ID=MLM145906&S=hc_electronica-audio-y-video',
    'Instrumentos Ópticos': 'https://fotografia.mercadolibre.com.mx/instrumentos-opticos/#CATEGORY_ID=MLM4708&S=hc_camaras-y-accesorios',
    'Laboratorios y Mini Labs': 'https://fotografia.mercadolibre.com.mx/laboratorios-mini-labs/#CATEGORY_ID=MLM10372&S=hc_camaras-y-accesorios',
    'Lentes y Filtros': 'https://fotografia.mercadolibre.com.mx/lentes-filtros/#CATEGORY_ID=MLM437477&S=hc_camaras-y-accesorios',
    'Repuestos para Cámaras': 'https://fotografia.mercadolibre.com.mx/repuestos-camaras/#CATEGORY_ID=MLM430989&S=hc_camaras-y-accesorios',
    'Accesorios para Celulares': 'https://celulares.mercadolibre.com.mx/accesorios/#CATEGORY_ID=MLM3813&S=hc_celulares-y-telefonia',
    'Celulares y Smartphones': 'https://celulares.mercadolibre.com.mx/#CATEGORY_ID=MLM1055&S=hc_celulares-y-telefonia',
    'Equipos de Radiofrecuencia': 'https://telefonos.mercadolibre.com.mx/equipos-radiofrecuencia/#CATEGORY_ID=MLM1058&S=hc_celulares-y-telefonia',
    'Lentes de Realidad Virtual': 'https://celulares.mercadolibre.com.mx/lentes-realidad-virtual/#CATEGORY_ID=MLM179588&S=hc_celulares-y-telefonia',
    'Repuestos para Celulares': 'https://celulares.mercadolibre.com.mx/repuestos/#CATEGORY_ID=MLM192051&S=hc_celulares-y-telefonia',
    'Smartwatches y Accesorios': 'https://celulares.mercadolibre.com.mx/smartwatches-accesorios/#CATEGORY_ID=MLM194341&S=hc_celulares-y-telefonia',
    'Tarificadores y Casetas': 'https://telefonos.mercadolibre.com.mx/tarificadores-casetas/#CATEGORY_ID=MLM437904&S=hc_celulares-y-telefonia',
    'Telefonía Fija e Inalámbrica': 'https://telefonos.mercadolibre.com.mx/telefonia-fija-e-inalambrica/#CATEGORY_ID=MLM437210&S=hc_celulares-y-telefonia',
    'Telefonía IP': 'https://celulares.mercadolibre.com.mx/telefonia-ip/#CATEGORY_ID=MLM7502&S=hc_celulares-y-telefonia',
    'Accesorios de Antiestática': 'https://computacion.mercadolibre.com.mx/accesorios-antiestatica/#CATEGORY_ID=MLM191082&S=hc_computacion',
    'Accesorios para PC Gaming': 'https://videojuegos.mercadolibre.com.mx/accesorios-pc-gaming/#CATEGORY_ID=MLM123324&S=hc_consolas-y-videojuegos',
    'Almacenamiento': 'https://computacion.mercadolibre.com.mx/almacenamiento/#CATEGORY_ID=MLM430598&S=hc_computacion',
    'Cables y Conectores': 'https://computacion.mercadolibre.com.mx/cables-conectores/#CATEGORY_ID=MLM10848&S=hc_computacion',
    'Componentes de PC': 'https://computacion.mercadolibre.com.mx/componentes-de-pc/#CATEGORY_ID=MLM1691&S=hc_computacion',
    'Conectividad y Redes': 'https://computacion.mercadolibre.com.mx/conectividad-redes/#CATEGORY_ID=MLM1700&S=hc_computacion',
    'Estuches, Cajas y Sobres': 'https://computacion.mercadolibre.com.mx/estuches-cajas-sobres/#CATEGORY_ID=MLM3699&S=hc_computacion',
    'Impresión': 'https://computacion.mercadolibre.com.mx/impresion/#CATEGORY_ID=MLM182235&S=hc_computacion',
    'Laptops y Accesorios': 'https://computacion.mercadolibre.com.mx/laptops-accesorios/#CATEGORY_ID=MLM430687&S=hc_computacion',
    'Lectores y Scanners': 'https://computacion.mercadolibre.com.mx/lectores-scanners/#CATEGORY_ID=MLM439434&S=hc_computacion',
    'Limpieza y Cuidado de PCs': 'https://computacion.mercadolibre.com.mx/limpieza-cuidado-pcs/#CATEGORY_ID=MLM36845&S=hc_computacion',
    'Monitores y Accesorios': 'https://computacion.mercadolibre.com.mx/monitores-accesorios/#CATEGORY_ID=MLM1655&S=hc_computacion',
    'Palms y Pocket PCs': 'https://computacion.mercadolibre.com.mx/palms-y-pocket-pcs/#CATEGORY_ID=MLM1651&S=hc_computacion',
    'PC de Escritorio': 'https://computacion.mercadolibre.com.mx/pc-escritorio/#CATEGORY_ID=MLM438450&S=hc_computacion',
    'Periféricos de PC': 'https://computacion.mercadolibre.com.mx/perifericos-pc/#CATEGORY_ID=MLM454379&S=hc_computacion',
    'Proyectores y Pantallas': 'https://electronica.mercadolibre.com.mx/proyectores-y-pantallas/#CATEGORY_ID=MLM2830&S=hc_electronica-audio-y-video',
    'Reguladores y No Breaks': 'https://computacion.mercadolibre.com.mx/reguladores-no-breaks/#CATEGORY_ID=MLM1718&S=hc_computacion',
    'Software': 'https://computacion.mercadolibre.com.mx/software/#CATEGORY_ID=MLM1723&S=hc_computacion',
    'Tablets y Accesorios': 'https://computacion.mercadolibre.com.mx/tablets-y-accesorios/#CATEGORY_ID=MLM182456&S=hc_computacion',
    'Accesorios para Consolas': 'https://videojuegos.mercadolibre.com.mx/accesorios-consolas/#CATEGORY_ID=MLM438578&S=hc_consolas-y-videojuegos',
    'Consolas': 'https://videojuegos.mercadolibre.com.mx/consolas/#CATEGORY_ID=MLM167860&S=hc_consolas-y-videojuegos',
    'Maquinitas': 'https://videojuegos.mercadolibre.com.mx/maquinitas/#CATEGORY_ID=MLM8232&S=hc_consolas-y-videojuegos',
    'Repuestos para Consolas': 'https://videojuegos.mercadolibre.com.mx/repuestos-consolas/#CATEGORY_ID=MLM438579&S=hc_consolas-y-videojuegos',
    'Videojuegos': 'https://videojuegos.mercadolibre.com.mx/videojuegos/#CATEGORY_ID=MLM151595&S=hc_consolas-y-videojuegos',
    'Alpinismo y Escalada': 'https://deportes.mercadolibre.com.mx/alpinismo-escalada/#CATEGORY_ID=MLM1357&S=hc_deportes-y-fitness-',
    'Artes Marciales y Box': 'https://deportes.mercadolibre.com.mx/artes-marciales-box/#CATEGORY_ID=MLM2480&S=hc_deportes-y-fitness-',
    'Bádminton': 'https://deportes.mercadolibre.com.mx/badminton/#CATEGORY_ID=MLM191799&S=hc_deportes-y-fitness-',
    'Básquetbol': 'https://deportes.mercadolibre.com.mx/basquetbol/#CATEGORY_ID=MLM1309&S=hc_deportes-y-fitness-',
    'Bicicletas y Ciclismo': 'https://deportes.mercadolibre.com.mx/bicicletas-y-ciclismo/#CATEGORY_ID=MLM1292&S=hc_deportes-y-fitness-',
    'Buceo': 'https://deportes.mercadolibre.com.mx/buceo/#CATEGORY_ID=MLM8969&S=hc_deportes-y-fitness-',
    'Camping, Caza y Pesca': 'https://deportes.mercadolibre.com.mx/camping-caza-pesca/#CATEGORY_ID=MLM1362&S=hc_deportes-y-fitness-',
    'Canoas, Kayaks e Inflables': 'https://deportes.mercadolibre.com.mx/canoas-kayaks-e-inflables/#CATEGORY_ID=MLM438178&S=hc_deportes-y-fitness-',
    'Equitación y Polo': 'https://deportes.mercadolibre.com.mx/equitacion-polo/#CATEGORY_ID=MLM437767&S=hc_deportes-y-fitness-',
    'Esgrima': 'https://deportes.mercadolibre.com.mx/esgrima/#CATEGORY_ID=MLM417504&S=hc_deportes-y-fitness-',
    'Esqui y Snowboard': 'https://deportes.mercadolibre.com.mx/esqui-snowboard/#CATEGORY_ID=MLM421369&S=hc_deportes-y-fitness-',
    'Fitness y Musculación': 'https://deportes.mercadolibre.com.mx/fitness-musculacion/#CATEGORY_ID=MLM1338&S=hc_deportes-y-fitness-',
    'Fútbol ': 'https://deportes.mercadolibre.com.mx/futbol/#CATEGORY_ID=MLM1285&S=hc_deportes-y-fitness-',
    'Fútbol Americano': 'https://deportes.mercadolibre.com.mx/futbol-americano/#CATEGORY_ID=MLM1302&S=hc_deportes-y-fitness-',
    'Golf': 'https://deportes.mercadolibre.com.mx/golf/#CATEGORY_ID=MLM1342&S=hc_deportes-y-fitness-',
    'Handball': 'https://deportes.mercadolibre.com.mx/handball/#CATEGORY_ID=MLM438532&S=hc_deportes-y-fitness-',
    'Hockey': 'https://deportes.mercadolibre.com.mx/hockey/#CATEGORY_ID=MLM189113&S=hc_deportes-y-fitness-',
    'Juegos de Salón': 'https://listado.mercadolibre.com.mx/juegos-salon/#CATEGORY_ID=MLM436922&S=hc_juegos-y-juguetes',
    'Kitesurf': 'https://deportes.mercadolibre.com.mx/kitesurf/#CATEGORY_ID=MLM18308&S=hc_deportes-y-fitness-',
    'Monopatines y Scooters': 'https://deportes.mercadolibre.com.mx/monopatines-scooters/#CATEGORY_ID=MLM410723&S=hc_deportes-y-fitness-',
    'Natación': 'https://deportes.mercadolibre.com.mx/natacion/#CATEGORY_ID=MLM174624&S=hc_deportes-y-fitness-',
    'Paintball': 'https://deportes.mercadolibre.com.mx/paintball/#CATEGORY_ID=MLM4349&S=hc_deportes-y-fitness-',
    'Parapente': 'https://deportes.mercadolibre.com.mx/parapente/#CATEGORY_ID=MLM432691&S=hc_deportes-y-fitness-',
    'Patín, Gimnasia y Danza': 'https://deportes.mercadolibre.com.mx/patin-gimnasia-danza/#CATEGORY_ID=MLM437400&S=hc_deportes-y-fitness-',
    'Pilates y Yoga': 'https://deportes.mercadolibre.com.mx/pilates-y-yoga/#CATEGORY_ID=MLM69803&S=hc_deportes-y-fitness-',
    'Pulsómetros y Cronómetros': 'https://joyas.mercadolibre.com.mx/pulsometros-cronometros/#CATEGORY_ID=MLM436822&S=hc_joyas-y-relojes',
    'Ropa Deportiva': 'https://ropa.mercadolibre.com.mx/ropa-deportiva/#CATEGORY_ID=MLM120666&S=hc_ropa-bolsas-y-calzado',
    'Rugby': 'https://deportes.mercadolibre.com.mx/rugby/#CATEGORY_ID=MLM421387&S=hc_deportes-y-fitness-',
    'Skateboard y Sandboard': 'https://deportes.mercadolibre.com.mx/skateboard-sandboard/#CATEGORY_ID=MLM6140&S=hc_deportes-y-fitness-',
    'Slackline': 'https://deportes.mercadolibre.com.mx/slackline/#CATEGORY_ID=MLM194385&S=hc_deportes-y-fitness-',
    'Softball y Béisbol': 'https://deportes.mercadolibre.com.mx/softball-beisbol/#CATEGORY_ID=MLM1328&S=hc_deportes-y-fitness-',
    'Suplementos y Shakers': 'https://deportes.mercadolibre.com.mx/suplementos-shakers/#CATEGORY_ID=MLM438393&S=hc_deportes-y-fitness-',
    'Surf y Bodyboard': 'https://deportes.mercadolibre.com.mx/surf-bodyboard/#CATEGORY_ID=MLM4682&S=hc_deportes-y-fitness-',
    'Tenis': 'https://deportes.mercadolibre.com.mx/tenis/#CATEGORY_ID=MLM5607&S=hc_deportes-y-fitness-',
    'Tenis, Paddle y Squash': 'https://deportes.mercadolibre.com.mx/tenis-paddle-y-squash/#CATEGORY_ID=MLM6144&S=hc_deportes-y-fitness-',
    'Tiro Deportivo': 'https://deportes.mercadolibre.com.mx/tiro-deportivo/#CATEGORY_ID=MLM440904&S=hc_deportes-y-fitness-',
    'Volleyball': 'https://deportes.mercadolibre.com.mx/volleyball/#CATEGORY_ID=MLM422147&S=hc_deportes-y-fitness-',
    'Wakeboard': 'https://deportes.mercadolibre.com.mx/wakeboard/#CATEGORY_ID=MLM191639&S=hc_deportes-y-fitness-',
    'Windsurf': 'https://deportes.mercadolibre.com.mx/windsurf/#CATEGORY_ID=MLM438930&S=hc_deportes-y-fitness-',
    'Artefactos de Cuidado Personal': 'https://electrodomesticos.mercadolibre.com.mx/artefactos-cuidado-personal/#CATEGORY_ID=MLM438597&S=hc_electrodomesticos',
    'Climatización': 'https://electrodomesticos.mercadolibre.com.mx/climatizacion/#CATEGORY_ID=MLM158840&S=hc_electrodomesticos',
    'Cocción': 'https://electrodomesticos.mercadolibre.com.mx/coccion/#CATEGORY_ID=MLM158828&S=hc_electrodomesticos',
    'Filtros y Purificadores': 'https://electrodomesticos.mercadolibre.com.mx/filtros-purificadores/#CATEGORY_ID=MLM438451&S=hc_electrodomesticos',
    'Lavado': 'https://electrodomesticos.mercadolibre.com.mx/lavado/#CATEGORY_ID=MLM438282&S=hc_electrodomesticos',
    'Pequeños Electrodomésticos': 'https://electrodomesticos.mercadolibre.com.mx/pequenos/#CATEGORY_ID=MLM438284&S=hc_electrodomesticos',
    'Refrigeración': 'https://electrodomesticos.mercadolibre.com.mx/refrigeracion/#CATEGORY_ID=MLM1576&S=hc_electrodomesticos',
    'Accesorios para Audio y Video': 'https://electronica.mercadolibre.com.mx/accesorios-audio-y-video/#CATEGORY_ID=MLM4887&S=hc_electronica-audio-y-video',
    'Accesorios para TV': 'https://electronica.mercadolibre.com.mx/accesorios-tv/#CATEGORY_ID=MLM431414&S=hc_electronica-audio-y-video',
    'Audio': 'https://electronica.mercadolibre.com.mx/audio/#CATEGORY_ID=MLM438078&S=hc_electronica-audio-y-video',
    'Componentes Electrónicos': 'https://electronica.mercadolibre.com.mx/componentes-electronicos/#CATEGORY_ID=MLM189492&S=hc_electronica-audio-y-video',
    'Controles Remotos': 'https://electronica.mercadolibre.com.mx/controles-remotos/#CATEGORY_ID=MLM4914&S=hc_electronica-audio-y-video',
    'DVD Players y Video': 'https://electronica.mercadolibre.com.mx/dvd-players-y-video/#CATEGORY_ID=MLM1004&S=hc_electronica-audio-y-video',
    'Fundas y Bolsos': 'https://electronica.mercadolibre.com.mx/fundas-bolsos/#CATEGORY_ID=MLM189967&S=hc_electronica-audio-y-video',
    'Media Streaming': 'https://electronica.mercadolibre.com.mx/media-streaming/#CATEGORY_ID=MLM126075&S=hc_electronica-audio-y-video',
    'Pilas y Cargadores': 'https://electronica.mercadolibre.com.mx/pilas-cargadores/#CATEGORY_ID=MLM4900&S=hc_electronica-audio-y-video',
    'Repuestos para Audio y Video': 'https://electronica.mercadolibre.com.mx/repuestos-audio-y-video/#CATEGORY_ID=MLM126068&S=hc_electronica-audio-y-video',
    'Televisores': 'https://electronica.mercadolibre.com.mx/televisores/#CATEGORY_ID=MLM1002&S=hc_electronica-audio-y-video',
    'Otros Electrónicos': 'https://electronica.mercadolibre.com.mx/otros/#CATEGORY_ID=MLM1009&S=hc_electronica-audio-y-video',
    'Aberturas': 'https://listado.mercadolibre.com.mx/aberturas/#CATEGORY_ID=MLM438191&S=hc_herramientas-y-construccion',
    'Componentes Eléctricos': 'https://listado.mercadolibre.com.mx/componentes-electricos/#CATEGORY_ID=MLM189340&S=hc_herramientas-y-construccion',
    'Construcción': 'https://listado.mercadolibre.com.mx/herramientas-y-construccion/construccion/#CATEGORY_ID=MLM1500&S=hc_herramientas-y-construccion',
    'Herramientas': 'https://listado.mercadolibre.com.mx/herramientas-y-construccion/herramientas/#CATEGORY_ID=MLM2525&S=hc_herramientas-y-construccion',
    'Mobiliario para Baños': 'https://listado.mercadolibre.com.mx/mobiliario-banos/#CATEGORY_ID=MLM189241&S=hc_herramientas-y-construccion',
    'Mobiliario para Cocinas': 'https://listado.mercadolibre.com.mx/mobiliario-cocinas/#CATEGORY_ID=MLM411938&S=hc_herramientas-y-construccion',
    'Pinturería': 'https://listado.mercadolibre.com.mx/pintureria/#CATEGORY_ID=MLM178685&S=hc_herramientas-y-construccion',
    'Pisos, Paredes y Aberturas': 'https://hogar.mercadolibre.com.mx/pisos-paredes-aberturas/#CATEGORY_ID=MLM145907&S=hc_herramientas-y-construccion',
    'Plomería': 'https://listado.mercadolibre.com.mx/plomeria/#CATEGORY_ID=MLM191631&S=hc_herramientas-y-construccion',
    'Adornos y Decoración del Hogar': 'https://hogar.mercadolibre.com.mx/adornos-decoracion-del/#CATEGORY_ID=MLM1631&S=hc_hogar-muebles-y-jardin',
    'Baños': 'https://hogar.mercadolibre.com.mx/banos/#CATEGORY_ID=MLM1613&S=hc_hogar-muebles-y-jardin',
    'Camas, Colchones y Accesorios': 'https://hogar.mercadolibre.com.mx/camas-colchones-accesorios/#CATEGORY_ID=MLM437173&S=hc_hogar-muebles-y-jardin',
    'Cocina': 'https://hogar.mercadolibre.com.mx/cocina/#CATEGORY_ID=MLM8179&S=hc_hogar-muebles-y-jardin',
    'Cuidado del Hogar y Lavanderia': 'https://hogar.mercadolibre.com.mx/cuidado-del-hogar-lavanderia/#CATEGORY_ID=MLM194414&S=hc_hogar-muebles-y-jardin',
    'Iluminación para el Hogar': 'https://hogar.mercadolibre.com.mx/iluminacion-para-el-hogar/#CATEGORY_ID=MLM1582&S=hc_hogar-muebles-y-jardin',
    'Jardines y Exteriores': 'https://hogar.mercadolibre.com.mx/jardines-exteriores/#CATEGORY_ID=MLM1621&S=hc_hogar-muebles-y-jardin',
    'Muebles para el Hogar': 'https://hogar.mercadolibre.com.mx/muebles/#CATEGORY_ID=MLM436380&S=hc_hogar-muebles-y-jardin',
    'Organización para el Hogar': 'https://hogar.mercadolibre.com.mx/organizacion/#CATEGORY_ID=MLM436414&S=hc_hogar-muebles-y-jardin',
    'Seguridad para el Hogar': 'https://hogar.mercadolibre.com.mx/seguridad-para-el-hogar/#CATEGORY_ID=MLM107711&S=hc_hogar-muebles-y-jardin',
    'Textiles de Hogar y Decoración': 'https://hogar.mercadolibre.com.mx/textiles-decoracion/#CATEGORY_ID=MLM436246&S=hc_hogar-muebles-y-jardin',
    'Arquitectura y Diseño': 'https://listado.mercadolibre.com.mx/arquitectura-diseno/#CATEGORY_ID=MLM437317&S=hc_industrias-y-oficinas',
    'Embalaje y Logística': 'https://listado.mercadolibre.com.mx/embalaje-logistica/#CATEGORY_ID=MLM438242&S=hc_industrias-y-oficinas',
    'Equipamiento Médico': 'https://listado.mercadolibre.com.mx/salud-y-equipamiento-medico/equipamiento-medico/#CATEGORY_ID=MLM6556&S=hc_salud-y-equipamiento-medico',
    'Equipamiento para Comercios': 'https://listado.mercadolibre.com.mx/equipamiento-comercios/#CATEGORY_ID=MLM189757&S=hc_industrias-y-oficinas',
    'Equipamiento para Oficinas': 'https://listado.mercadolibre.com.mx/industrias-y-oficinas/equipamiento-para-oficinas/#CATEGORY_ID=MLM2102&S=hc_industrias-y-oficinas',
    'Gastronomía y Hotelería': 'https://listado.mercadolibre.com.mx/gastronomia-hoteleria/#CATEGORY_ID=MLM5182&S=hc_industrias-y-oficinas',
    'Gráfica e Impresión': 'https://listado.mercadolibre.com.mx/grafica-e-impresion/#CATEGORY_ID=MLM412676&S=hc_industrias-y-oficinas',
    'Herramientas Industriales': 'https://listado.mercadolibre.com.mx/herramientas-industriales/#CATEGORY_ID=MLM454785&S=hc_industrias-y-oficinas',
    'Publicidad y Promoción': 'https://listado.mercadolibre.com.mx/publicidad-promocion/#CATEGORY_ID=MLM437434&S=hc_industrias-y-oficinas',
    'Seguridad Laboral': 'https://listado.mercadolibre.com.mx/seguridad-laboral/#CATEGORY_ID=MLM187742&S=hc_industrias-y-oficinas',
    'Textil y Calzado': 'https://listado.mercadolibre.com.mx/textil-calzado/#CATEGORY_ID=MLM5160&S=hc_industrias-y-oficinas',
    'Uniformes': 'https://ropa.mercadolibre.com.mx/uniformes/#CATEGORY_ID=MLM191074&S=hc_ropa-bolsas-y-calzado',
    'Baterías y Percusión': 'https://instrumentos.mercadolibre.com.mx/baterias-y-percusion/#CATEGORY_ID=MLM3004&S=hc_instrumentos-musicales',
    'Equipos de DJ y Accesorios': 'https://instrumentos.mercadolibre.com.mx/equipos-dj-accesorios/#CATEGORY_ID=MLM435173&S=hc_instrumentos-musicales',
    'Estudio de Grabación': 'https://instrumentos.mercadolibre.com.mx/estudio-grabacion/#CATEGORY_ID=MLM438365&S=hc_instrumentos-musicales',
    'Instrumentos de Cuerdas': 'https://instrumentos.mercadolibre.com.mx/instrumentos-cuerdas/#CATEGORY_ID=MLM194141&S=hc_instrumentos-musicales',
    'Instrumentos de Viento': 'https://instrumentos.mercadolibre.com.mx/de-viento/#CATEGORY_ID=MLM3005&S=hc_instrumentos-musicales',
    'Metrónomos': 'https://instrumentos.mercadolibre.com.mx/metronomos/#CATEGORY_ID=MLM194207&S=hc_instrumentos-musicales',
    'Micrófonos y Amplificadores': 'https://instrumentos.mercadolibre.com.mx/microfonos-amplificadore/#CATEGORY_ID=MLM434816&S=hc_instrumentos-musicales',
    'Parlantes y Bafles': 'https://instrumentos.mercadolibre.com.mx/parlantes-bafles/#CATEGORY_ID=MLM434927&S=hc_instrumentos-musicales',
    'Partituras y Letras': 'https://instrumentos.mercadolibre.com.mx/partituras-atriles/#CATEGORY_ID=MLM194155&S=hc_instrumentos-musicales',
    'Pedales y Accesorios': 'https://instrumentos.mercadolibre.com.mx/pedales-accesorios/#CATEGORY_ID=MLM434786&S=hc_instrumentos-musicales',
    'Teclados y Pianos': 'https://instrumentos.mercadolibre.com.mx/teclados-y-pianos/#CATEGORY_ID=MLM3022&S=hc_instrumentos-musicales',
    'Exhibidores y Alhajeros': 'https://joyas.mercadolibre.com.mx/exhibidores-joyeros/#CATEGORY_ID=MLM123220&S=hc_joyas-y-relojes',
    'Insumos para Joyería': 'https://joyas.mercadolibre.com.mx/insumos-joyeria/#CATEGORY_ID=MLM404419&S=hc_joyas-y-relojes',
    'Joyería': 'https://joyas.mercadolibre.com.mx/joyeria/#CATEGORY_ID=MLM1431&S=hc_joyas-y-relojes',
    'Piedras Preciosas': 'https://joyas.mercadolibre.com.mx/piedras-preciosas/#CATEGORY_ID=MLM1441&S=hc_joyas-y-relojes',
    'Piercings': 'https://joyas.mercadolibre.com.mx/piercings/#CATEGORY_ID=MLM437168&S=hc_joyas-y-relojes',
    'Plumas y Bolígrafos': 'https://joyas.mercadolibre.com.mx/plumas-y-boligrafos/#CATEGORY_ID=MLM7667&S=hc_joyas-y-relojes',
    'Relojes': 'https://relojes.mercadolibre.com.mx/#CATEGORY_ID=MLM1442&S=hc_joyas-y-relojes',
    'Repuestos para Relojes': 'https://relojes.mercadolibre.com.mx/repuestos/#CATEGORY_ID=MLM117517&S=hc_joyas-y-relojes',
    'Smartwatch': 'https://relojes.mercadolibre.com.mx/smartwatch/#CATEGORY_ID=MLM179205&S=hc_joyas-y-relojes',
    'Bloques y Construcción': 'https://listado.mercadolibre.com.mx/bloques-construccion/#CATEGORY_ID=MLM191712&S=hc_juegos-y-juguetes',
    'Casas y Tiendas para Niños': 'https://listado.mercadolibre.com.mx/casas-carpas-ninos/#CATEGORY_ID=MLM433060&S=hc_juegos-y-juguetes',
    'Dibujo, Pintura y Manualidades': 'https://listado.mercadolibre.com.mx/dibujo-pintura-manualidades/#CATEGORY_ID=MLM418348&S=hc_juegos-y-juguetes',
    'Electrónicos para Niños': 'https://listado.mercadolibre.com.mx/electronicos-ninos/#CATEGORY_ID=MLM2961&S=hc_juegos-y-juguetes',
    'Estampas, Álbumes y Cromos': 'https://listado.mercadolibre.com.mx/estampas-albumes-cromos/#CATEGORY_ID=MLM438116&S=hc_juegos-y-juguetes',
    'Hobbies': 'https://listado.mercadolibre.com.mx/hobbies/#CATEGORY_ID=MLM432873&S=hc_juegos-y-juguetes',
    'Instrumentos Musicales': 'https://listado.mercadolibre.com.mx/instrumentos-musicales/#CATEGORY_ID=MLM11229&S=hc_juegos-y-juguetes',
    'Juegos de Agua y Playa': 'https://listado.mercadolibre.com.mx/juegos-agua-playa/#CATEGORY_ID=MLM433069&S=hc_juegos-y-juguetes',
    'Juegos de Mesa y Cartas': 'https://listado.mercadolibre.com.mx/juegos-mesa-cartas/#CATEGORY_ID=MLM432988&S=hc_juegos-y-juguetes',
    'Juegos de Plaza y Aire Libre': 'https://listado.mercadolibre.com.mx/juegos-plaza-aire-libre/#CATEGORY_ID=MLM437165&S=hc_juegos-y-juguetes',
    'Juguetes Antiestrés e Ingenio': 'https://listado.mercadolibre.com.mx/juguetes-antiestres-e-ingenio/#CATEGORY_ID=MLM189993&S=hc_juegos-y-juguetes',
    'Juguetes de Bromas': 'https://listado.mercadolibre.com.mx/juguetes-bromas/#CATEGORY_ID=MLM191696&S=hc_juegos-y-juguetes',
    'Juguetes de Oficios': 'https://listado.mercadolibre.com.mx/juguetes-oficios/#CATEGORY_ID=MLM432818&S=hc_juegos-y-juguetes',
    'Juguetes para Bebés': 'https://listado.mercadolibre.com.mx/juguetes-bebes/#CATEGORY_ID=MLM3655&S=hc_juegos-y-juguetes',
    'Lanzadores de Juguete': 'https://listado.mercadolibre.com.mx/lanzadores-juguete/#CATEGORY_ID=MLM352344&S=hc_juegos-y-juguetes',
    'Mesas y Sillas': 'https://listado.mercadolibre.com.mx/mesas-sillas/#CATEGORY_ID=MLM189320&S=hc_juegos-y-juguetes',
    'Montables para Niños': 'https://listado.mercadolibre.com.mx/montables-ninos/#CATEGORY_ID=MLM10811&S=hc_juegos-y-juguetes',
    'Muñecos y Muñecas': 'https://listado.mercadolibre.com.mx/munecos-munecas/#CATEGORY_ID=MLM187708&S=hc_juegos-y-juguetes',
    'Patines y Patinetas': 'https://listado.mercadolibre.com.mx/patines-patinetas/#CATEGORY_ID=MLM189879&S=hc_juegos-y-juguetes',
    'Peloteros y Brincolines': 'https://listado.mercadolibre.com.mx/peloteros-brincolines/#CATEGORY_ID=MLM437237&S=hc_juegos-y-juguetes',
    'Peluches': 'https://listado.mercadolibre.com.mx/peluches/#CATEGORY_ID=MLM1166&S=hc_juegos-y-juguetes',
    'Títeres y Marionetas': 'https://listado.mercadolibre.com.mx/titeres-marionetas/#CATEGORY_ID=MLM433047&S=hc_juegos-y-juguetes',
    'Vehículos de Juguete': 'https://listado.mercadolibre.com.mx/vehiculos-juguete/#CATEGORY_ID=MLM432871&S=hc_juegos-y-juguetes',
    'Catálogos': 'https://listado.mercadolibre.com.mx/catalogos/#CATEGORY_ID=MLM433385&S=hc_libros-revistas-y-comics',
    'Comics': 'https://listado.mercadolibre.com.mx/libros-revistas-y-comics/comics/#CATEGORY_ID=MLM3043&S=hc_libros-revistas-y-comics',
    'Libros': 'https://libros.mercadolibre.com.mx/#CATEGORY_ID=MLM1196&S=hc_libros-revistas-y-comics',
    'Manga': 'https://listado.mercadolibre.com.mx/manga/#CATEGORY_ID=MLM3044&S=hc_libros-revistas-y-comics',
    'Revistas': 'https://listado.mercadolibre.com.mx/libros-revistas-y-comics/revistas/#CATEGORY_ID=MLM1955&S=hc_libros-revistas-y-comics',
    'Cursos': 'https://listado.mercadolibre.com.mx/cursos/#CATEGORY_ID=MLM445795&S=hc_musica-peliculas-y-series',
    'Música': 'https://listado.mercadolibre.com.mx/musica-peliculas-y-series/musica/#CATEGORY_ID=MLM7809&S=hc_musica-peliculas-y-series',
    'Películas': 'https://listado.mercadolibre.com.mx/musica-peliculas-y-series/peliculas/#CATEGORY_ID=MLM7841&S=hc_musica-peliculas-y-series',
    'Series de TV': 'https://listado.mercadolibre.com.mx/musica-peliculas-y-series/series-de-tv/#CATEGORY_ID=MLM6217&S=hc_musica-peliculas-y-series',
    'Accesorios de Moda': 'https://ropa.mercadolibre.com.mx/accesorios-de-moda/#CATEGORY_ID=MLM115562&S=hc_ropa-bolsas-y-calzado',
    'Bermudas y Shorts': 'https://ropa.mercadolibre.com.mx/bermudas-y-shorts/#CATEGORY_ID=MLM109276&S=hc_ropa-bolsas-y-calzado',
    'Blusas': 'https://ropa.mercadolibre.com.mx/blusas/#CATEGORY_ID=MLM194159&S=hc_ropa-bolsas-y-calzado',
    'Calzado': 'https://ropa.mercadolibre.com.mx/calzado/#CATEGORY_ID=MLM5208&S=hc_ropa-bolsas-y-calzado',
    'Camisas': 'https://ropa.mercadolibre.com.mx/camisas/#CATEGORY_ID=MLM194157&S=hc_ropa-bolsas-y-calzado',
    'Chamarras': 'https://ropa.mercadolibre.com.mx/chamarras/#CATEGORY_ID=MLM112197&S=hc_ropa-bolsas-y-calzado',
    'Equipaje y Bolsas': 'https://ropa.mercadolibre.com.mx/equipaje-bolsas/#CATEGORY_ID=MLM3964&S=hc_ropa-bolsas-y-calzado',
    'Faldas': 'https://ropa.mercadolibre.com.mx/faldas/#CATEGORY_ID=MLM7697&S=hc_ropa-bolsas-y-calzado',
    'Jumpsuits y Overoles': 'https://ropa.mercadolibre.com.mx/jumpsuits-overoles/#CATEGORY_ID=MLM194280&S=hc_ropa-bolsas-y-calzado',
    'Leggings': 'https://ropa.mercadolibre.com.mx/leggings/#CATEGORY_ID=MLM194176&S=hc_ropa-bolsas-y-calzado',
    'Lotes de Ropa': 'https://ropa.mercadolibre.com.mx/lotes/#CATEGORY_ID=MLM431078&S=hc_ropa-bolsas-y-calzado',
    'Pantalones y Jeans': 'https://ropa.mercadolibre.com.mx/pantalones-jeans/#CATEGORY_ID=MLM194175&S=hc_ropa-bolsas-y-calzado',
    'Playeras': 'https://ropa.mercadolibre.com.mx/playeras/#CATEGORY_ID=MLM113782&S=hc_ropa-bolsas-y-calzado',
    'Ropa de Danza y Patín': 'https://ropa.mercadolibre.com.mx/ropa-danza-patin/#CATEGORY_ID=MLM417479&S=hc_ropa-bolsas-y-calzado',
    'Ropa Interior y de Dormir': 'https://ropa.mercadolibre.com.mx/ropa-interior-dormir/#CATEGORY_ID=MLM437535&S=hc_ropa-bolsas-y-calzado',
    'Ropa para Bebés': 'https://ropa.mercadolibre.com.mx/ropa-para-bebes/#CATEGORY_ID=MLM3122&S=hc_ropa-bolsas-y-calzado',
    'Saquitos, Sweaters y Chalecos': 'https://ropa.mercadolibre.com.mx/saquitos-sweaters-chalecos/#CATEGORY_ID=MLM437387&S=hc_ropa-bolsas-y-calzado',
    'Sudaderas y Hoodies': 'https://ropa.mercadolibre.com.mx/sudaderas-y-hoodies/#CATEGORY_ID=MLM115350&S=hc_ropa-bolsas-y-calzado',
    'Trajes': 'https://ropa.mercadolibre.com.mx/trajes/#CATEGORY_ID=MLM112157&S=hc_ropa-bolsas-y-calzado',
    'Trajes de Baño': 'https://ropa.mercadolibre.com.mx/trajes-de-bano/#CATEGORY_ID=MLM115684&S=hc_ropa-bolsas-y-calzado',
    'Vestidos': 'https://ropa.mercadolibre.com.mx/vestidos/#CATEGORY_ID=MLM112156&S=hc_ropa-bolsas-y-calzado',
    'Cuidado de la Salud': 'https://listado.mercadolibre.com.mx/salud-y-equipamiento-medico/cuidado-de-la-salud/#CATEGORY_ID=MLM5395&S=hc_salud-y-equipamiento-medico',
    'Masajes': 'https://listado.mercadolibre.com.mx/salud-y-equipamiento-medico/masajes/#CATEGORY_ID=MLM10217&S=hc_salud-y-equipamiento-medico',
    'Movilidad': 'https://listado.mercadolibre.com.mx/movilidad/#CATEGORY_ID=MLM6567&S=hc_salud-y-equipamiento-medico',
    'Ortopedia': 'https://listado.mercadolibre.com.mx/ortopedia/#CATEGORY_ID=MLM174912&S=hc_salud-y-equipamiento-medico',
    'Suplementos Alimenticios': 'https://listado.mercadolibre.com.mx/suplementos-alimenticios/#CATEGORY_ID=MLM438195&S=hc_salud-y-equipamiento-medico',
    'Terapias Alternativas': 'https://listado.mercadolibre.com.mx/terapias-alternativas/#CATEGORY_ID=MLM438156&S=hc_salud-y-equipamiento-medico',
    'Antigüedades': 'https://listado.mercadolibre.com.mx/arte-antiguedades/antiguedades/#CATEGORY_ID=MLM1372&S=hc_antiguedades-y-colecciones',
    'Coleccionables de Deportes': 'https://coleccionables.mercadolibre.com.mx/coleccionables-deportes/#CATEGORY_ID=MLM2820&S=hc_antiguedades-y-colecciones',
    'Esculturas': 'https://listado.mercadolibre.com.mx/esculturas/#CATEGORY_ID=MLM35869&S=hc_antiguedades-y-colecciones',
    'Filatelia': 'https://coleccionables.mercadolibre.com.mx/filatelia/#CATEGORY_ID=MLM1861&S=hc_antiguedades-y-colecciones',
    'Militaria y Afines': 'https://coleccionables.mercadolibre.com.mx/militaria-afines/#CATEGORY_ID=MLM1805&S=hc_antiguedades-y-colecciones',
    'Monedas y Billetes': 'https://coleccionables.mercadolibre.com.mx/monedas-billetes/#CATEGORY_ID=MLM1806&S=hc_antiguedades-y-colecciones',
    'Posters': 'https://coleccionables.mercadolibre.com.mx/posters/#CATEGORY_ID=MLM1834&S=hc_antiguedades-y-colecciones'
}

key_list = list(cat_map.keys())
val_list = list(cat_map.values())

cat_key_list = list(cat_dict.keys())
cat_val_list = list(cat_dict.values())


def cat_scraper(cat_value):
    item_counter = 0
    client = ScraperAPIClient('#INSERT SCRAPER API KEY HERE')
    cat_position = cat_val_list.index(cat_value)
    subcategory_name = cat_key_list[cat_position]
    cat_code = cat_map[subcategory_name]
    cat_name = cat_names[cat_code]

    with open('category_items/CONCURRENT/' + str(cat_name).replace(' ', '_') + '_bsc_test_2.csv', 'a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(['snapshot_date', 'page', 'item_id', 'title', 'seller_id', 'category_name',
                             'category_id', 'subcategory_name', 'official_store_id', 'price', 'base_price',
                             'original_price', 'initial_quantity', 'sold_quantity', 'listing_type_id', 'start_time',
                             'stop_time', 'permalink', 'shipping_free', 'shipping_logistic_type',
                             'seller_city', 'seller_state', 'seller_neighbourhood', 'deals_id', 'is_ad'])

        r1 = re.search(r"#CATEGORY_ID=MLM(\d+)[\s\S]+", cat_value).group(0)
        clean_link = cat_value.replace(r1, '')

        # paging goes in increments of 50
        full_web = client.get(clean_link + '_Desde_01_BestSellers_YES')
        # cat_web = client.get(clean_link) REGULAR LINK WITHOUT FILTERS
        full_soup = BeautifulSoup(full_web.text, 'lxml')
        try:
            full_results = full_soup.find('span', class_='ui-search-search-result__quantity-results').text
            full_results = full_results.replace(' resultados', '')
            full_results = full_results.replace(',', '')

            pages = math.floor(int(full_results) / 50)
            if pages > 41:
                pages = 41

        except AttributeError:
            print("pages not found")
            pages = 1

        print(str(cat_name) + ': ' + str(subcategory_name) + ' scrape initiating...')

        for n in range(pages):
            n_web = client.get(clean_link + '_Desde_' + str(50 * n + 1) + '_BestSellers_YES')
            soup = BeautifulSoup(n_web.text, 'lxml')

            for i in soup.find_all('div', class_='ui-search-item__group ui-search-item__group--title'):
                item_counter += 1
                try:
                    link = i.next['href']
                except KeyError:
                    break
                try:
                    r2 = re.search(r"MLM(-?)\d+", link).group(0)
                    r2 = r2.replace('-', '')
                    is_ad = 0
                except AttributeError:
                    try:
                        ad_web = client.get(link)
                        ad_soup = BeautifulSoup(ad_web.text, 'lxml')
                        link = ad_soup.find('meta', attrs={'name': 'twitter:app:url:ipad'})
                        r2 = re.search(r"MLM(-?)\d+", str(link)).group(0)
                        r2 = r2.replace('-', '')
                        is_ad = 1
                    except AttributeError:
                        print("R2 ERROR: ", link)

                item_web = requests.get('https://api.mercadolibre.com/items/' + r2)
                print(item_web)
                s = item_web.json()

                try:
                    item_id = s['id']
                except KeyError:
                    item_id = 'N/A'
                try:
                    title = s['title']
                except KeyError:
                    item_id = 'N/A'
                try:
                    seller_id = s['seller_id']
                except KeyError:
                    seller_id = 'N/A'
                try:
                    category_id = s['category_id']
                except KeyError:
                    category_id = 'N/A'
                try:
                    official_store_id = s['official_store_id']
                except KeyError:
                    official_store_id = 'N/A'
                try:
                    price = s['price']
                except KeyError:
                    price = 'N/A'
                try:
                    base_price = s['base_price']
                except KeyError:
                    base_price = 'N/A'
                try:
                    original_price = s['original_price']
                except KeyError:
                    original_price = 'N/A'
                try:
                    initial_quantity = s['initial_quantity']
                except KeyError:
                    initial_quantity = 'N/A'
                try:
                    sold_quantity = s['sold_quantity']
                except KeyError:
                    sold_quantity = 'N/A'
                try:
                    listing_type_id = s['listing_type_id']
                except KeyError:
                    listing_type_id = 'N/A'
                try:
                    start_time = s['start_time']
                except KeyError:
                    start_time = 'N/A'
                try:
                    stop_time = s['stop_time']
                except KeyError:
                    stop_time = 'N/A'
                try:
                    permalink = s['permalink']
                except KeyError:
                    permalink = 'N/A'
                try:
                    shipping_free = s['shipping']['free_shipping']
                except KeyError:
                    shipping_free = 'N/A'
                try:
                    shipping_logistic_type = s['shipping']['logistic_type']
                except KeyError:
                    shipping_logistic_type = 'N/A'
                try:
                    seller_city = s['seller_address']['city']['name']
                except KeyError:
                    seller_city = 'N/A'
                try:
                    seller_state = s['seller_address']['state']['name']
                except KeyError:
                    seller_state = 'N/A'
                try:
                    seller_neighbourhood = s['seller_address']['search_location']['neighborhood']['name']
                except KeyError:
                    seller_neighbourhood = 'N/A'
                try:
                    deal_ids = s['deal_ids']
                except KeyError:
                    deal_ids = 'N/A'

                csv_writer.writerow([today.strftime("%d/%m/%Y"), int(n) + 1, item_id, title, seller_id,
                                     cat_name, category_id, subcategory_name,
                                     official_store_id, price, base_price, original_price, initial_quantity,
                                     sold_quantity, listing_type_id, start_time, stop_time,
                                     permalink, shipping_free, shipping_logistic_type,
                                     seller_city, seller_state, seller_neighbourhood, deal_ids, is_ad])

                print(subcategory_name, n, r2, is_ad, title)


with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(cat_scraper, cat_val_list)

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')

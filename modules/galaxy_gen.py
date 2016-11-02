import random
import roman


# STATIC VARS.
SYSTEM_NAMES = ('Abydos', 'Aegis', 'Aldebaran', 'Amel', 'Aurelia', 'Balaho', 'Ballybran', 'Belzagor', 'Chiron', 'Chthon', 'Corneria', 'Cyteen', 'Demeter', 'Deucalion', 'Dosadi', 'Eayn', 'Erna', 'Etheria', 'Fhloston', 'Finisterre', 'Furya', 'Gallifrey', 'Gor', "Gorta")
SYSTEM_NAMES_PREFIXES = ('Al', 'Omi', 'Bah')
SYSTEM_NAMES_SUFFIXES = ('Prime', 'Alpha', 'Beta', 'Delta', 'Gamma', 'Minor')

# There needs to be at least two entries per var to make sure the random.choice works properly
STARS = (
	['Blue Dwarf', ['/static/images/stars/B_D_1.png']],
	['Blue Giant', ['/static/images/stars/B_G_1.png']],
	['Blue Main', ['/static/images/stars/B_M_1.png']],
	['Red Dwarf', ['/static/images/stars/R_D_1.png']],
	['Red Giant', ['/static/images/stars/R_G_1.png']],
	['Red Main', ['/static/images/stars/R_M_1.png']],
	['Red Super Giant', ['/static/images/stars/R_SG_1.png']],
	['Yellow Main', ['/static/images/stars/Y_M_1.png']]
)

PLANETS = (
	['Barren', ['/static/images/planets/BAR_1.png']],
	['Barren', ['/static/images/planets/BAR_1.png']]
)

MOONS = (
	['Rocky', ['/static/images/moons/ROC_1.png']],
	['Rocky', ['/static/images/moons/ROC_1.png']]
)

ASTEROIDS = (
	['Small Belt', ['/static/images/asteroids/SMA_1.png']],
	['Small Belt', ['/static/images/asteroids/SMA_1.png']]
)

COMETS = (
	['Ice', ['/static/images/comets/ICE.png']],
	['Ice', ['/static/images/comets/ICE.png']]
)


class Galaxy(object):
	def __init__(self):
		self.chunks_loaded = [[-1, 1], [-1, 0], [-1, 1], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]]
		# Change this to a list for ease of access. Solar systems have name/global coords for information lost.
		self.system_list = []
		self.current_position = [0, 0]
		self.current_chunk = [0, 0]
		self.initiated = False

	def initial_galaxy_generation(self, default=True):
		# Generate the initial 3x3 chunk
		self.system_list = []
		# Generates the base planets if selected to do so.
		if default:
			self.system_list.append(SolarSystem((0, 0), "Helios Alpha", total_planets=8, bodies=[
				Planet('Icarus', 0),
				Planet('Picon', 1),
				Planet('Caprica', 2),
				Planet('Gemenon', 3),
				Planet('Tauron', 4, moons=[TerrestrialBody('Minos', MOONS, 0)]),
				CelestialBody('Eberos Asteroid Belt', ASTEROIDS, 5),
				Planet('Zeus', 6),
				Planet('Persephone', 7)
			]))
			self.system_list.append(SolarSystem((1, 1), "Helios Beta", total_planets=6, bodies=[
				Planet('Troy', 0),
				Planet('Leonis', 1),
				Planet('Pallas', 2),
				CelestialBody('Ouranos Asteroid Belt', ASTEROIDS, 3),
				Planet('Virgon', 4, moons=[TerrestrialBody('Hibernia', MOONS, 0)]),
				Planet('Hera', 5)
			]))
			self.system_list.append(SolarSystem((-2, 2), "Helios Gamma", total_planets=6, bodies=[
				Planet('Thanatos', 0),
				CelestialBody('Acheron Asteroid Belt', ASTEROIDS, 1),
				Planet('Libran', 2, moons=[TerrestrialBody('Herse', MOONS, 0), TerrestrialBody('Pandrossos', MOONS, 1)]),
				Planet('Scorpia', 3),
				Planet('Sagittaron', 4),
				Planet('Ophion', 5)
			]))
			self.system_list.append(SolarSystem((-3, 3), "Helios Delta", total_planets=7, bodies=[
				Planet('Phoebe', 0),
				Planet('Styx', 1),
				CelestialBody('Aeolus Asteroid Belt', ASTEROIDS, 2),
				Planet('Aerilon', 3),
				Planet('Hestia', 4),
				Planet('Canceron', 5),
				Planet('Aquaria', 6)
			]))
		self.__create_solar_systems([-90, 90], [-90, 90])
		self.initiated = True

	def galaxy_chunk_generation(self):
		gen_list = []
		# -1 and +2 are to ensure that the range works properly from the current chunk and does not cut out the border chunks.
		for x in range(self.current_chunk[0] - 1, self.current_chunk[0] + 2):
			for y in range(self.current_chunk[1] - 1, self.current_chunk[1] + 2):
				gen_list.append([x, y])

		for chunk in gen_list:
			if chunk not in self.chunks_loaded:
				self.__create_solar_systems([chunk[0] * 60 - 30, chunk[0] * 60 + 30], [chunk[1] * 60 - 30, chunk[1] * 60 + 30])
				self.chunks_loaded.append(chunk)

	def __create_solar_systems(self, x_bounds, y_bounds, chance=20):
		total_count = 0
		# +1 is to ensure that the range works properly and does not cut out the extra border.
		for x in range(x_bounds[0], x_bounds[1] + 1):
			for y in range(y_bounds[0], y_bounds[1] + 1):
				system_chance = random.randint(0, chance)
				if system_chance == 0:

					# Check if the generated system is too close to any other created systems.
					system_too_close = False
					for system in self.system_list:
						if -1 <= x - system.global_position[0] <= 1 and -1 <= y - system.global_position[1] <= 1:
							system_too_close = True

					# Name and create the system
					if not system_too_close:
						name_chance = random.randint(1, 20)
						if name_chance == 10:
							system_name = random.choice(SYSTEM_NAMES_PREFIXES) + ' ' + random.choice(SYSTEM_NAMES) + ' ' + random.choice(SYSTEM_NAMES_SUFFIXES)
						elif name_chance == 9:
							system_name = random.choice(SYSTEM_NAMES_PREFIXES) + ' ' + random.choice(SYSTEM_NAMES)
						elif name_chance == 8:
							system_name = random.choice(SYSTEM_NAMES) + ' ' + random.choice(SYSTEM_NAMES_SUFFIXES)
						else:
							system_name = random.choice(SYSTEM_NAMES)
						solar_system = SolarSystem((x, y), system_name)
						self.system_list.append(solar_system)
						print(self.system_list[self.system_list.index(solar_system)].name, self.system_list[self.system_list.index(solar_system)].global_position)
						total_count += 1
		print('Total Count:', total_count)

	def generate_bodies(self, x_bounds, y_bounds, other_bounds):
		for solar_system in self.system_list:
			if solar_system.global_position[0] in range(x_bounds[0], x_bounds[1] + 1) \
			and solar_system.global_position[1] in range(y_bounds[0], y_bounds[1 + 1]):
				solar_system.generate_bodies()
			else:
				for bound in other_bounds:
					if solar_system.global_position[0] in range(bound[0][0], bound[0][1] + 1) \
					and solar_system.global_position[1] in range(bound[1][0], bound[1][1] + 1):
						solar_system.generate_bodies()

	def galaxy_serialize(self):
		galaxy_dict = {
			'chunks_loaded': self.chunks_loaded,
			'current_position': self.current_position,
			'system_list': [],
			'current_chunk': self.current_chunk,
			'initiated': self.initiated
		}
		for system in self.system_list:
			system_dict = {
				'global_position': system.global_position,
				'total_planets': system.total_planets,
				'name': system.name,
				'bodies': [],
				'type': system.type,
				'file': system.file,
				'visited': system.visited,
				'bodies_generated': system.bodies_generated
			}
			for body in system.bodies:
				body_dict = {
					'name': body.name,
					'resources': body.resources,
					'type': body.type,
					'file': body.file,
					'parent_body': body.parent_body,
					'orbit': body.orbit
				}
				if type(body) is TerrestrialBody or type(body) is Planet:
					body_dict['visited'] = body.visited
				if type(body) is Planet:
					body_dict['moons'] = []
					for moon in body.moons:
						moon_dict = {
							'name': moon.name,
							'resources': moon.resources,
							'type': moon.type,
							'file': moon.file,
							'parent_body': moon.parent_body,
							'orbit': moon.orbit,
							'visited': moon.visited
						}
						body_dict['moons'].append(moon_dict)
				system_dict['bodies'].append(body_dict)
			galaxy_dict['system_list'].append(system_dict)
		return galaxy_dict


class SolarSystem(object):
	def __init__(self, position, name, **kwargs):
		# Generating key information
		self.global_position = [position[0], position[1]]
		self.total_planets = random.randint(0, 8)
		self.bodies = []
		self.bodies_generated = False
		self.name = name

		# Choosing a star and assigning it.
		star = random.choice(STARS)
		self.type = star[0]
		self.file = star[1]

		# History of the star.
		self.visited = 'never'

		# Updating any specific args.
		self.__dict__.update(kwargs)

	def generate_bodies(self, asteroid_chance=10):
		# Generate planets and asteroids for a solar system. Call when necessary, not on generation of the system.
		if not self.bodies_generated:
			for orbit_index in range(0, self.total_planets):
				body_name = self.name + " " + roman.toRoman(orbit_index + 1)
				if random.randint(1, asteroid_chance) == 1:
					# Generate asteroids
					self.bodies.append(CelestialBody(body_name, ASTEROIDS, orbit_index))
				else:
					# generate planet
					planet = Planet(body_name, orbit_index)
					planet.generate_moons()
					self.bodies.append(planet)

				print(self.bodies[orbit_index].name)


# Basis for Comets, Asteroids, Planets, Moons or any other object located within a system.
# Instantiate this for asteroid belts and for comets.
class CelestialBody(object):
	def __init__(self, name, BODY, orbit, **kwargs):
		self.name = name

		# for resources, [Abundance, Amount available]. Can increase amount available from planets and moons.
		self.resources = {
			'water': [random.randint(0, 1), 100],
			'food': [random.randint(0, 1), 100],
			'tylium_ore': [random.randint(0, 1), 100],
			'aluminium': [random.randint(0, 1), 100],
			'copper': [random.randint(0, 1), 100],
			'iron': [random.randint(0, 1), 100],
			'uranium': [random.randint(0, 1), 100],
			'graphene': [random.randint(0, 1), 100],
			'oils': [random.randint(0, 1), 100],
			'hydrocarbons': [random.randint(0, 1), 100]
		}

		# Assigning what body it will be. (Aster, Comet, Planet, Moon)
		body = random.choice(BODY)
		self.type = body[0]
		self.file = random.choice(body[1])

		# 0 to n for objects that orbit sun (Planets and asteroid belts), and -1 for comets. Moons have 0 to n for their orbits around parent planet.
		self.parent_body = 'Star'
		self.orbit = orbit
		self.__dict__.update(kwargs)


# Basis for Planets and Moons
# Instantiate this for moons
class TerrestrialBody(CelestialBody):
	def __init__(self, name, BODY, orbit, anomaly_chance=10, **kwargs):
		super().__init__(name, BODY, orbit)
		self.visited = 'never'

		# code for anomaly. Generate inside __init__ function
		# base one in ten chance of creating anomaly.
		if random.randint(1, anomaly_chance) == 1:
			pass

		self.__dict__.update(kwargs)


class Planet(TerrestrialBody):
	def __init__(self, name, orbit, **kwargs):
		super().__init__(name, PLANETS, orbit)
		self.moons = []
		self.__dict__.update(kwargs)

	def generate_moons(self):
		for orbit_index in range(0, random.randint(0, 4)):
			name = self.name + " - Moon " + str(orbit_index + 1)
			self.moons.append(TerrestrialBody(name, MOONS, orbit_index))
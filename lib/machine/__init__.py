from .cpu import CPU
from .memory import Memory
from .storage import Storage
from .network import Network
from .host import Host
from .battery import Battery


class Machine:

	def __init__(self):
		self.cpu = CPU()
		self.memory = Memory()
		self.storage = Storage()
		self.network = Network()
		self.host = Host()
		self.battery = Battery()

	async def get_full_info(self):
		return {
			"cpu": (await self.cpu.get_full_info()),
			"memory": self.memory.get_usage(),
			"storage": self.storage.get_usage(),
			"network": self.network.get_net(),
			"host": self.host.get_host(),
			"battery": self.battery.get_usage()
		}

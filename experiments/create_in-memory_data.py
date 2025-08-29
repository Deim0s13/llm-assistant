from utils.memory import Memory, MemoryBackend

mem = Memory(backend=MemoryBackend.IN_MEMORY)  # force RAM
mem.clear()  # start clean
for i in range(5):
    mem.save({"role": "user", "content": f"msg {i}"})
    mem.save({"role": "assistant", "content": f"reply {i}"})

assert len(mem.load()) == 10

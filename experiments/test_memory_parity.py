def test_roundtrip(mem):
    mem.clear()
    mem.save({"role": "user", "content": "ping"})
    mem.save({"role": "assistant", "content": "pong"})
    turns = mem.load()
    assert turns[-1]["content"] == "pong"
    assert len(turns) == 2

def test_trim_limit(mem):
    mem.clear()
    for i in range(60):
        mem.save({"role": "user", "content": f"u{i}"})
    turns = mem.load(limit := 50)
    assert len(turns) <= limit
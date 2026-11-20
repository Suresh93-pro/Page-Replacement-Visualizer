import random

ALGORITHMS = [
    "FIFO", "LRU", "Optimal", "LFU", "MFU",
    "Second Chance", "Clock", "MRU", "Random"
]

def simulate(reference, capacity, algorithm):
    if not reference:
        raise ValueError("Enter at least one page reference.")
    if capacity < 1:
        raise ValueError("Frame count must be at least 1.")

    frames = []
    history = []
    faults = hits = 0
    counts = {}
    last_used = {}
    arrival = {}
    ref_list = list(reference)
    pointer = 0
    second_chance = {}

    for i, page in enumerate(ref_list):
        hit = page in frames
        evicted = None
        if hit:
            hits += 1
            counts[page] = counts.get(page, 0) + 1
            last_used[page] = i
            second_chance[page] = True
        else:
            faults += 1
            counts[page] = counts.get(page, 0) + 1
            if len(frames) < capacity:
                frames.append(page)
                arrival[page] = i
                last_used[page] = i
                second_chance[page] = True
            else:
                if algorithm == "FIFO":
                    victim = min(frames, key=lambda p: arrival[p])
                elif algorithm == "LRU":
                    victim = min(frames, key=lambda p: last_used[p])
                elif algorithm == "Optimal":
                    def next_use(p):
                        try: return ref_list.index(p, i + 1)
                        except ValueError: return float("inf")
                    victim = max(frames, key=next_use)
                elif algorithm == "LFU":
                    victim = min(frames, key=lambda p: (counts.get(p, 0), arrival[p]))
                elif algorithm == "MFU":
                    victim = max(frames, key=lambda p: (counts.get(p, 0), -arrival[p]))
                elif algorithm == "MRU":
                    victim = max(frames, key=lambda p: last_used[p])
                elif algorithm == "Random":
                    victim = random.choice(frames)
                elif algorithm in ("Second Chance", "Clock"):
                    while True:
                        candidate = frames[pointer % len(frames)]
                        if second_chance.get(candidate, False):
                            second_chance[candidate] = False
                            pointer = (pointer + 1) % len(frames)
                        else:
                            victim = candidate
                            pointer = (pointer + 1) % len(frames)
                            break
                else:
                    raise ValueError("Unknown algorithm")
                evicted = victim
                frames[frames.index(victim)] = page
                arrival.pop(victim, None)
                last_used.pop(victim, None)
                second_chance.pop(victim, None)
                arrival[page] = i
                last_used[page] = i
                second_chance[page] = True

        history.append({
            "step": i + 1, "page": page, "frames": frames.copy(),
            "hit": hit, "fault": not hit, "evicted": evicted
        })

    return {
        "history": history, "faults": faults, "hits": hits,
        "total": len(ref_list),
        "fault_rate": faults / len(ref_list) * 100,
        "hit_rate": hits / len(ref_list) * 100
    }

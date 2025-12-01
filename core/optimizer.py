# core/optimizer.py
import random
from typing import Callable, Tuple

def simple_ga(evaluate_fn: Callable[[Tuple[float,float]], float],
              pop_size: int = 12, gens: int = 10,
              cam_range: tuple = (-0.6,0.6), th_range: tuple = (0.7,1.4)):
    # population: tuples (camber_scale, thickness_scale)
    pop = [(random.uniform(*cam_range), random.uniform(*th_range)) for _ in range(pop_size)]
    best = None; best_score = -1e9
    for g in range(gens):
        scored = []
        for ind in pop:
            score = evaluate_fn(ind)
            scored.append((score, ind))
            if score > best_score:
                best_score = score; best = ind
        scored.sort(reverse=True, key=lambda x: x[0])
        # keep top half
        keep = [ind for (_,ind) in scored[:max(2, pop_size//2)]]
        # repopulate
        newpop = keep.copy()
        while len(newpop) < pop_size:
            if random.random() < 0.6:
                a = random.choice(keep); b = random.choice(keep)
                alpha = random.random()
                child = (alpha*a[0] + (1-alpha)*b[0], alpha*a[1] + (1-alpha)*b[1])
            else:
                parent = random.choice(keep)
                child = parent
            # mutate
            if random.random() < 0.3:
                child = (child[0] + random.gauss(0,0.03), child[1] + random.gauss(0,0.03))
            # clamp
            child = (min(max(child[0], cam_range[0]), cam_range[1]), min(max(child[1], th_range[0]), th_range[1]))
            newpop.append(child)
        pop = newpop
    return best, best_score

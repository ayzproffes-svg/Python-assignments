calls = [
"seeds not received seeds delayed",
"fertiliser price high",
"seeds price high subsidy not received",
]
STOP = {"not", "high"}

def frequencies(texts, stop):
    # TODO 1: Return a dictionary word -> count for every word that is not in stop,
    # using dict.get()
    counts = {}
    for text in texts:
        for word in text.split():
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1
    return counts

def top(counts, k):
    # TODO 2: Return the k most frequent (word, count) pairs, highest count first and
    # alphabetical for ties
    return sorted(counts.items(), key=lambda p: (-p[1], p[0]))[:k]

print(top(frequencies(calls, STOP), 3))

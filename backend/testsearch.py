import time
from search import search_duckduckgo

test_queries = [
    "Nike Air Force 1",
    "Levi's 501 jeans",
    "Champion reverse weave hoodie",
    "New Balance 550",
    "Nike Tech Fleece",
    "Vans Old Skool",
    "Adidas Samba",
    "Timberland 6-inch boots",
    "Converse Chuck Taylor",
    "The North Face puffer jacket",
    "UGG Classic Ultra Mini",
    "Crocs Classic Clog",
    "Dickies work pants",
    "Nike Dunk Low",
    "Carhartt Detroit jacket",
    "Fila Disruptor II",
    "Puma Suede Classic",
    "Air Jordan 1 Mid",
    "Reebok Club C 85",
    "Birkenstock Boston"
]

total = len(test_queries)
correct = 0
total_time = 0

print("\n🔍 Running accuracy + speed test on 20 queries...\n")

for i, query in enumerate(test_queries, 1):
    print(f"{i:2d}. Testing: {query}")
    start = time.time()
    results = search_duckduckgo(query)
    elapsed = time.time() - start
    total_time += elapsed

    found_valid_price = any(r["price"] and "$" in r["price"] for r in results)

    if found_valid_price:
        print(f"    ✅ Valid price found | Time: {elapsed:.2f}s")
        correct += 1
    else:
        print(f"    ❌ No valid price     | Time: {elapsed:.2f}s")

# ── Final summary ─────────────────────
accuracy = (correct / total) * 100
avg_time = total_time / total

print("\n📊 Summary:")
print(f"✔️  {correct}/{total} results returned a valid price")
print(f"🎯 Accuracy: {accuracy:.1f}%")
print(f"⚡ Avg response time: {avg_time:.2f} seconds\n")

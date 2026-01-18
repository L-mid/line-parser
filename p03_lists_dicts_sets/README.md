# Mini Order Aggregator

takes a tiny list of raw "order lines" (strings), parses them into dicts, dedupe/normlaize tags with sets and build a report with dict-of-dicts + lists.

## Repo skeleton
- p03_lists_dicts_sets/
    - src/p03.py
    - tests/test_p03.py
    - README.md



## When would you choose a set over a list:
Sets dedup contents, so it's a simple way to ensure there's never any duplicates, or to dedupe a list later.


list is mutible in pyhton so not hashable, will error with type error i think

dict.get(k, 0) + 1 is cool because if the 0 key does not exist, it gets replaced with 0, which is immediately added to +1.
so essentally you get an index count that starts as 1 and initalization is within the count itself.

I mutated only the values the aggregator compiles, there was no need to mutate anything else
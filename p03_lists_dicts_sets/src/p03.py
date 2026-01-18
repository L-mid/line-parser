from typing import Tuple, List



def is_float(v) -> bool:
    try:
        float(v)
        return True
    except ValueError:
        return False
    
def is_int(v) -> bool:
    try: 
        int(v)
        return True
    except ValueError:
        return False
    

def parse_kv_line(line: str) -> dict:

    parsed = {}

    line = line.strip()
    tokens = line.split()

    for token in tokens:
        k, v = token.split("=", 1)
        k, v = k.strip().casefold(), v.strip().casefold()

        if v == "":
            v = None

        elif is_int(v):
            v = int(v)

        elif is_float(v):
            v = float(v)

        if k in parsed:
            raise ValueError(f"Duplicate key found: {k}.") 
        parsed[k] = v  

    return parsed


def normalize_tags(raw: str | None) -> set[str]:
    missing = ["missing", "n/a", "na", None, ""]

    if raw in missing:
        return set()
    
    tags = raw.split("|", -1)

    tags_set = set()
    for tag in tags:
        tag = tag.strip().casefold()
        if tag:
            tags_set.add(tag)

    return tags_set



def parse_order(line: str) -> dict:

    order_schema = {"order_id": None, "sku": None, "qty": None, 
                    "price": None, "marketplace": None, "tags": None}


    parsed_fields = parse_kv_line(line)
    
    for key in order_schema:
        if key not in parsed_fields:
            parsed_fields[key] = order_schema[key]

    raw_tags = parsed_fields['tags']     
    parsed_tags = normalize_tags(raw_tags)
    parsed_fields['tags'] = parsed_tags

    return parsed_fields


def aggregate_orders(lines: list[str]) -> dict[str, dict]:
    """dict keyed by sku:"""
    
    agg = {}


    for line in lines:      # full run through
        parsed_fields = parse_order(line)

        sku = parsed_fields["sku"]

        if sku not in agg:
            agg.setdefault(sku, {"units": 0, "revenue": 0.0, "marketplaces": set(), "tags": set()})


        units = parsed_fields["qty"] + agg[sku]["units"]

        revenue = parsed_fields["price"] * parsed_fields["qty"] + agg[sku]["revenue"]

        agg[sku]["marketplaces"].add(parsed_fields["marketplace"])
        marketplaces = agg[sku]["marketplaces"]

        for tag in parsed_fields["tags"]:
            agg[sku]["tags"].add(tag)
        tags = agg[sku]["tags"]

        agg[sku] = {"units": units, "revenue": revenue, "marketplaces": marketplaces, "tags": tags}   # returning

    return agg


def top_skus_by_revenue(agg: dict, n: int) -> List[Tuple[str, float]]:


    # return a list of (sku, revenue) sorted by:
    #   revenue desc
    #   sku asc (tie-breaker)

    revenues = []
    for sku in agg:
        revenues.append((sku, agg[sku]["revenue"]))
    
    top_revenues = sorted(revenues, key=lambda x: (-x[1], x[0]))[:n]
    
    return top_revenues


    









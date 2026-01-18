
from p03_lists_dicts_sets.src.p03 import parse_kv_line, normalize_tags, parse_order, aggregate_orders, top_skus_by_revenue

lines = [
"order_id=1 sku=OXFORD qty=1 price=73.86 marketplace=Amazon tags=Coupon|Winter",
"order_id=2 sku=POLO qty=2 price=40.35 marketplace=Amazon tags=LightningDeal|Winter|winter",
"order_id=3 sku=OXFORD qty=3 price=70.00 marketplace=eBay tags=Clearance",
"order_id=4 sku=SOCKS qty=10 price=3.50 marketplace=Amazon tags=",
"order_id=5 sku=POLO qty=1 price=39.99 marketplace=eBay tags=clearance|LightningDeal",
"order_id=6 sku=HAT qty=1 price=12 marketplace=Amazon",
]


def test_parse_kv_line():
    
    res = parse_kv_line(lines[3])
    assert isinstance(res, dict)
    assert res == {'order_id': 4, 'sku': 'socks', 'qty': 10, 'price': 3.5, 'marketplace': 'amazon', 'tags': None}

    assert isinstance(res['order_id'], int) 
    assert isinstance(res['qty'], int)
    assert isinstance(res['price'], float)
    assert res["tags"] == None

        

def test_normalize_tags():
    raw_tag = "LightningDeal|Winter|winter"
    tag_set = normalize_tags(raw_tag)
    
    assert isinstance(tag_set, set)
    assert tag_set == {"lightningdeal", "winter"}

    # empty:
    raw_tag = None
    tag_set = normalize_tags(raw_tag)
    
    assert isinstance(tag_set, set)
    assert tag_set == set()


def test_parse_order():
    for line in lines:
        parsed_lines = parse_order(line)

        assert isinstance(parsed_lines, dict)
        
        for entry in parsed_lines.items():
            _, maybe_str = entry
            if isinstance(maybe_str, str):
                assert maybe_str.casefold() == maybe_str

        assert isinstance(parsed_lines["tags"], set)    # including order 4 & 6

    

def test_aggregate_orders():

    aggregated = aggregate_orders(lines)
    
    for sku in aggregated:
        assert isinstance(sku, str)

        # not none 
        assert isinstance(aggregated[sku]["marketplaces"], set)
        assert isinstance(aggregated[sku]["tags"], set)

    # specifics
    assert aggregated["oxford"]["units"] == 4
    assert aggregated["oxford"]["revenue"] == 283.86
    assert aggregated["polo"]["units"] == 3
    assert aggregated["polo"]["marketplaces"] == {"amazon", "ebay"}



def test_top_skus_by_revenue():
    aggregated = aggregate_orders(lines)

    assert len(top_skus_by_revenue(aggregated, n=1)) == 1

    max_revenues = top_skus_by_revenue(aggregated, n=4)
    assert len(max_revenues) == 4

    amounts = []
    for _, amount in max_revenues:
        amounts.append(amount)
    assert max(amounts) == amounts[0]
    
    assert top_skus_by_revenue(aggregated, n=2) == [("oxford", 283.86), ("polo", 120.69)]


    
        
        



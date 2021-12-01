from itertools import product
from core.entities import Agent

from utils.spatial import Position
from utils.datastructures import Bucket, KDTree


def test_distance_with_bucket_store():
    bucket = Bucket()

    for x, y in product(range(20),repeat=2):
        bucket.put(Agent(Position(x,y)))
    
    assert len(bucket.in_distance(Agent(Position(0,0)), 1.42)) == 4

def test_distance_with_bucket_store_edge_case():
    bucket = Bucket()

    for x, y in product(range(20),repeat=2):
        bucket.put(Agent(Position(x,y)))
    
    assert len(bucket.in_distance(Agent(Position(0,0)), 1)) == 3

def test_bucket_with_negatives():
    bucket = Bucket()

    for x, y in product(range(-20,20),repeat=2):
        bucket.put(Agent(Position(x,y)))
    
    assert len(bucket.in_distance(Agent(Position(0,0)), 1)) == 5

def test_distance_with_kd_tree_store():
    bucket = KDTree()

    for x, y in product(range(20),repeat=2):
        bucket.put(Agent(Position(x,y)))
    
    assert len(bucket.in_distance(Agent(Position(0,0)), 1.42)) == 4

def test_distance_with_kd_tree_store_edge_case():
    bucket = KDTree()

    for x, y in product(range(20),repeat=2):
        bucket.put(Agent(Position(x,y)))
    
    assert len(bucket.in_distance(Agent(Position(0,0)), 1)) == 3

def test_kd_tree_with_negatives():
    bucket = KDTree()

    for x, y in product(range(-20,20),repeat=2):
        bucket.put(Agent(Position(x,y)))
    
    assert len(bucket.in_distance(Agent(Position(0,0)), 1)) == 5
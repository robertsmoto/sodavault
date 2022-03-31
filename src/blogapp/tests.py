from django.test import TestCase
# from headlines.models import HeadlinePost
import redis

from decouple import config

# Create your tests here.
print("hello world")

"""
REDIS_ACCK=A1al1gwtr7wr9ilq04fyejygk6tenezf2wc0isdfmirpipohaj6
REDIS_USRK=S69k77gxn0lfl3z2rwlwuf6ay7lm5jdjaeljmpwb2jah82s1ik7
REDIS_APIN=sodavault_access_key
"""

def main():

    r = redis.Redis(
            host=config('REDIS_ENDP'),
            port=config('REDIS_PORT'),
            password=config('REDIS_PASS'),
            )

    print(f"Connected to db: {r}")

    graph = r.graph(index_name='items')
    print(f"Graph instance: {graph}")
    # from r.graph import Node, Edge, Graph, Path

    from redis.commands.graph import node

    product = node.Node(
            node_id='SKU004',
            alias='SKU004',
            label='product',
            properties={
                'sku': 'SKU0004',
                'nam': 'A good product',
                'des': 'This is a description',
                'rpr': 1244,
                'spr': 933,
                }
            )

    print("product", product, type(product))

    graph.add_node(product)
    graph.commit()

    query = """
        MATCH (p:product)
        RETURN p.sku, p.nam, p.des, p.rpr"""

    result = graph.query(query, timeout=10)


    print("\n####")
    for result in result.result_set:
        print(f"result: {result}")
        print(result[0])
        print(result[1])
        print(result[2])


#     product = graph.Node(
            # label='product',
            # properties={
                # }
            # )

#     graph.commit(product)


    # john = Node(label='person', properties={'name': 'John Doe', 'age': 33, 'gender': 'male', 'status': 'single'})
    # redis_graph.add_node(john)

    # japan = Node(label='country', properties={'name': 'Japan'})
    # redis_graph.add_node(japan)

    # edge = Edge(john, 'visited', japan, properties={'purpose': 'pleasure'})
    # redis_graph.add_edge(edge)

    # redis_graph.commit()

    # query = """MATCH (p:person)-[v:visited {purpose:"pleasure"}]->(c:country)
               # RETURN p.name, p.age, v.purpose, c.name"""

    # result = redis_graph.query(query)

    # # Print resultset
    # result.pretty_print()

    # # Use parameters
    # params = {'purpose':"pleasure"}
    # query = """MATCH (p:person)-[v:visited {purpose:$purpose}]->(c:country)
               # RETURN p.name, p.age, v.purpose, c.name"""

    # result = redis_graph.query(query, params)

    # # Print resultset
    # result.pretty_print()

    # # Use query timeout to raise an exception if the query takes over 10 milliseconds
    # result = redis_graph.query(query, params, timeout=10)

    # # Iterate through resultset
    # for record in result.result_set:
        # person_name = record[0]
        # person_age = record[1]
        # visit_purpose = record[2]
        # country_name = record[3]

    # query = """MATCH p = (:person)-[:visited {purpose:"pleasure"}]->(:country) RETURN p"""

    # result = redis_graph.query(query)

    # # Iterate through resultset
    # for record in result.result_set:
        # path = record[0]
        # print(path)


    # # All done, remove graph.
    # redis_graph.delete()

    return


if __name__ == "__main__":
    main()

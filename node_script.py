from ttypes import Node
from bootstrap_connection import BootstrapServerConnection

if __name__ == "__main__":
    bs_node = Node("127.0.0.1", 5000, "BootstrapServer")
    my_node = Node("127.0.0.1", 6000, "MyNode")

    with BootstrapServerConnection(bs_node, my_node) as connection:
        other_nodes = connection.users
        print("Connected nodes:", other_nodes)
        # Perform operations with other nodes

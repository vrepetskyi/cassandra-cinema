from cassandra.cluster import Cluster


def get_cassandra_session():
    HOSTNAME = "127.0.0.1"
    PORTS = range(9042, 9045)

    cluster = Cluster([(HOSTNAME, PORT) for PORT in PORTS])
    session = cluster.connect()

    return session

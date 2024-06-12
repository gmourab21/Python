class Route:
    def __init__(self, depot):
        self.depot = depot
        self.customers = []

    def add_customer(self, customer, savings):
        self.customers.append((customer, savings))


def euclidean_distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


def calculate_savings(customers, depot):
    savings = {}
    for i in range(len(customers)):
        for j in range(i + 1, len(customers)):
            distance_ij = euclidean_distance(customers[i], customers[j])
            distance_id = euclidean_distance(customers[i], depot)
            distance_jd = euclidean_distance(customers[j], depot)
            savings[(i, j)] = distance_id + distance_jd - distance_ij
    return savings


def clarke_wright(customers, depot, capacity):
    savings = calculate_savings(customers, depot)
    savings = sorted(savings.items(), key=lambda x: x[1], reverse=True)

    routes = [Route(depot) for _ in range(len(customers))]
    for (i, j), saving in savings:
        customer_i, customer_j = customers[i], customers[j]
        for route in routes:
            if (customer_i in route.customers or customer_j in route.customers) and \
                    route.depot not in (customer_i, customer_j) and \
                    sum(euclidean_distance(route.depot, c) for c, _ in route.customers) <= capacity:
                route.add_customer(customer_i, saving)
                route.add_customer(customer_j, saving)
                break

    return routes

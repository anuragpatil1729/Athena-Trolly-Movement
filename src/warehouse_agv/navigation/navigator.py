"""High-level AGV navigation."""


class Navigator:

    def __init__(
        self,
        route_planner
    ):

        self.route_planner = route_planner

    def go_to(
        self,
        current_node,
        target_node
    ):

        route = self.route_planner.find_route(
            current_node,
            target_node
        )

        return route

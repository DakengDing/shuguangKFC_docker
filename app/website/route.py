import math

class Route:
    graph = None

    @staticmethod
    def calculate_distance(systemA, systemB):
        light_year = 9460730472580800  # meters
        distance = math.sqrt(
            (systemB["x"] - systemA["x"]) ** 2 +
            (systemB["y"] - systemA["y"]) ** 2 +
            (systemB["z"] - systemA["z"]) ** 2
        )
        return round((distance / light_year) * 1000) / 1000

    @staticmethod
    def find_closer_system(within_range_of, closer_to, max_range):
        current_distance = Route.calculate_distance(within_range_of, closer_to)

        best_system = None

        last_distance1 = 0
        last_distance2 = float("inf")

        for system in Route.graph:
            if system["security"] >= 0.5:
                continue

            distance1 = Route.calculate_distance(within_range_of, system)
            distance2 = Route.calculate_distance(closer_to, system)

            if (
                    distance1 <= max_range and
                    distance2 < current_distance and
                    distance1 > last_distance1 and
                    distance2 < last_distance2
            ):
                best_system = system
                last_distance1 = distance1
                last_distance2 = distance2

        return best_system

    @staticmethod
    def find_system(name):
        for system in Route.graph:
            if system["name"] == name:
                return system
        print(f'System "{name}" not found')

    @staticmethod
    def calculate_route(start, destination,ship_type):
        if not start or not destination or destination["security"] >= 0.5:
            return []
        jump_fatigue = 0
        jump_activation = 0
        reduction = 1
        time = 0
        total_fuel = 0
        if ship_type == "Black OP":
            max_range = 8
            reduction = reduction - 0.75
            fuel = 700
        elif ship_type == 'Jump Freighters':
            max_range = 10
            reduction = reduction - 0.9
            fuel = 10000
        elif ship_type == "Jump Gate":
            max_range = 5
            reduction = 0
            fuel = 0
        else:
            max_range = 7
            fuel = 3000
        route = []
        sysA = start
        sysB = destination
        distance = float("inf")

        while distance > max_range:
            distance = Route.calculate_distance(sysA, sysB)


            if distance <= max_range:
                # if jump_fatigue == 0:
                #     jump_fatigue = min(10 * (1 + distance) * reduction, 300)  # 分钟
                #     jump_activation = min(1 + distance, 30)  # 分钟
                #     print(distance)
                #     print(jump_activation)
                # else:
                #     jump_fatigue = jump_fatigue - jump_activation
                #     jump_activation = min(jump_fatigue / 10, 30)
                #     jump_fatigue = min(jump_fatigue * (1 + distance) * reduction, 300)

                # if ship_type == "Jump Gate":
                #     jump_activation = 0

                # time = time + jump_activation

                subtotal_fuel = distance * fuel
                subtotal_fuel = math.ceil(subtotal_fuel)
                total_fuel = total_fuel + subtotal_fuel
                route.append({
                    "from": {"name": sysA["name"], "security": sysA["security"]},
                    "to": {"name": sysB["name"], "security": sysB["security"]},
                    "distance": distance,
                    "Jump_Fatigue": jump_fatigue,
                    "Jump_Activation": jump_activation,
                    "fuel_cost": subtotal_fuel
                })
                sysA = sysB
                if sysB != destination:
                    sysB = destination
                    distance = float("inf")
            else:
                sysB = Route.find_closer_system(sysA, sysB, max_range)
                if sysB is None:
                    return []
        return route, total_fuel
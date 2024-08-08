

class Utils:

    def create_dict_est_params(area, velocity, wetted_perimeter, hydraulic_radius):
        est_dict_params = {'Wetted Area (m2)': area,
                        'Velocity (m/s)': velocity,
                        'Wetted_perimeter (m)': wetted_perimeter,
                        'Hydraulic_radius (m)': hydraulic_radius,
                        }

        return est_dict_params

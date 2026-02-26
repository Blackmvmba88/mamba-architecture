"""
Natural Flows Module for Mamba Architecture

This module implements simulations and calculations for natural flows:
air, water, light, and heat in architectural contexts.
"""

import math
import numpy as np
from typing import Tuple, List, Optional, Callable


class FlowSimulator:
    """Simulate natural flows in architectural contexts."""
    
    # Physical constants
    GRAVITY = 9.81  # m/s²
    AIR_DENSITY = 1.225  # kg/m³ at sea level, 15°C
    WATER_DENSITY = 1000  # kg/m³
    STEFAN_BOLTZMANN = 5.67e-8  # W/(m²·K⁴)
    
    @staticmethod
    def reynolds_number(velocity: float, length: float, 
                        kinematic_viscosity: float = 1.5e-5) -> float:
        """
        Calculate Reynolds number for flow characterization.
        
        Args:
            velocity: Flow velocity (m/s)
            length: Characteristic length (m)
            kinematic_viscosity: Kinematic viscosity (m²/s), default for air at 20°C
            
        Returns:
            Reynolds number (dimensionless)
        """
        return velocity * length / kinematic_viscosity
    
    @staticmethod
    def is_laminar(reynolds: float) -> bool:
        """
        Determine if flow is laminar based on Reynolds number.
        
        Args:
            reynolds: Reynolds number
            
        Returns:
            True if laminar (Re < 2300), False if turbulent
        """
        return reynolds < 2300
    
    @staticmethod
    def chimney_effect_pressure(height: float, temp_inside: float, 
                                 temp_outside: float, avg_temp: float) -> float:
        """
        Calculate pressure difference due to stack/chimney effect.
        
        Args:
            height: Height difference (m)
            temp_inside: Inside temperature (°C)
            temp_outside: Outside temperature (°C)
            avg_temp: Average temperature (°C)
            
        Returns:
            Pressure difference (Pa)
        """
        # Convert to Kelvin
        Ti = temp_inside + 273.15
        Te = temp_outside + 273.15
        Ta = avg_temp + 273.15
        
        delta_p = FlowSimulator.AIR_DENSITY * FlowSimulator.GRAVITY * height * (Ti - Te) / Ta
        return delta_p
    
    @staticmethod
    def natural_ventilation_flow_rate(pressure_diff: float, opening_area: float,
                                       discharge_coeff: float = 0.6) -> float:
        """
        Calculate flow rate through opening due to pressure difference.
        
        Args:
            pressure_diff: Pressure difference (Pa)
            opening_area: Area of opening (m²)
            discharge_coeff: Discharge coefficient (typical 0.6-0.65)
            
        Returns:
            Volumetric flow rate (m³/s)
        """
        if pressure_diff < 0:
            pressure_diff = abs(pressure_diff)
        
        velocity = math.sqrt(2 * pressure_diff / FlowSimulator.AIR_DENSITY)
        flow_rate = discharge_coeff * opening_area * velocity
        return flow_rate
    
    @staticmethod
    def wind_pressure_coefficient(angle: float, building_shape: str = 'rectangular') -> float:
        """
        Estimate wind pressure coefficient based on wind angle.
        
        Args:
            angle: Wind angle relative to facade (degrees, 0 = perpendicular)
            building_shape: 'rectangular', 'circular', or 'aerodynamic'
            
        Returns:
            Pressure coefficient Cp (dimensionless)
        """
        angle_rad = math.radians(angle)
        
        if building_shape == 'rectangular':
            # Simplified model
            if abs(angle) < 45:
                return 0.8 * math.cos(angle_rad)  # Windward
            else:
                return -0.5  # Leeward/side
        
        elif building_shape == 'circular':
            # Circular cylinder
            return 1.0 - 4 * math.sin(angle_rad)**2
        
        elif building_shape == 'aerodynamic':
            # Streamlined shape
            if abs(angle) < 45:
                return 0.4 * math.cos(angle_rad)
            else:
                return -0.3
        
        return 0.0
    
    @staticmethod
    def wind_pressure(wind_speed: float, pressure_coefficient: float) -> float:
        """
        Calculate wind pressure on surface.
        
        Args:
            wind_speed: Wind speed (m/s)
            pressure_coefficient: Cp coefficient
            
        Returns:
            Pressure (Pa)
        """
        dynamic_pressure = 0.5 * FlowSimulator.AIR_DENSITY * wind_speed**2
        return pressure_coefficient * dynamic_pressure


class WaterFlow:
    """Water flow calculations."""
    
    @staticmethod
    def bernoulli_velocity(height: float, pressure: float = 0) -> float:
        """
        Calculate velocity from Bernoulli's equation.
        
        Args:
            height: Height of water column (m)
            pressure: Additional pressure (Pa)
            
        Returns:
            Flow velocity (m/s)
        """
        v = math.sqrt(2 * FlowSimulator.GRAVITY * height + 
                      2 * pressure / FlowSimulator.WATER_DENSITY)
        return v
    
    @staticmethod
    def capillary_rise(surface_tension: float, contact_angle: float, 
                       radius: float, density: float = 1000) -> float:
        """
        Calculate capillary rise height.
        
        Args:
            surface_tension: Surface tension (N/m), water ~0.073
            contact_angle: Contact angle (degrees)
            radius: Tube radius (m)
            density: Liquid density (kg/m³)
            
        Returns:
            Rise height (m)
        """
        angle_rad = math.radians(contact_angle)
        h = (2 * surface_tension * math.cos(angle_rad)) / \
            (density * FlowSimulator.GRAVITY * radius)
        return h
    
    @staticmethod
    def rainfall_catchment(area: float, rainfall: float, 
                           efficiency: float = 0.8) -> float:
        """
        Calculate water collected from rainfall.
        
        Args:
            area: Catchment area (m²)
            rainfall: Rainfall depth (mm)
            efficiency: Collection efficiency (0-1)
            
        Returns:
            Volume collected (liters)
        """
        # Convert mm to m and m³ to liters
        volume = area * (rainfall / 1000) * 1000 * efficiency
        return volume
    
    @staticmethod
    def drainage_time(volume: float, flow_rate: float) -> float:
        """
        Calculate time to drain volume.
        
        Args:
            volume: Volume to drain (m³)
            flow_rate: Drainage rate (m³/s)
            
        Returns:
            Time (seconds)
        """
        return volume / flow_rate if flow_rate > 0 else float('inf')


class LightFlow:
    """Light and illumination calculations."""
    
    @staticmethod
    def daylight_factor(indoor_illuminance: float, 
                        outdoor_illuminance: float) -> float:
        """
        Calculate daylight factor percentage.
        
        Args:
            indoor_illuminance: Indoor light level (lux)
            outdoor_illuminance: Outdoor unobstructed light level (lux)
            
        Returns:
            Daylight factor (%)
        """
        if outdoor_illuminance == 0:
            return 0
        return (indoor_illuminance / outdoor_illuminance) * 100
    
    @staticmethod
    def penetration_depth(window_height: float, multiplier: float = 2.5) -> float:
        """
        Estimate effective daylight penetration depth.
        
        Args:
            window_height: Height of window (m)
            multiplier: Rule of thumb multiplier (typically 2-2.5)
            
        Returns:
            Penetration depth (m)
        """
        return window_height * multiplier
    
    @staticmethod
    def reflectance_factor(incident_angle: float, surface_type: str = 'diffuse') -> float:
        """
        Calculate reflectance based on angle and surface.
        
        Args:
            incident_angle: Angle from normal (degrees)
            surface_type: 'diffuse', 'specular', or 'mixed'
            
        Returns:
            Reflectance factor (0-1)
        """
        angle_rad = math.radians(incident_angle)
        
        if surface_type == 'diffuse':
            # Lambertian reflection
            return math.cos(angle_rad) if angle_rad < math.pi/2 else 0
        
        elif surface_type == 'specular':
            # Fresnel approximation for glass
            cos_theta = math.cos(angle_rad)
            return 0.04 + 0.96 * (1 - cos_theta)**5
        
        else:  # mixed
            return 0.5 * (math.cos(angle_rad) + 0.5)
    
    @staticmethod
    def solar_altitude(latitude: float, day_of_year: int, hour: float) -> float:
        """
        Calculate solar altitude angle (simplified).
        
        Args:
            latitude: Location latitude (degrees)
            day_of_year: Day of year (1-365)
            hour: Hour of day (0-24, solar time)
            
        Returns:
            Solar altitude angle (degrees)
        """
        # Solar declination
        declination = 23.45 * math.sin(math.radians(360 * (284 + day_of_year) / 365))
        
        # Hour angle
        hour_angle = 15 * (hour - 12)  # degrees
        
        # Solar altitude
        lat_rad = math.radians(latitude)
        dec_rad = math.radians(declination)
        ha_rad = math.radians(hour_angle)
        
        sin_alt = (math.sin(lat_rad) * math.sin(dec_rad) + 
                   math.cos(lat_rad) * math.cos(dec_rad) * math.cos(ha_rad))
        
        altitude = math.degrees(math.asin(max(-1, min(1, sin_alt))))
        return max(0, altitude)


class HeatFlow:
    """Heat transfer calculations."""
    
    @staticmethod
    def conduction_heat_transfer(k: float, area: float, temp_diff: float, 
                                  thickness: float) -> float:
        """
        Calculate heat transfer by conduction.
        
        Args:
            k: Thermal conductivity (W/(m·K))
            area: Surface area (m²)
            temp_diff: Temperature difference (K)
            thickness: Material thickness (m)
            
        Returns:
            Heat transfer rate (W)
        """
        if thickness == 0:
            return 0
        return k * area * temp_diff / thickness
    
    @staticmethod
    def convection_heat_transfer(h: float, area: float, temp_diff: float) -> float:
        """
        Calculate heat transfer by convection.
        
        Args:
            h: Convection coefficient (W/(m²·K))
            area: Surface area (m²)
            temp_diff: Temperature difference (K)
            
        Returns:
            Heat transfer rate (W)
        """
        return h * area * temp_diff
    
    @staticmethod
    def radiation_heat_transfer(emissivity: float, area: float, 
                                 temp1: float, temp2: float) -> float:
        """
        Calculate heat transfer by radiation.
        
        Args:
            emissivity: Surface emissivity (0-1)
            area: Surface area (m²)
            temp1: Surface temperature (K)
            temp2: Environment temperature (K)
            
        Returns:
            Heat transfer rate (W)
        """
        return emissivity * FlowSimulator.STEFAN_BOLTZMANN * area * (temp1**4 - temp2**4)
    
    @staticmethod
    def thermal_mass_response(mass: float, specific_heat: float, 
                              temp_change: float) -> float:
        """
        Calculate energy stored/released by thermal mass.
        
        Args:
            mass: Mass of material (kg)
            specific_heat: Specific heat capacity (J/(kg·K))
            temp_change: Temperature change (K)
            
        Returns:
            Energy (J)
        """
        return mass * specific_heat * temp_change
    
    @staticmethod
    def evaporative_cooling_potential(air_temp: float, relative_humidity: float,
                                       airflow: float = 1.0) -> float:
        """
        Estimate evaporative cooling potential (simplified).
        
        Args:
            air_temp: Dry bulb temperature (°C)
            relative_humidity: Relative humidity (0-1)
            airflow: Air velocity factor (m/s)
            
        Returns:
            Estimated temperature reduction (°C)
        """
        # Simplified wet bulb depression
        wet_bulb_depression = (100 - relative_humidity * 100) / 3
        
        # Effectiveness based on airflow
        effectiveness = min(0.9, 0.5 + 0.1 * airflow)
        
        return wet_bulb_depression * effectiveness
    
    @staticmethod
    def u_value(layer_thicknesses: List[float], 
                layer_conductivities: List[float],
                inside_h: float = 8.0, outside_h: float = 25.0) -> float:
        """
        Calculate overall U-value for multi-layer wall.
        
        Args:
            layer_thicknesses: List of layer thicknesses (m)
            layer_conductivities: List of thermal conductivities (W/(m·K))
            inside_h: Inside convection coefficient
            outside_h: Outside convection coefficient
            
        Returns:
            U-value (W/(m²·K))
        """
        # Total resistance
        r_total = 1/inside_h + 1/outside_h
        
        for thickness, k in zip(layer_thicknesses, layer_conductivities):
            if k > 0:
                r_total += thickness / k
        
        return 1 / r_total if r_total > 0 else 0


class VectorField:
    """Vector field operations for flow visualization."""
    
    @staticmethod
    def create_vector_field(width: int, height: int, 
                           velocity_func: Callable[[float, float], Tuple[float, float]]
                           ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create 2D vector field.
        
        Args:
            width: Field width
            height: Field height
            velocity_func: Function (x, y) -> (vx, vy)
            
        Returns:
            Tuple of (vx_field, vy_field) arrays
        """
        vx = np.zeros((height, width))
        vy = np.zeros((height, width))
        
        for i in range(height):
            for j in range(width):
                vx[i, j], vy[i, j] = velocity_func(j, i)
        
        return vx, vy
    
    @staticmethod
    def uniform_flow(velocity: float, angle: float = 0) -> Callable:
        """
        Create uniform flow field.
        
        Args:
            velocity: Flow speed
            angle: Flow direction (degrees)
            
        Returns:
            Velocity function
        """
        angle_rad = math.radians(angle)
        vx = velocity * math.cos(angle_rad)
        vy = velocity * math.sin(angle_rad)
        
        return lambda x, y: (vx, vy)
    
    @staticmethod
    def vortex_flow(strength: float, center: Tuple[float, float]) -> Callable:
        """
        Create vortex flow field.
        
        Args:
            strength: Vortex strength
            center: Vortex center (x, y)
            
        Returns:
            Velocity function
        """
        cx, cy = center
        
        def velocity(x, y):
            dx, dy = x - cx, y - cy
            r = math.sqrt(dx**2 + dy**2)
            if r < 0.1:
                return (0, 0)
            # Tangential velocity
            vx = -strength * dy / r**2
            vy = strength * dx / r**2
            return (vx, vy)
        
        return velocity


def main():
    """Demonstrate flow simulations."""
    print("Mamba Architecture - Natural Flows Module")
    print("=" * 50)
    
    print("\n1. AIRFLOW ANALYSIS")
    print("-" * 50)
    
    # Stack effect
    height = 10  # m
    temp_in, temp_out = 25, 15  # °C
    temp_avg = (temp_in + temp_out) / 2
    pressure = FlowSimulator.chimney_effect_pressure(height, temp_in, temp_out, temp_avg)
    print(f"Stack effect pressure ({height}m, ΔT={temp_in-temp_out}°C): {pressure:.2f} Pa")
    
    # Natural ventilation
    opening_area = 2.0  # m²
    flow_rate = FlowSimulator.natural_ventilation_flow_rate(pressure, opening_area)
    print(f"Natural ventilation flow rate: {flow_rate:.2f} m³/s")
    
    # Reynolds number
    velocity = 2.0  # m/s
    length = 1.0  # m
    re = FlowSimulator.reynolds_number(velocity, length)
    flow_type = "laminar" if FlowSimulator.is_laminar(re) else "turbulent"
    print(f"Reynolds number (v={velocity} m/s, L={length} m): {re:.0f} ({flow_type})")
    
    print("\n2. WATER FLOW")
    print("-" * 50)
    
    # Rainfall collection
    roof_area = 100  # m²
    rainfall_mm = 50  # mm
    collected = WaterFlow.rainfall_catchment(roof_area, rainfall_mm)
    print(f"Water collected from {rainfall_mm}mm on {roof_area}m²: {collected:.0f} liters")
    
    # Capillary rise
    capillary = WaterFlow.capillary_rise(0.073, 0, 0.001)  # 1mm radius
    print(f"Capillary rise in 1mm tube: {capillary*1000:.1f} mm")
    
    print("\n3. LIGHT")
    print("-" * 50)
    
    # Daylight factor
    indoor_lux, outdoor_lux = 500, 10000
    df = LightFlow.daylight_factor(indoor_lux, outdoor_lux)
    print(f"Daylight factor: {df:.1f}%")
    
    # Penetration depth
    window_h = 2.0  # m
    penetration = LightFlow.penetration_depth(window_h)
    print(f"Effective daylight penetration (window h={window_h}m): {penetration:.1f} m")
    
    # Solar position
    latitude = 40  # degrees
    day = 172  # Summer solstice
    hour = 12  # noon
    altitude = LightFlow.solar_altitude(latitude, day, hour)
    print(f"Solar altitude at noon, summer solstice, {latitude}°N: {altitude:.1f}°")
    
    print("\n4. HEAT TRANSFER")
    print("-" * 50)
    
    # Conduction
    k_concrete = 1.4  # W/(m·K)
    area = 10  # m²
    temp_diff = 10  # K
    thickness = 0.2  # m
    q_cond = HeatFlow.conduction_heat_transfer(k_concrete, area, temp_diff, thickness)
    print(f"Heat conduction through 20cm concrete: {q_cond:.0f} W")
    
    # Evaporative cooling
    air_temp = 35  # °C
    rh = 0.3  # 30%
    cooling = HeatFlow.evaporative_cooling_potential(air_temp, rh)
    print(f"Evaporative cooling potential ({air_temp}°C, {rh*100}% RH): {cooling:.1f}°C reduction")
    
    # U-value
    thicknesses = [0.01, 0.10, 0.01]  # plaster, insulation, plaster
    conductivities = [0.5, 0.04, 0.5]  # W/(m·K)
    u_val = HeatFlow.u_value(thicknesses, conductivities)
    print(f"Wall U-value: {u_val:.3f} W/(m²·K)")
    
    print("\n" + "=" * 50)
    print("Use these calculations to design passive systems:")
    print("- Natural ventilation with stack effect")
    print("- Rainwater harvesting")
    print("- Daylighting optimization")
    print("- Passive heating and cooling")


if __name__ == "__main__":
    main()

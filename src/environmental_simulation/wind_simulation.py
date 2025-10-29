"""
Wind Simulation - Simplified wind flow and pressure analysis.
"""

import numpy as np
from typing import Tuple, Dict, List


class WindSimulation:
    """Simulate wind flow around structures."""
    
    @staticmethod
    def wind_pressure(velocity: float,
                     air_density: float = 1.225) -> float:
        """
        Calculate wind pressure using Bernoulli's equation.
        
        Args:
            velocity: Wind velocity in m/s
            air_density: Air density in kg/m³
            
        Returns:
            Dynamic pressure in Pa (N/m²)
        """
        return 0.5 * air_density * velocity**2
    
    @staticmethod
    def wind_force_on_surface(velocity: float,
                             surface_area: float,
                             drag_coefficient: float = 1.2,
                             angle: float = 0.0) -> float:
        """
        Calculate wind force on a surface.
        
        Args:
            velocity: Wind velocity in m/s
            surface_area: Surface area in m²
            drag_coefficient: Drag coefficient (1.0-2.0 for buildings)
            angle: Angle between wind and surface normal in degrees
            
        Returns:
            Force in Newtons
        """
        pressure = WindSimulation.wind_pressure(velocity)
        effective_area = surface_area * abs(np.cos(np.radians(angle)))
        force = drag_coefficient * pressure * effective_area
        return force
    
    @staticmethod
    def velocity_profile(height: float,
                        reference_height: float = 10.0,
                        reference_velocity: float = 10.0,
                        terrain_category: str = 'suburban') -> float:
        """
        Calculate wind velocity at height using power law.
        
        Args:
            height: Height above ground in meters
            reference_height: Reference height in meters
            reference_velocity: Wind velocity at reference height in m/s
            terrain_category: 'sea', 'rural', 'suburban', or 'urban'
            
        Returns:
            Wind velocity at specified height in m/s
        """
        # Power law exponents for different terrain
        exponents = {
            'sea': 0.10,
            'rural': 0.15,
            'suburban': 0.22,
            'urban': 0.30
        }
        
        alpha = exponents.get(terrain_category, 0.22)
        
        velocity = reference_velocity * (height / reference_height) ** alpha
        return velocity
    
    @staticmethod
    def flow_around_cylinder(cylinder_radius: float,
                            wind_velocity: float,
                            grid_size: Tuple[int, int],
                            grid_extent: Tuple[float, float]) -> Dict[str, np.ndarray]:
        """
        Simulate simplified 2D wind flow around cylindrical obstacle.
        
        Args:
            cylinder_radius: Radius of cylinder in meters
            wind_velocity: Incoming wind velocity in m/s
            grid_size: Size of computation grid (nx, ny)
            grid_extent: Physical extent (width, height)
            
        Returns:
            Dictionary with velocity field and pressure
        """
        nx, ny = grid_size
        width, height = grid_extent
        
        x = np.linspace(-width/2, width/2, nx)
        y = np.linspace(-height/2, height/2, ny)
        X, Y = np.meshgrid(x, y)
        
        # Potential flow around cylinder (simplified)
        r = np.sqrt(X**2 + Y**2)
        theta = np.arctan2(Y, X)
        
        # Velocity potential
        phi = wind_velocity * (r + cylinder_radius**2 / r) * np.cos(theta)
        
        # Stream function
        psi = wind_velocity * (r - cylinder_radius**2 / r) * np.sin(theta)
        
        # Velocity components
        u = wind_velocity * (1 - cylinder_radius**2 * (r**2 - X**2) / r**4)
        v = -wind_velocity * cylinder_radius**2 * X * Y / r**4
        
        # Mask inside cylinder
        inside = r < cylinder_radius
        u[inside] = 0
        v[inside] = 0
        
        # Pressure (Bernoulli)
        velocity_magnitude = np.sqrt(u**2 + v**2)
        base_pressure = WindSimulation.wind_pressure(wind_velocity)
        pressure = base_pressure - WindSimulation.wind_pressure(velocity_magnitude)
        
        return {
            'u': u,
            'v': v,
            'velocity_magnitude': velocity_magnitude,
            'pressure': pressure,
            'X': X,
            'Y': Y
        }
    
    @staticmethod
    def ventilation_potential(opening_area: float,
                             height_difference: float,
                             wind_velocity: float,
                             temperature_difference: float = 0.0) -> Dict[str, float]:
        """
        Calculate natural ventilation potential.
        
        Args:
            opening_area: Effective opening area in m²
            height_difference: Vertical distance between openings in m
            wind_velocity: External wind velocity in m/s
            temperature_difference: Indoor-outdoor temp difference in °C
            
        Returns:
            Dictionary with ventilation rates
        """
        # Wind-driven ventilation
        wind_pressure = WindSimulation.wind_pressure(wind_velocity)
        wind_flow_rate = 0.6 * opening_area * np.sqrt(2 * wind_pressure / 1.225)
        
        # Buoyancy-driven ventilation (stack effect)
        if temperature_difference != 0:
            g = 9.81  # gravity
            T_avg = 293  # average temperature in K
            stack_pressure = 1.225 * g * height_difference * temperature_difference / T_avg
            stack_flow_rate = 0.6 * opening_area * np.sqrt(2 * abs(stack_pressure) / 1.225)
        else:
            stack_flow_rate = 0
        
        # Combined ventilation
        total_flow_rate = np.sqrt(wind_flow_rate**2 + stack_flow_rate**2)
        
        return {
            'wind_driven_flow': wind_flow_rate,
            'stack_driven_flow': stack_flow_rate,
            'total_flow': total_flow_rate,
            'air_changes_per_hour': total_flow_rate * 3600 / (opening_area * 100)  # approximate
        }
    
    @staticmethod
    def comfort_wind_speed(activity_level: str = 'sitting') -> Tuple[float, float]:
        """
        Return comfortable wind speed range for outdoor spaces.
        
        Args:
            activity_level: 'sitting', 'standing', 'walking'
            
        Returns:
            Tuple of (min_comfort, max_comfort) in m/s
        """
        comfort_ranges = {
            'sitting': (0.5, 1.5),
            'standing': (1.0, 2.5),
            'walking': (1.5, 4.0)
        }
        
        return comfort_ranges.get(activity_level, (0.5, 2.5))
    
    @staticmethod
    def wind_rose_analysis(wind_data: List[Dict]) -> Dict:
        """
        Analyze wind rose data for site analysis.
        
        Args:
            wind_data: List of dicts with 'direction' and 'speed'
            
        Returns:
            Dictionary with prevailing wind analysis
        """
        if not wind_data:
            return {}
        
        directions = np.array([d['direction'] for d in wind_data])
        speeds = np.array([d['speed'] for d in wind_data])
        
        # Bin directions into 16 sectors (22.5° each)
        n_sectors = 16
        sector_width = 360 / n_sectors
        sectors = (directions / sector_width).astype(int) % n_sectors
        
        sector_frequencies = np.zeros(n_sectors)
        sector_speeds = np.zeros(n_sectors)
        
        for i in range(n_sectors):
            mask = sectors == i
            sector_frequencies[i] = np.sum(mask) / len(directions) * 100
            if np.any(mask):
                sector_speeds[i] = np.mean(speeds[mask])
        
        # Find prevailing direction
        prevailing_sector = np.argmax(sector_frequencies)
        prevailing_direction = prevailing_sector * sector_width + sector_width / 2
        
        return {
            'sector_frequencies': sector_frequencies,
            'sector_speeds': sector_speeds,
            'prevailing_direction': prevailing_direction,
            'average_speed': np.mean(speeds),
            'max_speed': np.max(speeds)
        }

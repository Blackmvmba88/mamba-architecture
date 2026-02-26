"""
Light Analysis - Analyze natural light incidence and shadows.
"""

import numpy as np
from typing import Tuple, List, Dict


class LightAnalysis:
    """Analyze light distribution and shadows."""
    
    @staticmethod
    def calculate_irradiance(altitude: float,
                            azimuth: float,
                            surface_normal: np.ndarray,
                            solar_constant: float = 1000.0) -> float:
        """
        Calculate solar irradiance on a surface.
        
        Args:
            altitude: Sun altitude in degrees
            azimuth: Sun azimuth in degrees
            surface_normal: Normal vector of surface [x, y, z]
            solar_constant: Solar irradiance at perpendicular (W/m²)
            
        Returns:
            Irradiance value (W/m²)
        """
        if altitude <= 0:
            return 0.0
        
        # Sun direction vector
        alt_rad = np.radians(altitude)
        az_rad = np.radians(azimuth)
        
        sun_direction = np.array([
            np.cos(alt_rad) * np.sin(az_rad),
            np.cos(alt_rad) * np.cos(az_rad),
            np.sin(alt_rad)
        ])
        
        # Normalize surface normal
        surface_normal = surface_normal / np.linalg.norm(surface_normal)
        
        # Calculate angle of incidence
        cos_incidence = np.dot(sun_direction, surface_normal)
        cos_incidence = max(0, cos_incidence)  # No negative irradiance
        
        # Atmospheric attenuation (simplified)
        air_mass = 1 / (np.sin(alt_rad) + 0.15 * (altitude + 3.885)**(-1.253))
        atmospheric_transmission = 0.7 ** (air_mass ** 0.678)
        
        irradiance = solar_constant * cos_incidence * atmospheric_transmission
        
        return irradiance
    
    @staticmethod
    def shadow_map_2d(sun_altitude: float,
                     sun_azimuth: float,
                     obstacles: List[Dict],
                     grid_size: Tuple[int, int],
                     grid_extent: Tuple[float, float]) -> np.ndarray:
        """
        Generate 2D shadow map from obstacles.
        
        Args:
            sun_altitude: Sun altitude in degrees
            sun_azimuth: Sun azimuth in degrees
            obstacles: List of obstacle dictionaries with 'position', 'height'
            grid_size: Size of grid (nx, ny)
            grid_extent: Physical extent (width, height)
            
        Returns:
            Shadow map (0=shadow, 1=sunlight)
        """
        nx, ny = grid_size
        width, height = grid_extent
        
        shadow_map = np.ones((ny, nx))
        
        if sun_altitude <= 0:
            return np.zeros((ny, nx))
        
        # Calculate shadow direction
        alt_rad = np.radians(sun_altitude)
        az_rad = np.radians(sun_azimuth)
        
        shadow_length_factor = 1 / np.tan(alt_rad)
        shadow_dx = shadow_length_factor * np.sin(az_rad)
        shadow_dy = shadow_length_factor * np.cos(az_rad)
        
        x = np.linspace(0, width, nx)
        y = np.linspace(0, height, ny)
        X, Y = np.meshgrid(x, y)
        
        for obstacle in obstacles:
            obs_x, obs_y = obstacle['position']
            obs_height = obstacle.get('height', 1.0)
            obs_radius = obstacle.get('radius', 0.5)
            
            # Calculate shadow extent
            shadow_length = obs_height * shadow_length_factor
            
            # Shadow end position
            shadow_x = obs_x + shadow_dx * obs_height
            shadow_y = obs_y + shadow_dy * obs_height
            
            # Create shadow cone
            for i in range(int(shadow_length * 10)):
                t = i / (shadow_length * 10)
                sx = obs_x + shadow_dx * obs_height * t
                sy = obs_y + shadow_dy * obs_height * t
                sr = obs_radius * (1 + t * 0.5)
                
                distance = np.sqrt((X - sx)**2 + (Y - sy)**2)
                shadow_map[distance < sr] = 0
        
        return shadow_map
    
    @staticmethod
    def daylight_factor(point: np.ndarray,
                       surrounding_geometry: List[Dict],
                       sky_visibility: float = 1.0) -> float:
        """
        Calculate daylight factor at a point.
        
        Args:
            point: Point coordinates [x, y, z]
            surrounding_geometry: List of surrounding surfaces
            sky_visibility: Fraction of sky visible (0-1)
            
        Returns:
            Daylight factor (0-100%)
        """
        # Simplified calculation
        # In reality, this would involve complex ray tracing
        
        # Base daylight from sky visibility
        sky_component = sky_visibility * 100
        
        # Reduction from surroundings
        obstruction = 0
        for surface in surrounding_geometry:
            surface_center = surface.get('center', [0, 0, 0])
            surface_area = surface.get('area', 1.0)
            
            # Distance to surface
            distance = np.linalg.norm(np.array(point) - np.array(surface_center))
            
            # Solid angle approximation
            solid_angle = surface_area / (distance**2 + 1)
            obstruction += solid_angle
        
        # Reduce daylight based on obstruction
        daylight_factor = sky_component * np.exp(-obstruction * 0.5)
        
        return min(100, max(0, daylight_factor))
    
    @staticmethod
    def illuminance_distribution(surface_points: np.ndarray,
                                surface_normals: np.ndarray,
                                sun_altitude: float,
                                sun_azimuth: float) -> np.ndarray:
        """
        Calculate illuminance distribution across a surface.
        
        Args:
            surface_points: Array of surface points (N x 3)
            surface_normals: Array of surface normals (N x 3)
            sun_altitude: Sun altitude in degrees
            sun_azimuth: Sun azimuth in degrees
            
        Returns:
            Array of illuminance values (N,)
        """
        illuminance = np.zeros(len(surface_points))
        
        for i, (point, normal) in enumerate(zip(surface_points, surface_normals)):
            illuminance[i] = LightAnalysis.calculate_irradiance(
                sun_altitude, sun_azimuth, normal
            )
        
        return illuminance
    
    @staticmethod
    def annual_insolation(latitude: float,
                         surface_normal: np.ndarray,
                         clear_sky_fraction: float = 0.7) -> float:
        """
        Estimate annual solar insolation on a surface.
        
        Args:
            latitude: Latitude in degrees
            surface_normal: Surface normal vector [x, y, z]
            clear_sky_fraction: Fraction of clear sky days
            
        Returns:
            Annual insolation in kWh/m²/year
        """
        # Simplified calculation
        # Average across year using representative days
        
        total_insolation = 0
        days_per_season = 91
        
        # Representative days for each season
        representative_days = [80, 172, 266, 355]
        
        for day in representative_days:
            # Calculate sun path for this day
            from .solar_calculator import SolarCalculator
            
            # Simplified: calculate for several hours
            daily_total = 0
            for hour in range(6, 19):  # 6 AM to 6 PM
                # Approximate sun position
                hour_angle = 15 * (hour - 12)
                declination = SolarCalculator.solar_declination(day)
                
                lat_rad = np.radians(latitude)
                dec_rad = np.radians(declination)
                ha_rad = np.radians(hour_angle)
                
                sin_altitude = (np.sin(lat_rad) * np.sin(dec_rad) + 
                              np.cos(lat_rad) * np.cos(dec_rad) * np.cos(ha_rad))
                altitude = np.degrees(np.arcsin(np.clip(sin_altitude, -1, 1)))
                
                if altitude > 0:
                    # Simplified azimuth
                    azimuth = 180 if hour_angle < 0 else 180
                    
                    irradiance = LightAnalysis.calculate_irradiance(
                        altitude, azimuth, surface_normal
                    )
                    daily_total += irradiance * clear_sky_fraction
            
            # Average over one hour intervals
            total_insolation += daily_total * days_per_season
        
        # Convert to kWh/m²/year
        annual_insolation = (total_insolation / 1000) / len(representative_days)
        
        return annual_insolation

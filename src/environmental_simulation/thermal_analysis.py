"""
Thermal Analysis - Heat transfer and thermal comfort analysis.
"""

import numpy as np
from typing import Dict, List, Tuple


class ThermalAnalysis:
    """Analyze thermal behavior and comfort."""
    
    @staticmethod
    def heat_transfer_conduction(thickness: float,
                                thermal_conductivity: float,
                                area: float,
                                temp_inside: float,
                                temp_outside: float) -> Dict[str, float]:
        """
        Calculate conductive heat transfer through a material.
        
        Args:
            thickness: Material thickness in meters
            thermal_conductivity: Thermal conductivity in W/(m·K)
            area: Surface area in m²
            temp_inside: Inside temperature in °C
            temp_outside: Outside temperature in °C
            
        Returns:
            Dictionary with heat transfer rate and R-value
        """
        # Thermal resistance (R-value)
        r_value = thickness / thermal_conductivity
        
        # Heat transfer rate (Q = A * ΔT / R)
        delta_t = abs(temp_inside - temp_outside)
        heat_flow = area * delta_t / r_value
        
        return {
            'heat_flow_watts': heat_flow,
            'r_value': r_value,
            'u_value': 1 / r_value,  # Overall heat transfer coefficient
            'temperature_difference': delta_t
        }
    
    @staticmethod
    def thermal_mass_effect(mass: float,
                           specific_heat: float,
                           initial_temp: float,
                           ambient_temp: float,
                           time_hours: float,
                           heat_transfer_coef: float = 5.0) -> Dict[str, float]:
        """
        Calculate temperature change with thermal mass.
        
        Args:
            mass: Mass of material in kg
            specific_heat: Specific heat capacity in J/(kg·K)
            initial_temp: Initial temperature in °C
            ambient_temp: Ambient temperature in °C
            time_hours: Time period in hours
            heat_transfer_coef: Heat transfer coefficient in W/(m²·K)
            
        Returns:
            Dictionary with final temperature and stored energy
        """
        # Thermal capacity
        thermal_capacity = mass * specific_heat
        
        # Time constant (hours)
        time_constant = thermal_capacity / (heat_transfer_coef * 3600)
        
        # Temperature after time (exponential decay)
        temp_difference = initial_temp - ambient_temp
        final_temp = ambient_temp + temp_difference * np.exp(-time_hours / time_constant)
        
        # Energy stored/released
        energy_change = thermal_capacity * (final_temp - initial_temp)
        
        return {
            'final_temperature': final_temp,
            'energy_change_joules': energy_change,
            'energy_change_kwh': energy_change / 3.6e6,
            'time_constant_hours': time_constant
        }
    
    @staticmethod
    def solar_heat_gain(window_area: float,
                       solar_irradiance: float,
                       shgc: float = 0.7,
                       shading_factor: float = 1.0) -> float:
        """
        Calculate solar heat gain through glazing.
        
        Args:
            window_area: Window area in m²
            solar_irradiance: Solar irradiance in W/m²
            shgc: Solar Heat Gain Coefficient (0-1)
            shading_factor: Shading reduction factor (0-1)
            
        Returns:
            Heat gain in Watts
        """
        heat_gain = window_area * solar_irradiance * shgc * shading_factor
        return heat_gain
    
    @staticmethod
    def thermal_comfort_pmv(air_temp: float,
                           radiant_temp: float,
                           air_velocity: float,
                           relative_humidity: float,
                           metabolic_rate: float = 1.2,
                           clothing_insulation: float = 0.5) -> Dict[str, float]:
        """
        Calculate Predicted Mean Vote (PMV) for thermal comfort.
        Simplified ISO 7730 calculation.
        
        Args:
            air_temp: Air temperature in °C
            radiant_temp: Mean radiant temperature in °C
            air_velocity: Air velocity in m/s
            relative_humidity: Relative humidity in % (0-100)
            metabolic_rate: Metabolic rate in met (1 met = 58.15 W/m²)
            clothing_insulation: Clothing insulation in clo (1 clo = 0.155 m²·K/W)
            
        Returns:
            Dictionary with PMV and PPD
        """
        # Simplified PMV calculation
        # Full calculation is very complex, this is an approximation
        
        # Optimal temperature based on clothing and activity
        optimal_temp = 24.0 - 2.0 * (clothing_insulation - 0.5)
        optimal_temp += -1.0 * (metabolic_rate - 1.2) * 3
        
        # Temperature difference from optimal
        temp_diff = air_temp - optimal_temp
        
        # Effect of humidity
        humidity_effect = (relative_humidity - 50) * 0.01
        
        # Effect of air velocity
        velocity_effect = -2.0 * air_velocity
        
        # PMV calculation (simplified)
        pmv = 0.303 * np.exp(-0.036 * metabolic_rate * 58.15) + 0.028
        pmv *= (temp_diff + humidity_effect + velocity_effect)
        pmv = np.clip(pmv, -3, 3)
        
        # PPD (Predicted Percentage of Dissatisfied)
        ppd = 100 - 95 * np.exp(-0.03353 * pmv**4 - 0.2179 * pmv**2)
        
        # Comfort category
        if abs(pmv) < 0.5:
            category = 'Comfortable (Category A)'
        elif abs(pmv) < 0.7:
            category = 'Comfortable (Category B)'
        elif abs(pmv) < 1.0:
            category = 'Acceptable (Category C)'
        else:
            category = 'Uncomfortable'
        
        return {
            'pmv': pmv,
            'ppd': ppd,
            'category': category,
            'optimal_temperature': optimal_temp
        }
    
    @staticmethod
    def thermal_bridge_effect(bridge_conductivity: float,
                             bridge_area: float,
                             wall_r_value: float,
                             temp_difference: float) -> Dict[str, float]:
        """
        Calculate heat loss through thermal bridge.
        
        Args:
            bridge_conductivity: Linear thermal transmittance in W/(m·K)
            bridge_area: Bridge cross-section area in m²
            wall_r_value: Wall R-value in m²·K/W
            temp_difference: Indoor-outdoor temperature difference in °C
            
        Returns:
            Dictionary with thermal bridge heat loss
        """
        # Heat loss through bridge
        bridge_heat_loss = bridge_conductivity * bridge_area * temp_difference
        
        # Heat loss through normal wall (same area)
        wall_heat_loss = bridge_area * temp_difference / wall_r_value
        
        # Additional heat loss due to bridge
        additional_loss = bridge_heat_loss - wall_heat_loss
        
        return {
            'bridge_heat_loss': bridge_heat_loss,
            'wall_heat_loss': wall_heat_loss,
            'additional_loss': additional_loss,
            'loss_increase_percent': (additional_loss / wall_heat_loss) * 100 if wall_heat_loss > 0 else 0
        }
    
    @staticmethod
    def passive_heating_potential(latitude: float,
                                 window_area_south: float,
                                 window_area_other: float,
                                 shgc: float = 0.7,
                                 heating_degree_days: float = 2000) -> Dict[str, float]:
        """
        Estimate annual passive solar heating potential.
        
        Args:
            latitude: Latitude in degrees
            window_area_south: South-facing window area in m²
            window_area_other: Other orientation window area in m²
            shgc: Solar Heat Gain Coefficient
            heating_degree_days: Annual heating degree days
            
        Returns:
            Dictionary with heating potential
        """
        # Average daily solar radiation (simplified by latitude)
        base_radiation = 1000  # W/m² at equator
        latitude_factor = np.cos(np.radians(abs(latitude)))
        avg_daily_radiation = base_radiation * latitude_factor * 0.5  # Account for day/night
        
        # South-facing gain (winter optimal)
        south_gain = window_area_south * avg_daily_radiation * shgc * 0.7  # 70% winter efficiency
        
        # Other orientations gain
        other_gain = window_area_other * avg_daily_radiation * shgc * 0.4  # 40% efficiency
        
        # Annual energy (kWh/year)
        daily_gain_kwh = (south_gain + other_gain) * 8 / 1000  # 8 hours equivalent
        annual_gain_kwh = daily_gain_kwh * 180  # Heating season days
        
        # Heating load reduction
        heating_load_kwh = heating_degree_days * 24  # Simplified
        reduction_percent = (annual_gain_kwh / heating_load_kwh) * 100 if heating_load_kwh > 0 else 0
        
        return {
            'annual_solar_gain_kwh': annual_gain_kwh,
            'daily_average_gain_kwh': daily_gain_kwh,
            'heating_load_reduction_percent': min(100, reduction_percent),
            'equivalent_heating_cost_saved': annual_gain_kwh * 0.12  # Assuming $0.12/kWh
        }
    
    @staticmethod
    def thermal_lag(wall_thickness: float,
                   thermal_diffusivity: float) -> Dict[str, float]:
        """
        Calculate thermal lag (time delay) through a wall.
        
        Args:
            wall_thickness: Wall thickness in meters
            thermal_diffusivity: Thermal diffusivity in m²/s
            
        Returns:
            Dictionary with thermal lag time
        """
        # Thermal lag time (simplified)
        lag_hours = (wall_thickness ** 2) / (thermal_diffusivity * 3600 * np.pi)
        
        # Decrement factor (amplitude reduction)
        decrement_factor = np.exp(-wall_thickness * np.sqrt(np.pi / (thermal_diffusivity * 86400)))
        
        return {
            'lag_hours': lag_hours,
            'decrement_factor': decrement_factor,
            'temperature_swing_reduction_percent': (1 - decrement_factor) * 100
        }

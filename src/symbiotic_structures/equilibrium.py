"""
Equilibrium Calculator - Calculate balance and stability in structures.
"""

import numpy as np
from typing import Dict, List, Tuple


class EquilibriumCalculator:
    """Calculate equilibrium states and stability."""
    
    @staticmethod
    def energy_balance(solar_gain: float,
                      internal_gain: float,
                      heat_loss: float,
                      target_temp: float,
                      current_temp: float) -> Dict:
        """
        Calculate thermal energy balance.
        
        Args:
            solar_gain: Solar heat gain in Watts
            internal_gain: Internal heat gain in Watts
            heat_loss: Heat loss in Watts
            target_temp: Target temperature
            current_temp: Current temperature
            
        Returns:
            Dictionary with energy balance
        """
        total_gain = solar_gain + internal_gain
        net_energy = total_gain - heat_loss
        
        is_balanced = abs(net_energy) < 100  # Within 100W
        
        # Calculate required adjustment
        temp_diff = target_temp - current_temp
        required_adjustment = temp_diff * 50  # Simplified: 50W per degree
        
        return {
            'total_gain': total_gain,
            'heat_loss': heat_loss,
            'net_energy': net_energy,
            'is_balanced': is_balanced,
            'balance_factor': 1 - abs(net_energy) / (total_gain + 1),
            'required_adjustment': required_adjustment
        }
    
    @staticmethod
    def structural_equilibrium(forces: List[np.ndarray],
                              moments: List[np.ndarray]) -> Dict:
        """
        Check structural equilibrium.
        
        Args:
            forces: List of force vectors
            moments: List of moment vectors
            
        Returns:
            Dictionary with equilibrium analysis
        """
        # Sum of forces
        total_force = np.sum(forces, axis=0)
        force_magnitude = np.linalg.norm(total_force)
        
        # Sum of moments
        total_moment = np.sum(moments, axis=0)
        moment_magnitude = np.linalg.norm(total_moment)
        
        # Check equilibrium conditions
        force_equilibrium = force_magnitude < 0.01
        moment_equilibrium = moment_magnitude < 0.01
        
        return {
            'force_sum': total_force,
            'force_magnitude': force_magnitude,
            'moment_sum': total_moment,
            'moment_magnitude': moment_magnitude,
            'force_equilibrium': force_equilibrium,
            'moment_equilibrium': moment_equilibrium,
            'is_in_equilibrium': force_equilibrium and moment_equilibrium
        }
    
    @staticmethod
    def ecological_balance(resource_input: float,
                          resource_consumption: float,
                          waste_output: float,
                          recycling_rate: float = 0.5) -> Dict:
        """
        Calculate ecological balance of building.
        
        Args:
            resource_input: Resource input rate
            resource_consumption: Consumption rate
            waste_output: Waste output rate
            recycling_rate: Fraction of waste recycled (0-1)
            
        Returns:
            Dictionary with ecological balance
        """
        recycled_resources = waste_output * recycling_rate
        net_resource_need = resource_consumption - resource_input - recycled_resources
        
        # Sustainability index
        if resource_consumption > 0:
            sustainability = (resource_input + recycled_resources) / resource_consumption
        else:
            sustainability = 1.0
        
        is_sustainable = sustainability >= 0.95
        
        return {
            'resource_input': resource_input,
            'resource_consumption': resource_consumption,
            'waste_output': waste_output,
            'recycled_resources': recycled_resources,
            'net_resource_need': net_resource_need,
            'sustainability_index': sustainability,
            'is_sustainable': is_sustainable
        }
    
    @staticmethod
    def comfort_equilibrium(thermal_comfort: float,
                           visual_comfort: float,
                           acoustic_comfort: float,
                           air_quality: float,
                           weights: Dict[str, float] = None) -> Dict:
        """
        Calculate overall comfort equilibrium.
        
        Args:
            thermal_comfort: Thermal comfort score (0-1)
            visual_comfort: Visual comfort score (0-1)
            acoustic_comfort: Acoustic comfort score (0-1)
            air_quality: Air quality score (0-1)
            weights: Optional weights for each factor
            
        Returns:
            Dictionary with comfort equilibrium
        """
        if weights is None:
            weights = {
                'thermal': 0.35,
                'visual': 0.25,
                'acoustic': 0.20,
                'air': 0.20
            }
        
        # Weighted average
        overall_comfort = (
            thermal_comfort * weights['thermal'] +
            visual_comfort * weights['visual'] +
            acoustic_comfort * weights['acoustic'] +
            air_quality * weights['air']
        )
        
        # Check balance (all factors should be within reasonable range)
        factors = [thermal_comfort, visual_comfort, acoustic_comfort, air_quality]
        variance = np.var(factors)
        is_balanced = variance < 0.1  # Low variance means balanced
        
        return {
            'thermal_comfort': thermal_comfort,
            'visual_comfort': visual_comfort,
            'acoustic_comfort': acoustic_comfort,
            'air_quality': air_quality,
            'overall_comfort': overall_comfort,
            'variance': variance,
            'is_balanced': is_balanced,
            'weakest_factor': ['thermal', 'visual', 'acoustic', 'air'][np.argmin(factors)]
        }
    
    @staticmethod
    def symbiotic_index(building_metrics: Dict,
                       environment_metrics: Dict) -> float:
        """
        Calculate symbiotic relationship index.
        
        Args:
            building_metrics: Building performance metrics
            environment_metrics: Environmental impact metrics
            
        Returns:
            Symbiotic index (0-1, higher is better)
        """
        # Energy efficiency
        energy_efficiency = building_metrics.get('energy_efficiency', 0.5)
        
        # Resource efficiency
        resource_efficiency = building_metrics.get('resource_efficiency', 0.5)
        
        # Environmental impact (lower is better, so invert)
        env_impact = 1 - environment_metrics.get('carbon_footprint_normalized', 0.5)
        
        # Biodiversity support
        biodiversity = environment_metrics.get('biodiversity_support', 0.5)
        
        # Water cycle integration
        water_integration = environment_metrics.get('water_integration', 0.5)
        
        # Calculate symbiotic index
        symbiotic_index = (
            energy_efficiency * 0.25 +
            resource_efficiency * 0.20 +
            env_impact * 0.25 +
            biodiversity * 0.15 +
            water_integration * 0.15
        )
        
        return symbiotic_index
    
    @staticmethod
    def homeostasis_control(current_state: Dict,
                           target_state: Dict,
                           control_gains: Dict = None) -> Dict:
        """
        Calculate control actions for homeostasis (self-regulation).
        
        Args:
            current_state: Current system state
            target_state: Target system state
            control_gains: PID-like control gains
            
        Returns:
            Dictionary with control actions
        """
        if control_gains is None:
            control_gains = {
                'proportional': 0.5,
                'integral': 0.1,
                'derivative': 0.2
            }
        
        control_actions = {}
        
        for param in target_state:
            if param in current_state:
                error = target_state[param] - current_state[param]
                
                # Proportional control
                p_action = error * control_gains['proportional']
                
                # Simplified - in real system would track integral and derivative
                control_actions[param] = {
                    'error': error,
                    'control_action': p_action,
                    'action_type': 'increase' if p_action > 0 else 'decrease',
                    'urgency': min(1.0, abs(error) / 10)
                }
        
        return control_actions

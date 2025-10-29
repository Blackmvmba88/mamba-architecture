"""
Adaptive System - Structures that adapt to environmental conditions.
"""

import numpy as np
from typing import Dict, List, Callable


class AdaptiveSystem:
    """System for adaptive architectural responses."""
    
    def __init__(self):
        """Initialize adaptive system."""
        self.state_history = []
        self.adaptation_memory = {}
    
    def thermal_adaptation(self,
                          current_temp: float,
                          target_temp: float,
                          thermal_mass: float,
                          adaptation_rate: float = 0.1) -> Dict:
        """
        Adapt structure for thermal comfort.
        
        Args:
            current_temp: Current temperature
            target_temp: Target temperature
            thermal_mass: Thermal mass of structure
            adaptation_rate: Rate of adaptation (0-1)
            
        Returns:
            Dictionary with adaptation actions
        """
        temp_diff = target_temp - current_temp
        
        # Determine adaptations
        adaptations = {
            'adjust_shading': 0.0,
            'adjust_ventilation': 0.0,
            'adjust_thermal_mass_exposure': 0.0
        }
        
        if temp_diff > 0:  # Need heating
            # Reduce shading for more solar gain
            adaptations['adjust_shading'] = -adaptation_rate * abs(temp_diff) / 10
            # Reduce ventilation
            adaptations['adjust_ventilation'] = -adaptation_rate * 0.5
            # Expose thermal mass during day
            adaptations['adjust_thermal_mass_exposure'] = adaptation_rate
        
        elif temp_diff < 0:  # Need cooling
            # Increase shading
            adaptations['adjust_shading'] = adaptation_rate * abs(temp_diff) / 10
            # Increase ventilation
            adaptations['adjust_ventilation'] = adaptation_rate
            # Expose thermal mass at night
            adaptations['adjust_thermal_mass_exposure'] = -adaptation_rate
        
        # Clip values
        for key in adaptations:
            adaptations[key] = np.clip(adaptations[key], -1, 1)
        
        return adaptations
    
    def light_adaptation(self,
                        current_illuminance: float,
                        target_illuminance: float,
                        sun_altitude: float) -> Dict:
        """
        Adapt for optimal daylighting.
        
        Args:
            current_illuminance: Current light level (lux)
            target_illuminance: Target light level (lux)
            sun_altitude: Sun altitude in degrees
            
        Returns:
            Dictionary with adaptation actions
        """
        lux_diff = target_illuminance - current_illuminance
        
        adaptations = {
            'adjust_louvers_angle': 0.0,
            'adjust_window_opacity': 0.0,
            'redirect_sunlight': False
        }
        
        if lux_diff > 0:  # Need more light
            # Open louvers
            adaptations['adjust_louvers_angle'] = min(90, 45 + abs(lux_diff) / 50)
            # Increase transparency
            adaptations['adjust_window_opacity'] = max(0, 0.2 - abs(lux_diff) / 1000)
            # Use light shelves/redirectors
            adaptations['redirect_sunlight'] = True
        
        else:  # Need less light
            # Close louvers
            adaptations['adjust_louvers_angle'] = max(0, 45 - abs(lux_diff) / 50)
            # Decrease transparency
            adaptations['adjust_window_opacity'] = min(0.8, 0.2 + abs(lux_diff) / 1000)
            adaptations['redirect_sunlight'] = False
        
        return adaptations
    
    def wind_adaptation(self,
                       wind_speed: float,
                       wind_direction: float,
                       comfort_threshold: float = 2.5) -> Dict:
        """
        Adapt to wind conditions.
        
        Args:
            wind_speed: Wind speed in m/s
            wind_direction: Wind direction in degrees
            comfort_threshold: Maximum comfortable wind speed
            
        Returns:
            Dictionary with adaptation actions
        """
        adaptations = {
            'adjust_openings': 'open',
            'deploy_windbreaks': False,
            'redirect_airflow': False
        }
        
        if wind_speed > comfort_threshold:
            # Strong wind - protect
            adaptations['adjust_openings'] = 'close'
            adaptations['deploy_windbreaks'] = True
            adaptations['redirect_airflow'] = True
        
        elif wind_speed < 0.5:
            # Weak wind - encourage flow
            adaptations['adjust_openings'] = 'open'
            adaptations['deploy_windbreaks'] = False
            adaptations['redirect_airflow'] = False
        
        else:
            # Moderate wind - channel for ventilation
            adaptations['adjust_openings'] = 'partial'
            adaptations['redirect_airflow'] = True
        
        return adaptations
    
    def integrated_adaptation(self,
                             environmental_state: Dict) -> Dict:
        """
        Integrate multiple environmental factors for holistic adaptation.
        
        Args:
            environmental_state: Dictionary with environmental parameters
            
        Returns:
            Dictionary with all adaptation recommendations
        """
        all_adaptations = {}
        
        # Thermal adaptation
        if 'temperature' in environmental_state and 'target_temp' in environmental_state:
            thermal = self.thermal_adaptation(
                environmental_state['temperature'],
                environmental_state['target_temp'],
                environmental_state.get('thermal_mass', 1.0)
            )
            all_adaptations['thermal'] = thermal
        
        # Light adaptation
        if 'illuminance' in environmental_state and 'target_illuminance' in environmental_state:
            light = self.light_adaptation(
                environmental_state['illuminance'],
                environmental_state['target_illuminance'],
                environmental_state.get('sun_altitude', 45)
            )
            all_adaptations['light'] = light
        
        # Wind adaptation
        if 'wind_speed' in environmental_state:
            wind = self.wind_adaptation(
                environmental_state['wind_speed'],
                environmental_state.get('wind_direction', 0),
                environmental_state.get('comfort_threshold', 2.5)
            )
            all_adaptations['wind'] = wind
        
        # Store state
        self.state_history.append({
            'environmental_state': environmental_state.copy(),
            'adaptations': all_adaptations.copy()
        })
        
        return all_adaptations
    
    def learn_optimal_response(self,
                              environmental_patterns: List[Dict],
                              comfort_feedback: List[float]) -> Dict:
        """
        Learn optimal responses from historical data.
        
        Args:
            environmental_patterns: List of environmental states
            comfort_feedback: List of comfort scores (0-1)
            
        Returns:
            Dictionary with learned response patterns
        """
        if len(environmental_patterns) != len(comfort_feedback):
            raise ValueError("Patterns and feedback must have same length")
        
        # Group by similar conditions
        learned_responses = {}
        
        for pattern, comfort in zip(environmental_patterns, comfort_feedback):
            # Create pattern key (simplified)
            temp_range = int(pattern.get('temperature', 20) / 5) * 5
            light_range = int(pattern.get('illuminance', 500) / 500) * 500
            
            pattern_key = f"temp_{temp_range}_light_{light_range}"
            
            if pattern_key not in learned_responses:
                learned_responses[pattern_key] = {
                    'conditions': [],
                    'comfort_scores': [],
                    'avg_comfort': 0
                }
            
            learned_responses[pattern_key]['conditions'].append(pattern)
            learned_responses[pattern_key]['comfort_scores'].append(comfort)
        
        # Calculate averages
        for key in learned_responses:
            scores = learned_responses[key]['comfort_scores']
            learned_responses[key]['avg_comfort'] = np.mean(scores)
        
        self.adaptation_memory = learned_responses
        
        return learned_responses
    
    def predict_adaptation_need(self,
                               current_state: Dict,
                               time_ahead_hours: float = 1.0) -> Dict:
        """
        Predict future adaptation needs.
        
        Args:
            current_state: Current environmental state
            time_ahead_hours: Hours to predict ahead
            
        Returns:
            Dictionary with predicted adaptations
        """
        # Simple linear extrapolation
        if len(self.state_history) < 2:
            return {}
        
        recent_states = self.state_history[-10:]  # Last 10 states
        
        # Calculate trends
        temps = [s['environmental_state'].get('temperature', 20) for s in recent_states]
        temp_trend = (temps[-1] - temps[0]) / len(temps) if len(temps) > 1 else 0
        
        predicted_temp = current_state.get('temperature', 20) + temp_trend * time_ahead_hours
        
        # Predict adaptations based on predicted state
        predicted_state = current_state.copy()
        predicted_state['temperature'] = predicted_temp
        
        predicted_adaptations = self.integrated_adaptation(predicted_state)
        
        return {
            'predicted_state': predicted_state,
            'predicted_adaptations': predicted_adaptations,
            'confidence': min(1.0, len(self.state_history) / 100)
        }

"""
Response Behavior - Define how structures respond to stimuli.
"""

import numpy as np
from typing import Dict, List, Callable, Tuple


class ResponseBehavior:
    """Define behavioral responses to environmental stimuli."""
    
    @staticmethod
    def threshold_response(stimulus: float,
                          threshold: float,
                          response_magnitude: float = 1.0) -> float:
        """
        Simple threshold response (on/off).
        
        Args:
            stimulus: Stimulus value
            threshold: Activation threshold
            response_magnitude: Response strength
            
        Returns:
            Response value
        """
        return response_magnitude if stimulus >= threshold else 0.0
    
    @staticmethod
    def linear_response(stimulus: float,
                       min_stimulus: float,
                       max_stimulus: float,
                       min_response: float = 0.0,
                       max_response: float = 1.0) -> float:
        """
        Linear response mapping.
        
        Args:
            stimulus: Stimulus value
            min_stimulus: Minimum stimulus value
            max_stimulus: Maximum stimulus value
            min_response: Minimum response value
            max_response: Maximum response value
            
        Returns:
            Response value
        """
        if stimulus <= min_stimulus:
            return min_response
        elif stimulus >= max_stimulus:
            return max_response
        else:
            # Linear interpolation
            t = (stimulus - min_stimulus) / (max_stimulus - min_stimulus)
            return min_response + t * (max_response - min_response)
    
    @staticmethod
    def sigmoidal_response(stimulus: float,
                          midpoint: float,
                          steepness: float = 1.0,
                          min_response: float = 0.0,
                          max_response: float = 1.0) -> float:
        """
        Sigmoidal (S-curve) response.
        
        Args:
            stimulus: Stimulus value
            midpoint: Midpoint of sigmoid
            steepness: Steepness of sigmoid
            min_response: Minimum response
            max_response: Maximum response
            
        Returns:
            Response value
        """
        # Logistic function
        response = 1 / (1 + np.exp(-steepness * (stimulus - midpoint)))
        return min_response + response * (max_response - min_response)
    
    @staticmethod
    def hysteresis_response(stimulus: float,
                           current_state: bool,
                           activate_threshold: float,
                           deactivate_threshold: float,
                           response_magnitude: float = 1.0) -> Tuple[float, bool]:
        """
        Response with hysteresis (different thresholds for activation/deactivation).
        
        Args:
            stimulus: Current stimulus value
            current_state: Current state (True=active, False=inactive)
            activate_threshold: Threshold to activate
            deactivate_threshold: Threshold to deactivate
            response_magnitude: Response strength
            
        Returns:
            Tuple of (response_value, new_state)
        """
        if current_state:
            # Currently active - check deactivation
            if stimulus < deactivate_threshold:
                return 0.0, False
            else:
                return response_magnitude, True
        else:
            # Currently inactive - check activation
            if stimulus >= activate_threshold:
                return response_magnitude, True
            else:
                return 0.0, False
    
    @staticmethod
    def adaptive_response(stimulus_history: List[float],
                         adaptation_rate: float = 0.1) -> float:
        """
        Response that adapts to repeated stimuli.
        
        Args:
            stimulus_history: History of stimulus values
            adaptation_rate: Rate of adaptation (0-1)
            
        Returns:
            Adapted response value
        """
        if not stimulus_history:
            return 0.0
        
        # Calculate baseline from history
        baseline = np.mean(stimulus_history[-10:]) if len(stimulus_history) > 0 else 0
        
        # Current stimulus relative to baseline
        current = stimulus_history[-1]
        relative_stimulus = current - baseline
        
        # Response decreases with repeated exposure
        adaptation_factor = 1 - min(1.0, len(stimulus_history) * adaptation_rate / 100)
        
        return relative_stimulus * adaptation_factor
    
    @staticmethod
    def anticipatory_response(current_stimulus: float,
                            stimulus_trend: float,
                            prediction_horizon: float = 1.0) -> float:
        """
        Response that anticipates future conditions.
        
        Args:
            current_stimulus: Current stimulus value
            stimulus_trend: Rate of change of stimulus
            prediction_horizon: How far ahead to predict
            
        Returns:
            Anticipatory response value
        """
        # Predict future stimulus
        predicted_stimulus = current_stimulus + stimulus_trend * prediction_horizon
        
        # Response based on predicted value
        if predicted_stimulus > current_stimulus * 1.2:
            # Strong increase predicted
            return 1.0
        elif predicted_stimulus < current_stimulus * 0.8:
            # Strong decrease predicted
            return -1.0
        else:
            # Moderate change
            return (predicted_stimulus - current_stimulus) / (current_stimulus + 1)
    
    @staticmethod
    def multi_stimulus_integration(stimuli: Dict[str, float],
                                   weights: Dict[str, float] = None,
                                   integration_type: str = 'weighted_sum') -> float:
        """
        Integrate multiple stimuli into single response.
        
        Args:
            stimuli: Dictionary of stimulus values
            weights: Dictionary of weights for each stimulus
            integration_type: 'weighted_sum', 'max', 'min', or 'product'
            
        Returns:
            Integrated response value
        """
        if weights is None:
            weights = {key: 1.0 for key in stimuli}
        
        if integration_type == 'weighted_sum':
            total_weight = sum(weights.values())
            response = sum(stimuli[key] * weights.get(key, 1.0) for key in stimuli) / total_weight
        
        elif integration_type == 'max':
            response = max(stimuli.values())
        
        elif integration_type == 'min':
            response = min(stimuli.values())
        
        elif integration_type == 'product':
            response = np.prod(list(stimuli.values()))
        
        else:
            response = np.mean(list(stimuli.values()))
        
        return response
    
    @staticmethod
    def rhythmic_response(time: float,
                         period: float,
                         amplitude: float = 1.0,
                         phase: float = 0.0) -> float:
        """
        Generate rhythmic/circadian response.
        
        Args:
            time: Current time
            period: Period of rhythm
            amplitude: Amplitude of oscillation
            phase: Phase shift
            
        Returns:
            Rhythmic response value
        """
        return amplitude * np.sin(2 * np.pi * time / period + phase)
    
    @staticmethod
    def emergent_behavior(local_states: List[Dict],
                         interaction_rule: Callable) -> List[Dict]:
        """
        Generate emergent behavior from local interactions.
        
        Args:
            local_states: List of local state dictionaries
            interaction_rule: Function defining interaction between neighbors
            
        Returns:
            Updated list of local states
        """
        new_states = []
        
        for i, state in enumerate(local_states):
            # Get neighbors (simplified - adjacent elements)
            neighbors = []
            if i > 0:
                neighbors.append(local_states[i-1])
            if i < len(local_states) - 1:
                neighbors.append(local_states[i+1])
            
            # Apply interaction rule
            new_state = interaction_rule(state, neighbors)
            new_states.append(new_state)
        
        return new_states

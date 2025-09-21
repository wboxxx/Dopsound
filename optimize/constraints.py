#!/usr/bin/env python3
"""
Parameter Constraints and Validation
===================================

Defines parameter bounds, constraints, and validation rules
for Magicstomp parameter optimization.
"""

from typing import Dict, Any, List, Tuple
from dataclasses import dataclass


@dataclass
class ParameterConstraint:
    """Defines constraints for a parameter."""
    min_value: float
    max_value: float
    step_size: float
    default_value: float
    unit: str = ""
    description: str = ""


class MagicstompConstraints:
    """
    Parameter constraints for Yamaha Magicstomp optimization.
    
    Defines valid ranges, step sizes, and relationships between parameters
    to ensure realistic and musical parameter combinations.
    """
    
    def __init__(self):
        """Initialize parameter constraints."""
        self.constraints = {}
        self._setup_parameter_constraints()
    
    def _setup_parameter_constraints(self):
        """Setup all parameter constraints."""
        
        # Delay parameters
        self.constraints['delay_mix'] = ParameterConstraint(
            min_value=0.0, max_value=1.0, step_size=0.08, default_value=0.2,
            unit="", description="Delay mix level (dry/wet balance)"
        )
        
        self.constraints['delay_feedback'] = ParameterConstraint(
            min_value=0.0, max_value=0.95, step_size=0.10, default_value=0.3,
            unit="", description="Delay feedback amount"
        )
        
        self.constraints['delay_time_ms'] = ParameterConstraint(
            min_value=30, max_value=1500, step_size=25, default_value=300,
            unit="ms", description="Delay time in milliseconds"
        )
        
        # Reverb parameters
        self.constraints['reverb_mix'] = ParameterConstraint(
            min_value=0.0, max_value=1.0, step_size=0.06, default_value=0.15,
            unit="", description="Reverb mix level"
        )
        
        self.constraints['reverb_decay_s'] = ParameterConstraint(
            min_value=0.1, max_value=3.0, step_size=0.4, default_value=1.5,
            unit="s", description="Reverb decay time"
        )
        
        # Amp/tonality parameters
        self.constraints['treble'] = ParameterConstraint(
            min_value=0.0, max_value=1.0, step_size=0.10, default_value=0.5,
            unit="", description="Treble frequency response"
        )
        
        self.constraints['presence'] = ParameterConstraint(
            min_value=0.0, max_value=1.0, step_size=0.10, default_value=0.5,
            unit="", description="Presence frequency response"
        )
        
        self.constraints['gain'] = ParameterConstraint(
            min_value=0.0, max_value=1.0, step_size=0.08, default_value=0.5,
            unit="", description="Input gain/overdrive"
        )
        
        # Modulation parameters
        self.constraints['mod_depth'] = ParameterConstraint(
            min_value=0.0, max_value=1.0, step_size=0.10, default_value=0.35,
            unit="", description="Modulation depth"
        )
        
        self.constraints['mod_rate_hz'] = ParameterConstraint(
            min_value=0.1, max_value=10.0, step_size=0.2, default_value=0.8,
            unit="Hz", description="Modulation rate"
        )
        
        self.constraints['mod_mix'] = ParameterConstraint(
            min_value=0.0, max_value=1.0, step_size=0.08, default_value=0.18,
            unit="", description="Modulation mix level"
        )
    
    def get_constraint(self, parameter_name: str) -> ParameterConstraint:
        """Get constraint for a parameter."""
        return self.constraints.get(parameter_name)
    
    def validate_parameter(self, parameter_name: str, value: float) -> bool:
        """Validate a parameter value against its constraints."""
        constraint = self.get_constraint(parameter_name)
        if not constraint:
            return False
        
        return constraint.min_value <= value <= constraint.max_value
    
    def clamp_parameter(self, parameter_name: str, value: float) -> float:
        """Clamp a parameter value to its valid range."""
        constraint = self.get_constraint(parameter_name)
        if not constraint:
            return value
        
        return max(constraint.min_value, min(constraint.max_value, value))
    
    def get_valid_parameters(self) -> List[str]:
        """Get list of all valid parameter names."""
        return list(self.constraints.keys())
    
    def get_parameter_info(self, parameter_name: str) -> Dict[str, Any]:
        """Get detailed information about a parameter."""
        constraint = self.get_constraint(parameter_name)
        if not constraint:
            return {}
        
        return {
            'name': parameter_name,
            'min_value': constraint.min_value,
            'max_value': constraint.max_value,
            'step_size': constraint.step_size,
            'default_value': constraint.default_value,
            'unit': constraint.unit,
            'description': constraint.description
        }


class ParameterValidator:
    """
    Validates parameter combinations and relationships.
    
    Ensures that parameter combinations make musical sense
    and don't create unrealistic or problematic configurations.
    """
    
    def __init__(self):
        """Initialize parameter validator."""
        self.constraints = MagicstompConstraints()
    
    def validate_patch(self, patch: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate an entire patch configuration.
        
        Args:
            patch: Patch configuration dictionary
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Validate individual parameters
        for param_name, value in patch.items():
            if not self.constraints.validate_parameter(param_name, value):
                constraint = self.constraints.get_constraint(param_name)
                if constraint:
                    errors.append(f"{param_name}: {value} not in range [{constraint.min_value}, {constraint.max_value}]")
                else:
                    errors.append(f"{param_name}: unknown parameter")
        
        # Validate parameter relationships
        relationship_errors = self._validate_relationships(patch)
        errors.extend(relationship_errors)
        
        return len(errors) == 0, errors
    
    def _validate_relationships(self, patch: Dict[str, Any]) -> List[str]:
        """Validate parameter relationships."""
        errors = []
        
        # Check delay feedback vs mix relationship
        if 'delay_feedback' in patch and 'delay_mix' in patch:
            feedback = patch['delay_feedback']
            mix = patch['delay_mix']
            
            # High feedback with low mix doesn't make sense
            if feedback > 0.8 and mix < 0.1:
                errors.append("High delay feedback with low mix may cause instability")
        
        # Check modulation rate vs depth relationship
        if 'mod_rate_hz' in patch and 'mod_depth' in patch:
            rate = patch['mod_rate_hz']
            depth = patch['mod_depth']
            
            # Very high rate with high depth can be harsh
            if rate > 8.0 and depth > 0.8:
                errors.append("High modulation rate with high depth may sound harsh")
        
        # Check reverb decay vs mix relationship
        if 'reverb_decay_s' in patch and 'reverb_mix' in patch:
            decay = patch['reverb_decay_s']
            mix = patch['reverb_mix']
            
            # Very long decay with high mix can muddy the sound
            if decay > 2.5 and mix > 0.7:
                errors.append("Long reverb decay with high mix may muddy the sound")
        
        return errors
    
    def suggest_fixes(self, patch: Dict[str, Any]) -> Dict[str, float]:
        """
        Suggest fixes for invalid parameters.
        
        Args:
            patch: Patch configuration dictionary
            
        Returns:
            Dictionary of suggested parameter values
        """
        suggestions = {}
        
        for param_name, value in patch.items():
            if not self.constraints.validate_parameter(param_name, value):
                clamped_value = self.constraints.clamp_parameter(param_name, value)
                suggestions[param_name] = clamped_value
        
        return suggestions


def demo_constraints():
    """Demo function to test parameter constraints."""
    
    # Test parameter validation
    constraints = MagicstompConstraints()
    validator = ParameterValidator()
    
    # Valid parameters
    valid_params = {
        'delay_mix': 0.3,
        'delay_feedback': 0.4,
        'delay_time_ms': 250,
        'reverb_mix': 0.2,
        'treble': 0.6
    }
    
    is_valid, errors = validator.validate_patch(valid_params)
    print(f"Valid patch: {is_valid}")
    if errors:
        print(f"Errors: {errors}")
    
    # Invalid parameters
    invalid_params = {
        'delay_mix': 1.5,  # Out of range
        'delay_feedback': 0.4,
        'delay_time_ms': 2000,  # Out of range
        'reverb_mix': -0.1  # Out of range
    }
    
    is_valid, errors = validator.validate_patch(invalid_params)
    print(f"Invalid patch: {is_valid}")
    if errors:
        print(f"Errors: {errors}")
    
    # Get suggestions
    suggestions = validator.suggest_fixes(invalid_params)
    print(f"Suggestions: {suggestions}")


if __name__ == "__main__":
    demo_constraints()

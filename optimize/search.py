#!/usr/bin/env python3
"""
Coordinate Search Optimization
=============================

Implements coordinate search optimization for Magicstomp parameter tuning.
Uses Hardware-in-the-Loop feedback to optimize parameters through
real hardware processing.
"""

import numpy as np
import logging
import time
from typing import Dict, Any, List, Tuple, Optional, Callable
from dataclasses import dataclass


@dataclass
class ParameterBounds:
    """Defines bounds and step size for a parameter."""
    min_val: float
    max_val: float
    step_size: float
    current_val: float
    
    def clamp(self, value: float) -> float:
        """Clamp value to bounds."""
        return max(self.min_val, min(self.max_val, value))
    
    def is_valid(self, value: float) -> bool:
        """Check if value is within bounds."""
        return self.min_val <= value <= self.max_val


class ParameterSpace:
    """
    Manages parameter space for optimization.
    
    Defines which parameters can be optimized and their constraints.
    """
    
    def __init__(self):
        """Initialize parameter space with default bounds."""
        self.parameters = {}
        self._setup_default_parameters()
    
    def _setup_default_parameters(self):
        """Setup default parameter bounds for Magicstomp optimization."""
        # Delay parameters
        self.parameters['delay_mix'] = ParameterBounds(0.0, 1.0, 0.08, 0.2)
        self.parameters['delay_feedback'] = ParameterBounds(0.0, 1.0, 0.10, 0.3)
        self.parameters['delay_time_ms'] = ParameterBounds(30, 1500, 25, 300)
        
        # Reverb parameters
        self.parameters['reverb_mix'] = ParameterBounds(0.0, 1.0, 0.06, 0.15)
        self.parameters['reverb_decay_s'] = ParameterBounds(0.1, 3.0, 0.4, 1.5)
        
        # Amp/tonality parameters
        self.parameters['treble'] = ParameterBounds(0.0, 1.0, 0.10, 0.5)
        self.parameters['presence'] = ParameterBounds(0.0, 1.0, 0.10, 0.5)
        self.parameters['gain'] = ParameterBounds(0.0, 1.0, 0.08, 0.5)
        
        # Modulation parameters
        self.parameters['mod_depth'] = ParameterBounds(0.0, 1.0, 0.10, 0.35)
        self.parameters['mod_rate_hz'] = ParameterBounds(0.1, 10.0, 0.2, 0.8)
        self.parameters['mod_mix'] = ParameterBounds(0.0, 1.0, 0.08, 0.18)
    
    def get_parameter_value(self, name: str) -> float:
        """Get current value of a parameter."""
        return self.parameters[name].current_val
    
    def set_parameter_value(self, name: str, value: float) -> bool:
        """
        Set value of a parameter.
        
        Args:
            name: Parameter name
            value: New value (will be clamped to bounds)
            
        Returns:
            True if parameter exists and was set
        """
        if name in self.parameters:
            clamped_value = self.parameters[name].clamp(value)
            self.parameters[name].current_val = clamped_value
            return True
        return False
    
    def get_parameter_bounds(self, name: str) -> Optional[ParameterBounds]:
        """Get bounds for a parameter."""
        return self.parameters.get(name)
    
    def list_parameters(self) -> List[str]:
        """List all available parameters."""
        return list(self.parameters.keys())
    
    def get_parameter_dict(self) -> Dict[str, float]:
        """Get current parameter values as dictionary."""
        return {name: param.current_val for name, param in self.parameters.items()}


class CoordinateSearchOptimizer:
    """
    Coordinate search optimizer for Magicstomp parameters.
    
    Performs coordinate-wise optimization by varying one parameter
    at a time and measuring the perceptual loss through hardware.
    """
    
    def __init__(self, parameter_space: ParameterSpace,
                 loss_function: Callable[[Dict[str, float]], float],
                 max_iterations: int = 20,
                 min_improvement: float = 1e-6):
        """
        Initialize coordinate search optimizer.
        
        Args:
            parameter_space: Parameter space to optimize
            loss_function: Function that takes parameter dict and returns loss
            max_iterations: Maximum number of optimization iterations
            min_improvement: Minimum improvement threshold for stopping
        """
        self.parameter_space = parameter_space
        self.loss_function = loss_function
        self.max_iterations = max_iterations
        self.min_improvement = min_improvement
        
        self.logger = logging.getLogger(__name__)
        
        # Optimization state
        self.current_loss = float('inf')
        self.best_loss = float('inf')
        self.best_parameters = {}
        self.iteration = 0
        self.history = []
    
    def optimize(self, initial_parameters: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Perform coordinate search optimization.
        
        Args:
            initial_parameters: Starting parameter values
            
        Returns:
            Optimization results dictionary
        """
        self.logger.info("Starting coordinate search optimization...")
        
        # Initialize parameters
        if initial_parameters:
            for name, value in initial_parameters.items():
                self.parameter_space.set_parameter_value(name, value)
        
        # Get initial loss
        self.current_loss = self.loss_function(self.parameter_space.get_parameter_dict())
        self.best_loss = self.current_loss
        self.best_parameters = self.parameter_space.get_parameter_dict().copy()
        
        self.logger.info(f"Initial loss: {self.current_loss:.6f}")
        
        # Main optimization loop
        for iteration in range(self.max_iterations):
            self.iteration = iteration
            self.logger.info(f"Iteration {iteration + 1}/{self.max_iterations}")
            
            # Try optimizing each parameter
            improved = False
            
            for param_name in self.parameter_space.list_parameters():
                if self._optimize_parameter(param_name):
                    improved = True
            
            # Check stopping criteria
            if not improved:
                self.logger.info("No improvement found, stopping optimization")
                break
            
            # Record history
            self.history.append({
                'iteration': iteration,
                'loss': self.best_loss,
                'parameters': self.best_parameters.copy()
            })
            
            # Check convergence
            if iteration > 0:
                prev_loss = self.history[-2]['loss']
                improvement = prev_loss - self.best_loss
                
                if improvement < self.min_improvement:
                    self.logger.info(f"Converged (improvement < {self.min_improvement})")
                    break
        
        # Final results
        results = {
            'success': True,
            'iterations': self.iteration + 1,
            'initial_loss': self.history[0]['loss'] if self.history else self.current_loss,
            'final_loss': self.best_loss,
            'improvement': self.history[0]['loss'] - self.best_loss if self.history else 0.0,
            'best_parameters': self.best_parameters,
            'history': self.history
        }
        
        self.logger.info(f"Optimization complete:")
        self.logger.info(f"  Iterations: {results['iterations']}")
        self.logger.info(f"  Initial loss: {results['initial_loss']:.6f}")
        self.logger.info(f"  Final loss: {results['final_loss']:.6f}")
        self.logger.info(f"  Improvement: {results['improvement']:.6f}")
        
        return results
    
    def _optimize_parameter(self, param_name: str) -> bool:
        """
        Optimize a single parameter using coordinate search.
        
        Args:
            param_name: Name of parameter to optimize
            
        Returns:
            True if parameter was improved
        """
        param_bounds = self.parameter_space.get_parameter_bounds(param_name)
        if not param_bounds:
            return False
        
        current_value = param_bounds.current_val
        current_loss = self.best_loss
        
        self.logger.debug(f"Optimizing {param_name}: current={current_value:.4f}, loss={current_loss:.6f}")
        
        # Try positive direction
        positive_value = param_bounds.clamp(current_value + param_bounds.step_size)
        if positive_value != current_value:
            self.parameter_space.set_parameter_value(param_name, positive_value)
            positive_loss = self.loss_function(self.parameter_space.get_parameter_dict())
            
            if positive_loss < self.best_loss:
                self.best_loss = positive_loss
                self.best_parameters = self.parameter_space.get_parameter_dict().copy()
                self.logger.debug(f"  + direction: {positive_value:.4f} -> loss={positive_loss:.6f} (improvement)")
                return True
        
        # Try negative direction
        negative_value = param_bounds.clamp(current_value - param_bounds.step_size)
        if negative_value != current_value:
            self.parameter_space.set_parameter_value(param_name, negative_value)
            negative_loss = self.loss_function(self.parameter_space.get_parameter_dict())
            
            if negative_loss < self.best_loss:
                self.best_loss = negative_loss
                self.best_parameters = self.parameter_space.get_parameter_dict().copy()
                self.logger.debug(f"  - direction: {negative_value:.4f} -> loss={negative_loss:.6f} (improvement)")
                return True
        
        # Restore original value if no improvement
        self.parameter_space.set_parameter_value(param_name, current_value)
        
        return False


class GridSearchOptimizer:
    """
    Grid search optimizer for fine-tuning parameters.
    
    Performs exhaustive search over a small parameter grid
    around the current best parameters.
    """
    
    def __init__(self, parameter_space: ParameterSpace,
                 loss_function: Callable[[Dict[str, float]], float],
                 grid_size: int = 3):
        """
        Initialize grid search optimizer.
        
        Args:
            parameter_space: Parameter space to optimize
            loss_function: Function that takes parameter dict and returns loss
            grid_size: Number of grid points per parameter (odd number)
        """
        self.parameter_space = parameter_space
        self.loss_function = loss_function
        self.grid_size = grid_size
        
        self.logger = logging.getLogger(__name__)
    
    def optimize(self, center_parameters: Dict[str, float],
                 parameters_to_optimize: List[str]) -> Dict[str, Any]:
        """
        Perform grid search optimization around center parameters.
        
        Args:
            center_parameters: Center point for grid search
            parameters_to_optimize: List of parameter names to optimize
            
        Returns:
            Optimization results
        """
        self.logger.info(f"Starting grid search optimization for {len(parameters_to_optimize)} parameters")
        
        # Generate grid points
        grid_points = self._generate_grid_points(center_parameters, parameters_to_optimize)
        
        best_loss = float('inf')
        best_parameters = center_parameters.copy()
        
        # Evaluate all grid points
        for i, grid_point in enumerate(grid_points):
            self.logger.debug(f"Evaluating grid point {i+1}/{len(grid_points)}")
            
            loss = self.loss_function(grid_point)
            
            if loss < best_loss:
                best_loss = loss
                best_parameters = grid_point.copy()
                self.logger.debug(f"  New best: loss={loss:.6f}")
        
        results = {
            'success': True,
            'grid_points_evaluated': len(grid_points),
            'initial_loss': self.loss_function(center_parameters),
            'final_loss': best_loss,
            'improvement': self.loss_function(center_parameters) - best_loss,
            'best_parameters': best_parameters
        }
        
        self.logger.info(f"Grid search complete:")
        self.logger.info(f"  Grid points: {results['grid_points_evaluated']}")
        self.logger.info(f"  Initial loss: {results['initial_loss']:.6f}")
        self.logger.info(f"  Final loss: {results['final_loss']:.6f}")
        self.logger.info(f"  Improvement: {results['improvement']:.6f}")
        
        return results
    
    def _generate_grid_points(self, center: Dict[str, float], 
                            param_names: List[str]) -> List[Dict[str, float]]:
        """Generate grid points around center parameters."""
        grid_points = []
        
        # Generate all combinations
        param_values = {}
        for param_name in param_names:
            bounds = self.parameter_space.get_parameter_bounds(param_name)
            if bounds:
                center_val = center.get(param_name, bounds.current_val)
                step = bounds.step_size
                
                # Generate grid values
                half_grid = self.grid_size // 2
                values = []
                for i in range(self.grid_size):
                    val = center_val + (i - half_grid) * step
                    val = bounds.clamp(val)
                    values.append(val)
                
                param_values[param_name] = values
        
        # Generate all combinations
        import itertools
        
        keys = list(param_values.keys())
        value_lists = [param_values[key] for key in keys]
        
        for combination in itertools.product(*value_lists):
            grid_point = center.copy()
            for key, value in zip(keys, combination):
                grid_point[key] = value
            grid_points.append(grid_point)
        
        return grid_points


def demo_optimization():
    """Demo function to test optimization algorithms."""
    
    # Create a simple loss function (parabola)
    def test_loss_function(params):
        x = params.get('test_param', 0.5)
        return (x - 0.7) ** 2 + 0.1
    
    # Create parameter space
    param_space = ParameterSpace()
    param_space.parameters['test_param'] = ParameterBounds(0.0, 1.0, 0.1, 0.5)
    
    # Test coordinate search
    optimizer = CoordinateSearchOptimizer(param_space, test_loss_function)
    results = optimizer.optimize()
    
    print(f"Coordinate search results: {results}")
    
    # Test grid search
    grid_optimizer = GridSearchOptimizer(param_space, test_loss_function)
    grid_results = grid_optimizer.optimize({'test_param': 0.5}, ['test_param'])
    
    print(f"Grid search results: {grid_results}")


if __name__ == "__main__":
    demo_optimization()

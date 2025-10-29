#!/usr/bin/env python3
"""
Symbiotic Structure Demo - Complete integration example.
Demonstrates how all modules work together to create adaptive architecture.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from datetime import datetime

from src.sacred_geometry import GoldenRatio, PlatonicSolids
from src.parametric_design import FormGenerator, StructureOptimizer
from src.environmental_simulation import SolarCalculator, LightAnalysis, WindSimulation, ThermalAnalysis
from src.organic_models import GrowthRules
from src.symbiotic_structures import AdaptiveSystem, EquilibriumCalculator


def create_symbiotic_pavilion(latitude: float = 40.7128, longitude: float = -74.0060):
    """
    Create a symbiotic pavilion that adapts to its environment.
    
    This example demonstrates the complete Mamba Architecture workflow:
    1. Sacred geometry for base proportions
    2. Parametric form generation
    3. Environmental analysis
    4. Adaptive response
    5. Equilibrium calculation
    """
    
    print("=" * 70)
    print(" MAMBA ARCHITECTURE - SYMBIOTIC PAVILION DESIGN")
    print("=" * 70)
    print(f"\nLocation: Latitude {latitude}°, Longitude {longitude}°")
    print(f"Date: Summer Solstice (June 21)")
    print()
    
    # PHASE 1: Sacred Geometry Foundation
    print("PHASE 1: Establishing Sacred Geometry Foundation")
    print("-" * 70)
    
    phi = GoldenRatio.get_phi()
    print(f"✓ Golden ratio (φ): {phi:.6f}")
    
    # Use golden ratio for structural proportions
    base_radius = 5.0  # meters
    height = base_radius * phi
    print(f"✓ Base radius: {base_radius:.2f} m")
    print(f"✓ Height: {height:.2f} m (golden ratio proportion)")
    
    # Use dodecahedron for structural inspiration (element: Ether)
    dodecahedron = PlatonicSolids.dodecahedron()
    print(f"✓ Structural inspiration: {dodecahedron['name']} ({dodecahedron['element']})")
    print(f"  {dodecahedron['num_vertices']} vertices, {dodecahedron['num_faces']} faces")
    
    # PHASE 2: Parametric Form Generation
    print(f"\nPHASE 2: Generating Parametric Form")
    print("-" * 70)
    
    # Create shell structure using golden spiral
    shell_form = FormGenerator.shell_spiral(
        a=0.2, b=0.5, turns=3, resolution=100
    )
    print(f"✓ Shell structure generated: {len(shell_form)} control points")
    
    # Optimize column spacing using golden ratio
    column_positions = StructureOptimizer.golden_ratio_proportions(
        base_dimension=base_radius * 2, elements=5
    )
    print(f"✓ Column spacing optimized: {len(column_positions)} columns")
    print(f"  Spacing pattern (m): {[f'{p:.2f}' for p in column_positions[:3]]}...")
    
    # PHASE 3: Environmental Analysis
    print(f"\nPHASE 3: Analyzing Environmental Conditions")
    print("-" * 70)
    
    # Solar analysis for summer solstice
    solar_calc = SolarCalculator()
    
    # Morning, noon, afternoon
    times = [
        datetime(2024, 6, 21, 9, 0),   # 9 AM
        datetime(2024, 6, 21, 12, 0),  # Noon
        datetime(2024, 6, 21, 15, 0),  # 3 PM
    ]
    
    sun_positions = []
    for time in times:
        pos = solar_calc.solar_position(
            latitude=latitude,
            longitude=longitude,
            date_time=time,
            timezone_offset=-5
        )
        sun_positions.append(pos)
        print(f"✓ {time.strftime('%I:%M %p')}: Altitude {pos['altitude']:.1f}°, "
              f"Azimuth {pos['azimuth']:.1f}°")
    
    # Light analysis
    print(f"\n✓ Analyzing solar irradiance on horizontal roof...")
    roof_normal = np.array([0, 0, 1])  # Horizontal surface
    noon_pos = sun_positions[1]
    
    irradiance = LightAnalysis.calculate_irradiance(
        altitude=noon_pos['altitude'],
        azimuth=noon_pos['azimuth'],
        surface_normal=roof_normal
    )
    print(f"  Solar irradiance at noon: {irradiance:.1f} W/m²")
    
    # Annual insolation estimate
    annual_insolation = LightAnalysis.annual_insolation(
        latitude=latitude,
        surface_normal=roof_normal
    )
    print(f"  Estimated annual insolation: {annual_insolation:.1f} kWh/m²/year")
    
    # Wind analysis
    print(f"\n✓ Analyzing wind conditions...")
    wind_speed = 3.5  # m/s (typical urban)
    wind_force = WindSimulation.wind_force_on_surface(
        velocity=wind_speed,
        surface_area=np.pi * base_radius**2,  # Circular roof
        drag_coefficient=1.2,
        angle=0
    )
    print(f"  Wind speed: {wind_speed} m/s")
    print(f"  Wind force on roof: {wind_force:.1f} N")
    
    # Ventilation potential
    ventilation = WindSimulation.ventilation_potential(
        opening_area=5.0,  # m²
        height_difference=height,
        wind_velocity=wind_speed,
        temperature_difference=5.0  # °C
    )
    print(f"  Natural ventilation: {ventilation['total_flow']:.2f} m³/s")
    print(f"  Air changes per hour: {ventilation['air_changes_per_hour']:.1f}")
    
    # Thermal analysis
    print(f"\n✓ Analyzing thermal performance...")
    thermal_comfort = ThermalAnalysis.thermal_comfort_pmv(
        air_temp=24,
        radiant_temp=26,
        air_velocity=ventilation['total_flow'] / 10,
        relative_humidity=60,
        metabolic_rate=1.2,
        clothing_insulation=0.5
    )
    print(f"  PMV (Predicted Mean Vote): {thermal_comfort['pmv']:.2f}")
    print(f"  PPD (Predicted Percentage Dissatisfied): {thermal_comfort['ppd']:.1f}%")
    print(f"  Comfort category: {thermal_comfort['category']}")
    
    # PHASE 4: Adaptive Response System
    print(f"\nPHASE 4: Implementing Adaptive Response")
    print("-" * 70)
    
    adaptive = AdaptiveSystem()
    
    # Current environmental state
    env_state = {
        'temperature': 26,
        'target_temp': 22,
        'thermal_mass': 2.0,
        'illuminance': irradiance * 0.8,  # Approximate lux from W/m²
        'target_illuminance': 500,
        'sun_altitude': noon_pos['altitude'],
        'wind_speed': wind_speed
    }
    
    print(f"✓ Current environmental state:")
    print(f"  Temperature: {env_state['temperature']}°C (target: {env_state['target_temp']}°C)")
    print(f"  Illuminance: {env_state['illuminance']:.0f} lux (target: {env_state['target_illuminance']} lux)")
    
    # Calculate adaptations
    adaptations = adaptive.integrated_adaptation(env_state)
    
    print(f"\n✓ Adaptive responses activated:")
    
    if 'thermal' in adaptations:
        thermal_adapt = adaptations['thermal']
        print(f"  THERMAL:")
        print(f"    - Shading adjustment: {thermal_adapt['adjust_shading']:+.2f}")
        print(f"    - Ventilation adjustment: {thermal_adapt['adjust_ventilation']:+.2f}")
        print(f"    - Thermal mass exposure: {thermal_adapt['adjust_thermal_mass_exposure']:+.2f}")
    
    if 'light' in adaptations:
        light_adapt = adaptations['light']
        print(f"  LIGHT:")
        print(f"    - Louvers angle: {light_adapt['adjust_louvers_angle']:.1f}°")
        print(f"    - Window opacity: {light_adapt['adjust_window_opacity']:.2f}")
        print(f"    - Light redirection: {light_adapt['redirect_sunlight']}")
    
    if 'wind' in adaptations:
        wind_adapt = adaptations['wind']
        print(f"  WIND:")
        print(f"    - Opening adjustment: {wind_adapt['adjust_openings']}")
        print(f"    - Deploy windbreaks: {wind_adapt['deploy_windbreaks']}")
    
    # Growth response simulation
    print(f"\n✓ Simulating phototropic growth response...")
    growth_vectors = []
    
    for i, pos in enumerate(sun_positions):
        sun_direction = np.array([
            np.cos(np.radians(pos['azimuth'])) * np.cos(np.radians(pos['altitude'])),
            np.sin(np.radians(pos['azimuth'])) * np.cos(np.radians(pos['altitude'])),
            np.sin(np.radians(pos['altitude']))
        ])
        
        growth_dir = GrowthRules.phototropism(
            current_direction=np.array([0, 0, 1]),
            light_direction=sun_direction,
            strength=0.3
        )
        growth_vectors.append(growth_dir)
        
        time_str = times[i].strftime('%I:%M %p')
        print(f"  {time_str}: Growth vector [{growth_dir[0]:+.3f}, {growth_dir[1]:+.3f}, {growth_dir[2]:+.3f}]")
    
    # PHASE 5: Equilibrium Analysis
    print(f"\nPHASE 5: Calculating System Equilibrium")
    print("-" * 70)
    
    # Energy balance
    solar_gain = irradiance * np.pi * base_radius**2 * 0.7  # 70% efficiency
    internal_gain = 500  # W (people, equipment)
    heat_loss = 800  # W (transmission + ventilation)
    
    energy_balance = EquilibriumCalculator.energy_balance(
        solar_gain=solar_gain,
        internal_gain=internal_gain,
        heat_loss=heat_loss,
        target_temp=env_state['target_temp'],
        current_temp=env_state['temperature']
    )
    
    print(f"✓ Energy balance:")
    print(f"  Solar gain: {energy_balance['total_gain']:.1f} W")
    print(f"  Heat loss: {energy_balance['heat_loss']:.1f} W")
    print(f"  Net energy: {energy_balance['net_energy']:+.1f} W")
    print(f"  Balance factor: {energy_balance['balance_factor']:.3f}")
    print(f"  System balanced: {'Yes' if energy_balance['is_balanced'] else 'No'}")
    
    # Comfort equilibrium
    comfort_eq = EquilibriumCalculator.comfort_equilibrium(
        thermal_comfort=0.8,
        visual_comfort=0.85,
        acoustic_comfort=0.75,
        air_quality=0.9
    )
    
    print(f"\n✓ Comfort equilibrium:")
    print(f"  Overall comfort: {comfort_eq['overall_comfort']:.3f}")
    print(f"  System balanced: {'Yes' if comfort_eq['is_balanced'] else 'No'}")
    print(f"  Weakest factor: {comfort_eq['weakest_factor']}")
    
    # Ecological balance
    ecological = EquilibriumCalculator.ecological_balance(
        resource_input=100,
        resource_consumption=120,
        waste_output=30,
        recycling_rate=0.6
    )
    
    print(f"\n✓ Ecological balance:")
    print(f"  Sustainability index: {ecological['sustainability_index']:.3f}")
    print(f"  Is sustainable: {'Yes' if ecological['is_sustainable'] else 'No'}")
    print(f"  Recycled resources: {ecological['recycled_resources']:.1f} units")
    
    # SUMMARY
    print("\n" + "=" * 70)
    print(" SYMBIOTIC PAVILION DESIGN COMPLETE")
    print("=" * 70)
    print(f"\n✓ Structure designed using sacred geometry (φ = {phi:.4f})")
    print(f"✓ Parametric form optimized for {len(column_positions)} support columns")
    print(f"✓ Environmental analysis complete for all conditions")
    print(f"✓ Adaptive response system operational with {len(adaptations)} subsystems")
    print(f"✓ Energy balance factor: {energy_balance['balance_factor']:.1%}")
    print(f"✓ Overall comfort: {comfort_eq['overall_comfort']:.1%}")
    print(f"✓ Sustainability index: {ecological['sustainability_index']:.1%}")
    
    print(f"\n" + "=" * 70)
    print(' "El Núcleo Mamba respira — la arquitectura evoluciona"')
    print("=" * 70)
    
    return {
        'geometry': {'phi': phi, 'base_radius': base_radius, 'height': height},
        'form': {'shell': shell_form, 'columns': column_positions},
        'environment': {'sun_positions': sun_positions, 'irradiance': irradiance},
        'adaptations': adaptations,
        'balance': energy_balance,
        'comfort': comfort_eq,
        'ecology': ecological
    }


if __name__ == '__main__':
    # Create symbiotic pavilion for New York City
    result = create_symbiotic_pavilion(latitude=40.7128, longitude=-74.0060)
    
    print(f"\nDesign data saved to result dictionary.")
    print(f"Keys: {list(result.keys())}")

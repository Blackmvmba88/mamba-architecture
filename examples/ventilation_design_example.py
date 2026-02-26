#!/usr/bin/env python3
"""
Example: Natural Ventilation Design Calculator

This example demonstrates how to calculate natural ventilation parameters
for passive cooling and air quality in buildings.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from flows.natural_flows import FlowSimulator, HeatFlow


def main():
    print("=" * 70)
    print("MAMBA ARCHITECTURE - Natural Ventilation Design")
    print("=" * 70)
    
    # Building parameters
    print("\n🏢 Building Parameters")
    print("-" * 70)
    
    building = {
        'height': 12,  # m
        'floor_area': 400,  # m²
        'volume': 1200,  # m³
        'window_area_low': 6,  # m² (ground floor)
        'window_area_high': 6,  # m² (top floor)
    }
    
    for key, value in building.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Environmental conditions
    print("\n🌡️  Environmental Conditions")
    print("-" * 70)
    
    conditions = {
        'temp_outside': 28,  # °C
        'temp_inside_desired': 26,  # °C
        'temp_inside_current': 32,  # °C
        'wind_speed': 3.5,  # m/s
        'relative_humidity': 0.6,  # 60%
    }
    
    for key, value in conditions.items():
        unit = "°C" if 'temp' in key else "m/s" if 'wind' in key else "%"
        if 'humidity' in key:
            value = value * 100
        print(f"  {key.replace('_', ' ').title()}: {value} {unit}")
    
    # Stack Effect Calculation
    print("\n" + "=" * 70)
    print("🌬️  STACK EFFECT (Buoyancy-Driven Ventilation)")
    print("=" * 70)
    
    temp_in = conditions['temp_inside_current']
    temp_out = conditions['temp_outside']
    temp_avg = (temp_in + temp_out) / 2
    height = building['height']
    
    pressure_diff = FlowSimulator.chimney_effect_pressure(
        height, temp_in, temp_out, temp_avg
    )
    
    print(f"\n📊 Stack Effect Analysis:")
    print(f"  Temperature difference: {temp_in - temp_out:.1f}°C")
    print(f"  Vertical height: {height} m")
    print(f"  Pressure difference: {pressure_diff:.2f} Pa")
    
    # Flow rate calculation
    opening_area = min(building['window_area_low'], building['window_area_high'])
    flow_rate = FlowSimulator.natural_ventilation_flow_rate(
        pressure_diff, opening_area
    )
    
    print(f"\n💨 Ventilation Flow:")
    print(f"  Effective opening area: {opening_area} m²")
    print(f"  Volumetric flow rate: {flow_rate:.2f} m³/s")
    print(f"  Flow rate per floor area: {flow_rate / building['floor_area'] * 3600:.1f} m³/(h·m²)")
    
    # Air changes per hour
    ach = (flow_rate * 3600) / building['volume']
    print(f"  Air changes per hour (ACH): {ach:.2f}")
    
    # Recommendations
    print(f"\n✓ Ventilation Assessment:")
    if ach < 3:
        assessment = "INSUFFICIENT - Increase opening size or height difference"
    elif ach < 6:
        assessment = "ADEQUATE - Meets minimum comfort standards"
    elif ach < 10:
        assessment = "GOOD - Comfortable natural ventilation"
    else:
        assessment = "EXCELLENT - High ventilation rate"
    print(f"  {assessment}")
    
    # Wind-Driven Ventilation
    print("\n" + "=" * 70)
    print("🌪️  WIND-DRIVEN VENTILATION")
    print("=" * 70)
    
    wind_speed = conditions['wind_speed']
    
    # Different wind angles
    angles = [0, 30, 45, 90]
    print(f"\n📐 Wind Pressure at Different Angles (Wind speed: {wind_speed} m/s):")
    print(f"\n{'Angle':<10} {'Cp':<8} {'Pressure (Pa)':<15} {'Effect'}")
    print("-" * 60)
    
    for angle in angles:
        cp = FlowSimulator.wind_pressure_coefficient(angle, 'rectangular')
        pressure = FlowSimulator.wind_pressure(wind_speed, cp)
        
        if angle < 45:
            effect = "Windward (positive pressure)"
        elif angle == 45:
            effect = "Transition"
        else:
            effect = "Leeward (suction)"
        
        print(f"{angle:>4}°     {cp:>6.2f}  {pressure:>12.2f}   {effect}")
    
    # Combined wind and stack effect
    print(f"\n🔄 Combined Effect:")
    wind_pressure_front = FlowSimulator.wind_pressure(wind_speed, 0.8)
    wind_pressure_back = FlowSimulator.wind_pressure(wind_speed, -0.5)
    total_wind_pressure = wind_pressure_front - wind_pressure_back
    
    combined_pressure = pressure_diff + total_wind_pressure
    combined_flow = FlowSimulator.natural_ventilation_flow_rate(
        combined_pressure, opening_area
    )
    
    print(f"  Stack effect pressure: {pressure_diff:.2f} Pa")
    print(f"  Wind pressure difference: {total_wind_pressure:.2f} Pa")
    print(f"  Combined pressure: {combined_pressure:.2f} Pa")
    print(f"  Combined flow rate: {combined_flow:.2f} m³/s")
    print(f"  Combined ACH: {(combined_flow * 3600) / building['volume']:.2f}")
    
    # Cooling Potential
    print("\n" + "=" * 70)
    print("❄️  COOLING POTENTIAL")
    print("=" * 70)
    
    # Ventilative cooling
    temp_reduction_vent = min(temp_in - temp_out, 
                               (temp_in - temp_out) * (ach / 10))
    
    print(f"\n🌬️  Ventilative Cooling:")
    print(f"  Current indoor temp: {temp_in}°C")
    print(f"  Outdoor temp: {temp_out}°C")
    print(f"  Achievable indoor temp: {temp_in - temp_reduction_vent:.1f}°C")
    
    # Evaporative cooling potential
    evap_cooling = HeatFlow.evaporative_cooling_potential(
        temp_out, conditions['relative_humidity']
    )
    
    print(f"\n💧 Evaporative Cooling Potential:")
    print(f"  Temperature reduction: {evap_cooling:.1f}°C")
    print(f"  Achievable temperature: {temp_out - evap_cooling:.1f}°C")
    
    if temp_out - evap_cooling < conditions['temp_inside_desired']:
        print(f"  ✓ Can reach desired temp ({conditions['temp_inside_desired']}°C)")
    else:
        print(f"  ⚠ Additional cooling needed for desired temp")
    
    # Design Recommendations
    print("\n" + "=" * 70)
    print("💡 DESIGN RECOMMENDATIONS")
    print("=" * 70)
    
    print("\n1. Opening Configuration:")
    
    # Calculate optimal opening sizes
    target_ach = 6
    required_flow = (target_ach * building['volume']) / 3600
    required_area = required_flow / (
        FlowSimulator.natural_ventilation_flow_rate(combined_pressure, 1.0)
    )
    
    print(f"   Target ACH: {target_ach}")
    print(f"   Current effective area: {opening_area} m²")
    print(f"   Recommended area: {required_area:.2f} m²")
    
    if required_area > opening_area:
        print(f"   ⚠ Increase opening area by {required_area - opening_area:.2f} m²")
    else:
        print(f"   ✓ Current openings are adequate")
    
    print("\n2. Vertical Configuration:")
    print(f"   Current height difference: {height} m")
    print(f"   Stack pressure: {pressure_diff:.2f} Pa")
    print("   💡 Maximize height between inlet and outlet")
    print("   💡 Place outlets at highest point possible")
    
    print("\n3. Cross-Ventilation:")
    print("   💡 Align openings with prevailing wind direction")
    print("   💡 Use larger outlets than inlets (1.25x ratio)")
    print("   💡 Minimize internal obstructions")
    
    print("\n4. Night Cooling:")
    if temp_out < temp_in - 5:
        print("   ✓ Good potential for night purge cooling")
        print("   💡 Open all windows at night")
        print("   💡 Close in morning to trap cool air")
    else:
        print("   ⚠ Limited night cooling potential")
        print("   💡 Consider thermal mass to store coolness")
    
    print("\n5. Evaporative Cooling:")
    if conditions['relative_humidity'] < 0.5:
        print("   ✓ Excellent conditions for evaporative cooling")
        print("   💡 Add water features or misting systems")
        print("   💡 Use wetted surfaces in airflow path")
    else:
        print("   ⚠ High humidity limits evaporative cooling")
        print("   💡 Focus on ventilative cooling instead")
    
    print("\n" + "=" * 70)
    print("📋 Summary:")
    print(f"  Current ACH: {ach:.2f}")
    print(f"  Combined ACH (wind + stack): {(combined_flow * 3600) / building['volume']:.2f}")
    print(f"  Cooling potential: {temp_reduction_vent + evap_cooling:.1f}°C")
    print(f"  Final achievable temp: {temp_in - temp_reduction_vent - evap_cooling:.1f}°C")
    print("=" * 70)


if __name__ == "__main__":
    main()

"""
Solar Calculator - Calculate sun position and trajectory.
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Tuple, List, Dict


class SolarCalculator:
    """Calculate solar position and angles."""
    
    @staticmethod
    def solar_declination(day_of_year: int) -> float:
        """
        Calculate solar declination angle.
        
        Args:
            day_of_year: Day number (1-365)
            
        Returns:
            Declination angle in degrees
        """
        # Cooper's equation
        declination = 23.45 * np.sin(np.radians((360/365) * (day_of_year - 81)))
        return declination
    
    @staticmethod
    def equation_of_time(day_of_year: int) -> float:
        """
        Calculate equation of time correction.
        
        Args:
            day_of_year: Day number (1-365)
            
        Returns:
            Time correction in minutes
        """
        b = (360/365) * (day_of_year - 81)
        b_rad = np.radians(b)
        
        eot = 9.87 * np.sin(2 * b_rad) - 7.53 * np.cos(b_rad) - 1.5 * np.sin(b_rad)
        return eot
    
    @staticmethod
    def solar_position(latitude: float,
                      longitude: float,
                      date_time: datetime,
                      timezone_offset: float = 0) -> Dict[str, float]:
        """
        Calculate sun position (altitude and azimuth) for given location and time.
        
        Args:
            latitude: Latitude in degrees (positive for North)
            longitude: Longitude in degrees (positive for East)
            date_time: DateTime object
            timezone_offset: Timezone offset from UTC in hours
            
        Returns:
            Dictionary with altitude, azimuth, and other solar angles
        """
        day_of_year = date_time.timetuple().tm_yday
        hour = date_time.hour + date_time.minute / 60.0
        
        # Solar declination
        declination = SolarCalculator.solar_declination(day_of_year)
        
        # Equation of time
        eot = SolarCalculator.equation_of_time(day_of_year)
        
        # Local Standard Time Meridian
        lstm = 15 * timezone_offset
        
        # Time correction factor
        tc = 4 * (longitude - lstm) + eot
        
        # Local Solar Time
        lst = hour + tc / 60
        
        # Hour angle
        hour_angle = 15 * (lst - 12)
        
        # Convert to radians
        lat_rad = np.radians(latitude)
        dec_rad = np.radians(declination)
        ha_rad = np.radians(hour_angle)
        
        # Solar altitude (elevation)
        sin_altitude = (np.sin(lat_rad) * np.sin(dec_rad) + 
                       np.cos(lat_rad) * np.cos(dec_rad) * np.cos(ha_rad))
        altitude = np.degrees(np.arcsin(sin_altitude))
        
        # Solar azimuth
        cos_azimuth = ((np.sin(dec_rad) - np.sin(lat_rad) * sin_altitude) / 
                      (np.cos(lat_rad) * np.cos(np.radians(altitude))))
        cos_azimuth = np.clip(cos_azimuth, -1, 1)
        azimuth = np.degrees(np.arccos(cos_azimuth))
        
        # Correct azimuth for afternoon
        if hour_angle > 0:
            azimuth = 360 - azimuth
        
        return {
            'altitude': altitude,
            'azimuth': azimuth,
            'declination': declination,
            'hour_angle': hour_angle,
            'is_daylight': altitude > 0
        }
    
    @staticmethod
    def sun_path(latitude: float,
                longitude: float,
                date: datetime,
                timezone_offset: float = 0,
                interval_minutes: int = 60) -> List[Dict]:
        """
        Calculate sun path for entire day.
        
        Args:
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            date: Date for sun path
            timezone_offset: Timezone offset from UTC
            interval_minutes: Time interval between points
            
        Returns:
            List of solar positions throughout the day
        """
        sun_path = []
        
        for hour in range(0, 24, interval_minutes // 60):
            for minute in range(0, 60, interval_minutes % 60 if interval_minutes < 60 else 60):
                current_time = date.replace(hour=hour, minute=minute)
                position = SolarCalculator.solar_position(
                    latitude, longitude, current_time, timezone_offset
                )
                position['time'] = current_time
                sun_path.append(position)
        
        return sun_path
    
    @staticmethod
    def annual_sun_paths(latitude: float,
                        longitude: float,
                        year: int = 2024,
                        key_days: List[int] = None) -> Dict[str, List[Dict]]:
        """
        Calculate sun paths for key days of the year.
        
        Args:
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            year: Year for calculation
            key_days: List of day numbers (default: solstices and equinoxes)
            
        Returns:
            Dictionary of sun paths for each key day
        """
        if key_days is None:
            # Default: equinoxes and solstices
            key_days = [
                80,   # Spring Equinox (≈Mar 21)
                172,  # Summer Solstice (≈Jun 21)
                266,  # Fall Equinox (≈Sep 23)
                355   # Winter Solstice (≈Dec 21)
            ]
        
        annual_paths = {}
        day_names = {
            80: 'Spring Equinox',
            172: 'Summer Solstice',
            266: 'Fall Equinox',
            355: 'Winter Solstice'
        }
        
        for day in key_days:
            date = datetime(year, 1, 1) + timedelta(days=day - 1)
            path = SolarCalculator.sun_path(latitude, longitude, date)
            day_name = day_names.get(day, f'Day {day}')
            annual_paths[day_name] = path
        
        return annual_paths
    
    @staticmethod
    def solar_noon(latitude: float,
                  longitude: float,
                  date: datetime,
                  timezone_offset: float = 0) -> datetime:
        """
        Calculate solar noon (when sun reaches highest altitude).
        
        Args:
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            date: Date for calculation
            timezone_offset: Timezone offset from UTC
            
        Returns:
            DateTime of solar noon
        """
        day_of_year = date.timetuple().tm_yday
        eot = SolarCalculator.equation_of_time(day_of_year)
        lstm = 15 * timezone_offset
        tc = 4 * (longitude - lstm) + eot
        
        solar_noon_hour = 12 - tc / 60
        hour = int(solar_noon_hour)
        minute = int((solar_noon_hour - hour) * 60)
        
        return date.replace(hour=hour, minute=minute, second=0, microsecond=0)

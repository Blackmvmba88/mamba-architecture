"""Typed conceptual architecture style catalog; aesthetic metadata, not engineering certification."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Style:
    id: str
    family: str
    geometry: str
    material_palette: tuple[str, ...]
    roof_type: str
    aperture_style: str
    light_strategy: str
    symmetry_mode: str
    biophilia_level: float
    ornament_density: float
    glazing_ratio: float
    radial_pattern_complexity: int
    ritual_center: bool = False
    water_feature: bool = False
    technical_risks: tuple[str, ...] = ()

STYLES = {
    s.id: s for s in (
        Style("sacred_dome","sacred","radial_dome",("timber","glass"),"ribbed_dome","oculus","zenith","radial",0.2,0.8,0.30,12,True,False,("radial joints","snow/wind loads","fire safety")),
        Style("geodesic_suite","organic_futurist","geodesic_shell",("timber","glass","steel"),"faceted_dome","panoramic","diffuse","radial",0.5,0.1,0.72,8,False,False,("glazing connections","overheating","egress")),
        Style("stained_glass_pavilion","sacred","circular_pavilion",("metal","stained_glass"),"ornamental_dome","arched","colored","radial",0.3,0.95,0.55,10,True,False,("thermal performance","glass safety","ventilation")),
        Style("heritage_villa","heritage","rectilinear",("brick","stone","iron"),"pitched","arched","daylight","bilateral",0.25,0.8,0.25,0,False,False,("heritage regulation","existing-structure verification")),
        Style("ceremonial_estate","heritage","courtyard",("stone","stucco","iron"),"ornate","colonnade","ambient","bilateral",0.6,1.0,0.22,0,True,True,("accessibility","crowd egress","waterproofing")),
        Style("biophilic_oasis","biophilic","courtyard",("timber","glass","stone"),"oculus","large","zenith","organic",1.0,0.15,0.50,0,False,True,("condensation","water sanitation","plant loads")),
        Style("stone_timber_rotunda","sacred","radial_dome",("stone","timber"),"ribbed_dome","arched","zenith","radial",0.45,0.40,0.15,16,True,False,("fireplace ventilation","stone lateral support","timber connections")),
    )
}

def get_style(style_id: str) -> Style:
    try:
        return STYLES[style_id]
    except KeyError as exc:
        raise ValueError(f"unknown style: {style_id}") from exc

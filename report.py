def resumen_ejecutivo(gen, trat, eficiencia, co2_evit, co2_neto):
    return f"""
Durante el período analizado se generaron **{gen/1000:.1f} toneladas** de residuos,
de las cuales **{trat/1000:.1f} toneladas** fueron valorizadas, alcanzando una
**eficiencia del {eficiencia:.1f}%**.

Las estrategias de tratamiento permitieron evitar aproximadamente
**{co2_evit/1000:.1f} toneladas de CO₂ equivalente**, contribuyendo positivamente
a los objetivos de sostenibilidad y economía circular de la organización.
"""

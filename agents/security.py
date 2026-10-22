"""Revisor de seguridad: edita aquí las instrucciones de revisión."""

from graph.state import WorkflowState
from graph.context import _ctx, _const_block, _feedback_block


INSTRUCTIONS = (
    "Eres el Revisor de seguridad del equipo. Revisa el código y los cambios "
    "propuestos con base en la evidencia disponible.\n"
    "Actividades principales:\n"
    "- Examina autenticación, autorización y controles de acceso a recursos; "
    "comprueba especialmente si una persona podría leer o modificar recursos "
    "pertenecientes a otra.\n"
    "- Revisa validación de entradas y riesgos de inyección en los límites de "
    "confianza, así como manejo de secretos y exposición de datos sensibles.\n"
    "- Para cada hallazgo, indica identificador y severidad, archivo y ubicación "
    "concreta, impacto, evidencia observada, corrección recomendada y una "
    "comprobación reproducible que permita verificar la corrección.\n"
    "- Distingue claramente los riesgos detectados, las correcciones propuestas "
    "y las verificaciones realmente ejecutadas. Marca cada comprobación como "
    "EJECUTADA con su resultado, o como PENDIENTE/NO EJECUTADA; nunca afirmes "
    "que una prueba se ejecutó si no hay evidencia de ello.\n"
    "Devuelve un informe con resumen, hallazgos respaldados por evidencia, "
    "correcciones propuestas y comprobaciones ejecutadas o pendientes. Si no "
    "hay evidencia suficiente para confirmar un riesgo, indícalo como limitación "
    "o pregunta pendiente y no lo presentes como vulnerabilidad confirmada.\n"
)


def security_node(state: WorkflowState, invoke) -> dict:
    prompt = (INSTRUCTIONS + _const_block(state, "Respeta las restricciones del proyecto y la constitución.") + "\nRepositorio: " + state["repo_name"] + "\nPlan:\n" + _ctx(state.get("out_plan", ""),2500) + "\nCódigo original:\n" + _ctx(state.get("snapshot", ""),4000) + "\nBackend:\n" + _ctx(state.get("out_backend", ""),6000) + "\nFrontend:\n" + _ctx(state.get("out_frontend", ""),6000) + _feedback_block(state) + '\nDevuelve un informe de tu rol.')
    if state.get("include_data"):
        prompt += "\nContrato aprobado de Datos y persistencia:\n" + _ctx(state.get("out_data", ""), 6000)
    return {"out_security": invoke(prompt)}

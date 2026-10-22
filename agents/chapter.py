"""Rol chapter: edita aquí sus instrucciones y entregables."""

from graph.state import WorkflowState
from graph.context import _ctx, _runs, _const_block, _ronda, _feedback_block

INSTRUCTIONS = '''Eres el Chapter del equipo, responsable de la revisión técnica del cambio.

Identifica los criterios de aceptación explícitos en el contexto, el análisis
y el plan. No inventes criterios. Contrasta cada criterio con la arquitectura,
la persistencia, la implementación, las pruebas y la seguridad. Considera los
datos y las migraciones cuando estén incluidos en los informes.

Detecta contratos incompatibles, criterios sin cobertura y hallazgos
pendientes. Sustenta cada observación con evidencia concreta de los informes o
cambios disponibles. Distingue entre información ausente, evidencia insuficiente
y una verificación que falló. No afirmes haber inspeccionado código ni ejecutado
pruebas si los informes no lo demuestran.

Organiza la revisión en estas secciones:
1. Criterios de aceptación: estado de cada criterio, evidencia y cobertura.
2. Compatibilidad: contratos incompatibles entre arquitectura, persistencia e
   implementación, o indica que no encontraste incompatibilidades.
3. Hallazgos: por cada observación indica criterio o área afectada, evidencia,
   responsable, cambio requerido y cómo verificar la corrección.
4. Observaciones anteriores: estado de cada observación previa y evidencia de
   su resolución. Las observaciones no resueltas o corregidas parcialmente
   deben volver a desarrollo; indica el cambio requerido y cómo verificarlo.
5. Pruebas pendientes: pruebas faltantes, no ejecutadas o cuyo resultado no
   está disponible.
6. Justificación del veredicto: resume la evidencia determinante.

No presentes como ejecutadas pruebas que solo se proponen. Conserva las
aprobaciones humanas: este informe es una evaluación técnica y no las concede
ni las sustituye.

Termina con una sola línea que indique exactamente uno de estos veredictos:
VEREDICTO: APROBADO
VEREDICTO: APROBADO CON OBSERVACIONES
VEREDICTO: RECHAZADO
'''


def chapter_node(state: WorkflowState, invoke) -> dict:
    """
    Revisa los cambios y emite veredicto. Si deja observaciones, quedan en
    `review_feedback` para que el dev las incorpore en la ronda siguiente.

    Usa `context` como checklist de compliance.
    Escribe en: out_chapter, review_feedback, last_verdict, approved, review_round
    """
    ronda = _ronda(state)  # esta revision incrementa el contador
    print(f"[chapter_node] Revisando cambios (ronda {ronda})...")

    prev = (
        "\nEn rondas anteriores diste observaciones. "
        "Verifica si se han incorporado correctamente.\n"
        if ronda > 1
        else ""
    )
    reports = "\n\n".join(
        f"## {label}\n{_ctx(state.get(field, ''), 6000)}"
        for field, label in (
            ("out_backend", "Backend"),
            ("out_frontend", "Frontend"),
            ("out_testing", "Pruebas"),
            ("out_security", "Seguridad"),
        )
    )

    prompt = (INSTRUCTIONS + _const_block(state, "Respeta las restricciones del proyecto y la constitución.") + "\nRepositorio: " + state["repo_name"] + "\nPlan:\n" + _ctx(state.get("out_plan", ""),1500) + "\nCambios:\n" + reports + '\nEmite VEREDICTO: APROBADO, APROBADO CON OBSERVACIONES o RECHAZADO.')
    if state.get("include_data"):
        prompt += "\nRevisa también tablas, relaciones, restricciones y migraciones de Datos y persistencia:\n" + _ctx(state.get("out_data", ""), 6000)
    salida = invoke(prompt)
    veredicto = parse_verdict(salida)

    etiqueta = {
        "aprobado": "APROBADO ✓",
        "observaciones": "APROBADO CON OBSERVACIONES",
        "rechazado": "RECHAZADO ✗",
    }[veredicto]
    print(f"[chapter_node] Ronda {ronda}: {etiqueta}")

    return {
        "out_chapter": salida,
        "review_feedback": salida,  # lo lee el dev en la ronda siguiente
        "last_verdict": veredicto,
        "approved": veredicto == "aprobado",
        "review_round": ronda,
    }


def parse_verdict(text: str) -> str:
    """
    Interpreta el veredicto de forma conservadora: si no dice claramente
    APROBADO sin observaciones, fuerza otra ronda.

    Retorna: "aprobado" | "observaciones" | "rechazado"
    """
    t = (text or "").lower()
    if "rechazado" in t or "rejected" in t:
        return "rechazado"
    if "aprobado con observaciones" in t or "approved with comments" in t:
        return "observaciones"
    if "aprobado" in t or "approved" in t:
        return "aprobado"
    return "observaciones"

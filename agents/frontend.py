"""Rol frontend: edita aquí sus instrucciones y entregables."""

from graph.state import WorkflowState
from graph.context import _ctx, _runs, _const_block, _ronda, _feedback_block


INSTRUCTIONS = 'Eres un desarrollador frontend/API senior. Realiza la tarea de tu rol.\n'


def frontend_node(state: WorkflowState, invoke) -> dict:
    """
    Implementa el recorrido de usuario definido en el plan y el contrato de API
    aprobado. Identifica campos, tipos, obligatoriedad y restricciones; no inventes
    endpoints, datos ni respuestas que el contrato no contemple.

    Incluye validaciones visibles y coherentes con el servidor, acciones claras y
    mensajes de éxito y error que no expongan detalles internos. Representa los
    estados de carga, vacío, éxito y error; bloquea envíos repetidos mientras la
    petición está pendiente y vuelve a habilitar la acción al finalizar.

    Conserva etiquetas accesibles, operación por teclado, foco visible y errores
    asociados a sus campos. Indica comprobaciones reproducibles para casos válidos,
    inválidos y respuestas de error; marca como NO EJECUTADO cualquier prueba que
    no se haya ejecutado.

    En rondas posteriores, incorpora todas las observaciones del Chapter recibidas
    mediante el feedback del backend y deja evidencia verificable de su resolución.
    Se salta si project_type no incluye frontend.
    Escribe en: out_frontend, con bloques `### ruta/archivo.ext` y código Markdown.
    """
    if not _runs(state, "frontend"):
        print("[frontend_node] project_type no incluye frontend — saltando.")
        return {}

    print(f"[frontend_node] Refactorizando frontend/API (ronda {_ronda(state)})...")

    prompt = (INSTRUCTIONS + _const_block(state, "Respeta las restricciones del proyecto y la constitución.") + "\nRepositorio: " + state["repo_name"] + "\nPlan:\n" + _ctx(state.get("out_plan", ""),2500) + "\nCódigo original:\n" + _ctx(state.get("snapshot", ""),4000) + _feedback_block(state) + '\nPara código usa ### ruta/archivo.ext seguida de un bloque markdown. ')
    return {"out_frontend": invoke(prompt)}

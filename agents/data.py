"""Datos y persistencia: perfil opcional para el equipo de siete."""
from graph.state import WorkflowState
from graph.context import _ctx, _const_block, _feedback_block

INSTRUCTIONS = (
  "Eres el responsable de Datos y persistencia. Parte de la arquitectura aprobada y del esquema, "
  "código y datos existentes; no inventes entidades, columnas ni evidencia. Define un contrato de "
  "persistencia verificable y coordínalo con Backend. Conserva los datos existentes y no ejecutes "
  "migraciones, consultas ni cambios en el repositorio.\n"
)


def data_node(state: WorkflowState, invoke) -> dict:
    prompt = (INSTRUCTIONS
              + _const_block(state, "Conserva los datos existentes y respeta el alcance del Issue.")
              + "\nRepositorio: " + state["repo_name"]
              + "\nArquitectura aprobada:\n" + _ctx(state.get("out_architect", ""), 4000)
              + "\nPlan aprobado:\n" + _ctx(state.get("out_plan", ""), 2500)
              + "\nEsquema y código existentes:\n" + _ctx(state.get("snapshot", ""), 6000)
              + _feedback_block(state)
              + "\nDevuelve el informe completo que la CLI guarda como data_report.md, con estas secciones:\n"
                "1. Entidades y diccionario: para cada entidad, enumera atributos, tipos compatibles con "
                "el motor existente, nulabilidad, valores por defecto y restricciones; indica claves "
                "primarias, claves foráneas, unicidad e índices. Expresa cardinalidades y reglas de integridad.\n"
                "2. Contrato para Backend: identifica las operaciones de persistencia implicadas por la "
                "arquitectura; especifica campos de entrada/salida, generación de identificadores, "
                "comportamiento transaccional y cómo traducir conflictos de unicidad o referencias. "
                "Backend implementa contra este contrato y no rediseña el esquema ni regenera estas migraciones.\n"
                "3. Migraciones propuestas: explica compatibilidad con los datos existentes, requisitos "
                "previos, orden de pasos (incluyendo backfill antes de imponer restricciones cuando aplique), "
                "comprobaciones posteriores y estrategia de reversión o recuperación. Evita operaciones "
                "destructivas; señala explícitamente cualquier riesgo de reversión con pérdida de datos.\n"
                "4. Verificaciones: incluye consultas o pruebas propuestas para relaciones, duplicados y "
                "valores inválidos, con resultado esperado. Distingue propuestas de ejecuciones reales y "
                "marca NO EJECUTADO todo lo que no se haya comprobado.\n"
                "5. Decisiones pendientes y evidencia: cita lo observado en arquitectura/esquema; marca "
                "supuestos y datos faltantes en vez de presentarlos como hechos. Incorpora y responde cada "
                "observación de Chapter recibida en rondas posteriores.\n"
                "Presenta cada propuesta SQL bajo una cabecera exacta ### ruta/archivo.sql seguida de un "
                "bloque de código con el dialecto del producto; incluye también las comprobaciones SQL "
                "propuestas cuando correspondan. No ejecutes SQL ni migraciones. Si no hacen falta cambios "
                "de persistencia, justifícalo con evidencia del esquema y la arquitectura.")
    return {"out_data": invoke(prompt)}

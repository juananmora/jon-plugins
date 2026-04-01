# bbva-copilot-plugins

Colección de **plugins y activos reutilizables para Copilot** orientados a BBVA ✨

Este repositorio agrupa agentes, skills, comandos e instrucciones para estandarizar tareas de ingeniería (documentación, calidad, testing, automatizaciones) en proyectos BBVA, con especial foco en APX.

## 🎯 Objetivo

- Acelerar tareas repetibles (documentación, revisiones, tests) con flujos guiados y consistentes.
- Centralizar estándares corporativos (plantillas, instrucciones, guías) para que se apliquen de forma homogénea.
- Proveer componentes listos para reutilizar como “building blocks” en nuevos repos.

## 📦 Estructura del repositorio

- `plugins/`: plugins por dominio/tecnología.
	- `apx/`: contenidos para proyectos APX (BBVA Application eXperience Platform).
		- `agents/`: agentes especializados (orquestación, generador de código, generador de documentación, calidad).
		- `skills/`: skills instalables con referencias y scripts.
		- `instructions/`: instrucciones aplicables a ficheros del repositorio consumidor.
		- `commands/`: comandos reutilizables.
		- `hooks/`: hooks/scripts auxiliares.

## 🔌 Plugins disponibles

### APX

- **Documentación**: generación y estandarización de documentación funcional/arquitectura.
- **Calidad**: guías e integración con análisis de calidad.
- **Testing**: generación/ejecución de tests unitarios con reporting.

## 🤝 Contribuir

Lee la guía en [CONTRIBUTING.md](CONTRIBUTING.md) y el [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) antes de enviar cambios.

## 📄 Licencia

MIT: ver [LICENSE](LICENSE).

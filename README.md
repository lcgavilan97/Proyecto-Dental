# Nuba Dental

Sistema de gestión de citas para clínica dental, construido con Django.

## Tecnologías

- **Backend:** Django 5.x + Django REST Framework
- **Base de datos:** MariaDB
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Interoperabilidad:** HL7 FHIR R4 (en desarrollo)

## Funcionalidades

- Gestión de pacientes (CRUD)
- Gestión de dentistas (CRUD)
- Agenda de citas con estados (pendiente/confirmada/cancelada/realizada)
- API RESTful para operaciones principales
- Panel de administración Django
- Endpoints FHIR R4 (próximamente)

## Instalación

```bash
git clone https://github.com/lcgavilan97/Proyecto-Dental.git
cd Proyecto-Dental
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # configurar credenciales BD
python manage.py migrate
python manage.py runserver
```

## Licencia

MIT

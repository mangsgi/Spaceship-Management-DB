# Pilots CRUD
from .pilots import (
    create_pilot,
    get_all_pilots,
    update_pilot,
    delete_pilot
)

# Flights CRUD
from .flights import (
    create_flight,
    get_all_flights,
    update_flight,
    delete_flight
)

# Spaceships CRUD
from .spaceships import (
    create_spaceship,
    get_all_spaceships,
    update_spaceship,
    delete_spaceship
)

# PilotFlights CRUD
from .pilot_flights import (
    create_pilot_flight,
    get_all_pilot_flights,
    update_pilot_flight,
    delete_pilot_flight
)

# MaintenanceTasks CRUD
from .maintenance_tasks import (
    create_maintenance_task,
    get_all_maintenance_tasks,
    update_maintenance_task,
    delete_maintenance_task
)

# MaintenanceRecords CRUD
from .maintenance_records import (
    create_maintenance_record,
    get_all_maintenance_records,
    update_maintenance_record,
    delete_maintenance_record
)

# Customers CRUD
from .customers import (
    create_customer,
    get_all_customers,
    update_customer,
    delete_customer
)

# Reservations CRUD
from .reservations import (
    create_reservation,
    get_all_reservations,
    update_reservation,
    delete_reservation
)

# Mechanics CRUD
from .mechanics import (
    create_mechanic,
    get_all_mechanics,
    update_mechanic,
    delete_mechanic
)

# Administrators CRUD
from .administrators import (
    create_administrator,
    get_all_administrators,
    update_administrator,
    delete_administrator
)

# UserRoles CRUD
from .user_roles import (
    create_user_role,
    get_all_user_roles,
    update_user_role,
    delete_user_role
)
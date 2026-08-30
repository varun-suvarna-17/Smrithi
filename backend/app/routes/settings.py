# NOTE: The PUT /settings/{patient_id} route that was previously here has been
# absorbed into PATCH /api/patients/{patientId} (see routes/profile.py).
# This stub is kept so existing imports don't error during migration.
# It can be deleted once no other code references it.

from fastapi import APIRouter

router = APIRouter(prefix="/settings", tags=["settings-deprecated"])

# No active endpoints. Use PATCH /api/patients/{patientId} instead.
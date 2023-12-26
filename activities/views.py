import uuid

from django.urls import reverse_lazy
from django.views.generic import ListView, FormView
from django.db import transaction

from metrics.models import ResidentActivity
from .models import Activity
from residents.models import Residency, Resident
from metrics.forms import ResidentActivityForm


# TODO: replace ActivityListView with ResidentActivityListView
class ActivityListView(ListView):
    template_name = "activities/list.html"
    queryset = Activity.objects.all()
    context_object_name = "activities"
    paginate_by = 10
    ordering = ["-date"]


class ResidentActivityFormView(FormView):
    template_name = "activities/resident_activity_form.html"
    form_class = ResidentActivityForm
    success_url = reverse_lazy("activity-list-view")

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Override the post method to add the resident activity in the same
        transaction as the activity."""
        form = self.get_form()
        is_form_valid = form.is_valid()

        if is_form_valid:
            # create a resident activity for each resident in the form
            residents_field_errors = []

            resident_ids = form.cleaned_data["residents"]

            # generate group activity ID based on current epoch time
            group_activity_id = uuid.uuid4()

            for resident_id in resident_ids:
                try:
                    resident = Resident.objects.get(id=resident_id)
                    _create_resident_activity(resident, group_activity_id, form)
                except Resident.DoesNotExist:
                    transaction.set_rollback(True)

                    error_message = f"Resident ID {resident_id} does not exist."

                    is_form_valid = False
                    residents_field_errors.append(error_message)
                except Residency.DoesNotExist:
                    transaction.set_rollback(True)

                    error_message = (
                        f"Resident {resident} is not currently residing in a home."
                    )

                    is_form_valid = False
                    residents_field_errors.append(error_message)

            if residents_field_errors:
                form.add_error("residents", residents_field_errors)

        return self.form_valid(form) if is_form_valid else self.form_invalid(form)


def _create_resident_activity(
    resident: Resident,
    group_activity_id: uuid.UUID,
    form: ResidentActivityForm,
):
    """Create a resident activity for the given resident and form."""

    try:
        residency = Residency.objects.get(
            resident=resident,
            move_out__isnull=True,
        )
    except Residency.DoesNotExist:
        raise

    home = residency.home
    activity_type = form.cleaned_data["activity_type"]
    activity_minutes = form.cleaned_data["activity_minutes"]
    caregiver_role = form.cleaned_data["caregiver_role"]
    activity_date = form.cleaned_data["activity_date"]

    resident_activity = ResidentActivity.objects.create(
        resident=resident,
        residency=residency,
        home=home,
        activity_type=activity_type,
        activity_minutes=activity_minutes,
        caregiver_role=caregiver_role,
        activity_date=activity_date,
        group_activity_id=group_activity_id,
    )

    resident_activity.save()

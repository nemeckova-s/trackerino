from django import forms

from issues.models import IssueStateChange


class IssueForm(forms.ModelForm):
    """
    Form for creating or updating an issue.
    """

    state = forms.ChoiceField(choices=IssueStateChange.State.choices)

    def get_initial_for_field(self, field: forms.Field, field_name: str):
        if field_name == 'state':
            if (
                hasattr(self.instance, 'last_state_change')
                and self.instance.last_state_change is not None
            ):
                # Current state of the issue.
                return self.instance.last_state_change.new_state
            # Default state.
            return IssueStateChange.DEFAULT_STATE
        return super(IssueForm, self).get_initial_for_field(field, field_name)

    def save(self, commit=True):
        new_state = IssueStateChange.State(self.cleaned_data['state'])
        issue = super(IssueForm, self).save(commit=commit)
        # Save the new state to the Issue instance so that
        # it is created in the `save` method on the model.
        # FIXME: This is pretty awful and needs a better solution.
        issue._set_new_state = new_state
        return issue

from django.contrib import messages
from django.views.generic import DeleteView


class BaseDeleteView(DeleteView):
    success_message = None

    def get(self, request, *args, **kwargs):
        if self.success_message is None:
            messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)

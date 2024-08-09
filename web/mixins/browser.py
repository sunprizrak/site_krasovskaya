import re


class CheckBrowserVersionMixin:

    def get_safari_version(self, user_agent):
        match = re.search(r'Version/(\d+)\.(\d+)', user_agent)

        if match:
            major_version = int(match.group(1))
            minor_version = int(match.group(2))
            return major_version, minor_version
        else:
            return 0, 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')

        if 'Safari' in user_agent and 'Chrome' not in user_agent:
            safari_version = self.get_safari_version(user_agent)
            if safari_version < (17, 2):
                context['show_update_message'] = True
            else:
                context['show_update_message'] = False
        else:
            context['show_update_message'] = False

        return context
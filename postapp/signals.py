from django.dispatch import Signal

comment_signal = Signal(use_caching=True)
post_signal = Signal(use_caching=True)

import os
import ssl

from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend
from django.utils.functional import cached_property


class CertifiEmailBackend(DjangoEmailBackend):
    """SMTP backend that uses certifi's CA bundle for TLS verification.

    This avoids depending on the OS CA store, which can cause TLS verification
    failures on some Windows + Python/OpenSSL combinations.
    """

    @cached_property
    def ssl_context(self):
        # If a corporate proxy/antivirus injects a "self-signed" root certificate,
        # certifi will *not* trust it. In that scenario, using the OS trust store
        # (Windows "Trusted Root") is the right fix.
        use_truststore = os.getenv('EMAIL_USE_OS_TRUSTSTORE', '1').strip() in {'1', 'true', 'True', 'yes', 'YES'}

        if use_truststore:
            try:
                import truststore

                truststore.inject_into_ssl()
                context = ssl.create_default_context()
            except Exception:
                context = ssl.create_default_context()
        else:
            try:
                import certifi

                context = ssl.create_default_context(cafile=certifi.where())
            except Exception:
                context = ssl.create_default_context()

        # Keep Django's behavior for optional client certs.
        if self.ssl_certfile or self.ssl_keyfile:
            context.load_cert_chain(self.ssl_certfile, self.ssl_keyfile)

        return context

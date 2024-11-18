import json
import logging
from datetime import datetime

from fastapi import Request

from app.event import Event

logger = logging.getLogger(__name__)


class AuditRecordCreator:
    """
    Class responsible for creation and holding all audit records per request.
    When middleware use audit for logging, this instance will provide all
    audit record instances that have been made during request.
    """

    def __init__(self, request: Request, application: str) -> None:
        """
        Initializing audit record creator instance. Saves request which will be
        used in all audit records during request. Creates new audit record list
        for that request.

        :param request: instance of request object. It will be used for getting
        information about current request in audit record.

        """
        self.app = application
        self.request = request
        self.audit_logger = logging.getLogger("audit")
        self._audit_record = None

    def __call__(self, event: Event) -> None:
        """
        With every call of this instance one audit record instance will be
        created and stored in list.
        List will be used for logging in audit file.

        :param event: instance of event which holds information such as
        id and type of current event
        """
        audit_record = AuditRecord(
            request=self.request,
            application=self.app,
            event=event
        )
        self._audit_record = audit_record

    @property
    def has_record(self) -> bool:
        """Returns information if audit record exists."""
        return bool(self._audit_record)

    def log_record(self, response_status: int = 200) -> None:
        """
        Goes through all audit record instances and log event into audit log.

        :param response_status: status code of response of request
        """
        try:
            self.audit_logger.info(json.dumps(
                self._audit_record.format(response_code=response_status)
            ))
        except Exception as e:
            logger.error(f"Audit logger error {str(e)}", exc_info=True)


class AuditRecord:
    """
    Single audit record entry.

    Holds information about current request (and consequently user that sent
    request), resource on which action is being performed, event that occurred
    and any additional data.

    Knows how to construct dict suitable for audit log.
    """
    def __init__(
        self, request: Request, application: str, event: Event
    ) -> None:
        """
        Creates one audit record object with provided information about request

        :param request: instance of request object. It will be used for getting
        information about current request in audit record.
        :param application: name of application.
        :param event: instance of event which holds information such as
        id and type of current event
        """
        self.app = application
        self.request = request
        self._event = event

    def format(self, response_code: int = 200) -> dict:
        """
        Formats audit record body using stored provided information about
        request, resource, event and data in audit record object.

        :param response_code: status code of response of request
        :return: formatted body of audit record
        """

        ip = self.request.client.host
        user_agent = self.request.headers.get("user-agent", "")
        url = str(self.request.url)

        if self._event is not None:
            # self.event is a tuple with event ID at index 0 and
            # event description at index 1
            event = {
                "id": self._event.id,
                "description": self._event.description,
                "success": response_code < 400,
            }
        else:
            event = {}

        return {
            "app": self.app,
            "time": datetime.utcnow().isoformat() + "Z",
            "event": event,
            "request": {
                "ip": ip,
                "user_agent": user_agent,
                "url": url,
                "method": self.request.method,
                "response": response_code,
            }
        }

from abc import ABC

from sqlalchemy.orm import joinedload

from indico.modules.events.contributions.models.contributions import Contribution
from indico.modules.events.editing.models.editable import Editable

from indico.modules.events.editing.models.revision_files import EditingRevisionFile
from indico.modules.events.editing.models.revisions import EditingRevision, InitialRevisionState

from indico.web.flask.util import url_for



class ABCExportFile(ABC):
    def _serialize_editable_revision(self, event, contribution, revision):

        editing_revision_files = EditingRevisionFile.query.with_parent(revision).all()

        return {
            "id": revision.id,
            "comment": revision.comment,
            "created_dt": revision.created_dt,
            "files": [
                self._serialize_file(event, contribution,
                                     revision, erf)
                for erf in editing_revision_files if erf.file_type.type == 1 and erf.file_type.publishable
            ]
        }

    def _serialize_file(self, event, contribution, revision, editing_revision_file):
        
        # print(editing_revision_file)
        
        file = editing_revision_file.file
        file_type = editing_revision_file.file_type

        # content_type: "application/pdf"
        # contribution_id: 2591
        # event_id: 12
        # filename: "WEP60.pdf"
        # id: 16664
        # revision_id: 5949
        # url: "http://127.0.0.1:8005/event/12/contributions/2591/editing/paper/5949/16664/WEP60.pdf"
        
        download_url = editing_revision_file.download_url
        external_download_url = editing_revision_file.external_download_url
        
        # print(download_url, external_download_url)

        # base_url = "http://127.0.0.1:8005"
        contribution_url = f"event/{event.id}/contributions/{contribution.id}"
        file_url = f"editing/paper/{revision.id}/{file.id}/{file.filename}"

        return {
            "id": file.id,
            "uuid": file.uuid,
            "filename": file.filename,
            "content_type": file.content_type,
            "file_type": {
                'type': file_type.type,
                'name': file_type.name,
                'extensions': file_type.extensions,
                'required': file_type.required,
                'publishable': file_type.publishable,
                'filename_template': file_type.filename_template
            },
            "event_id": event.id,
            "contribution_id": contribution.id,
            "revision_id": revision.id,
            
            "contribution_url": contribution_url,
            "file_url": file_url,
            
            "download_url": download_url,
            "external_download_url": external_download_url,

            # "download_url": url_for('.download_archive', event, type="paper", uuid=file.uuid), # archive_type=archive_type,
            # "external_download_url": url_for('attachments.download', filename=file.filename, _external=True)
        }

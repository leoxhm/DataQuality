from docx import Document
from report.styles import init_document_style,init_header_style,init_page_style,init_footer_style
from report.sections.TitleSection import CoverSection
from report.sections.TitleSection import SummarySection
from report.sections.TitleSection import SampleSection
from report.sections.TitleSection import FieldSection

class ReportBuilder:
    def __init__(self, ctx):
        self.ctx = ctx
        self.document = Document()
        init_document_style(self.document)
        init_page_style(self.document)
        init_header_style(self.document)
        init_footer_style(self.document)

    def build(self):

        CoverSection().render(
            self.document,
            self.ctx
        )
        SummarySection().render(
            self.document,
            self.ctx
        )

        SampleSection().render(
            self.document,
            self.ctx
        )

        FieldSection().render(
            self.document,
            self.ctx
        )

        return self.document
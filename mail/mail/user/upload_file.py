# import xlrd
# import os
# import sys
#
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# import django
# from user.models import EmailSending
#
# django.setup()
#
#
# class UploadingFile(object):
#     foreign_key_field = ['email']
#     model = EmailSending
#
#     def __init__(self, data):
#         data = data
#         self.uploaded_file = data.get('file')
#         self.parsing()
#
#     def get_related_model(self, field_name):
#         related_model = self.model._meta.get_field(field_name).rel.to
#         return related_model
#
#     def getting_headers(self):
#         s = self.s
#         headers = dict()
#         for column in range(s.ncols):
#             value = s.cell(0, column).value
#             headers[column] = value
#         return headers
#
#     def parsing(self):
#         uploaded_file = self.uploaded_file
#         wb = xlrd.open_workbook(file_contents=uploaded_file.read())
#         s = wb.sheet_by_index(0)
#         self.s = s
#
#         headers = self.getting_headers()
#
#         email_bulk_list = list()
#         for row in range(1, s.nrows):
#             row_dict = {}
#             for column in range(s.ncols):
#                 value = s.cell(row, column).value
#                 field_name = headers[column]
#
#                 if field_name == 'id' and not value:
#                     continue
#
#                 if field_name in self.foreign_key_field:
#                     related_model = self.get_related_model(field_name)
#                     instance, created = related_model.objects.get_ir_create(name=value)
#                     value = instance
#
#                 row_dict[field_name] = value
#
#             email_bulk_list.append(EmailSending(**row_dict))
#
#         EmailSending.objects.bulk_create(email_bulk_list)
#         return True

from re import match


def get_page_type(file_path):
  f = ''
  page_type = ''

  try:
    f = match(r'.*/_static/(.*)/', file_path).group(1)
  except:
    f = '/'

  if f == 'posts':
    page_type = 'blogPost'
  elif f == 'pages':
    page_type = 'brochurePage'
  else:
    page_type = 'custom'

  return page_type

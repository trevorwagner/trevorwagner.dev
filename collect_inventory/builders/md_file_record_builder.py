from datetime import datetime

from site_data_service import MDFile


def build_md_file_record(file):
  mod_time = file.stat().st_mtime

  return MDFile(
    file_path=str(file),
    mod_time=datetime.fromtimestamp(mod_time)
  )

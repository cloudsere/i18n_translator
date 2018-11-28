import os
from os.path import basename
import re
import csv
from translate import trans

resultRows = []

def write_csv(rows):
  with open("result.csv", "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["key", "中文", "英文", "代码原文"])
    writer.writerows(rows)

def get_rows(finalKey, chn, eng, origin):
  cur_row = [finalKey, chn, eng, origin]
  resultRows.append(cur_row)

def get_module_name(path):
  module_name = os.path.dirname(path).split('/')
  module_name_len = len(module_name)
  module_name = module_name[module_name_len-1][:10]
  return module_name

def get_key(module_name, eng_str):
  return ("Kani_{}_{}").format(module_name, eng_str).upper().replace('.', '').replace('-', '_').replace(' ', '_')

def extract_chinese(path):
  for file in os.listdir(path):
    current_file = os.path.join(path, file)
    if not any(value in current_file for value in (".DS_Store", "scss", "fonts", "mock", "assets", "script", "img", "protobuf")):
      if(os.path.isfile(current_file)):
        module_name = get_module_name(current_file)
        with open(current_file, "rb") as r:
          lineslist = r.readlines()
        with open(current_file, "w") as w:
          for l in lineslist:
            chn = []
            origin_l = l.decode('utf8')
            l = l.decode('utf8')

            llist = list(l)
            for char in llist:
              m = re.findall(u"[\u4e00-\u9fa5]", char)
              if len(m):
                chn.append(m[0])
              else:
                if len(chn):
                  chn_str = ''.join(chn)
                  eng_str = trans([chn_str])[0]
                  final_key = get_key(module_name, eng_str)
                  get_rows(final_key, chn_str, eng_str, origin_l)
                  l = l.replace(chn_str, 'intl("' + final_key + '")')
                  print(l)
                  chn = []
            w.write(l)
      else:
        extract_chinese(current_file)

def translator():
  directory = input("Enter the location of the files")
  path = r"%s" % directory
  extract_chinese(path)
  write_csv(resultRows)

translator()
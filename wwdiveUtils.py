
import sys
import subprocess

def run_command_with_output(cmd):
  p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  return(p.stdout.read().decode())

def get_overlays():
  overlay_list = []
  overlay_output = run_command_with_output('wwctl overlay list')
  overlay_output = overlay_output.split('\n')
  
  for i, x in enumerate(overlay_output):
    if ':' not in overlay_output[i]:
      if i > 0:
        if i < (len(overlay_output) - 1):
          overlay_list.append(overlay_output[i].split())
  
  return overlay_list

def get_overlay_files(overlay_name):
  file_list = []
  file_list_output = run_command_with_output('wwctl overlay list ' + overlay_name + ' -l')
  file_list_output = file_list_output.split('\n')
  
  for i, x in enumerate(file_list_output):
    if i > 0:
      if i < (len(file_list_output) - 1):
        file_list.append(file_list_output[i])
  
  return file_list

def get_file_content(overlay_name, file_path):
  outp = run_command_with_output('wwctl overlay show ' + overlay_name + ' ' + file_path)
  return outp

if __name__ == '__main__':
  o_list = get_overlays()
  print(o_list)



##Database=group
##project_file=string
##passfilenames

load(project_file)

setwd(LUMENS_path_user)
unlink(list.files(pattern="*"))

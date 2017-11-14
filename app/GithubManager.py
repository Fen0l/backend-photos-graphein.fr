# -*- coding: utf-8 -*-
import os, sys

from subprocess import Popen, PIPE

GITHUB['username'] = 'GitHub-photo-graphein'
GITHUB['password'] = 'Af38ghrzzefez'

class GithubWorker:
	def __init__(self):
		self.local_path = os.getcwd() + '/tmp/local_git/'
		self.tmp_local_path = os.getcwd() + '/tmp/'

		self.subprocess_path = self.tmp_local_path

		# Check if the repo is present localy
		self._is_cloned()


	def _is_cloned(self):
		if not (os.path.isdir(self.local_path)):
			print("Creating the local directory for the repository")

			self.execute("git clone https://{gh_username}:{gh_password}@github.com/GitHub-photo-graphein/Test-script.git {local_path}".
				format(local_path = self.local_path, gh_username = GITHUB['username'], gh_password = GITHUB['password']))

		# git remote add origin https://github.com/GitHub-photo-graphein/Test-script.git
		# if the repo is already present, change the subprocess path and update the repo
		self.subprocess_path = self.local_path
		self.execute("git checkout")


	def execute(self, command):
		'''
			Execute a command
		'''
		p = Popen(command.split(" "), stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self.subprocess_path)
		p.wait()
		output, err = p.communicate(b"input data that is passed to subprocess' stdin")
		rc = p.returncode

		print(output, err, rc)



	def get_folders(self):
		'''
			Return the current folder for markdowns and pictures files
		'''
		return {'markdown': self.local_path + "_posts/", 'picture': self.local_path + "assets/img/"}



# from github import Github
# from github import InputGitTreeElement

# Get the correct repository
# def _find_repo():
#     photoRepo = None
#     for repo in gh.get_user().get_repos():
#         photoRepo = repo if repo.name == "Test-script" else None;


#     return photoRepo


# # Not working for now
# def commit_gh(file_list):
#     repo = _find_repo()

#     commit_message = 'New Photo'
#     master_ref = repo.get_git_ref('heads/master')
#     master_sha = master_ref.object.sha
#     base_tree = repo.get_git_tree(master_sha)

#     # Add files
#     element_list = list()

#     #for file in [file_list[0]]:
#     for file in file_list:
#         filename = file.split("/")[-1]
#         print(filename)

#         if("markdown" in filename):
#             f = open(file, 'r')
#             contents = f.read()
#         else:
#             #with open(file, "rb") as imageFile:
#             image_handle = open(file, 'rb')
#             contents = base64.b64encode(image_handle.read())

#         f_blob = repo.create_git_blob(contents, 'utf-8')
#         path = "_posts/{}".format(filename) if ".markdown" in filename else "assets/img/{}".format(filename)
#         element = InputGitTreeElement(path=path, mode='100644', type='blob', sha=f_blob.sha)
#         element_list.append(element)

#     tree = repo.create_git_tree(element_list, base_tree)
#     parent = repo.get_git_commit(master_sha)
#     commit = repo.create_git_commit(commit_message, tree, [parent])
#     master_ref.edit(commit.sha)


#     for file in file_list:
#         filename = file.split("/")[-1]

#         if("markdown" in filename): continue
#         print(filename)

#         path = "assets/img/{}".format(filename)

#         with open(file, 'rb') as input_file:
#             data = input_file.read()

#         old_file = repo.get_contents(path)
#         commit = repo.update_file('/' + file, 'Update PNG content', data, old_file.sha)


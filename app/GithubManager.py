# -*- coding: utf-8 -*-
import os, sys

from subprocess import Popen, PIPE

class GithubWorker:
	def __init__(self, GITHUB):
		# Local path for the repository
		self.local_git_path = "/tmp/local_git/"
		self.tmp_directory = '/tmp/'
		self.repository_name = 'local_git'

		self.GITHUB = GITHUB

		# --git-dir=/path/to/my/directory/.git/ --work-tree=/path/to/my/directory/
		# --git-dir=self.git_dir --work-tree=self.work_tree
		git_dir = self.local_git_path + ".git/"
		work_tree = self.local_git_path
		self.git_dir_tree = "--git-dir={git_dir} --work-tree={work_tree}".format(git_dir = git_dir, work_tree = work_tree)

		# Check if the repo is present localy
		self._is_cloned()


	def _is_cloned(self):
		if not (os.path.isdir(self.local_git_path)):
			print("Creating the local directory for the repository")
			self.execute('pwd')
			self.execute("git clone https://{gh_username}:{gh_password}@{github_repo_url} {local_path}".
				format(github_repo_url = self.GITHUB['REPO_URL'], local_path = self.local_git_path, gh_username = self.GITHUB['username'], gh_password = self.GITHUB['password']))

		# git remote add origin https://github.com/GitHub-photo-graphein/Test-script.git
		# if the repo is already present, change the subprocess path and update the repo
		self.subprocess_path = self.local_git_path
		self.execute("git {git_dir} fetch origin master".format(git_dir = self.git_dir_tree))


	def execute(self, command):
		'''
			Execute a command
		'''
		cmd = command if isinstance(command, list) else command.split(" ")
		p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self.subprocess_path)
		sStdout, sStdErr = p.communicate()

		print("LOGGIN sStdout -> " + str(sStdout) + '\n')
		print("LOGGIN sStdErr -> " + str(sStdErr) + '\n')


	def get_folders(self):
		'''
			Return the current folder for markdowns and pictures files
		'''
		return {'markdown': self.local_git_path + "_posts/", 'picture': self.local_git_path + "assets/img/"}

	def get_local_path(self):
		return self.local_git_path


	def commit(self, photo_file, markdown_file):
		self.execute("git {git_dir} fetch".format(git_dir = self.git_dir_tree))
		self.execute('git {git_dir} add assets/img/{filename}'.format(git_dir = self.git_dir_tree, filename = photo_file))
		self.execute('git {git_dir} add _posts/{filename}'.format(git_dir = self.git_dir_tree, filename = markdown_file))
		self.execute("git {git_dir} commit -m 'Photo_upload_{filename}' --allow-empty".format(git_dir = self.git_dir_tree, filename = photo_file))
		self.execute('git {git_dir} push origin master'.format(git_dir = self.git_dir_tree))

		# subprocess.call(["git", "commit", "-m", "'{}'".format("commit message"), "--allow-empty"], shell=True)

		return True


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


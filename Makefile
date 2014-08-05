#
# This file is part of sshoot.

# sshoot is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# sshoot is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with sshoot.  If not, see <http://www.gnu.org/licenses/>.

PRJDIR = procs

all:
	python setup.py sdist bdist

clean:
	python setup.py clean
	find -type d -name  _trial_\* -exec rm -rf {} \+
	find -name \*~ -delete
	find -name \*.pyc -delete
	rm -rf MANIFEST html build dist *.egg-info

doc html:
	epydoc --no-private ${PRJDIR}

lint:
	find -name \*.py | xargs flake8 -v

.PHONY: html

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

"""A sshuttle VPN profile."""


class Profile(object):
    """Hold information about a sshuttle profile."""

    _config_attrs = (
        "remote", "subnets", "auto_hosts", "auto_nets", "dns",
        "exclude_subnets", "seed_hosts", "extra_opts")

    remote = None
    subnets = None
    auto_hosts = False
    auto_nets = False
    dns = False
    exclude_subnets = None
    seed_hosts = None
    extra_opts = None

    def __init__(self, remote=None, subnets=None):
        if not remote and not subnets:
            raise ProfileError()

        self.remote = remote
        self.subnets = subnets

    @classmethod
    def from_dict(cls, config):
        """Create a profile from a dict holding config attributes."""
        config = config.copy()  # shallow, only first-level keys are changed
        remote = config.pop("remote", None)
        subnets = config.pop("subnets", None)

        profile = Profile(remote=remote, subnets=subnets)
        for attr in cls._config_attrs:
            value = config.get(attr)
            if value is not None:
                setattr(profile, attr, value)
        return profile

    def cmdline(self, binary="sshuttle", extra_opts=None):
        """Return a sshuttle cmdline based on the profile."""
        cmd = [binary]
        if self.auto_hosts:
            cmd.append("--auto-hosts")
        if self.auto_nets:
            cmd.append("--auto-nets")
        if self.dns:
            cmd.append("--dns")
        if self.extra_opts:
            cmd.extend(self.extra_opts.split())
        if self.remote:
            cmd.append("--remote={}".format(self.remote))
        if self.subnets:
            cmd.extend(self.subnets)
        if self.exclude_subnets:
            cmd.extend(
                "--exclude={}".format(
                    subnet for subnet in self.exclude_subnets.split()))
        if self.seed_hosts:
            cmd.append("--seed-hosts={}".format(",".join(self.seed_hosts)))
        if extra_opts:
            cmd.extend(extra_opts)
        return cmd

    def config(self):
        """Return profile configuration as a dict."""
        conf = {}
        for attr in self._config_attrs:
            value = getattr(self, attr)
            if value:
                conf[attr] = value
        return dict(conf)


class ProfileError(Exception):
    """Profile configuration is not correct."""

    def __init__(self, message=None):
        if not message:
            message = "Remote host or subnets must be specified."
        super(ProfileError, self).__init__(message)

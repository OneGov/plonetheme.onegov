from ftw.upgrade import UpgradeStep


class InstallFtwLogo(UpgradeStep):
    """Install ftw.logo.
    """

    def __call__(self):
        self.setup_install_profile('profile-ftw.logo:default')
        self.install_upgrade_profile()

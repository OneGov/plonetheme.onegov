from ftw.upgrade import UpgradeStep


class RemoveLivesearchJavasciptResource(UpgradeStep):
    """Remove livesearch javascipt resource.
    """

    def __call__(self):
        self.install_upgrade_profile()

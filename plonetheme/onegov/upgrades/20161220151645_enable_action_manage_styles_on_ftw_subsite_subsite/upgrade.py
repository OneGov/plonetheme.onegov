from ftw.upgrade import UpgradeStep


class EnableActionManageStylesOnFtwSubsiteSubsite(UpgradeStep):
    """Enable action "manage_styles" on "ftw.subsite.Subsite".
    """

    def __call__(self):
        self.install_upgrade_profile()

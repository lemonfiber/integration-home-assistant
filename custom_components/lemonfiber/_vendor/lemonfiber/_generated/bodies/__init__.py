# Copyright (c) 2026 NightWorksIO
"""The request each action is posted with, and the shapes only that action carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

from . import actions_accept as _actions_accept
from . import actions_adopt as _actions_adopt
from . import actions_ask as _actions_ask
from . import actions_backup as _actions_backup
from . import actions_bandwidth as _actions_bandwidth
from . import actions_companion_pair as _actions_companion_pair
from . import actions_config_set as _actions_config_set
from . import actions_credentials_revoke as _actions_credentials_revoke
from . import actions_diagnose as _actions_diagnose
from . import actions_down as _actions_down
from . import actions_downloads_pause as _actions_downloads_pause
from . import actions_downloads_resume as _actions_downloads_resume
from . import actions_forget as _actions_forget
from . import actions_grant as _actions_grant
from . import actions_hosting_install as _actions_hosting_install
from . import actions_hosting_remove as _actions_hosting_remove
from . import actions_household_allow as _actions_household_allow
from . import actions_household_approve as _actions_household_approve
from . import actions_household_decline as _actions_household_decline
from . import actions_household_handoff as _actions_household_handoff
from . import actions_internal_certificate_replace as _actions_internal_certificate_replace
from . import actions_invite as _actions_invite
from . import actions_migrate_adopt as _actions_migrate_adopt
from . import actions_migrate_beside as _actions_migrate_beside
from . import actions_migrate_import as _actions_migrate_import
from . import actions_migrate_replace as _actions_migrate_replace
from . import actions_notify_choose as _actions_notify_choose
from . import actions_play as _actions_play
from . import actions_plugin_install as _actions_plugin_install
from . import actions_plugin_prove as _actions_plugin_prove
from . import actions_plugin_remove as _actions_plugin_remove
from . import actions_plugin_run as _actions_plugin_run
from . import actions_plugin_update as _actions_plugin_update
from . import actions_pull as _actions_pull
from . import actions_push_woken as _actions_push_woken
from . import actions_quality_reapply as _actions_quality_reapply
from . import actions_quality_set as _actions_quality_set
from . import actions_quality_upgrade as _actions_quality_upgrade
from . import actions_reissue as _actions_reissue
from . import actions_remove as _actions_remove
from . import actions_repair as _actions_repair
from . import actions_reset as _actions_reset
from . import actions_restart as _actions_restart
from . import actions_restore as _actions_restore
from . import actions_run as _actions_run
from . import actions_search as _actions_search
from . import actions_seed as _actions_seed
from . import actions_settings_clear as _actions_settings_clear
from . import actions_settings_set as _actions_settings_set
from . import actions_space as _actions_space
from . import actions_stop_seeding as _actions_stop_seeding
from . import actions_support as _actions_support
from . import actions_switch as _actions_switch
from . import actions_tune as _actions_tune
from . import actions_undo as _actions_undo
from . import actions_uninstall as _actions_uninstall
from . import actions_up as _actions_up
from . import actions_update as _actions_update
from . import actions_walkthrough as _actions_walkthrough
from . import actions_watch as _actions_watch
from . import actions_watched as _actions_watched
from . import actions_wiring_fill as _actions_wiring_fill

from .actions_accept import *
from .actions_adopt import *
from .actions_ask import *
from .actions_backup import *
from .actions_bandwidth import *
from .actions_companion_pair import *
from .actions_config_set import *
from .actions_credentials_revoke import *
from .actions_diagnose import *
from .actions_down import *
from .actions_downloads_pause import *
from .actions_downloads_resume import *
from .actions_forget import *
from .actions_grant import *
from .actions_hosting_install import *
from .actions_hosting_remove import *
from .actions_household_allow import *
from .actions_household_approve import *
from .actions_household_decline import *
from .actions_household_handoff import *
from .actions_internal_certificate_replace import *
from .actions_invite import *
from .actions_migrate_adopt import *
from .actions_migrate_beside import *
from .actions_migrate_import import *
from .actions_migrate_replace import *
from .actions_notify_choose import *
from .actions_play import *
from .actions_plugin_install import *
from .actions_plugin_prove import *
from .actions_plugin_remove import *
from .actions_plugin_run import *
from .actions_plugin_update import *
from .actions_pull import *
from .actions_push_woken import *
from .actions_quality_reapply import *
from .actions_quality_set import *
from .actions_quality_upgrade import *
from .actions_reissue import *
from .actions_remove import *
from .actions_repair import *
from .actions_reset import *
from .actions_restart import *
from .actions_restore import *
from .actions_run import *
from .actions_search import *
from .actions_seed import *
from .actions_settings_clear import *
from .actions_settings_set import *
from .actions_space import *
from .actions_stop_seeding import *
from .actions_support import *
from .actions_switch import *
from .actions_tune import *
from .actions_undo import *
from .actions_uninstall import *
from .actions_up import *
from .actions_update import *
from .actions_walkthrough import *
from .actions_watch import *
from .actions_watched import *
from .actions_wiring_fill import *

__all__: list[str] = []
__all__ += _actions_accept.__all__
__all__ += _actions_adopt.__all__
__all__ += _actions_ask.__all__
__all__ += _actions_backup.__all__
__all__ += _actions_bandwidth.__all__
__all__ += _actions_companion_pair.__all__
__all__ += _actions_config_set.__all__
__all__ += _actions_credentials_revoke.__all__
__all__ += _actions_diagnose.__all__
__all__ += _actions_down.__all__
__all__ += _actions_downloads_pause.__all__
__all__ += _actions_downloads_resume.__all__
__all__ += _actions_forget.__all__
__all__ += _actions_grant.__all__
__all__ += _actions_hosting_install.__all__
__all__ += _actions_hosting_remove.__all__
__all__ += _actions_household_allow.__all__
__all__ += _actions_household_approve.__all__
__all__ += _actions_household_decline.__all__
__all__ += _actions_household_handoff.__all__
__all__ += _actions_internal_certificate_replace.__all__
__all__ += _actions_invite.__all__
__all__ += _actions_migrate_adopt.__all__
__all__ += _actions_migrate_beside.__all__
__all__ += _actions_migrate_import.__all__
__all__ += _actions_migrate_replace.__all__
__all__ += _actions_notify_choose.__all__
__all__ += _actions_play.__all__
__all__ += _actions_plugin_install.__all__
__all__ += _actions_plugin_prove.__all__
__all__ += _actions_plugin_remove.__all__
__all__ += _actions_plugin_run.__all__
__all__ += _actions_plugin_update.__all__
__all__ += _actions_pull.__all__
__all__ += _actions_push_woken.__all__
__all__ += _actions_quality_reapply.__all__
__all__ += _actions_quality_set.__all__
__all__ += _actions_quality_upgrade.__all__
__all__ += _actions_reissue.__all__
__all__ += _actions_remove.__all__
__all__ += _actions_repair.__all__
__all__ += _actions_reset.__all__
__all__ += _actions_restart.__all__
__all__ += _actions_restore.__all__
__all__ += _actions_run.__all__
__all__ += _actions_search.__all__
__all__ += _actions_seed.__all__
__all__ += _actions_settings_clear.__all__
__all__ += _actions_settings_set.__all__
__all__ += _actions_space.__all__
__all__ += _actions_stop_seeding.__all__
__all__ += _actions_support.__all__
__all__ += _actions_switch.__all__
__all__ += _actions_tune.__all__
__all__ += _actions_undo.__all__
__all__ += _actions_uninstall.__all__
__all__ += _actions_up.__all__
__all__ += _actions_update.__all__
__all__ += _actions_walkthrough.__all__
__all__ += _actions_watch.__all__
__all__ += _actions_watched.__all__
__all__ += _actions_wiring_fill.__all__

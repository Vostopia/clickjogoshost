gevent runserver replacement
============================

Replaces the runserver command with a runserver that first monkeypatches all. This seems to be required for debugging
to work when `SUPPORT_GEVENT is enabled in pycharm <http://blog.jetbrains.com/pycharm/2012/08/gevent-debug-support/>`.

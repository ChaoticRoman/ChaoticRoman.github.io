# ANDROID

## How to delete protected packages

Some applications are not allowed to be deleted using normal uninstall process.
This is the case of e.g. Huawei Retail demo application that prevents normal use of
the phone.

1. Enter developer mode by tapping repeatedly on Build number in About the phone Settings section.
2. Allow USB debugging in the Developer Options.
3. Connect to computer, allow file transfer.
4. Install `adb` by `sudo apt install adb`.
5. Then you can list installed packages by `adb shell 'pm list packages -f'`.
6. You can then remove the package with `./adb shell 'pm uninstall -k --user 0 com.huawei.retaildemo'`.

## Huawei tricks

Interesting menu on Huawei devices is accessible by dialing `*#*#2846579#*#*`.

Huawei Retail Demo App is periodically cleaning the phone and preventing normal
use by other means. You can turn these featues off by tapping in the left upper corner
and using following password: `1122334455`. It is better to remove the app using
process described above.

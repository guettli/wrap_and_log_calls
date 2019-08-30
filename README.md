# wrap_and_log_calls

Wrapper to log all calls to a linux command

particular use case: My configuration management tool calls `/usr/bin/dpkg`. An error occurs, but unfortunately my configuration management tool 
does not show me the whole stdout/stderr. I have no clue what's wrong.

General use case: Wrap a linux command like `/usr/bin/dpkg` and write out all calls to this.

Caution: This is just for debugging. There is a heavy symlink-attack, since the log file has a fixed name in /var/tmp.

# Install

This example uses `/usr/bin/dpkg`, but any command can be wrapper. You just need to modify the python script a little bit.

```
cp -a /usr/bin/dpkg /usr/bin/dpkg-orig
ln -s wrap_and_log_calls.py /usr/bin/dpkg
```

Now run the configuration management tool.

You see the calls to `/usr/bin/dpkg` logged in `/var/tmp/dpkg-calls.log`.

The calls contain the parent processes, too.

Example:

```
Parent: python2.7 /var/tmp/.root_dcdf8c_salt/salt-call --retcode-passthrough --local --metadata --out json -l quiet -c /var/tmp/.root_dcdf8c_salt -- state.pkg /var/tmp/.root_dcdf8c_salt/salt
_state.tgz test=None pkg_sum=7683cfdcaf0ef6b6c907889fab738da83b6f897fe02387251db02a25f541e4ca hash_type=sha256
Parent: /usr/bin/apt-get -q -y -o DPkg::Options::=--force-confold -o DPkg::Options::=--force-confdef install openssl-foo-bar-user.cert
Parent: python /usr/bin/dpkg --force-confold --force-confdef --status-fd 70 --no-triggers --unpack --auto-deconfigure /var/cache/apt/archives/openssl-foo-bar-user.cert_1-2_all.deb
stdout:
(Reading database ... 365773 files and directories currently installed.)
Preparing to unpack .../openssl-foo-bar-user.cert_1-2_all.deb ...
Unpacking openssl-foo-bar-user.cert (1-2) ...


stderr:
dpkg: error processing archive /var/cache/apt/archives/openssl-foo-bar-user.cert_1-2_all.deb (--unpack):
 trying to overwrite '/etc/ssl/server/foo-bar_user.pem', which is also in package server-certificates-user 2-2.1
dpkg-deb (subprocess): decompressing archive member: lzma write error: Broken pipe
dpkg-deb: error: <decompress> subprocess returned error exit status 2
Errors were encountered while processing:
 /var/cache/apt/archives/openssl-foo-bar-user.cert_1-2_all.deb
```
# Uninstall

Important, don't forget this step!

```
rm /usr/bin/dpkg
cp -a /usr/bin/dpkg-orig /usr/bin/dpkg
```

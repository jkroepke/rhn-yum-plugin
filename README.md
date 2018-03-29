# rhn-yum-plugin
Additional YUM Plugin to successfully build docker images in a enterprise RHEL world

## How it works
The host must be registered to an spacewalk based system e.g. RedHat Satellite 5. Also a rhnd must be installed. 
The YUM Plugin used the local cached credential file from the host to 
add the authorization header to all http requests.

The method works only on plain `docker build`, not Openshift Origin. 
A RedHat patched docker daemon is also required, since volume mount
on builds work only here. See http://www.projectatomic.io/docs/docker_patches/ for more informations.


## Plain requirements
* Works only on plain `docker builds`
* ... and only on docker daemons from RedHat/Centos
* A active host subscription to a spacewalk system or RedHat Satellite 5
* a min hourly cronjob to refresh to local cached authentication file
  On our setup, we use `0 * * * * yum repolist > /dev/null`
* All repositories from the host are available on the container. If you miss
  some repositories, check the host subscriptions or run `yum repolist` to update
  the local cache.
* The docker build must be run with the arguments `-v /var/spool/up2date/loginAuth.pkl:/var/spool/up2date/loginAuth.pkl`

# Additions stuff

Good luck! RedHat Satellite 5 goes EOL in 2020! You should migrate to Satellite 6 or other open source solutions like pulp.
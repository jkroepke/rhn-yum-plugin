# rhn-yum-plugin
Additional YUM plugin to successfully build docker images in a enterprise RHEL world.

## How it works
The docker host must be registered to an spacewalk based system e.g. Red Hat Satellite 5. Also thr rhnd daemon must be installed and activated.

The YUM plugin used the local cached credential file from rhnd on the host to add http authorization header from yum.

The method works only on plain `docker build`, not Openshift. 
A RedHat patched docker daemon is also required, since volume mount
on builds work only here. See http://www.projectatomic.io/docs/docker_patches/ for more informations.


## Plain requirements
* Works only on plain `docker builds`
* ... and only on docker daemons from RedHat/Centos
* A active host subscription to a spacewalk system or Red Hat Satellite 5
* a min hourly cronjob to refresh to local cached authentication file
  On our setup, we use `0 * * * * yum repolist > /dev/null`
* All repositories from the host are available on the container. If you miss
  some repositories, check the host subscriptions or run `yum repolist` to update
  the local cache.
* The docker build must be run with the arguments `-v /var/spool/up2date/loginAuth.pkl:/var/spool/up2date/loginAuth.pkl`
* An environment variable `SPACEWALK_HOST` that contains the hostname of the spacewalk host 

# Additions stuff

Good luck! Red Hat Satellite 5 goes [EOL in 2020](https://access.redhat.com/support/policy/updates/satellite?translation-out-of-date=de)! 


You should migrate to Red Hat Satellite 6 or other open source solutions like [pulp](https://pulpproject.org/).

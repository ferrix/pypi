PyPI Cloud for Elastic Beanstalk
================================

This package is a Pyramid application that runs PyPI Cloud on AWS Elastic
Beanstalk.

History
-------

`Steven Arcangeli`__ has made this nice private PyPI server pypicloud_
that uses S3 for the file backend. That is way cool. However the docker
setup bundles a database and the settings did not come nicely from the
env.

.. __: https://github.com/stevearc/
.. _pypicloud: https://github.com/mathcamp/pypicloud/

Features
--------

* Reads RDS configuration from the environment variables
* Redirect HTTP to HTTPS with `pyramid_hsts`
* Serve static files through Apache

Use
---

Prerequisites:

* Amazon Web Services account
* A SSL certificate uploaded to be used with Elastic Loadbalancer
* S3 bucket that has granted access for an instance role used by EB

Then execute::

    git clone https://github.com/ferrix/pypi
    cd pypi
    pip install -r development.txt
    eb init -r REGION -p 'Python 2.7'
    eb create --database.engine postgres
    eb setenv ENCRYPT_KEY=<here_be_entropy> VALIDATE_KEY=<more_entropy> BUCKET_NAME=<bucket>

Then enable SSL on the ELB. To do that from the command line
run `eb config` and replace HTTPS Port on loadbalancer with 443
also, set the SSLCertificateId to the ARN of the key. Here it is
in a oneliner spell. You may need to `brew install gnu-sed` on a
Mac. Here goes::

    EDITOR="sed -i -e '/HTTPSPort/ s/OFF/443/' -e '/LoadBalancerSSLPortProtocol: HTTPS/{n;s/null/arn:aws:iam::1234567890:server-certificates\/mycert/}'" eb config

When everything is really set up, the service should answer on both
HTTP and HTTPS ports the former redirecting to the latter with gusto.
The initial run will ask the admin to register an account.

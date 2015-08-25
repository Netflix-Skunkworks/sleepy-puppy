Sleepy Puppy
============

![Sleepy Puppy](http://i.imgur.com/cngjSzb.jpg)

##What is Sleepy Puppy?##

Sleepy Puppy is a cross-site scripting (XSS) payload management framework which simplifies the ability to capture, manage, and track XSS propagation over long periods of time.


##Why Should I use Sleepy Puppy?##
Often when testing for client side injections (HTML/JS/etc.) security engineers are looking for where the injection occurs within the application they are testing *only*.  While this provides ample coverage for the application in scope, there is a possibility that the code engineers are injecting may be reflected back in a completely separate application.

Sleepy Puppy helps facilitate inter-application XSS testing by providing JavaScript payloads that callback to the Sleepy Puppy application. This allows tracking when/where a payload fires even if the execution is triggered by a different user, occurs in a different application, or happens long after the initial test was performed.

These payloads and the JavaScripts that define them are completely customizable, allowing you to capture only the information you need depending on your environment.


##How Does Sleepy Puppy Do It?##
Sleepy Puppy provides you with a number of payloads, Javascripts, and captures/collectors.  Payloads are the actual XSS strings that are used to load Sleepy Puppy Javascripts.  The JavaScripts provide a way to collect the information on the client and application where the payload was executed.  Captures and Collectors allow you to view the data you have returned from your Javascripts.  Everything is configurable and you can create your own payloads and javascripts as needed.

Testers can leverage the Sleepy Puppy Assessment model, to categorize payloads and subscribe to email notifications when delayed cross-site scripting events are triggered.

The default JavaScript we use most often generates useful capture metadata including the url, DOM with payload highlighting, user-agent, cookies, referer header, and a screenshot of the application where the payload executed.  This provides the tester ample knowledge to quickly identify what the application is so they may mitigate the vulnerability quickly.  As payloads propagate throughout a network, the tester can trace what applications the payload executes in throughout the payload’s lifecycle.

Sleepy Puppy also supports email notifications for captures received for specific assessments.

Sleepy Puppy exposes an API for users who may want to develop plugins for scanners such as Burp or Zap.

[API Documentation](https://github.com/sbehrens/sleepy-puppy/wiki/API)


#Release History#
V0.3 "Netflix OSS Release"
* Support for custom JavaScripts and JavaScript chaining with new JavaScript model
* ACE JavaScript editor integration into JavaScript models
* Created new model for collecting arbitrary data from JavaScripts (Generic Collector)
* Created new model for logging anytime a JavaScript is requested but not necessarily executed (Access Log)
* Added "Snooze" and "Run Once" option for noisy Payloads
* Updated a large number of dependencies to latest releases
* Migrated from Bootstrap2 to Bootstrap3
* Numerous UI fixes/improvements
* Improved Default JavaScript for collecting captures with better module loading
* Additional error logging has been integrated
* Better exception handling throughout the application
* New API endpoints for all new models (Javascript, Generic Collector, Access Log)
* New setup directive (setup_sleepy_puppy) creates example javascrpts, payloads, and an assessment.

V0.2 "OWASP Beta Release" - 7/9/2015
* Updated a number of third party dependencies
* Bug fixes for jQuery and Email Notifications
* Amazon S3 storage configuration is now available for screenshots
* Amazon SES email support is now available
* Allowed domains config directive allows users to whitelist which domains to log captures for
* Callback configuration settings for hostname and protocol now supported
* PEP 8 changes (thanks @monkey_security)
* manage.py now supports a new commnad 'create_bootstrap_assessment' which adds a number of example payloads and an example assessment
* Added comprehensive Wiki documentation

V0.1 Alpha - 2/26/2014
* Initial release

#Documentation#
Documentation is maintained in the Github [Wiki](https://github.com/sbehrens/sleepy-puppy/wiki)

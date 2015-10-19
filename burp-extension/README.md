Sleepy Puppy Burp Extension
===========================

Sleepy Puppy (https://github.com/Netflix/sleepy-puppy) is a cross-site scripting (XSS) payload management framework which simplifies the ability to capture, manage, and track XSS propagation over long periods of time. 

The Sleepy Puppy Burp Extension simplifies the usage of Sleepy Puppy payloads from inside the Burp Suite during a security assessment.


## Features
* Integrates with an existing Sleepy Puppy Server
* Select an existing assessment or create a new assessment
* When an Active Scan is run, the XSS payloads from the selected Sleepy Puppy Assessment get executed after Burp's in-built XSS payloads
* In Intruder, Sleepy Puppy Extension can be chosen as the payload generator for the XSS fuzzing
* In Repeater, select a value in an exsiting request and replace with Sleepy Puppy payloads using context menu
* Provides information about any payloads that have been triggered for the selected assessment 
* Create new payload from the extension

## Limitations
* Payload gets url-encoded automatically if it is not part of POST body. User might need to encode/decode as needed

## Usage
* Enable the extension in Burp
* Go to the "Sleepy Puppy" tab and enter the Sleepy Puppy Server URL and your API Key (from the adminstrator tab in Sleepy Puppy) and test connection with server
* Create a new assessment, if needed
* Select the assessment that is being conducted. This will populate the payloads for the assessment in to Burp
* Performing Active scan in Burp will automatically send Sleepy Puppy payloads
* Go to: Intruder > Payloads; Under "Payload Sets" section, click on the "Payload Type" dropdown and Extension-Generated option as the payload type; Under "Payload Options [Extension-Generated]" section, click on "Select generator..." button. In the "Select payload generator" popup window, click the "Extension payload generator" dropdown and choose the "Sleepy Puppy" option. You can now start the attack from Intruder to deliver the Sleepy Puppy payloads.
* From the Repeater window, select the value that you want to modify in the request. Right-clicking on the selected text, you will see "Sleepy Puppy Payloads" as a menu option. Navigating over the Sleepy Puppy Payloads" menu will list the payloads from the selected assessment. Clicking on a payload will replace the selected text in the request with the selected payload
* Any failure messages will be posted to the "Alerts" tab

## Installation

* Download dependencies

  Burp: [portswigger.net](https://portswigger.net/burp/download.html)

  Sleepy Puppy: [Sleepy Puppy - Netflix OSS @ Github](https://github.com/Netflix/sleepy-puppy)

  Sleepy Puppy Extension: [Sleepy Puppy Extension - Netflix OSS @ Github](https://github.com/Netflix/sleepy-puppy/burp-extension)
  

* Launch Burp

* Go to: Extender > Extensions
![Extensions Tab](https://github.com/Netflix/sleepy-puppy/burp-extension/images/burp_extensions_tab.png?raw=true)

* Click "Add"

* In the "Load Burp Extension" popup window,

** Select "Java" for "Extension type".

** Click on the "Select file..." button and choose the sleepy_puppy-<version>.jar file for "Extension file" & click on "Open".
![Extension Load](https://github.com/Netflix/sleepy-puppy/burp-extension/images/add_extension.png?raw=true)

* Click "Next" and ensure that no errors were generated.
![Successful Load](https://github.com/Netflix/sleepy-puppy/burp-extension/images/extension_loaded_without_errors.png?raw=true)

* You will see a new Burp Suite tab titled "Sleepy Puppy"
 
## Detailed Usage

* After loading the extension, navigate to the "Sleepy Puppy" tab and setup your Sleepy Puppy Server URL and your API key. **Once you enter these two pieces of information, they get persisted locally by Burp and will be automatically reloaded the next time you start Burp Suite.**
![SleepyPuppy Extension](https://github.com/Netflix/sleepy-puppy/burp-extension/images/sleepypuppy_extension.png?raw=true)

* Perform Active scanning
![Active Scanner Setup](https://github.com/Netflix/sleepy-puppy/burp-extension/images/scanner_uses_burp_payloads_followed_by_sleepypuppy_payloads.png?raw=true)
![Active Scanner Results](https://github.com/Netflix/sleepy-puppy/burp-extension/images/scanner_found_issues.png?raw=true)

* Perform Intruder Attacks
![Intruder Setup](https://github.com/Netflix/sleepy-puppy/burp-extension/images/intruder_attack_config_1.png?raw=true)
![Intruder Setup](https://github.com/Netflix/sleepy-puppy/burp-extension/images/intruder_attack_config_2.png?raw=true)
![Intruder Setup](https://github.com/Netflix/sleepy-puppy/burp-extension/images/intruder_attack_config_3.png?raw=true)
![Intruder Setup](https://github.com/Netflix/sleepy-puppy/burp-extension/images/intruder_attack_config_4.png?raw=true)
![Intruder Setup](https://github.com/Netflix/sleepy-puppy/burp-extension/images/intruder_attack_config_5.png?raw=true)
![Intruder Setup](https://github.com/Netflix/sleepy-puppy/burp-extension/images/intruder_attack_config_6.png?raw=true)
![Intruder Setup](https://github.com/Netflix/sleepy-puppy/burp-extension/images/intruder_attack_config_7.png?raw=true)
![Intruder Results](https://github.com/Netflix/sleepy-puppy/burp-extension/images/intruder_using_sleepypuppy_payloads.png?raw=true)
![Intruder Results](https://github.com/Netflix/sleepy-puppy/burp-extension/images/intruder_attacks_completed.png?raw=true)

* Modify the requests to add payload in Intruder
![Repeater Setup](https://github.com/Netflix/sleepy-puppy/burp-extension/images/repeater_request_value_to_be_replaced_with_sleepypuppy_payload.png?raw=true)
![Repeater Setup](https://github.com/Netflix/sleepy-puppy/burp-extension/images/repeater_request_value_replaced_with_sleepypuppy_payload.png?raw=true)
![Repeater Results](https://github.com/Netflix/sleepy-puppy/burp-extension/images/repeater_sent_request_with_sleepypuppy_payload.png?raw=true)

* Check the "Alerts" tab for error messages.

* Minimal information of assessment results will be fetched from Sleepy Puppy server and will be displayed in the "Sleepy Puppy" tab.

## Credits

 - @sbehrens for providing the awesome Sleepy Puppy and its API documentation
 - @rajatb & @sbehrens for testing the plugin

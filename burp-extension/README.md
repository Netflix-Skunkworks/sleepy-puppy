Sleepy Puppy Burp Extension
===========================

Sleepy Puppy (https://github.com/Netflix/sleepy-puppy) is a cross-site scripting (XSS) payload management framework which simplifies the ability to capture, manage, and track XSS propagation over long periods of time. 

The Sleepy Puppy Burp Extension simplifies the usage of Sleepy Puppy payloads from inside the Burp Suite during a security assessment.


## Features
* Integrates with an existing Sleepy Puppy Server
* Select an existing assessment or create a new assessment
* When an Active Scan is run, the XSS payloads from the selected Sleepy Puppy Assessment get executed after Burp's built-in XSS payloads
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
* Select the assessment that is being conducted. This will populate the payloads for the assessment into Burp
* Performing Active scan in Burp will automatically send Sleepy Puppy payloads
* Go to: Intruder > Payloads; Under "Payload Sets" section, click on the "Payload Type" dropdown and Extension-Generated option as the payload type; Under "Payload Options [Extension-Generated]" section, click on "Select generator..." button. In the "Select payload generator" popup window, click the "Extension payload generator" dropdown and choose the "Sleepy Puppy" option. You can now start the attack from Intruder to deliver the Sleepy Puppy payloads.
* From the Repeater window, select the value that you want to modify in the request. Right-clicking on the selected text, you will see "Sleepy Puppy Payloads" as a menu option. Navigating over the Sleepy Puppy Payloads" menu will list the payloads from the selected assessment. Clicking on a payload will replace the selected text in the request with the selected payload
* Any failure messages will be posted to the "Alerts" tab

## HTTPS Connection

* If your Sleepy Puppy server is running over HTTPS, you would need to inform the burp JVM to trust the CA that signed your Sleepy Puppy server certificate.

* There are 2 ways to do this & both involve starting burp will extra command-line properties.


#### Secure & Recommended option:

The recommended option is to import the cert from Sleepy Puppy server in to a keystore and specify the keystore location and passphrase while starting burp.

- Visit your Sleep Puppy server and export the sleepypuppy cert using firefox in pem format

- Import the cert in pem format in to a keystore with the command below.
```
keytool -import -file </path/to/cert.pem> -keystore sleepypuppy_truststore.jks -alias sleepypuppy
```
- You can specify the truststore information for the plugin in 2 ways.
  - Set truststore info as environmental variables and start burp as shown below
  ```
  export SLEEPYPUPPY_TRUSTSTORE_LOCATION=</path/to/sleepypuppy_truststore.jks>
  export SLEEPYPUPPY_TRUSTSTORE_PASSWORD=<passphrase provided while creating the truststore using keytool command above>
  java -jar burp.jar
  ```
  - Set truststore info as part of the burp startup command as shown below
  ```
  java -DSLEEPYPUPPY_TRUSTSTORE_PASSWORD=</path/to/sleepypuppy_truststore.jks> -DSLEEPYPUPPY_TRUSTSTORE_PASSWORD=<passphrase provided while creating the truststore using keytool command above> -jar burp.jar
  ```

#### Insecure option:

This option involves setting a flag for the sleepy puppy extension to trust all certs.

- Start Burp with the following command
```
java -DSLEEPYPUPPY_TRUST_ALL_CERTS=true -jar burp.jar
```

## Installation

* Download dependencies

  Burp: [portswigger.net](https://portswigger.net/burp/download.html)

  Sleepy Puppy: [Sleepy Puppy - Netflix OSS @ Github](https://github.com/Netflix/sleepy-puppy)

  Sleepy Puppy Extension: [Sleepy Puppy Extension - Netflix OSS @ Github](https://github.com/Netflix/sleepy-puppy/raw/master/burp-extension)
  

* Launch Burp

* Go to: Extender > Extensions
![Extensions Tab](https://github.com/Netflix/sleepy-puppy/raw/master/burp-extension/images/burp_extensions_tab.png)

* Click "Add"

* In the "Load Burp Extension" popup window,

  * Select "Java" for "Extension type".

  * Click on the "Select file..." button and choose the sleepy_puppy-<version>.jar file for "Extension file" & click on "Open".
![Extension Load](https://github.com/Netflix/sleepy-puppy/raw/master/burp-extension/images/add_extension.png)

* Click "Next" and ensure that no errors were generated.
![Successful Load](https://github.com/Netflix/sleepy-puppy/raw/master/burp-extension/images/extension_loaded_without_errors.png)

* You will see a new Burp Suite tab titled "Sleepy Puppy"
 
## Detailed Usage

* After loading the extension, navigate to the "Sleepy Puppy" tab and setup your Sleepy Puppy Server URL and your API key. **Once you enter these two pieces of information, they get persisted locally by Burp and will be automatically reloaded the next time you start Burp Suite.**
![SleepyPuppy Extension](https://github.com/Netflix/sleepy-puppy/raw/master/burp-extension/images/sleepypuppy_extension.png)

## Active Scanner

* When you send a host/URL for Active scanning, the Active scanner will use Sleepy Puppy payloads once the native Burp payloads are completed.
![Active Scanner Setup](https://github.com/Netflix/sleepy-puppy/raw/master/burp-extension/images/scanner_uses_burp_payloads_followed_by_sleepypuppy_payloads.png)

## Intruder Attacks

* To conduct Intruder Attacks, you would need to setup SleepyPuppy extension to be set as the payload generator. 
* In the payload type dropdown under the "Payloads Sets" section, scroll down and select the "Extension-generated" option.
![Intruder Setup](https://github.com/Netflix/sleepy-puppy/raw/master/burp-extension/images/intruder_attack_config_3.png)

* In the "Payload Options [Extension-generated]" section, click on "Select generator"
![Intruder Setup](https://github.com/Netflix/sleepy-puppy/raw/master/burp-extension/images/intruder_attack_config_4.png)

* In the "Select Payload Generator" dialog box, select "Sleepy Puppy" and click on OK.
![Intruder Setup](https://github.com/Netflix/sleepy-puppy/raw/master/burp-extension/images/intruder_attack_config_6.png)

* The Intruder is now all setup to use the payloads generated by Sleepy Puppy for the selected Assessment.
![Intruder Setup](https://github.com/Netflix/sleepy-puppy/raw/master/burp-extension/images/intruder_attack_config_7.png)

* Once the Intruder attack is completed, you can see that the payloads from Sleepy Puppy were sent as part of the attack.
![Intruder Results](https://github.com/Netflix/sleepy-puppy/raw/master/burp-extension/images/intruder_attacks_completed.png)

## Repeater Attacks

* Select the value that needs to be replaced with Sleepy Puppy Payload. When you right-click over the selected text, you will see the "Sleepy Puppy Payloads" menu option. 
![Repeater Setup](https://github.com/Netflix/sleepy-puppy/raw/master/burp-extension/images/repeater_request_value_to_be_replaced_with_sleepypuppy_payload.png)

* When you pick any of these payload, the selected text will be replaced by the selected payload.
![Repeater Setup](https://github.com/Netflix/sleepy-puppy/raw/master/burp-extension/images/repeater_request_value_replaced_with_sleepypuppy_payload.png)

* Any output or errors from the extension will be logged under the respective tab for Sleepy Puppy Burp extension.
![Output/Errors from Extension](https://github.com/Netflix/sleepy-puppy/raw/master/burp-extension/images/sleepypuppy_errors_output.png)

* Minimal information of assessment results will be fetched from Sleepy Puppy server and will be displayed in the "Sleepy Puppy" tab.

## Credits

 - [Scott Behrens](https://github.com/sbehrens) & [Patrick Kelley](https://github.com/monkeysecurity) for developing the awesome Sleepy Puppy and its API documentation
 - [Rajat Bhargava](https://github.com/rajatb) & [Scott Behrens](https://github.com/sbehrens) for testing the plugin

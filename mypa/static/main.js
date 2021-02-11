/** Global variable for Data after nlp processing*/
var responseData = [];

/** Global variable for name_list after nlp processing*/
var responseName = [];

/** Variable for available languages that the API supports*/
var langs =
[['Afrikaans',       ['af-ZA']],
 ['Bahasa Indonesia',['id-ID']],
 ['Bahasa Melayu',   ['ms-MY']],
 ['Català',          ['ca-ES']],
 ['Čeština',         ['cs-CZ']],
 ['Deutsch',         ['de-DE']],
 ['English',         ['en-AU', 'Australia'],
                     ['en-CA', 'Canada'],
                     ['en-IN', 'India'],
                     ['en-NZ', 'New Zealand'],
                     ['en-ZA', 'South Africa'],
                     ['en-GB', 'United Kingdom'],
                     ['en-US', 'United States']],
 ['Español',         ['es-AR', 'Argentina'],
                     ['es-BO', 'Bolivia'],
                     ['es-CL', 'Chile'],
                     ['es-CO', 'Colombia'],
                     ['es-CR', 'Costa Rica'],
                     ['es-EC', 'Ecuador'],
                     ['es-SV', 'El Salvador'],
                     ['es-ES', 'España'],
                     ['es-US', 'Estados Unidos'],
                     ['es-GT', 'Guatemala'],
                     ['es-HN', 'Honduras'],
                     ['es-MX', 'México'],
                     ['es-NI', 'Nicaragua'],
                     ['es-PA', 'Panamá'],
                     ['es-PY', 'Paraguay'],
                     ['es-PE', 'Perú'],
                     ['es-PR', 'Puerto Rico'],
                     ['es-DO', 'República Dominicana'],
                     ['es-UY', 'Uruguay'],
                     ['es-VE', 'Venezuela']],
 ['Euskara',         ['eu-ES']],
 ['Français',        ['fr-FR']],
 ['Galego',          ['gl-ES']],
 ['Hrvatski',        ['hr_HR']],
 ['IsiZulu',         ['zu-ZA']],
 ['Íslenska',        ['is-IS']],
 ['Italiano',        ['it-IT', 'Italia'],
                     ['it-CH', 'Svizzera']],
 ['Magyar',          ['hu-HU']],
 ['Nederlands',      ['nl-NL']],
 ['Norsk bokmål',    ['nb-NO']],
 ['Polski',          ['pl-PL']],
 ['Português',       ['pt-BR', 'Brasil'],
                     ['pt-PT', 'Portugal']],
 ['Română',          ['ro-RO']],
 ['Slovenčina',      ['sk-SK']],
 ['Suomi',           ['fi-FI']],
 ['Svenska',         ['sv-SE']],
 ['Türkçe',          ['tr-TR']],
 ['български',       ['bg-BG']],
 ['Pусский',         ['ru-RU']],
 ['Српски',          ['sr-RS']],
 ['한국어',            ['ko-KR']],
 ['中文',             ['cmn-Hans-CN', '普通话 (中国大陆)'],
                     ['cmn-Hans-HK', '普通话 (香港)'],
                     ['cmn-Hant-TW', '中文 (台灣)'],
                     ['yue-Hant-HK', '粵語 (香港)']],
 ['日本語',           ['ja-JP']],
 ['Lingua latīna',   ['la']]];

/**Creating javascript options object for selected language(recursively)*/
for (var i = 0; i < langs.length; i++) {
  select_language.options[i] = new Option(langs[i][0], i);
}

/**Variable Declaration*/
select_language.selectedIndex = 6;
updateCountry();
select_dialect.selectedIndex = 2;
showInfo('info_start');


/** Function for updating country */
function updateCountry() {
  for (var i = select_dialect.options.length - 1; i >= 0; i--) {
    select_dialect.remove(i);
  }
  var list = langs[select_language.selectedIndex];
  for (var i = 1; i < list.length; i++) {
    select_dialect.options.add(new Option(list[i][1], list[i][0]));
  }
  select_dialect.style.visibility = list[1].length == 1 ? 'hidden' : 'visible';
}

/**Variable Declaration*/
var typeData = ''
var create_email = false;
var final_transcript = '';
var recognizing = false;
var data = ''
var prev_list = ''
var recent_final_transcript=''
var c = 0
var done  = 1
var ignore_onend;
var start_timestamp;

/**Webspeech API Call*/
if (!('webkitSpeechRecognition' in window)) {
        upgrade();
} else {

        start_button.style.display = 'inline-block';

        var recognition = new webkitSpeechRecognition();


        recognition.continuous = true;
        recognition.interimResults = true;


        recognition.onstart = function() {
                recognizing = true;
                showInfo('info_speak_now');
        };


        recognition.onerror = function(event) {
                if (event.error == 'no-speech') {
//                    start_img.src = "../static/mic.gif";
                    showInfo('info_no_speech');
                    ignore_onend = true;
                }
                if (event.error == 'audio-capture') {
//                     start_img.src = "{% static 'mic.gif' %}";
                     showInfo('info_no_microphone');
                     ignore_onend = true;
                }
                if (event.error == 'not-allowed') {
                    if (event.timeStamp - start_timestamp < 100) {
                        showInfo('info_blocked');
                    } else {
                        showInfo('info_denied');
                      }
        ignore_onend = true;
                }
        };


        recognition.onend = function() {
            recognizing = false;
            if (ignore_onend) {
                return;
            }
            if (!final_transcript) {
                showInfo('info_start');
                return;
            }

            showInfo('');
            if (window.getSelection) {
                window.getSelection().removeAllRanges();
                var range = document.createRange();
                range.selectNode(document.getElementById('final_span'));
                window.getSelection().addRange(range);
            }
            if (create_email) {
                create_email = false;
                createEmail();
            }
        };

        recognition.onresult = function(event) {
            var interim_transcript = '';
            for (var i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    final_transcript += event.results[i][0].transcript;
                    recent_final_transcript = event.results[i][0].transcript;
                } else {
                    interim_transcript += event.results[i][0].transcript;
                  }
            }
            final_transcript = capitalize(final_transcript);
            recent_final_transcript = capitalize(recent_final_transcript);
            final_span.innerHTML = linebreak(final_transcript);
            interim_span.innerHTML = linebreak(interim_transcript);
            if (final_transcript || interim_transcript) {
                showButtons('inline-block');
            }
        };
}


function upgrade() {
    start_button.style.visibility = 'hidden';
    showInfo('info_upgrade');
}

/**Variable Declaration*/
var two_line = /\n\n/g;
var one_line = /\n/g;


function linebreak(s) {
    return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
}

/**Variable Declaration*/
var first_char = /\S/;


function capitalize(s) {
    return s.replace(first_char, function(m) { return m.toUpperCase(); });
}


function downloadButton() {
    if (recognizing) {
        recognizing = false;
        recognition.stop();
    }
    var downloadable = final_transcript;
    if(downloadable === ''){
        alert("Please start the meeting! Then do download");
    } else {
        var filename = "meeting"+new Date().getTime()+".txt";
        download(filename, downloadable);
      }
}


function download(filename, downloadable){
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(downloadable));
    element.setAttribute('download',filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}


function sendEmail(email_data,information_type,event_id) {
    $.ajax({
                  type: "POST",
                  dataType: "json",
                  url: '/send_email/',
                  data:{
                  'email_raw_data': email_data,
                  'information_type':information_type,
                  'event_id':event_id,
                   csrfmiddlewaretoken: '{{ csrf_token }}'
                   },
                  success: function(response) {
                       var data_response = response.data
                       console.log(data_response)
                       if (information_type == 'original')
                            alert("Original transcript succesfully emailed");
                       else if(information_type == 'nlp')
                            alert("Summary succesfully emailed");
                  },
                  error: function(result){
                  alert("Failure");
                  }
                });
}


function emailButton(event_id) {
if (recognizing) {
        create_email = true;
        recognizing = false;
        recognition.stop();
  } else {
        if(final_transcript === ''){
        alert("Please start the meeting!");
        }
    else{
        var body = encodeURI(final_transcript);
        typeData = 'original'
        sendEmail(body,typeData,event_id);
    }
    }
}


function emailButtonNLP(event_id) {
    if (recognizing) {
        create_email = true;
        recognizing = false;
        recognition.stop();
  } else {
        console.log(responseData);
        if(responseData.length <= 0){
        alert("Please wait till the NLP does some processing!");
    }
    else{
        var body = encodeURI(responseData);
        typeData = 'nlp'
        sendEmail(body, typeData,event_id);
    }
  }
}


function startButton(event) {
  if (recognizing) {
    recognition.stop();
    return;
  }
  final_transcript = '';
  recognition.lang = select_dialect.value;
  recognition.start();
  ignore_onend = false;
  final_span.innerHTML = '';
  interim_span.innerHTML = '';
  document.getElementById('nlp-span').innerHTML = '';
  document.getElementById('nlp-entity').innerHTML = '';
  showInfo('info_allow');
  start_timestamp = event.timeStamp;
}


function showInfo(s) {
    if (s) {
        for (var child = info.firstChild; child; child = child.nextSibling) {
            if (child.style) {
                child.style.display = child.id == s ? 'inline' : 'none';
            }
        }
        info.style.visibility = 'visible';
    } else {
        info.style.visibility = 'hidden';
      }
}


var current_style;


function showButtons(style) {
    if (style == current_style) {
        return;
    }
    current_style = style;
}

/**Variable Declaration*/
var targetNode = document.getElementById('final_span');


// Options for the observer (which mutations to observe)
var config = { attributes: false, childList: true, characterData: true };


// Callback function to execute when mutations are observed
var callback = function(mutationsList) {
    for(var mutation of mutationsList) {
        if (mutation.type == 'childList'){
            if ( !(prev_list == recent_final_transcript)){
                data += recent_final_transcript
                c = c+1
                if(c == 1 && done == 1){
                    done = 0
                    buffer_data = data
                    data=''
                    $.ajax({
                               type: "POST",
                               dataType: "json",
                               url: '/get_processed_data/',
                               data:{
                               'buffer_data': buffer_data,
                               csrfmiddlewaretoken: '{{ csrf_token }}'
                               },
                               success: function(response) {
                               console.log("Succesful return firm ajax call");
                               responseData.push(response.data);
                               responseName.push(response.name_list);
                               document.getElementById("nlp-span").innerHTML = document.getElementById("nlp-span").innerHTML + response.data;
                               document.getElementById("nlp-entity").innerHTML = document.getElementById("nlp-entity").innerHTML + response.name_list;
                               c = 0
                               done = 1
                    },
                    error: function(result){
                    console.log("Failure");
                    }
                    });
                }
            }
        prev_list = recent_final_transcript;
        }
    };
};


// Create an observer instance linked to the callback function
var observer = new MutationObserver(callback);


// Start observing the target node for configured mutations
observer.observe(targetNode, config);


function downloadSummary(){
    console.log(responseData);
    if(responseData.length <= 0){
        alert("Please start the meeting! Then do download");
    }
    else{
    var data = responseData;
    if (data === ''){
        alert("Please start the meeting! Then do download");
    } else {
        var filename = "summary.txt";
        download(filename, data);
      }

    }
}



var audio_context;
var recorder;
var clicked = false;

function startUserMedia(stream) {
  var input = audio_context.createMediaStreamSource(stream);


  recorder = new Recorder(input, {
                numChannels: 1
              });

}

function startRecording(button) {
  if(!clicked){
  recorder && recorder.record();


}
else{
  recorder && recorder.stop();




  // create WAV download link using audio data blob
  createDownloadLink();

  recorder.clear();
}
clicked = !clicked;
}

function createDownloadLink() {
  recorder && recorder.exportWAV(function(blob) {

  });
}

window.onload = function init() {
  try {
    // webkit shim
    window.AudioContext = window.AudioContext || window.webkitAudioContext;
    navigator.getUserMedia = ( navigator.getUserMedia ||
                     navigator.webkitGetUserMedia ||
                     navigator.mozGetUserMedia ||
                     navigator.msGetUserMedia);
    window.URL = window.URL || window.webkitURL;

    audio_context = new AudioContext;

  } catch (e) {
    alert('No web audio support in this browser!');
  }

  navigator.getUserMedia({audio: true}, startUserMedia, function(e) {

  });
};




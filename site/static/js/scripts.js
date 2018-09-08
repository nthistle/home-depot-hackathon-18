(function() {

  var width = 1090;    // set
  var height = 0;     // auto-scaled 


  var streaming = false;

  var video = null;
  var canvas = null;
  //var startbutton = null;
  var photo = null;
  var socket = null;

  function startup() {
	video = document.getElementById('video');
	canvas = document.getElementById('canvas');
	//startbutton = document.getElementById('startbutton');
	photo = document.getElementById('result');
	// socket = io.connect('http://localhost:5000');
	// socket.on('checkface_resp', function (data) {
	//   	data = JSON.parse(data);
	//   	if(data.face_present){
	// 		photo.setAttribute('src', data.image);
	//   	}
	// 	takepicture();
	//   });
	// socket.on('disconnect', function() {

	// });


	navigator.getMedia = ( navigator.getUserMedia ||
						   navigator.webkitGetUserMedia ||
						   navigator.mozGetUserMedia ||
						   navigator.msGetUserMedia);

	navigator.getMedia({video: true, audio: false},
	  function(stream) {
			var vendorURL = window.URL || window.webkitURL;
			video.src = vendorURL.createObjectURL(stream);
			video.play();
	  },
	  function(err) {
		console.log("An error occured! " + err);
	  }
	);

	video.addEventListener('canplay', function(ev){
	  if (!streaming) {
		height = video.videoHeight / (video.videoWidth/width);
	  
		video.setAttribute('width', width);
		video.setAttribute('height', height);
		canvas.setAttribute('width', width);
		canvas.setAttribute('height', height);
		streaming = true;
	  }
	}, false);

	init_picture_taking();

  }

	function init_picture_taking(){

	  if (!(height && width)){
	    setTimeout(init_picture_taking,100);
	  } else {
	    takepicture();
	  }
	}


  function takepicture() {
	var context = canvas.getContext('2d');
	if (width && height) {
	  canvas.width = width;
	  canvas.height = height;
	  context.drawImage(video, 0, 0, width, height);
	
	  var data = canvas.toDataURL('image/png');

	  sendFrame(data);

	} else {

	}
  }


  function sendFrame(frame){
	//console.log(frame);

	var xhr = new XMLHttpRequest();
	xhr.open("POST", "http://localhost:5000/checkface", true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(JSON.stringify({
		'image': frame
	}));
	xhr.onload = function() {
	  var data = JSON.parse(this.responseText);
	  console.log(data.face_present);
	  if(data.face_present){
	  	//console.log(data.image);
	  	photo.setAttribute('src', data.image);
	  }
	  takepicture();
	}

  } 


   function SCKT_sendFrame(frame){
   		console.log("SENDING DATA OUT");
        socket.emit('checkface', { 'image': frame });
  } 


  // Set up our event listener to run the startup process
  // once loading is complete.
  window.addEventListener('load', startup, false);
})();
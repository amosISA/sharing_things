// Replace all img tags with placeholders
var all = document.getElementsByClassName("ag_post_image");
for (i = all.length - 1; i >= 0; i--) {
  var newimg;
  var smallName = all[i].src;

  if(smallName.indexOf(".jpg") > -1) {
    smallName = smallName.split(".jpg");
    smallName = smallName[0] + "_thumbnail.jpg";

    (newimg = document.createElement('div'));
    newimg.className = "placeholder";
    newimg.setAttribute("data-large", all[i].src)
    newimg.innerHTML = '<img src="' + smallName + '"class="img-small"><div style="padding-bottom: 66.6%;"></div>';
    all[i].parentNode.replaceChild(newimg, all[i]);
  }
}

// Standard loading
var placeHolders = document.querySelectorAll('.placeholder');
var lowResImages = [];
var hiResImages = [];

for (i = 0; i < placeHolders.length; i++) {
  var small = placeHolders[i].querySelector('.img-small');

  lowResImages.push(small.src);
  hiResImages.push(placeHolders[i].dataset.large);
}

function loader(items, job, allDone) {
  if (!items) {
    return;
  }

  if ("undefined" === items.length) {
    items = [items];
  }

  var count = items.length;

  var jobCompleted = function(items, i) {
    count--;
    if (0 == count) {
      allDone(items);
    }
  };

  for (var i = 0; i < items.length; i++) {
    job(items, i, jobCompleted);
  }
}

function loadLowRes(items, i, onComplete) {
  var onLoad = function(e) {
    e.target.removeEventListener("load", onLoad);

    // 1: Load small image
    placeHolders[i].querySelector('.img-small').classList.add('loaded');

    onComplete(items, i);
  }
  var img = new Image();
  img.addEventListener("load", onLoad, false);
  img.src = items[i];
}

function loadHighRes(items, i, onComplete) {
  var onLoad = function(e) {
    e.target.removeEventListener("load", onLoad);

    // 2: Load large image
    var imgLarge = new Image();
    imgLarge.src = placeHolders[i].dataset.large;
    imgLarge.classList.add('loaded');
    placeHolders[i].appendChild(imgLarge);

    onComplete(items, i);
  }
  var img = new Image();
  img.addEventListener("load", onLoad, false);
  img.src = items[i];
}

loader(lowResImages, loadLowRes, function() {
  loader(hiResImages, loadHighRes, function() {
    console.log("Loaded");
  });
});
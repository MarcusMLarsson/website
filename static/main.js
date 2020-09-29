//$( document ).ready(function() {
//$("#2").hide();
//});
//import VideoBg from './node_modules/vue-videobg/src/VideoBackground.vue'
//import VideoBg from 'vue-videobg'
//Vue.component('video-bg', VideoBg)
//import Vue from 'vue';
// @ts-ignore
//import VideoBackground from 'C:/Users/mla/Dev/cfehome/Flask/static/node_modules/vue-responsive-video-background-player/src/VideoBackground.vue'
//const VideoBackground = require('./vue-responsive-video-background-player');
//import VideoBackground from './node_modules/vue-responsive-video-background-player/src/index'
//const VideoBackground = require('./node_modules/vue-responsive-video-background-player/src/index');

//./components/VideoPlayer

//Vue.component('video-background', VideoBackground);

//new Vue({
//   el: '#app',
//  vuetify: new Vuetify(),
// delimiters: ['[[', ']]'],
//mounted: function() {
// this.$refs.videoRef.src = "http://127.0.0.1:5000/static/roadster-loop-imperial.mp4";
//this.$refs.videoRef.play();
// },
//data: () => ({
//items: [
// { title: 'Click Me', link: '<a class="dropdown-item" href="/energy">Energy</a>' },
// { title: 'Click Me', link: '<a class="dropdown-item" href="/energy">Energy</a>'},
// { title: 'Click Me', link: '<a class="dropdown-item" href="/energy">Energy</a>' },
// { title: 'Click Me 2', link: '<a class="dropdown-item" href="/energy">Energy</a>' },
//],
//drawer: false,

//}),
//});

//var two = new Vue({
//el: '#app1',
//components: { VideoBg }
//});

$(document).ready(function () {
    document.getElementsByTagName("html")[0].style.visibility = "visible";
});

$("div[name=USCrude]").hide();
$("div[name=OECDInventory]").hide();
$("div[name=OECDCrude]").hide();

$("div[name=USInventory_no_spr]").hide();
$("div[name=USCrude_no_spr]").hide();
$("div[name=OECDInventory_no_spr]").hide();
$("div[name=OECDCrude_no_spr]").hide();

$("input").change(() => {
    const first = $("input[name=FirstSelector]:checked").val();
    const second = $("input[name=SecondSelector]:checked").val();
    const third = $("input[name=ThirdSelector]:checked").val();
    $("div[name=USInventory]").toggle(
        first === "btnUS" && second === "btnInventory" && third === "btnIncSPR"
    );
    $("div[name=USCrude]").toggle(
        first === "btnUS" && second === "btnCrude" && third === "btnIncSPR"
    );
    $("div[name=OECDInventory]").toggle(
        first === "btnOECD" && second === "btnInventory" && third === "btnIncSPR"
    );
    $("div[name=OECDCrude]").toggle(
        first === "btnOECD" && second === "btnCrude" && third === "btnIncSPR"
    );
    $("div[name=USInventory_no_spr]").toggle(
        first === "btnUS" && second === "btnInventory" && third === "btnExlSPR"
    );
    $("div[name=USCrude_no_spr]").toggle(
        first === "btnUS" && second === "btnCrude" && third === "btnExlSPR"
    );
    $("div[name=OECDInventory_no_spr]").toggle(
        first === "btnOECD" && second === "btnInventory" && third === "btnExlSPR"
    );
    $("div[name=OECDCrude_no_spr]").toggle(
        first === "btnOECD" && second === "btnCrude" && third === "btnExlSPR"
    );
});

/*$("#btnUS, #btnInventory").click(function () {
  $("#USInventory").show();
  
  $("#OECDInventory").hide();
  $("#USCrude").hide();
  $("#OECDCrude").hide();
});


$("#btnUS, #btnCrude").click(function () {
  $("#USCrude").show();
  
  $("#OECDInventory").hide();
  $("#USInventory").hide();
  $("#OECDCrude").hide();
});


$("#btnOECD, #btnInventory").click(function () {
  $("#OECDInventory").show();
  
  $("#USInventory").hide();
  $("#USCrude").hide();
  $("#OECDCrude").hide();
});

$("#btnOECD, #btnCrude").click(function () {
  $("#OECDCrude").show();
  
  $("#OECDInventory").hide();
  $("#USInventory").hide();
  $("#USCrude").hide();
}); */

$(document).ready(function () {
    $("table tbody tr td").on("click", function () {
        $(this).closest("table").find("td").css({
            backgroundColor: "",
            border: "",
        });
        $(this).css({
            backgroundColor: "rgba(255, 65, 54, 0.2)",
            border: "1px solid hotpink",
        });
    });
});

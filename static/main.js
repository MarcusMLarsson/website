$(document).ready(function () {
    document.getElementsByTagName("html")[0].style.visibility = "visible";
});

window.onload = check;
function check() {
    document.getElementById("r01").checked = true;
}


$("div[name=USCrude]").hide();
$("div[name=OECDInventory]").hide();
$("div[name=OECDCrude]").hide();

$("div[name=USInventory_no_spr]").hide();
$("div[name=USCrude_no_spr]").hide();
$("div[name=OECDInventory_no_spr]").hide();
$("div[name=OECDCrude_no_spr]").hide();
$("div[name=OECD]").hide();

$("input").change(() => {
    const first = $("input[name=FirstSelector]:checked").val();
    const second = $("input[name=SecondSelector]:checked").val();
    const third = $("input[name=ThirdSelector]:checked").val();
    $("div[name=US]").toggle(first === "btnUS");
    $("div[name=OECD]").toggle(first === "btnOECD");
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

window.onresize = function () {
    Plotly.relayout("bargraph1", {
        "xaxis.autorange": true,
        "yaxis.autorange": true,
    });
    Plotly.relayout("bargraph2", {
        "xaxis.autorange": true,
        "yaxis.autorange": true,
    });
    Plotly.relayout("bargraph3", {
        "xaxis.autorange": true,
        "yaxis.autorange": true,
    });
    Plotly.relayout("bargraph4", {
        "xaxis.autorange": true,
        "yaxis.autorange": true,
    });
    Plotly.relayout("bargraph5", {
        "xaxis.autorange": true,
        "yaxis.autorange": true,
    });
    Plotly.relayout("bargraph6", {
        "xaxis.autorange": true,
        "yaxis.autorange": true,
    });
    Plotly.relayout("bargraph7", {
        "xaxis.autorange": true,
        "yaxis.autorange": true,
    });
    Plotly.relayout("bargraph8", {
        "xaxis.autorange": true,
        "yaxis.autorange": true,
    });
    Plotly.relayout("bargraph9", {
        "xaxis.autorange": true,
        "yaxis.autorange": true,
    });
    Plotly.relayout("bargraph10", {
        "xaxis.autorange": true,
        "yaxis.autorange": true,
    });
    Plotly.relayout("bargraph11", {
        "xaxis.autorange": true,
        "yaxis.autorange": true,
    });
};

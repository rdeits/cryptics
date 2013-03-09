var SAMPLE_CLUES = [["Spin broken shingle (7)", "ENGLISH"],
                    ["Be aware of nerd's flip-flop (4) k...", "KNOW"],
                    ["Stirs, spilling soda (4) .d..", "ADOS"],
                    ["Lee's horse galloping to dangerous_coasts (3,6) l.....r..", "LEE_SHORES"],
                    ["Bottomless sea, stormy sea - waters' surface rises_and_falls (7) s.es...", "SEESAWS"]];
var SERVER = "http://cryptic-solver.appspot.com/solve/";

function solve_clue(clue_text) {
    $("#solution").html("<img src='/static/img/loading.gif' alt='loading' />");
    var request = $.ajax({type: 'GET',
        url: "http://localhost:8080/solve/" + encodeURIComponent(clue_text),
        dataType: "html"});
    request.done(function (html) {$("#solution").html(html);});
    request.fail(function () {$("#solution").html("Sorry, I couldn't contact the server. You may want to try this again later");});
}

$(function() {
    var sample_html = "";
    for (var i = 0; i < SAMPLE_CLUES.length; i++) {
        sample_html += '<a href="javascript:void(0)" ' + "onclick='solve_clue(SAMPLE_CLUES[" + i + "][0]);'>" + SAMPLE_CLUES[i][0] + "</a><br>" + SAMPLE_CLUES[i][1] + "<br>";
        // sample_html += "<a href='" + SERVER + encodeURIComponent(SAMPLE_CLUES[i][0]) + "'>" + SAMPLE_CLUES[i][0] + "</a><br>" + SAMPLE_CLUES[i][1] + "<br>";
    }
    $("#sample_clues").html(sample_html);
    $("#clue_form").submit(function () {
        solve_clue($("#clue_text").val());
        return false;});
    // solve_clue("Spin broken shingle (7)");
});

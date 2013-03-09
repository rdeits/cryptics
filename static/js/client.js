var SAMPLE_CLUES = [["Spin broken shingle (7)", "ENGLISH"],
                    ["Be aware of nerd's flip-flop (4) k...", "KNOW"],
                    ["Stirs, spilling soda (4) .d..", "ADOS"],
                    ["Lee's horse galloping to dangerous_coasts (3,6) l.....r..", "LEE_SHORES"],
                    ["Bottomless sea, stormy sea - waters' surface rises_and_falls (7) s.es...", "SEESAWS"]];

function solve_clue(clue_text) {
    $("#solution").html("<img src='/static/img/loading.gif' alt='loading' />");
    $("#clue_text").val(clue_text);
    var request = $.ajax({type: 'GET',
        url: SERVER + encodeURIComponent(clue_text),
        dataType: "html"});
    request.done(function (html) {
        $("#solution").html(html);
        // $("#answers a").click(function (evt) {
        //     var target_id = "#" + evt.target.href.split("#").pop();
        //     $(target_id).css("color", "#2222gg");
        // });
    });
    request.fail(function () {$("#solution").html("Sorry, I couldn't contact the server. You may want to try this again later");});
}

function wrap_sample(i) {
    return '<div class="sample"><div class="sample_button"><input type="button" onclick="solve_clue(SAMPLE_CLUES[' + i + '][0])" value="Try it"/></div><div class="clue_ans_labels"><u>Clue:</u><br><u>Answer:</u></div><div class="sample_clue_ans">' + SAMPLE_CLUES[i][0] + "<br>" + SAMPLE_CLUES[i][1] + "</div></div>";
}

$(function() {
    var sample_html = "";
    for (var i = 0; i < SAMPLE_CLUES.length; i++) {
        sample_html += wrap_sample(i);
    }
    $("#sample_clues").html(sample_html);
    $("#clue_form").submit(function () {
        solve_clue($("#clue_text").val());
        return false;});
});

/**
 * Created by senorrift on 7/31/15.
 */

function getBackgroundColor(slideValue) {
    var colorCodes = ["#f5f5f5", "#dcdcdc", "#c4c4c4", "#ababab", "#939393",
        "#7a7a7a", "#626262", "#494949", "#313131", "#181818"];
    return colorCodes[slideValue - 1]
}

function getHeaderText(dataSelected) {
    switch (dataSelected) {
        case "chm":
            return 'Chicken v. Human v. Mouse';
            break;
        case "hco":
            return "Human v. Chimpanzee v. Orangutan";
            break;
        case "roc":
            return "Brassica rapa/B. oleraceae TO1000/B. oleraceae var.capitata";
            break;
        default:
            return 'Visualization Text Not Specified';
    }
}

$(document).ready( function() {
    /* Halt scrolling when controlling visualization. */
    $('#canvas').hover( function() {
        $("body").css("overflow", "hidden")
    }, function() {
        $("body").css("overflow", "scroll")
    });

    /* Change Background Color w/ Slider */
    var renderDiv = $("#rendering");
    var bg_slider = $("#bgslider");
    renderDiv.css('background-color', getBackgroundColor(bg_slider.val()));
    bg_slider.change( function() {
        var color = getBackgroundColor(bg_slider.val());
        renderDiv.css('background-color', color);
    });

    /* Change Header Description w/ Selection */
    var headerSpan = $("#current_demo");
    var selector = $("#dataset_select");
    headerSpan.html( getHeaderText(selector.val()) );
    selector.change( function() {
        headerSpan.html( getHeaderText(selector.val()) );
    })
});
$(document).ready(function(){
$(".fancybox").fancybox({
    openEffect: "none",
    closeEffect: "none"
    });
})

$(document).ready(function() {
    $('.select-basic-single').select2();
});

function submitFertilizerForm() {
        document.getElementById('fertilizer-form').submit();
}

function submitPesticideForm() {
        document.getElementById('pesticide-form').submit();
}
(function () {
    //?}) jquery plugin
    var joinus = $('.stasticjoin');
    var login = $('.stasticlogin');
    var containter = $('.sliding');
    var slidingloin = $('.information');
    var slidingsignup = $('.information-signup');

    joinus.on('click', function () {
        slidingloin.css('display', 'none');
        slidingsignup.css('display', 'initial');

        containter.animate({ left: "35%" }, 350); //easeOutBack?????

    });

    login.on('click', function () {
        //slidingloin.css('display', 'none');
        //slidingsignup.css('display', 'initial');

        slidingloin.css('display', 'initial');
        slidingsignup.css('display', 'none');

        containter.animate({left: "65%"},350);
    });

})();
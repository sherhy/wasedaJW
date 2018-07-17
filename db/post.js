// Example using HTTP POST operation

// "use strict";
console.log("running");
var page = require('webpage').create(),
	server = "https://www.wsl.waseda.jp/syllabus/JAA101.php?pLng=en",
	data = 'p_gakubu=212004';

console.log("opening page");

page.open(server, 'post', data, function (status) {
	// console.log("page opened");
	if (status !== 'success') {
		// console.log('Unable to post!');
		phantom.exit(1);
		return;	
	}

	// console.log("preevaluation");
	page.evaluate( function () {
		func_search('JAA103SubCon');
	});

	setTimeout( function() {
		page.evaluate( function () {
			func_showchg('JAA103SubCon', '1000'); //try '100' -> '1000'
		});

		setTimeout(function () {
			console.log(page.content);
			phantom.exit();
		}, 5000);		
	}, 5000);
});
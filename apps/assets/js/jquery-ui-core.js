$(document).ready(function() {
	$("#search-icon").css({'opacity' : 0.25 });
	$("#search-bar").toggle();
	$("#dropdownmenu").toggle();
	$("#toggle-search").click(function(){
		$("#search-bar").slideToggle();
 	});

	$("#dropdown-area").hover(function(){
		$("#dropdownmenu").slideDown('normal').show();
	}, function(){
		$("#dropdownmenu").slideUp('normal');
	});

	$("#search-icon").hover(function(){
		$(this).css({'opacity' : 1 });
	}, function(){
		$(this).css({'opacity' : 0.25 });
	});
});
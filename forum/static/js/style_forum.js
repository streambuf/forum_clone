
jQuery(document).ready(function() {



	// не изменять скролл при обновлении
	if( window.location.hash ) { // just in case there is no hash
        $(document.body).animate({
            'scrollTop':   $( window.location.hash ).offset().top
        }, 2000);
		}

	// фокусироваться в конце текста
	(function($){
    $.fn.focusTextToEnd = function(){
        this.focus();
        var $thisVal = this.val();
        this.val('').val($thisVal);
        return this;
    }
	}(jQuery));

	// показать окно ответа
	$(".show_comment_link").click(function(e){
		e.preventDefault();
		var username = $(this).closest('.answer_item').find('.a_profile').html() + ", ";
		$(this).closest('.answer_item').find("textarea").val(username);
		$(this).closest('.answer_item').find('.reply').slideToggle(400);
		$(this).closest('.answer_item').find("textarea").focusTextToEnd();
		$(this).html($(this).text() == 'Закрыть' ? 'Ответить' : 'Закрыть');
	});

	// ответ
	$('.answer').click(function() {
		var ans = $(this).closest('.answer_item').find("textarea").val();
		if (ans == '') {
			$('.replay_error').html("Ответ не должен быть пустым!");
			$(".alert").slideDown("slow").delay(4500).slideUp("slow");
			return;
		}
		if (ans.length > 2000) {
			$('.replay_error').html("Максимальная длина сообщения - 2000 символов!");
			$(".alert").slideDown("slow").delay(4500).slideUp("slow");
			return;
		}
		$.ajax({
			url: "/forum/replay/",
			method: "POST",
			data:  {
			ans: ans,
			url: window.location.pathname,
			},
		dataType: "json"
		}).done(function(data){
			if (data.status == 1) {
				location.reload();

			} else {
				$('.replay_error').html(data.error);
				$(".alert").slideDown("slow").delay(4500).slideUp("slow");
			}
		})
	});

	// id выбранного подфорума
	var id = 0;

	// показать окно авторизации
	$('#button_login').click(function() {
		$("#form_new_topic").hide();
		$("#form_login").show();
		$("#myModalLabel").html("Авторизация");
		$("#login").show();
		$("#create").hide();
	});

	// показать окно создания топика
	$('#new_topic').click(function() {
		$("#form_login").hide();
		$("#form_new_topic").show();
		$("#myModalLabel").html("Создать новую тему");
		$("#login").hide();
		$("#create").show();
	});

	// обработчик выбора категории при создании топика
	$('.choose_cat').click(function(e) {
		e.preventDefault()
		id = $(this).attr("href");
		$("#cat").html($(this).text());

	});

	// создание топика
	$('#create').click(function() {
		var category_id = 1;
		var title = $("#title").val();
		var answer = $("#ans").val();

		if (id == 0) {
			$('#label_error').html("Выберите подфорум!");
			$("#error_info").slideDown("slow").delay(4500).slideUp("slow");
			return;
		} else {
			category_id = id;
		}

		if (title == '') {
			$('#label_error').html("Заголовок не должен быть пустым!");
			$("#error_info").slideDown("slow").delay(4500).slideUp("slow");
			return;
		}
		if (title.length > 120) {
			$('#label_error').html("Максимальная длина заголовка - 120 символов!");
			$("#error_info").slideDown("slow").delay(4500).slideUp("slow");
			return;
		}

		if (answer == '') {
			$('#label_error').html("Сообщение не должно быть пустым!");
			$("#error_info").slideDown("slow").delay(4500).slideUp("slow");
			return;
		}
		if (answer.length > 2000) {
			$('#label_error').html("Максимальная длина сообщения - 2000 символов!");
			$("#error_info").slideDown("slow").delay(4500).slideUp("slow");
			return;
		}

		$.ajax({
			url: "/forum/new_topic/",
			method: "POST",
			data:  {
			answer: answer,
			title: title,
			category_id: id,

			},
		dataType: "json"
		}).done(function(data){
			if (data.status == 1) {
				location.reload();
			} else {
				$('#label_error').html(data.error);
				$("#error_info").slideDown("slow").delay(4500).slideUp("slow");
			}
		})
	});

	// авторизация
	$('#login').click(function() {
		var username = $("#username").val();
		var password = $("#password").val();
		if (username == '' || password == '') {
			text_error = (username == '')?'Заполните поле "Имя пользователя"':'Заполните поле "Пароль"'
			$('#form_error').html(text_error);
			$("#error_content").slideDown("slow").delay(4500).slideUp("slow");
			$("#login").slideUp("slow").delay(5000).slideDown("slow");
			return;
		}
		$.ajax({
			url: "/forum/login/",
			method: "POST",
			data:  {
			username: username,
			password: password
			},
		dataType: "json"
		}).done(function(data){
			if (data.status == 1) {
				$('#form_success').html(data.hello);
				$("#success_content").slideDown("slow");
				setTimeout(function(){
				  $('#myModal').modal('hide');
				}, 2000);

				$('#sign').hide("slow");
				$('#nav_username').html(data.username);
				$('#nav_username').attr('href', '#');
				$('#out').show("slow");
				$('.show_comment_link').show();
				$('.span_time').show();


			} else {
				$('#form_error').html(data.error);
				$("#error_content").slideDown("slow").delay(4500).slideUp("slow");
				$("#login").slideUp("slow").delay(5000).slideDown("slow");
			}
		})
		.fail(function(){

		});
	});

	// проверка занятости имени при авторизации
	$('#username').focusout(function() {

	    var username = $(this).val();

		if (username == '') {
			$("#login_exists").hide();
			return;
		}
		$.ajax({
			url: "/forum/login_out/",
			method: "POST",
			data:  {
			username: username,
            csrfmiddlewaretoken: '{{ csrf_token }}',
			},
		dataType: "json"
		}).done(function(data){
			if (data.status == 1) {
				if (data.user_exists == 0) {
					$("#login_exists").hide().html("Это имя свободно").removeClass("label-warning").addClass("label-success").slideDown();
				} else {
					$("#login_exists").hide().html("Это имя занятно").removeClass("label-success").addClass("label-warning").slideDown();
				}
			}
		})
		.fail(function(){

		});
	});



});



<!DOCTYPE html>
<html class="no-js" lang="pt-PT"><!--manifest="/static/main.manifest"-->
  <head>
    <meta charset="utf-8">
    <title>{{title}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="ERP +">
    <meta name="author" content="António Anacleto">

    <!-- Le styles -->
    <link href="/static/css/normalize.css" rel="stylesheet">
    <link href="/static/css/foundation.min.css" rel="stylesheet">
    <link href="/static/css/foundation-icons.css" rel="stylesheet">

    <style type="text/css">

    </style>

    <link rel="shortcut icon" href="/static/{{favicon}}"/>

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="/static/js/html5.js"></script>
    <![endif]-->

  </head>

  <body>

  <div data-alert  id="message_container" style="display:none" class="alert-box info radius">
    <div id="message" style="color:black;"></div>
    <a href="#" class="close">&times;</a>
  </div>

<div class="container large-12 columns">
&nbsp;
</br>
</br>
</div>

  <div class="container large-13 columns"><!-- /container -->

    <div class="large-5 columns" style="text-align:center;">&nbsp;</div>
    <div class="small-12 medium-12 large-3 columns" style="text-align:center;">
    	<img src="/static/logos/logo100x100.png"></img>
      <img src="/static/{{logotipo}}" width="100"></img>

      <form id="loginForm">
        <h2>Autenticação</h2>
        <input name="window_id" type="hidden" id="window_id" value="{{window_id}}"><!---->
        <input type="text" id="login" name="login" placeholder="Utilizador" autocomplete="on" autofocus tabindex="1">
        <input type="password" id="password" name="password" placeholder="Palavra Passe" autocomplete="off">
        <input type="password" id="new_password" name="new_password" placeholder="Nova Palavra Passe" style="display:none;">
        <input type="password" id="confirm_password" name= "confirm_password" placeholder="Confirma Palavra Passe" style="display:none;">
        <ul class="button-group">
          <li>
            <a href="#" class="button radius small" onclick="login_func();">Autenticar</a>
          </li>
          <li>
            <a href="#" class="button radius small" id="show_change_pass_btn" onclick="show_new_pass();">Muda Password</a>
          </li>
          <li>
            <a href="#" class="button radius small" id="change_pass_btn" onclick="change_pass_func();" style="display:none;">Muda Password</a>
          </li>
        </ul>

      </form>
    </div>
    <div class="large-5 columns" style="text-align:center;">&nbsp;</div>
    <div id="content"></div>
    </div> <!-- /container -->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="/static/js/jquery.min.js"></script>
    <script src="/static/js/modernizr.js"></script>
    <script src="/static/js/foundation.min.js"></script>
  	<script type="text/javascript">

        $(document).foundation();

        $('#password').keypress(function( event ) {
        if ( event.which == 13 ){
            event.preventDefault();
            login_func();
          }
        });

  		function login_func() {
  			$.ajax({
  						type: 'POST',
  						url: "/login",
  						data: $('#loginForm').serialize()
					}).success(function(r) {
                                          window.location = r;
					}).error(function(r) {
						$('#message_container').removeClass('info').removeClass('success').addClass('alert');
						$('#message_container').show();
						$('#message').html(r.responseText);
						$('#password').val('');
					});
				};

        function showMessage(type, message, id, container) {
            switch(type){
                case 'alert':
                    container.removeClass('success').removeClass('info').removeClass('warning').addClass('alert');
                    container.show();
                    id.html(message);
                    break;
                case 'warning':
                    container.removeClass('success').removeClass('info').removeClass('alert').addClass('warning');
                    container.show();
                    id.html(message);
                    break;
                case 'success':
                    container.removeClass('alert').removeClass('info').removeClass('warning').addClass('success');
                    container.show();
                    id.html(message);
                    break;
                default:
                    /*means its info*/
                    container.removeClass('success').removeClass('alert').removeClass('warning').addClass('info');
                    container.show();
                    id.html(message);
                    break;
            };
        container.delay(3000).slideUp();
        };

		function show_new_pass() {
			$("#new_password").show();
			$("#confirm_password").show();
			$("#show_change_pass_btn").hide();
			$("#change_pass_btn").show();
		};


		function change_pass_func() {
  			$.ajax({
  						type: 'POST',
  						url: "/change_pass",
  						data: $('#loginForm').serialize()
					}).success(function(r) {
						$('#message_container').removeClass('info').removeClass('alert').addClass('success');
  						$('#message_container').show();
						$('#message').html(r);
						$("#new_password").hide();
						$("#confirm_password").hide();
						$("#show_change_pass_btn").show();
						$("#change_pass_btn").hide();
						$('#password').val('');
					}).error(function(r) {
						showMessage('alert', r.responseText, $('#message'), $('#message_container'));
					});
				};

      function get_new_window_id(){
        $('#message').html('');
        var strURL = '/get_new_window_id/' + window.name + '_' + $('#window_id').val();
        $.ajax({type: 'POST', url: strURL
            }).done(function(r) {
                if (!(window.name)) {
                  window.name = r;
                };
            }).fail(function(r) {
                showMessage('alert', r.responseText, $('#message'), $('#message_container'));
            });
        };

      get_new_window_id();

      $('#window_id').val(window.name);

	</script>
  </body>
</html>

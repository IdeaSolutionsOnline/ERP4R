% setdefault('favicon', '')
%setdefault('title','')
%setdefault('playlist','')
%setdefault('playlistsize','')
<!doctype html>
<html class="no-js" lang="pt">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{{title}}</title>
        <link rel="stylesheet" href="/static/css/largefoundation.css" />
        <link rel="stylesheet" href="/static/css/gap.css" />
        <link rel="shortcut icon" href="/static/{{favicon}}">
    </head>
    <body>
            <div class="large-7 medium-8 columns">
                <br> <br>
                <br>
                <div class="row">
                    <div class="large-6 columns">
                        <div id="titulos" class="panel">
                            <pre class="frist">Serviço</pre>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div id="titulos" class="panel">
                            <pre class="frist">Senha</pre>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div id="titulos" class="panel">
                            <pre class="frist">Balcão</pre>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="large-6 columns">
                        <div id="tituloColuna" class="callout1 panel">
                            <pre id="service1" class="frist"></pre>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div class="callout2 panel">
                            <pre id="ticket1" class="second"></pre>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div class="callout2 panel">
                            <pre id="counter1" class="second"></pre>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="large-6 columns" >
                        <div class="callout1 panel" id="tituloColuna">
                            <pre id="service2" class="frist"></pre>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div class="callout2 panel">
                            <pre id="ticket2" class="second"></pre>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div class="callout2 panel">
                            <pre id="counter2"  class="second"></pre>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="large-6 columns">
                        <div class="callout1 panel" id="tituloColuna">
                            <pre id="service3" class="frist"></pre>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div  class="callout2 panel">
                            <pre id="ticket3" class="second"></pre>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div class="callout2 panel">
                            <pre id="counter3" class="second"></pre>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="large-6 columns">
                        <div class="callout1 panel" id="tituloColuna">
                            <pre id="service4" class="frist"></pre>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div class="callout2 panel">
                            <pre id="ticket4" class="second"></pre>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div  class="callout2 panel">
                            <pre id="counter4" class="second"></pre>
                        </div>
                    </div>
                </div>
            </div>
            <div class="large-5 columns">
                <br><br>
                <br>
                <div class="flex-video widescreen vimeo">
                    <video id="Videotv" width="520" height="500"  autoplay controls>
                </video>
                <img id="Imagetv" width="520" height="500">
                </div>
                 <!-- Player Controler helpers -->
                 <input  name="nextmultimedia"  id="nextmultimedia" type="hidden" value="0" ></input>
                 <input  name="playlistsize"  id="playlistsize" type="hidden" value="{{!playlistsize}}" ></input>
                 <input  name="playlist"  id="playlist" type="hidden" value="{{!playlist}}" ></input>
                 <input  name="currentTime"  id="currentTime" type="hidden" value="00:00:00" ></input>
                 <input  name="targetTime"  id="targetTime" type="hidden" value="00:00:00" ></input>
                 <!-- weather widget -->
                 <a href="http://www.accuweather.com/pt/cv/praia/55657/weather-forecast/55657" class="aw-widget-legal">
                 </a>
                 <div  id="time_widget" class="aw-widget-current"  data-locationkey="" data-unit="c" data-language="pt" data-useip="true" data-uid="awcc1430244570514">
                 </div>
                 <a href="http://time.is/Cape_Verde" id="time_is_link" rel="nofollow" style="font-size:36px; "></a>
                <span id="Cape_Verde_z503" style="font-size:45px; float: right;  font-weight: bold; "></span>
                <audio id="audiotv"  preload="auto"></audio>
        </div>
        <div class="large-12 columns">
                <br>
                <div  id="RodapeNoticias" class="callout2 panel"  style="position: relative; border: solid;background-color:  #e3f2fd;">
                     <marquee id="footermarquee"  scrollamount="13"><p id="footermessage" style="font-size: 50px; background-color: #e3f2fd;"></p></marquee>
                </div>
            </div>
        <script src="/static/js/modernizr.js"></script>
        <script src="/static/js/jquery.js"></script>
        <script src="/static/js/foundation.min.js"></script>
        <script src="/static/js/gap.js"></script>
        <script src="http://oap.accuweather.com/launch.js"></script>
        <script src="http://widget.time.is/t.js"></script>
        <script>
                $(document).foundation();
                //faz a busca pelo feed rss das noticias
                searchRSS();
                //apresenta o time widget
                time_is_widget.init({Cape_Verde_z503: {}});
                //Controla a lista de reproduçao
                playerControler();
                //websocket
                var ws = new WebSocket("wss://gap.ama.cv/ws");
                ws.onmessage = function(e){
                    setTvContent(e.data);
                    getVoicetv(e.data);
               };
        </script>
    </body>
</html>
